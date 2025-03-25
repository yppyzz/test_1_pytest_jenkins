pipeline {
    agent any  // 使用任意可用节点执行

    // 环境变量（全局配置）
    environment {
        PROJECT_DIR = "router_auto_test"  // 项目目录名
        PYTHON_PATH = "/usr/bin/python3"  // Python解释器路径
    }

    stages {
        // --------------------- 阶段1：代码检出 ---------------------
        stage('Checkout Code') {
            steps {
                checkout([
                    $class: 'GitSCM',
                    branches: [[name: 'main']],  // 分支名称
                    extensions: [],
                    userRemoteConfigs: [[
                        url: https://github.com/yppyzz/test_1_pytest_jenkins.git'  // 仓库地址
                    ]]
                ])
            }
        }

        // --------------------- 阶段2：安装依赖 ---------------------
        stage('Install Dependencies') {
            steps {
                sh """
                    cd ${PROJECT_DIR}
                    ${PYTHON_PATH} -m pip install --upgrade pip
                    pip install -r requirements.txt
                """
            }
        }

        // --------------------- 阶段3：执行测试 ---------------------
        stage('Run Tests') {
            steps {
                sh """
                    cd ${PROJECT_DIR}
                    pytest test_cases/ \
                        --alluredir=./allure-results \
                        --junitxml=./test-results/results.xml \
                        -v
                """
            }
        }

        // --------------------- 阶段4：生成报告 ---------------------
        stage('Generate Report') {
            steps {
                allure([
                    includeProperties: false,
                    jdk: '',
                    results: [[path: "${PROJECT_DIR}/allure-results"]],
                    reportBuildPolicy: 'ALWAYS'
                ])
                junit "${PROJECT_DIR}/test-results/results.xml"
            }
        }
    }

    // --------------------- 构建后处理 ---------------------
    post {
        always {
            // 清理临时文件
            cleanWs()
            // 发送邮件通知
            emailext(
                subject: "测试结果 - ${currentBuild.currentResult} (构建号: ${env.BUILD_NUMBER})",
                body: """
                    <h3>路由器自动化测试报告</h3>
                    <p>构建状态: <strong>${currentBuild.currentResult}</strong></p>
                    <p>构建详情: <a href="${env.BUILD_URL}">${env.BUILD_URL}</a></p>
                    <p>Allure报告: <a href="${env.BUILD_URL}allure/">点击查看</a></p>
                """,
                to: 'qa-team@example.com',
                mimeType: 'text/html'
            )
        }
    }
}
