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
                    catchError(buildResult: 'FAILURE', stageResult: 'FAILURE') {

                        // Kill any process using port 3000
                        bat '''
@echo off
echo Checking for process using port 3000...
for /f "tokens=5" %%a in ('netstat -aon ^| findstr :3000') do (
    echo Killing process using port 3000 - PID: %%a
    taskkill /PID %%a /F
)
'''

                        // Remove any existing container
                        bat 'docker rm -f test-container || echo "No existing container to remove"'

                        // Start test container
                        bat 'docker run -d --name test-container -p 3000:80 icon-library:latest'

                        // Give it some time to boot up
                        sleep(time: 15, unit: 'SECONDS')

                        // Retryable health check
                        bat '''
@echo off
set RETRIES=5
set WAIT=5

echo Running health check on http://localhost:3000 ...
:retry
curl -f http://localhost:3000
if %ERRORLEVEL% EQU 0 (
    echo Health check passed
    goto success
) else (
    echo Health check failed, retrying in %WAIT% seconds...
    timeout /T %WAIT% >nul
    set /A RETRIES=%RETRIES%-1
    if %RETRIES% GTR 0 goto retry
)

:fail
echo Health check failed after retries
exit /b 1

:success
exit /b 0
'''
                    }
                }
            }

            post {
                always {
                    // Print container logs and clean up
                    bat '''
@echo off
echo Fetching test-container logs...
docker logs test-container || echo "No logs found"

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
