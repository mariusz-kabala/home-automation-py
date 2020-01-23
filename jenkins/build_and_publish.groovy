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
                }
            }
        }
        stage ('Install dependencies') {
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
                        sh "poetry publish"
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
