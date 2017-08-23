pipeline {
    agent any
    stages {
        stage('Build') {
            steps {
                sh 'docker build -t dehaze-server .'
                sh 'docker run -p 5000:5000 --name my-dehaze-server dehaze-server'
            }
        }
    }
}
