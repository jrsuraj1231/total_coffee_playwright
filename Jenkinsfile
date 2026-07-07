pipeline {
    agent any

    parameters {
        choice(name: 'TEST_SUITE', choices: ['smoke', 'regression', 'api'], description: 'Marker to run')
        choice(name: 'TARGET_ENV', choices: ['qa', 'dev', 'stage', 'prod'], description: 'Environment config to use')
    }

    environment {
        ENV = "${params.TARGET_ENV}"
        HEADLESS = 'true'
    }

    stages {
        stage('Install') {
            steps {
                sh 'pip install -r requirements.txt'
                sh 'playwright install --with-deps chromium'
            }
        }

        stage('Test') {
            steps {
                sh "pytest -m ${params.TEST_SUITE} --alluredir=reports/allure-results"
            }
        }
    }

    post {
        always {
            junit 'reports/junit/results.xml'
            archiveArtifacts artifacts: 'reports/html/**, screenshots/failures/**, logs/**', allowEmptyArchive: true
        }
    }
}
