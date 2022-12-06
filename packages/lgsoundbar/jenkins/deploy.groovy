pipeline {
    agent { docker { image 'docker-registry.kabala.tech/alpine-terraform:latest' } }

    environment {
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
                            branches                         : [[name: "${branch}"]],
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
                dir("packages/lgsoundbar") {
                    script {
                        docker.withRegistry('https://docker-registry.kabala.tech', 'docker-registry-credentials') {
                            sh "terraform init"
                            sh "terraform plan -out deploy.plan -var=\"tag=${VERSION}\" -var=\"DOCKER_REGISTRY_USERNAME=${DOCKER_REGISTRY_USERNAME}\" -var=\"DOCKER_REGISTRY_PASSWORD=${DOCKER_REGISTRY_PASSWORD}\"" 
                            sh "terraform apply -auto-approve deploy.plan"
                        }
                    }
                }
            }
        }
    }
}
