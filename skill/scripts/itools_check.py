#!/usr/bin/env python3
"""Check statically visible command invocations against Innovus manual rules."""
import argparse, difflib, json, re, sys
from dataclasses import dataclass
from pathlib import Path

HERE = Path(__file__).resolve().parent
BUILTINS = set('set unset append lappend list lindex lrange llength concat dict array string regexp regsub expr incr puts gets open close read flush seek tell file glob pwd cd source package namespace variable global upvar uplevel return break continue error catch try throw eval subst format scan split join info rename trace clock after update vwait exit encoding binary chan socket load unload interp apply switch if for foreach lmap while proc'.split())

@dataclass
class Word:
    value: str
    start: int
    end: int
    dynamic: bool = False
    kind: str = 'bare'

def lex(text, base=0):
    """Minimal non-executing command/word segmentation, not a Tcl validator.

    Returns commands, nested command substitutions, and opaque regions. Malformed
    or unsupported input is never reported as a Tcl syntax error.
    """
    commands, nested, opaque = [], [], []
    words=[]
    i=0
    n=len(text)
    while i<n:
        if text.startswith('\\\n',i):
            i+=2
            while i<n and text[i] in ' \t': i+=1
            continue
        c=text[i]
        if c in ' \t\r': i+=1; continue
        if c in ';\n':
            if words: commands.append(words); words=[]
            i+=1;continue
        if c=='#' and not words:
            # Tcl comments also honor backslash-newline continuation.
            while i<n:
                if text.startswith('\\\n',i): i+=2;continue
                if text[i]=='\n': break
                i+=1
            continue
        start=i; dynamic=False; value=''; kind='bare'
        if text.startswith('{*}',i) and i+3<n and text[i+3] not in ' \t\r\n;':
            dynamic=True;i+=3;c=text[i]
        if c=='{':
            kind='brace';i+=1;inner=i;depth=1
            while i<n and depth:
                if text[i]=='\\': i+=2;continue
                if text[i]=='{': depth+=1
                elif text[i]=='}': depth-=1
                if depth: i+=1
            if depth:
                opaque.append(base+start);words=[];break
            value=text[inner:i];i+=1
            if i<n and text[i] not in ' \t\r\n;':
                opaque.append(base+start);words=[]
                while i<n and text[i] not in '\n;':i+=1
                continue
        else:
            quoted=c=='"'
            if quoted: kind='quote';i+=1
            closed=not quoted
            while i<n:
                c=text[i]
                if quoted and c=='"': i+=1;closed=True;break
                if not quoted and c in ' \t\r\n;':break
                if c=='\\':
                    if i+1<n:
                        nxt=text[i+1]
                        if nxt=='\n':
                            if not quoted: break
                            value+=' ';i+=2
                            while i<n and text[i] in ' \t':i+=1
                        else:
                            # Avoid inventing the value of Tcl backslash escapes.
                            if nxt in 'ntvrbfuxU01234567': dynamic=True
                            value+=nxt;i+=2
                    else: i+=1;dynamic=True
                    continue
                if c=='$':dynamic=True
                if c=='[':
                    dynamic=True
                    end=find_bracket(text,i)
                    if end is None:opaque.append(base+i);i=n;closed=False;break
                    nested.append((text[i+1:end],base+i+1))
                    value+=text[i:end+1];i=end+1;continue
                value+=c;i+=1
            if not closed:opaque.append(base+start);words=[];break
            if quoted and i<n and text[i] not in ' \t\r\n;':
                opaque.append(base+start);words=[]
                while i<n and text[i] not in '\n;':i+=1
                continue
        words.append(Word(value,base+start,base+i,dynamic,kind))
    if words:commands.append(words)
    return commands,nested,opaque

def find_bracket(text,start):
    # Track braces and quotes per substitution level, honoring braced literals.
    stack=[{'brace':0,'quote':False,'begin':True}]
    i=start+1
    while i<len(text):
        c=text[i];s=stack[-1]
        if c=='\\':i+=2;continue
        if s['brace']:
            if c=='{':s['brace']+=1
            elif c=='}':s['brace']-=1
        elif c=='[':stack.append({'brace':0,'quote':False,'begin':True})
        elif c==']' and not s['quote']:
            stack.pop()
            if not stack:return i
        elif c=='"':s['quote']=not s['quote'];s['begin']=False
        elif c=='{' and not s['quote'] and s['begin']:s['brace']=1;s['begin']=False
        elif not s['quote']:s['begin']=c in ' \t\r\n;'
        i+=1
    return None

class Checker:
    def __init__(self,rules): self.rules=rules
    def check(self,text,filename='<input>'):
        findings=[];seen=set();scopes=[];procedures=set();stats={'checked':0,'partial':0,'skipped':0}
        def emit(code,message,offset,command=None,page=None,severity='error'):
            key=(code,offset,message)
            if key in seen:return
            seen.add(key)
            line=text.count('\n',0,offset)+1
            col=offset-(text.rfind('\n',0,offset)+1)+1
            item=dict(file=filename,line=line,column=col,severity=severity,code=code,message=message)
            if command:item['command']=command
            if page:item['evidence']={'title':self.rules['source']['title'],'version':self.rules['version'],'pdf_page':page,'source':self.rules['source']['path']}
            findings.append(item)
        def walk(fragment,base=0,depth=0):
            if depth>100:
                emit('UNRESOLVED','嵌套过深，未继续静态分析',base,severity='info');return
            commands,nested,opaque=lex(fragment,base)
            for offset in opaque:emit('UNRESOLVED','此片段无法可靠拆分，未检查手册规则',offset,severity='info')
            scopes.extend(commands)
            for words in commands:
                name=words[0].value
                if name=='proc' and len(words)>=4 and not words[1].dynamic:procedures.add(words[1].value)
                bodies=[]
                if name=='proc' and len(words)==4:bodies=[words[3]]
                elif name=='if':
                    k=1
                    while k<len(words):
                        if words[k].value in ('elseif','else'):
                            if words[k].value=='else':
                                if k+1<len(words):bodies.append(words[k+1])
                                break
                            k+=1
                        k+=1 # condition
                        if k<len(words) and words[k].value=='then':k+=1
                        if k<len(words):bodies.append(words[k]);k+=1
                elif name in ('foreach','lmap','while') and len(words)>2:bodies=[words[-1]]
                elif name=='for' and len(words)==5:bodies=[words[1],words[3],words[4]]
                elif name=='catch' and len(words)>1:bodies=[words[1]]
                elif name=='namespace' and len(words)==4 and words[1].value=='eval':bodies=[words[3]]
                elif name in ('eval','uplevel','switch','try','apply'):
                    emit('UNRESOLVED','此控制结构的脚本内容尚未展开检查',words[0].start,severity='info')
                for body in bodies:
                    if body.kind=='brace':walk(body.value,body.start+1,depth+1)
                    else:emit('UNRESOLVED','动态脚本体未展开检查',body.start,severity='info')
            for inner,offset in nested:walk(inner,offset,depth+1)
        walk(text)
        for words in scopes:
            name=words[0].value
            if words[0].dynamic:
                stats['skipped']+=1;emit('UNRESOLVED','动态命令名无法匹配手册',words[0].start,severity='info');continue
            if name in procedures: continue
            rule=self.rules['commands'].get(name)
            if rule is None:
                if name not in BUILTINS:
                    stats['skipped']+=1
                    suggestions=difflib.get_close_matches(name,self.rules['commands'],n=1,cutoff=.8)
                    emit('UNLISTED_COMMAND','未在已提取命令中找到；可能为自定义或其他版本命令'+('；可能想写 '+suggestions[0] if suggestions else ''),words[0].start,severity='warning')
                continue
            stats['checked']+=1
            if not rule['reviewed']:
                stats['partial']+=1
                emit('PARTIAL_RULES','仅检查已明确提取的参数规则；选项全集及正文约束尚未人工核对',words[0].start,name,rule['page'],'info')
            opts=rule['options'];present={};uncertain=False;i=1
            while i<len(words):
                w=words[i]
                if w.dynamic or (w.value.startswith('{*}') and w.kind=='bare'):
                    uncertain=True;emit('UNRESOLVED','动态参数可能改变选项或参数数量，相关检查已跳过',w.start,name,rule['page'],'info');i+=1;continue
                if not re.match(r'^-[A-Za-z]',w.value):
                    if rule['reviewed']:
                        emit('UNEXPECTED_ARGUMENT','未匹配到手册选项的参数：'+w.value,w.start,name,rule['page'])
                    i+=1;continue
                present[w.value]=w
                spec=opts.get(w.value)
                if spec is None:
                    # An unknown flag can introduce unknown arity. Stop instead
                    # of cascading errors into following values.
                    severity='error' if rule['reviewed'] else 'info'
                    emit('UNKNOWN_OPTION' if rule['reviewed'] else 'UNVERIFIED_OPTION','选项未在'+('已核对语法' if rule['reviewed'] else '已提取的局部规则')+'中找到：'+w.value,w.start,name,rule['page'],severity)
                    uncertain=True;i+=1
                    while i<len(words) and not re.match(r'^-[A-Za-z]',words[i].value):i+=1
                    continue
                arity=spec['arity']
                if arity==0:i+=1;continue
                if arity is None:
                    uncertain=True;emit('UNRESOLVED','该选项的参数数量尚未可靠提取：'+w.value,w.start,name,spec['page'],'info');i+=1
                    while i<len(words) and not re.match(r'^-[A-Za-z]',words[i].value):i+=1
                    continue
                end=i+1
                if arity=='many':
                    while end<len(words) and not re.match(r'^-[A-Za-z]',words[end].value):end+=1
                elif end<len(words) and not (not words[end].dynamic and words[end].value in opts):end+=1
                if end==i+1:
                    if not uncertain:emit('MISSING_VALUE','选项缺少参数：'+w.value,w.start,name,spec['page'])
                    else:emit('UNRESOLVED','动态或未知参数使该选项的参数数量无法确定：'+w.value,w.start,name,spec['page'],'info')
                else:
                    value=words[i+1]
                    if value.dynamic:
                        emit('UNRESOLVED','参数值需要运行时求值：'+w.value,value.start,name,spec['page'],'info')
                    elif 'enum' in spec and value.value not in spec['enum']:
                        emit('INVALID_ENUM',w.value+' 的取值必须为 '+', '.join(spec['enum'])+'；实际为 '+value.value,value.start,name,spec['page'])
                i=end
            # -help is explicitly a standalone help request; syntax constraints
            # on operational arguments do not apply to that request.
            if '-help' in present:continue
            if not uncertain:
                for required in rule.get('required',[]):
                    if required not in present:emit('REQUIRED_OPTION','缺少必填选项：'+required,words[0].start,name,rule['page'])
                for group in rule.get('choices',[]):
                    selected=[o for o in group['options'] if o in present]
                    if not group['min']<=len(selected)<=group['max']:
                        emit('OPTION_CHOICE','以下选项必须且只能选择一个：'+', '.join(group['options']),words[0].start,name,rule['page'])
                for dep in rule.get('dependencies',[]):
                    if dep['option'] in present and dep['requires'] not in present:
                        emit('OPTION_DEPENDENCY',dep['option']+' 必须与 '+dep['requires']+' 一起使用',present[dep['option']].start,name,dep.get('page',rule['page']))
        return {'tool':'Innovus','version':self.rules['version'],'file':filename,'summary':{**stats,**{s:sum(f['severity']==s for f in findings) for s in ('error','warning','info')}},'diagnostics':sorted(findings,key=lambda f:(f['line'],f['column'],f['code']))}

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('files',nargs='*',type=Path)
    parser.add_argument('--rules',type=Path,default=HERE.parent/'references'/'itools-syntax'/'rules.json')
    parser.add_argument('--format',choices=['text','json'],default='text')
    parser.add_argument('--coverage',action='store_true')
    args=parser.parse_args()
    try:
        rules=json.loads(args.rules.read_text())
        if args.coverage:
            print(json.dumps({'version':rules['version'],'commands':len(rules['commands']),'reviewed_commands':[c for c,r in rules['commands'].items() if r['reviewed']],'option_rules':sum(len(r['options']) for r in rules['commands'].values()),'policy':rules['policy']},ensure_ascii=False,indent=2));return 0
        if not args.files:parser.error('请提供待检查脚本，或使用 --coverage')
        results=[Checker(rules).check(p.read_text(),str(p)) for p in args.files]
    except (OSError,ValueError,KeyError) as exc:
        print('无法完成检查：'+str(exc),file=sys.stderr);return 2
    if args.format=='json':print(json.dumps(results,ensure_ascii=False,indent=2))
    else:
        for result in results:
            for d in result['diagnostics']:
                evidence=d.get('evidence')
                suffix=f" [Innovus {evidence['version']}, PDF p.{evidence['pdf_page']}]" if evidence else ''
                print(f"{d['file']}:{d['line']}:{d['column']}: {d['severity']} {d['code']}: {d['message']}{suffix}")
            s=result['summary'];print(f"{result['file']}: {s['error']} errors, {s['warning']} warnings, {s['info']} info; {s['checked']} commands checked ({s['partial']} partial), {s['skipped']} unresolved/unlisted")
    return 1 if any(r['summary']['error'] for r in results) else 0

if __name__=='__main__':sys.exit(main())
