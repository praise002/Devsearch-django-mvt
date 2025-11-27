pipeline {
    agent any
    // environment {
    //     SETTINGS = credentials('django-settings')
    //     // Database
    //     SECRET_KEY = credentials('django-secret-key')
    //     POSTGRES_HOST = credentials('postgres-host')
    //     POSTGRES_PORT = credentials('postgres-port')
    //     POSTGRES_USER = credentials('postgres-user')
    //     POSTGRES_PASSWORD = credentials('postgres-password')
    //     POSTGRES_DB = credentials('postgres-db')
        
    //     // Cloudinary
    //     CLOUDINARY_CLOUD_NAME = credentials('cloudinary-cloud-name')
    //     CLOUDINARY_API_KEY = credentials('cloudinary-api-key')
    //     CLOUDINARY_API_SECRET = credentials('cloudinary-api-secret')
        
    //     // Email (these were missing!)
    //     EMAIL_HOST_USER = credentials('email-host-user')
    //     EMAIL_HOST_PASSWORD = credentials('email-host-password')
    //     EMAIL_HOST = credentials('email-host')
    //     EMAIL_PORT = credentials('email-port')
    //     EMAIL_USE_SSL = credentials('email-use-tls')
    //     DEFAULT_FROM_EMAIL = credentials('default-from-email')
        
    //     // Other services
    //     ALLOWED_HOSTS = credentials('allowed-hosts')
    //     REDIS_URL = credentials('redis-url')
    //     FLOWER_PASSWORD = credentials('flower-password')
        
    //     PYTHONPATH = "${env.WORKSPACE}"
    // }
    options {
        timeout(time: 30, unit: 'MINUTES')
        buildDiscarder(logRotator(numToKeepStr: '10'))
    }
    stages {
        stage('Checkout') {
            steps {
                checkout scm
                sh 'ls -la'  // Verify files are there
            }
        }
        
        stage('Setup Python') {
            steps {
                sh '''
                    python --version
                    pip --version
                    echo "Current directory: $(pwd)"
                    echo "Python path: ${PYTHONPATH}"
                '''
            }
        }
        
        stage('Install Dependencies') {
            steps {
                sh '''
                    pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }
        
        stage('Run Tests') {
            steps {
                sh '''
                    echo "Testing accounts app..."
                    python manage.py test apps.accounts --no-input
                    echo "Testing profiles app..."
                    python manage.py test apps.profiles --no-input
                    echo "Testing projects app..."
                    python manage.py test apps.projects --no-input
                    echo "Testing messaging app..."
                    python manage.py test apps.messaging --no-input
                '''
            }
        }
        
        stage('Build & Verify') {
            steps {
                sh '''
                    echo "Running migrations..."
                    python manage.py migrate --no-input
                    
                    echo "Collecting static files..."
                    python manage.py collectstatic --no-input
                    
                    echo "Checking deployment configuration..."
                    python manage.py check --deploy
                '''
            }
        }
    }
    post {
        always {
            echo "Pipeline completed - cleaning up"
            cleanWs()  // clean workspace
        }
        success {
            echo "✅ All tests passed! Pipeline succeeded."
        }
        failure {
            echo "❌ Pipeline failed. Check the test results above."
        }
    }
}