pipeline {
    agent any
    stages {
        stage('Build') {
            steps {
                sh 'ls'
                sh 'curl -H "Content-Type: application/json" --data "{"build": true}" -X POST https://registry.hub.docker.com/u/swapnil085/devops/trigger/bcb3d769-0d41-496e-a0cd-5b978518f9ef/'
            }
        }        
    }
}
