pipeline {
    agent { docker { image 'docker-registry.kabala.tech/python-poetry:latest' } }
    
    environment {
        CI = 'true'
        GIT_SSH_COMMAND = "ssh -o StrictHostKeyChecking=no"
        REGISTRY_USER = credentials('python-registry-username')
        REGISTRY_PASS = credentials('python-registry-password')
    }

    stages {
        stage ('Prepare') {
            steps {
                script {
                    sh "printenv"
                    try {
                        branch = env.GIT_LOCAL_BRANCH
                        branch = branch ?: env.GIT_BRANCH
                        if (branch == 'detached') {
                            branch = ''
                        }
                        branch = branch ?: env.ghprbActualCommit
                    } catch (e) {
                        println "GIT BRANCH not detected"
                    }

                    sh 'git config user.name "jenkins-kabala.tech"'
                    sh 'git config user.email "jenkins@kabala.tech"'

                    if (!branch) {
                        error "GIT branch to process not found"
                    }

                    if (branch.startsWith('origin/')) {
                        branch = branch.replaceAll('origin/', '')
                    }

                    println "GIT branch to process: ${branch}"
                    manager.addShortText(branch, "white", "navy", "1px", "navy")
                }
            }
        }
        stage ('Install dependencies') {
            when {
                expression { !env.skip_install  }
            }
            steps {
                script {
                    dir("packages/${PACKAGE}") {
                        sh "poetry install"
                    }
                }
            }
        }
        stage ('Bump version') {
            steps {
                script {
                    dir("packages/${PACKAGE}") {
                        sh "poetry version ${VERSION}"
                        sh "python -c 'import sys; print(sys.path)'"
                    }
                }
            }
        }
        stage ('Build package') {
            steps {
                script {
                    dir("packages/${PACKAGE}") {
                        sh "poetry build"
                    }
                }
            }
        }
        stage ('Publish package') {
            steps {
                script {
                    dir("packages/${PACKAGE}") {
                        sh "poetry config repositories.kabala-tech https://pypi.kabala.tech"
                        sh "poetry config http-basic.kabala-tech ${REGISTRY_USER} ${REGISTRY_PASS}"
                        sh "poetry publish -r kabala-tech"
                    }
                }
            }
        }
        stage ('Commit changes') {
            steps {
                script {
                    sshagent(['jenkins-ssh-key']) {
                        sh "git checkout ${branch}"
                        sh "git add -A"
                        sh "git commit -m 'chore: bump package version'"
                        sh "git push origin ${branch}"
                    }
                }
            }
        }
        stage ('Deploy') {
            when {
                environment name: 'deploy', value: 'true'
            }
            steps {
                build job: 'HomeAutomationPY-Deploy', wait: false, parameters: [
                    string(name: 'ghprbActualCommit', value: "${ghprbActualCommit}"),
                    string(name: 'app', value: "${PACKAGE}"),
                ]
            }
        }
    }

    post { 
        always { 
            cleanWs()
        }
    }
}
