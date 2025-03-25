# Jenkins流水线配置
pipeline {
    agent any

    stages {
        stage('Checkout Code') {
            steps {
                git branch: 'main', 
                url: 'https://github.com/yourname/router_web_auto_test.git'
            }
        }

        stage('Setup Environment') {
            steps {
                sh 'python -m venv venv'
                sh 'source venv/bin/activate && pip install -r requirements.txt'
            }
        }

        stage('Run Tests') {
            steps {
                sh '''
                    source venv/bin/activate
                    pytest test_cases/ \
                        --alluredir=allure-results \
                        --clean-alluredir \
                        -v
                '''
            }
        }

        stage('Generate Report') {
            steps {
                allure([
                    includeProperties: false,
                    jdk: '',
                    results: [[path: 'allure-results']],
                    reportBuildPolicy: 'ALWAYS'
                ])
            }
        }
    }

    post {
        always {
            emailext(
                subject: "Web登录冒烟测试结果 - ${currentBuild.currentResult}",
                body: """
                    <h3>测试报告详情</h3>
                    <p>构建编号: ${env.BUILD_NUMBER}</p>
                    <p>测试环境: Production</p>
                    <p>报告链接: <a href="${env.BUILD_URL}allure/">查看详情</a></p>
                """,
                to: 'qa-team@example.com',
                mimeType: 'text/html'
            )
        }
    }
}