properties([pipelineTriggers([githubPush()])])
void setBuildStatus(String message, String state) {
  step([
      $class: "GitHubCommitStatusSetter",
      reposSource: [$class: "ManuallyEnteredRepositorySource", url: "https://github.com/SophiaHadash/ArgueView"],
      contextSource: [$class: "ManuallyEnteredCommitContextSource", context: "ci/jenkins/build-status"],
      errorHandlers: [[$class: "ChangingBuildStatusErrorHandler", result: "UNSTABLE"]],
      statusResultSource: [ $class: "ConditionalStatusResultSource", results: [[$class: "AnyBuildResult", message: message, state: state]] ]
  ]);
}
def buildBadge = addEmbeddableBadgeConfiguration(id: "build", subject: "ArgueView Build");

pipeline {
  agent {
    docker {
      image 'python:3.6.12'
    }
  }
  options {
	skipStagesAfterUnstable()
  }
  stages {
    stage('test build context') {
      steps {
		sh 'python --version'
      }
    }
    stage('build') {
      steps {
        setBuildStatus("Building...", "PENDING");
        script{ buildBadge.setStatus('running'); }
        sh 'bash build.sh'
      }
    }
	stage('publish') {
	  when {
        branch 'master'
      }
	  steps {
		sh ''
	  }
	}
  }
  post {
    success {
	  setBuildStatus("Build succeeded", "SUCCESS");
	  script{ buildBadge.setStatus('passing'); }
    }
    failure {
      setBuildStatus("Build failed", "FAILURE");
  	  script{ buildBadge.setStatus('failing'); }
    }
  }
}
