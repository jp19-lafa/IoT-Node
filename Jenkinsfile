void setBuildStatus(String message, String state) {
  step([
      $class: "GitHubCommitStatusSetter",
      reposSource: [$class: "ManuallyEnteredRepositorySource", url: "https://github.com/jp19-lafa/IoT-Node"],
      contextSource: [$class: "ManuallyEnteredCommitContextSource", context: "ci/jenkins/build-status/node/unittest"],
      errorHandlers: [[$class: "ChangingBuildStatusErrorHandler", result: "UNSTABLE"]],
      statusResultSource: [ $class: "ConditionalStatusResultSource", results: [[$class: "AnyBuildResult", message: message, state: state]] ]
  ]);
}

pipeline {
    agent {
              docker {
                 image 'python:3'
               }
    }
    stages {
        stage('clone') {
            steps{
                git 'https://github.com/jp19-lafa/IoT-Node.git'
            }
        }
        stage('Build') {
            steps {
                sh 'cd src && python -m unittest'
            }
        }
    }
    post {
        success {
            setBuildStatus("Test succeeded", "SUCCESS");
        }
        unstable {
            setBuildStatus("Test is unstable", "UNSTABLE");
        }
        failure {
            setBuildStatus("Test failed", "FAILED");
        }
        
    }
}