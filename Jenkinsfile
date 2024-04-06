pipeline {
    agent any 
    environment {
        SONAR_TOKEN = credentials('Sonartoken') // Replace with your actual SonarQube token ID
    }
    parameters {
        string(name: 'DB_NAME', defaultValue: 'crmwebsite', description: 'Database name')
        string(name: 'DB_PORT', defaultValue: '5432', description: 'Database port')
        // Add more parameters as needed
    }
    
    options {
        disableConcurrentBuilds() // Disable concurrent builds to ensure sequential execution
    }
    
    stages {
        stage('Install Ansible') {
            steps {
                script {
                    // Install Ansible using apt-get on Ubuntu
                    sh 'sudo apt-get update -y'
                    sh 'sudo apt-get install software-properties-common -y'
                    sh 'sudo apt-add-repository --yes --update ppa:ansible/ansible'
                    sh 'sudo apt-get install ansible -y'
                    
                    // Check Ansible version
                    sh 'ansible --version'
                }
            }
        }

        stage('Install Python and Pip') {
            steps {
                ansiblePlaybook(
                    playbook: 'required-installations.yaml',
                    inventory: 'localhost',
                    installation: 'ansible'
                )
            }
        } 
        
        stage('Setup Environment') {
            steps {
                script {
                    // Create a virtual environment and activate it
                    sh 'python3 -m venv venv'
                    sh '. venv/bin/activate'
                    // Install dependencies
                    sh 'pip install -r requirements.txt'
                }
            }
        }
        
        stage('Create Database') {
            steps {
                script {
                    // Inject credentials into environment variables
                    withCredentials([
                        string(credentialsId: 'DB_HOST', variable: 'DB_HOST'),
                        string(credentialsId: 'DB_USER', variable: 'DB_USER'),
                        string(credentialsId: 'DB_PASSWORD', variable: 'DB_PASSWORD')
                    ]) {
                        // Set other environment variables
                        env.DB_NAME = "${params.DB_NAME}"
                        env.DB_PORT = "${params.DB_PORT}"

                        // Check if the database exists by running the check_db.sh script
                        def databaseExists = sh(script: 'chmod +x ./check_db.sh && ./check_db.sh', returnStatus: true)
                        if (databaseExists == 0) {
                            echo 'Database already exists. Skipping creation.'
                        } else {
                            // If the database does not exist, run the mydb.py script
                            sh 'python3 mydb.py'
                        }
                    }
                }
            }
        }
        
        stage('Database Migration') {
            steps {
                script {
                    withCredentials([
                        string(credentialsId: 'DB_HOST', variable: 'DB_HOST'),
                        string(credentialsId: 'DB_USER', variable: 'DB_USER'),
                        string(credentialsId: 'DB_PASSWORD', variable: 'DB_PASSWORD')
                    ]) {
                        // Set other environment variables
                        env.DB_NAME = "${params.DB_NAME}"
                        env.DB_PORT = "${params.DB_PORT}"
                        
                        // Check if migrations are needed
                        def migrationsNeeded = sh(script: 'python3 manage.py showmigrations --plan', returnStdout: true).trim()
                        if (migrationsNeeded.contains(' (no migrations)')) {
                            echo 'No new migrations found.'
                        } else {
                            // Run migrations
                            sh 'python3 manage.py migrate'
                        }
                    }
                }
            }
        }
        
        stage('Unit testing') {
            steps {
                script {
                    withCredentials([
                        string(credentialsId: 'DB_HOST', variable: 'DB_HOST'),
                        string(credentialsId: 'DB_USER', variable: 'DB_USER'),
                        string(credentialsId: 'DB_PASSWORD', variable: 'DB_PASSWORD')
                    ]) {
                        // Set other environment variables
                        env.DB_NAME = "${params.DB_NAME}"
                        env.DB_PORT = "${params.DB_PORT}"

                        sh 'python3 manage.py test website'
                    }
                }
            }
        }
        
        stage('SonarCloud Analysis') {
            steps {
                script {
                    withSonarQubeEnv('SonarCloud') {
                        docker.image('sonarsource/sonar-scanner-cli').inside {
                            sh """
                            sonar-scanner \
                               -Dsonar.organization=django \
                               -Dsonar.projectKey=django_jenkins-django \
                               -Dsonar.sources=. \
                               -Dsonar.host.url=https://sonarcloud.io \
                               -Dsonar.login=$SONAR_TOKEN
                            """
                        }
                    }
                }
            }
        }
        
        stage('Quality Gate Check') {
            steps {
                script {
                    def qg = waitForQualityGate()
                    if (qg.status != 'OK') {
                        error "Pipeline aborted due to quality gate failure: ${qg.status}"
                    }
                }
            }
        }
    
    
        stage('Build and Push Docker Image') {
            steps {
            script {
                withCredentials([
                string(credentialsId: 'DB_HOST', variable: 'DB_HOST'),
                string(credentialsId: 'DB_USER', variable: 'DB_USER'),
                string(credentialsId: 'DB_PASSWORD', variable: 'DB_PASSWORD')
                ]) {
               
                withDockerRegistry(credentialsId: 'docker-cred') {
                    env.DB_NAME = "${params.DB_NAME}"
                    sh "docker build -t mayank7833/django-cicd:latest ."
                    sh "docker push mayank7833/django-cicd:latest"
                    // Add your additional steps here
                }
                }
            }
            }
        }
    

        stage('Login to Azure CLI') {
            steps {
                script {
                    withCredentials([
                        string(credentialsId: 'AZURE_SUBSCRIPTION_ID', variable: 'AZURE_SUBSCRIPTION_ID'),
                        string(credentialsId: 'AZURE_CLIENT_ID', variable: 'AZURE_CLIENT_ID'),
                        string(credentialsId: 'AZURE_CLIENT_SECRET', variable: 'AZURE_CLIENT_SECRET'),
                        string(credentialsId: 'AZURE_TENANT_ID', variable: 'AZURE_TENANT_ID')
                    ]) {
                        sh """
                            az login --service-principal -u ${AZURE_CLIENT_ID} -p ${AZURE_CLIENT_SECRET} --tenant ${AZURE_TENANT_ID} 
                            az account set --subscription ${AZURE_SUBSCRIPTION_ID}
                        """
                    }
                }
            }
        }
    
                stage('Check AKS Cluster Existence') {
            steps {
                script {
                    withCredentials([string(credentialsId: 'TF_TOKEN', variable: 'TF_API_TOKEN')]){
                        def clusterExists = sh (
                            script: "az aks show --resource-group demoresourcegroup --name democluster",
                            returnStatus: true
                        )
                        if (clusterExists == 0) {
                            echo "AKS cluster exists. Skipping creation stage."
                        } else {
                            echo "AKS cluster does not exist. Proceeding with creation stage."
                            dir("${WORKSPACE}/kubernetes-cluster") {
                                sh "terraform init"
                                sh "terraform validate"
                                sh "terraform plan"
                                sh "terraform apply -auto-approve"
                                sh "terraform output"
                            }
                            dir("${WORKSPACE}/kubernetes") {
                                sh "az aks get-credentials --resource-group demoresourcegroup --name democluster --overwrite-existing"
                                sh "kubectl apply -f deployment.yaml"
                                echo "wait for 2 minutes to let loadbalancer get ready"
                                sh "sleep 120"
                                sh "kubectl get pods"
                                sh "kubectl get svc"
                                sh "kubectl get nodes"
                            }
                        }
                    }
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
}
