pipeline {
	agent any
	environment {
		COMPOSE_PROJECT_NAME = "pdftools"
	}
	stages{
		stage('clone'){
			step{
				git "https://github.com/sujanst98644/pdftools.git"
			}
		}
		stage('Build Docker Images'){ 
            step{
				sh 'docker compose build'
			}
		}
		stage('run migration'){
			steps{
				sh 'docker compose run web python manage.py migrate'
			}
		}
		stage('collect static files'){
			steps{
				sh 'docker compose run web python manage.py collectstatic --noinput'
			}
		}
		stage('deploy restart services'){
			steps{
				sh 'docker compose down'
				sh 'docker compose up -d'
			}
		}

	}
	post {
		success{
			echo "Deployment successful"
		} failure {
			echo "Deployment failed"
		}
	}
}

