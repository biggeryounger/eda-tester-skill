FROM jenkins/jenkins:lts-jdk21

USER root
RUN apt-get update \
    && apt-get install --yes --no-install-recommends ca-certificates git python3 python3-openpyxl tcl \
    && rm -rf /var/lib/apt/lists/*

USER jenkins
RUN jenkins-plugin-cli --plugins workflow-aggregator git credentials-binding htmlpublisher junit timestamper

COPY init.groovy.d/ /usr/share/jenkins/ref/init.groovy.d/
COPY Jenkinsfile /usr/share/jenkins/ref/Jenkinsfile
