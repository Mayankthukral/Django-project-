pipeline {
    agent {
        label 'slave-1' // Specify the label of the virtual machine agent
    }
    
    options {
        disableConcurrentBuilds() // Disable concurrent builds to ensure sequential execution
    }

    stages{
        stage('Setup Environment') {
            steps {
                // Set up Python environment
                sh 'python3 -m venv venv' // Use 'python3' for Python 3.x
                sh '. venv/bin/activate' // Use dot (.) to source the virtual environment
                
                // Install dependencies
                sh 'pip install -r requirements.txt'
            }
        }
        
        stage('Create Database') {
            steps {
                script {
                    // Check if the database exists
                    def databaseExists = sh(script: 'python mydb_check.py', returnStatus: true)
                    if (databaseExists == 0) {
                        echo 'Database already exists. Skipping creation.'
                    } else {
                        // Run database creation script
                        sh 'python mydb.py'
                    }
                }
            }
        }
        
        stage('Database Migration') {
            steps {
                script {
                    // Check if migrations are needed
                    def migrationsNeeded = sh(script: 'python manage.py showmigrations --plan', returnStdout: true).trim()
                    if (migrationsNeeded.contains(' (no migrations)')) {
                        echo 'No new migrations found.'
                    } else {
                        // Run migrations
                        sh 'python manage.py migrate'
                    }
                }
            }
        }
        
        stage('Dockerize') {
            steps {
                // Build the Docker image
                sh 'docker build -t $DOCKER_USERNAME/myapp:latest .'
                // Login to Docker Hub
                sh "echo $DOCKER_PASSWORD | docker login --username $DOCKER_USERNAME --password-stdin"
                // Push the Docker image to Docker Hub
                sh 'docker push $DOCKER_USERNAME/myapp:latest'
            }
        }
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

