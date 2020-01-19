def branch = '';

pipeline {
    agent { docker { image 'docker-registry.kabala.tech/ansible:latest' } }
    
    environment {
        CI = 'true'
        GIT_SSH_COMMAND = "ssh -o StrictHostKeyChecking=no"
        
    }

    stages {
        stage ('Prepare') {
            steps {
                script {
                    sh "printenv"
                }
            }
        }
        stage ('Deploy') {
             steps {
                script {
                    sshagent(['jenkins-local-ssh-key']) {
                        configFileProvider([configFile(fileId: 'homeAutomationPy-miio-config.py', targetLocation: 'config.py')]) {
                            def configPath = "${env.WORKSPACE}/config.py"
                            sh "ansible-playbook -i deploy/hosts deploy/deploy.yml -e 'app=${app} config_path=${configPath}' -vvv"
                        }
                    }
                }
            }
        }
    }
}
