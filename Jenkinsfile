pipeline {
    agent any

    stages {
        stage('1. Construccion (Build)') {
            steps {
                echo 'Construyendo imagen Docker de la aplicacion...'
                sh 'docker build -t securedev-app:latest .'
            }
        }

        stage('2. Pruebas (Test)') {
            steps {
                echo 'Ejecutando verificacion de sintaxis Python...'
                sh 'docker run --rm securedev-app:latest python -m py_compile app.py'
            }
        }

        stage('3. Despliegue Staging (Pre-ZAP)') {
            steps {
                echo 'Levantando contenedor para pruebas dinamicas...'
                sh 'docker rm -f securedev-prod || true'
                sh 'docker run -d --name securedev-prod -p 5000:5000 securedev-app:latest'
                sh 'sleep 5'
            }
        }

        stage('4. Pruebas Automatizadas de Seguridad (OWASP ZAP)') {
            steps {
                echo 'Ejecutando escaneo DAST con OWASP ZAP sobre /hello...'
                sh '''
                    docker rm -f zap-scanner || true
                    docker volume rm zap_wrk || true
                    docker run --name zap-scanner -u 0 -v zap_wrk:/zap/wrk -t zaproxy/zap-stable \
                    zap-baseline.py -t "http://host.docker.internal:5000/hello?name=TEST" -r zap_report.html || true
                    docker cp zap-scanner:/zap/wrk/zap_report.html ./zap_report.html
                    docker rm -f zap-scanner || true
                    docker volume rm zap_wrk || true
                '''
            }
        }

        stage('5. Despliegue Produccion (Deploy)') {
            steps {
                echo 'Aplicacion desplegada en http://localhost:5000/hello'
                sh 'docker ps | grep securedev-prod'
            }
        }
    }
}