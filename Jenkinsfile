pipeline {
    agent any
    stages {
        stage('Build') {
            steps {
                sh 'docker build -t dehaze-server .'
                sh 'docker rm -f my-dehaze-server'
                sh 'docker run --rm -p 5000:5000 --name my-dehaze-server -d dehaze-server'
            }
        }
    }
}
