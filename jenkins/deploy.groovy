def version = ''

pipeline {
    agent { docker { image 'docker-registry.kabala.tech/python-poetry:latest' } }
    
    environment {
        CI = 'true'
        GIT_SSH_COMMAND = "ssh -o StrictHostKeyChecking=no"
        JENKINS_USER_PASS = credentials('srv2-jenkins-user-pass')
        // STATS_DB_USER = credentials('home-automation-stats-db-user')
        // STATS_DB_PASS = credentials('home-automation-stats-db-pass')
    }

    stages {
        stage ('Determine last version to deploy') {
            when {
                expression { env.VERSION == "" }
            }
            steps {
                dir ("packages/${app}") {
                    script {
                        version = sh (
                            script: 'poetry version | awk \'{print $2}\'',
                            returnStdout: true
                        ).trim()
                    }
                }
            }
        }
        stage ('Prepare') {
            steps {
                script {
                    sh "ansible-galaxy collection install community.general"
                    sh "printenv"

                    if (!version) {
                        version = env.VERSION
                    }
                }
            }
        }
        stage ('Deploy won') {
            when {
                environment name: 'app', value: 'won'
            }
             steps {
                script {
                    sshagent(['jenkins-local-ssh-key']) {
                        sh "ansible-playbook -i deploy/hosts deploy/deploy_${app}.yml -e 'app=${app} version=${version} sudo_pass=${JENKINS_USER_PASS}' -vvv"
                    }
                }
            }
        }
        // stage ('Deploy sgp30') {
        //     when {
        //         environment name: 'app', value: 'sgp30'
        //     }
        //      steps {
        //         script {
        //             sshagent(['jenkins-local-ssh-key']) {
        //                 sh "ansible-playbook -i deploy/hosts deploy/deploy_${app}.yml -e 'app=${app} dbuser=${STATS_DB_USER} dbpass=${STATS_DB_PASS} version=${version}'"
        //             }
        //         }
        //     }
        // }
        // stage ('Deploy sensedashboard') {
        //     when {
        //         environment name: 'app', value: 'sensedashboard'
        //     }
        //      steps {
        //         script {
        //             sshagent(['jenkins-local-ssh-key']) {
        //                 sh "ansible-playbook -i deploy/hosts deploy/deploy_${app}.yml -e 'app=${app} dbuser=${STATS_DB_USER} dbpass=${STATS_DB_PASS} version=${version}'"
        //             }
        //         }
        //     }
        // }
        stage ('Deploy bedroomtv') {
            when {
                environment name: 'app', value: 'bedroomtv'
            }
             steps {
                script {
                    sshagent(['jenkins-local-ssh-key']) {
                        sh "ansible-playbook -i deploy/hosts deploy/deploy_${app}.yml -e 'app=${app} version=${version}'"
                    }
                }
            }
        }
        stage ('Deploy miio') {
            when {
                environment name: 'app', value: 'miio'
            }
             steps {
                script {
                    sshagent(['jenkins-local-ssh-key']) {
                        configFileProvider([configFile(fileId: 'homeAutomationPy-miio-config.py', targetLocation: 'config.py')]) {
                            def configPath = "${env.WORKSPACE}/config.py"
                            sh "ansible-playbook -i deploy/hosts deploy/deploy_${app}.yml -e 'app=${app} config_path=${configPath} version=${ghprbActualCommit}'"
                        }
                    }
                }
            }
        }
        stage ('Deploy garagegate') {
            when {
                environment name: 'app', value: 'garagegate'
            }
             steps {
                script {
                    sshagent(['jenkins-local-ssh-key']) {
                        sh "ansible-playbook -i deploy/hosts deploy/deploy_${app}.yml -e 'app=${app} version=${version}'"
                    }
                }
            }
        }
        stage ('Deploy projectorscreen') {
            when {
                environment name: 'app', value: 'projectorscreen'
            }
             steps {
                script {
                    sshagent(['jenkins-local-ssh-key']) {
                        sh "ansible-playbook -i deploy/hosts deploy/deploy_${app}.yml -e 'app=${app} version=${version}'"
                    }
                }
            }
        }
    }

    post { 
        always { 
            cleanWs()
        }
    }
}
