pipeline {
    agent { docker { image 'docker-registry.kabala.tech/alpine-terraform:latest' } }

    environment {
        DOCKER_REGISTRY_USERNAME = credentials('docker-registry-username')
        DOCKER_REGISTRY_PASSWORD = credentials('docker-registry-password')
        app = ''
        CI = 'true'
        GIT_SSH_COMMAND = 'ssh -o StrictHostKeyChecking=no'
        GH_TOKEN = credentials('jenkins-github-accesstoken')
    }

    stages {
        stage ('prepare') {
            steps {
                script {
                    sh 'printenv'
                    
                    sh 'git config user.name "jenkins-kabala.tech"'
                    sh 'git config user.email "jenkins@kabala.tech"'
                    
                    manager.addShortText("${env.VERSION}", 'white', 'navy', '1px', 'navy')
                    manager.addShortText("${env.DEPLOY_ENVIRONMENT}", "white", "blue", "1px", "navy")
                }
            }
        }
        stage ('Checkout') {
            steps {
                    checkout([
                            $class                           : 'GitSCM',
                            branches                         : [[name: "master"]],
                            browser                          : [$class: 'GithubWeb', repoUrl: 'https://github.com/mariusz-kabala/home-automation-py'],
                            doGenerateSubmoduleConfigurations: false,
                            userRemoteConfigs                : [[
                                credentialsId: 'github',
                                refspec      : '+refs/pull/*:refs/remotes/origin/pr/*',
                                url          : 'git@github.com:mariusz-kabala/home-automation-py.git'
                            ]]
                    ])
            }
        }
        stage ('Deploy') {
            steps {
                dir("packages/lgsoundbar/terraform") {
                    script {
                        docker.withRegistry('https://docker-registry.kabala.tech', 'docker-registry-credentials') {
                            sh "terraform init"
                            sh "terraform workspace select ${env.DEPLOY_ENVIRONMENT} || terraform workspace new ${env.DEPLOY_ENVIRONMENT}"
                            sh "terraform plan -out deploy.plan -var-file=${env.DEPLOY_ENVIRONMENT}.tfvars -var=\"tag=${version}\" -var=\"DOCKER_REGISTRY_USERNAME=${DOCKER_REGISTRY_USERNAME}\" -var=\"DOCKER_REGISTRY_PASSWORD=${DOCKER_REGISTRY_PASSWORD}\"" 
                            sh "terraform apply -auto-approve deploy.plan"
                        }
                    }
                }
            }
        }
    }
}
