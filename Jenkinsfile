pipeline {
    agent any
    
    stages {
        stage('Checkout') {
            steps {
                // Checkout code from version control
                git 'https://github.com/yourusername/yourrepository.git'
            }
        }
        
        stage('Setup Environment') {
            steps {
                // Set up Python environment
                sh 'python -m venv venv'
                sh 'source venv/bin/activate'
                
                // Install dependencies
                sh 'pip install -r requirements.txt'
            }
        }
        
        stage('Create Database') {
            steps {
                // Run database creation script
                sh 'python mydb.py'
            }
        }

         stage('Database Setup') {
            steps {
                // Run database migrations
                sh 'python manage.py migrate'
            }
        }

    
    post {
        success {
            // Send notification on success
            echo 'Pipeline succeeded!'
        }
        failure {
            // Send notification on failure
            echo 'Pipeline failed!'
        }
    }
}
