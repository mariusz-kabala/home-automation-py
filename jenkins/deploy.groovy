def branch = '';

pipeline {
    agent { docker { image 'ansible/ansible:default' } }
    
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
                    sshagent(['jenkins-ssh-key']) {
                        configFileProvider([configFile(fileId: 'homeAutomationPy-miio-config.py', targetLocation: 'config.py')]) {
                            sh "ansible-playbook -i hosts deploy.yml -e 'app=${app} config_path=config.py'"
                        }
                    }
                }
            }
        }
    }
}
