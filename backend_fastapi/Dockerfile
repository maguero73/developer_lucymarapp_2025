# Dockerfile
FROM jenkins/jenkins:lts

USER root

# Instala Docker dentro del contenedor Jenkins
RUN apt-get update && \
    apt-get install -y curl gnupg2 software-properties-common && \
    curl -fsSL https://download.docker.com/linux/debian/gpg | apt-key add - && \
    add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/debian bullseye stable" && \
    apt-get update && \
    apt-get install -y docker-ce-cli && \
    usermod -aG docker jenkins

USER jenkins

