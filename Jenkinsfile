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
                bat 'docker build -t icon-library:latest .'
            }
        }
        
        stage('Test') {
            steps {
                script {
            // Free the port if used
            bat 'for /f "tokens=5" %%a in (\'netstat -aon ^| findstr :3000\') do taskkill /PID %%a /F'
            // Remove any old container
            bat 'docker rm -f test-container || true'
            // Run container
            bat 'docker run -d --name test-container -p 3000:80 icon-library:latest'
        }
                // Wait for the container to be ready
                sleep(time: 30, unit: 'SECONDS')
                // Run tests
                bat 'curl -f http://localhost:3000 || exit 1'
            }
            post {
                always {
                    bat 'docker stop test-container || true'
                    bat 'docker rm test-container || true'
                }
            }
        }
        
        stage('Deploy') {
            steps {
                bat 'docker tag icon-library:latest ${DOCKER_HUB_USR}/icon-library:latest'
                bat 'docker login -u ${DOCKER_HUB_USR} -p ${DOCKER_HUB_PSW}'
                bat 'docker push ${DOCKER_HUB_USR}/icon-library:latest'
            }
        }
    }
}