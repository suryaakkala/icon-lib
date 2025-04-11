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
            // Kill any process on port 3000 (Windows)
            bat '''
@echo off
echo Checking for process using port 3000...
for /f "tokens=5" %%a in ('netstat -aon ^| findstr :3000') do (
    echo Killing process using port 3000 - PID: %%a
    taskkill /PID %%a /F
)
'''

            // Remove old container if it exists
            bat 'docker rm -f test-container || echo "No existing container to remove"'

            // Run container
            bat 'docker run -d --name test-container -p 3000:80 icon-library:latest'

            // Wait for app to be ready
            sleep(time: 15, unit: 'SECONDS')

            // Health check
            bat '''
@echo off
echo Running health check on http://localhost:3000 ...
curl -f http://localhost:3000
if %ERRORLEVEL% NEQ 0 (
    echo Health check failed
    exit /b 1
)
'''
        }
    }

    post {
        always {
            bat '''
@echo off
echo Stopping test-container...
docker stop test-container || echo "Docker stop failed, continuing..."

echo Removing test-container...
docker rm test-container || echo "Docker rm failed, continuing..."
'''
        }
    }
}


        stage('Deploy') {
            steps {
                bat 'docker tag icon-library:latest %DOCKER_HUB_USR%/icon-library:latest'
                bat 'docker login -u %DOCKER_HUB_USR% -p %DOCKER_HUB_PSW%'
                bat 'docker push %DOCKER_HUB_USR%/icon-library:latest'
            }
        }
    }
}
