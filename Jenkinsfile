pipeline {
    agent {
        slave-1
    }
    }

    parameters {
        string(name: 'DB_NAME', defaultValue: 'crmwebsite', description: 'Database name')
        string(name: 'DB_PORT', defaultValue: '5432', description: 'Database port')
        /*
        DB_USER = credentials('DB_USER')
        DB_PASSWORD = credentials('DB_PASSWORD') 
        DB_HOST = credentials('DB_HOST') 
        DOCKER_USERNAME = credentials('DOCKER_USERNAME')
        DOCKER_PASSWORD = credentials('DOCKER_PASSWORD')
        */
        // Add more parameters as needed
    }
    
    options {
        disableConcurrentBuilds() // Disable concurrent builds to ensure sequential execution
    }

    stages{
        stage('Setup Environment') {
            steps {
                sh 'python3 -m venv venv' // Create a virtual environment
                sh '. venv/bin/activate' // Activate the virtual environment
           
                 // Install dependencies
                sh 'pip install -r requirements.txt'
            }
        }
        
        stage('Create Database') {
            steps {
                 withCredentials([
                                    string(credentialsId: 'DB_PASSWORD', variable: 'DB_PASSWORD'),
                                    string(credentialsId: 'DB_USER', variable: 'DB_USER'),
                                    string(credentialsId: 'DB_HOST', variable: 'DB_HOST'),
                                    string(name: 'DB_NAME', defaultValue: 'crmwebsite', description: 'Database name'),
                                    string(name: 'DB_PORT', defaultValue: '5432', description: 'Database port')
                                ])
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

