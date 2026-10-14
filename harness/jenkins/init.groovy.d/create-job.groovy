import com.cloudbees.plugins.credentials.CredentialsScope
import com.cloudbees.plugins.credentials.SystemCredentialsProvider
import com.cloudbees.plugins.credentials.domains.Domain
import com.cloudbees.plugins.credentials.impl.UsernamePasswordCredentialsImpl
import hudson.model.ParametersDefinitionProperty
import hudson.model.StringParameterDefinition
import hudson.model.User
import hudson.plugins.git.BranchSpec
import hudson.plugins.git.GitSCM
import hudson.plugins.git.UserRemoteConfig
import hudson.security.FullControlOnceLoggedInAuthorizationStrategy
import hudson.security.HudsonPrivateSecurityRealm
import jenkins.model.Jenkins
import org.jenkinsci.plugins.workflow.cps.CpsScmFlowDefinition
import org.jenkinsci.plugins.workflow.job.WorkflowJob

def jenkins = Jenkins.get()
def password = System.getenv('JENKINS_ADMIN_PASSWORD')
def githubToken = System.getenv('GITHUB_PUSH_TOKEN')
if (!password) {
    throw new IllegalStateException('JENKINS_ADMIN_PASSWORD is required')
}

def realm
if (jenkins.securityRealm instanceof HudsonPrivateSecurityRealm) {
    realm = jenkins.securityRealm
} else {
    realm = new HudsonPrivateSecurityRealm(false)
    jenkins.securityRealm = realm
}
def admin = User.getById('admin', true)
admin.addProperty(HudsonPrivateSecurityRealm.Details.fromPlainPassword(password))
admin.save()
def authorization = new FullControlOnceLoggedInAuthorizationStrategy()
authorization.allowAnonymousRead = false
jenkins.authorizationStrategy = authorization

def jobName = 'eda-tester-skill-approved-merge'
def job = jenkins.getItem(jobName)
if (job == null) {
    job = jenkins.createProject(WorkflowJob, jobName)
}
def scm = new GitSCM(
    [new UserRemoteConfig('https://github.com/biggeryounger/eda-tester-skill.git', null, null, null)],
    [new BranchSpec('*/main')], false, [], null, null, []
)
def definition = new CpsScmFlowDefinition(scm, 'harness/jenkins/Jenkinsfile')
definition.lightweight = false
job.definition = definition
job.description = '测试候选提交的完整用例集，发布报告，等待人工审批后安全合入 main。'
job.removeProperty(ParametersDefinitionProperty)
job.addProperty(new ParametersDefinitionProperty(
    new StringParameterDefinition('CANDIDATE_REF', '', '待合入的远端分支或提交'),
    new StringParameterDefinition('TARGET_BRANCH', 'main', '目标分支')
))
job.save()

if (githubToken) {
    def provider = SystemCredentialsProvider.getInstance()
    def store = provider.getStore()
    def credentialId = 'github-eda-tester-skill-push'
    def replacement = new UsernamePasswordCredentialsImpl(
        CredentialsScope.GLOBAL,
        credentialId,
        'GitHub token used only after manual approval',
        'x-access-token',
        githubToken
    )
    def existing = provider.getCredentials().find { credential -> credential.id == credentialId }
    if (existing) {
        store.updateCredentials(Domain.global(), existing, replacement)
    } else {
        store.addCredentials(Domain.global(), replacement)
    }
}
jenkins.save()
