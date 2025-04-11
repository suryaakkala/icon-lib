pipeline {
    agent any
    
    environment {
        DOCKER_HUB = credentials('docker-hub-credentials')
    }
    
    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/suryaakkala/icon-lib.git'
            }
        }
        
        stage('Build') {
            steps {
                sh 'docker build -t icon-library:latest .'
            }
        }
        
        stage('Test') {
            steps {
                sh 'docker run -d --name test-container -p 3000:80 icon-library:latest'
                sh 'sleep 5' // Wait for container to start
                sh 'curl --fail http://localhost:3000 || exit 1'
            }
            post {
                always {
                    sh 'docker stop test-container || true'
                    sh 'docker rm test-container || true'
                }
            }
        }
        
        stage('Deploy') {
            steps {
                sh 'docker tag icon-library:latest ${DOCKER_HUB_USR}/icon-library:latest'
                sh 'docker login -u ${DOCKER_HUB_USR} -p ${DOCKER_HUB_PSW}'
                sh 'docker push ${DOCKER_HUB_USR}/icon-library:latest'
            }
        }
    }
    
    post {
        success {
            slackSend color: 'good', message: 'Icon Library deployment succeeded!'
        }
        failure {
            slackSend color: 'danger', message: 'Icon Library deployment failed!'
        }
    }
}