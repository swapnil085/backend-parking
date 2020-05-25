pipeline {
    agent any
    stages {
        stage('Build') {
            steps {
                // sh 'ls'
                // sh 'curl -H "Content-Type: application/json" --data "{"build": true}" -X POST https://registry.hub.docker.com/u/swapnil085/devops/trigger/bcb3d769-0d41-496e-a0cd-5b978518f9ef/'
                sh 'docker-compose build'
            }
        }
        stage('Test'){
            steps{
                sh 'pip3 install pytest'
                sh 'pytest'
            }
        }
        stage("Archive"){
            steps{
                sh 'docker login -u=swapnil085 -p=Swapnil@123'
                sh 'docker-compose push'
            }    
        }
        stage('Deploy') {
            steps {
                sh "wget -O docker-compose.yml https://raw.githubusercontent.com/swapnil085/backend-parking/master/docker-compose_test.yml"
                build 'RundeckJob'
            }
        }
    }
}