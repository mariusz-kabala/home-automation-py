def branch = ''

pipeline {
    agent any

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
                    try {
                        branch = env.GIT_LOCAL_BRANCH
                        branch = branch ?: env.GIT_BRANCH
                        if (branch == 'detached') {
                            branch = ''
                        }
                        branch = branch ?: env.ghprbActualCommit
                    } catch (e) {
                        println 'GIT BRANCH not detected'
                    }

                    sh 'git config user.name "jenkins-kabala.tech"'
                    sh 'git config user.email "jenkins@kabala.tech"'

                    if (!branch) {
                        error 'GIT branch to process not found'
                    }

                    if (branch.startsWith('origin/')) {
                        branch = branch.replaceAll('origin/', '')
                    }

                    println "GIT branch to process: ${branch}"
                    manager.addShortText(branch, 'white', 'navy', '1px', 'navy')
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
        stage ('Build') {
            steps {
                dir("packages/won") {
                    script {
                        VERSION = sh (
                            script: "./scripts/version.sh",
                            returnStdout: true
                        ).trim() 

                        println "version: ${VERSION}"
                        manager.addShortText("${VERSION}", 'white', 'navy', '1px', 'navy')

                        def app = docker.build("won", "-f Dockerfile .")
                        docker.withRegistry('https://docker-registry.kabala.tech', 'docker-registry-credentials') {
                            app.push("v${VERSION}")
                            app.push("latest")
                        }
                    }
                }
            }
        }
        stage ('Deploy') {
            when {
                environment name: 'deploy', value: 'true'
            }
            steps {
                script {
                    build job: 'home/python_lgsoundbar_deploy', wait: false, parameters: [
                        string(name: 'VERSION', value: "v${VERSION}"),
                        string(name: 'DEPLOY_ENVIRONMENT', value: env.DEPLOY_ENVIRONMENT),
                    ]
                }
            }
        }
    }
}
