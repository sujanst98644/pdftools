pipeline {
    agent any

    environment {
        COMPOSE_PROJECT_NAME = "pdftools"
    }

    stages {

        stage('Clone') {
            steps {
                git 'https://github.com/sujanst98644/pdftools.git'
            }
        }

        stage('Build Docker Images') {
            steps {
                sh 'docker compose build'
            }
        }

        stage('Run Migrations') {
            steps {
                sh 'docker compose run --rm web python manage.py migrate'
            }
        }

        stage('Collect Static Files') {
            steps {
                sh 'docker compose run --rm web python manage.py collectstatic --noinput'
            }
        }

        stage('Deploy Restart Services') {
            steps {
                sh 'docker compose down'
                sh 'docker compose up -d'
            }
        }
    }

    post {
        success {
            echo 'Deployment successful'
        }
        failure {
            echo 'Deployment failed'
        }
    }
}