pipeline {
    agent any
    environment {
        // GCloud SDK Image
        GCLOUD_SDK_IMAGE = "google/cloud-sdk:386.0.0"
        GCLOUD_AUTH_CREDENTIALS = "cloud-telephony-sa-key"

        // Service Configuration
        SERVICE_NAME = "whisper"
        SERVICE_PORT = "8080"

        // Cloud Run Configuration
        CLOUDRUN_PROJECT = "truecaller-cloud-telephony"
        CLOUDRUN_REGION = "asia-south1"
        CLOUDRUN_SERVICE_ACCOUNT = "whisper"

        // Image Configuration
        GCR_HOST = "asia.gcr.io"
        GCR_IMAGE = "${env.GCR_HOST}/${env.CLOUDRUN_PROJECT}/${env.SERVICE_NAME}"
        IMAGE_VERSION = "${env.BUILD_NUMBER}-${env.GIT_COMMIT}"

        // Branch from which we publish changes
        PUBLISH_BRANCH = "master"

    }
	stages {
        stage('Build') {
            steps {
                script {
                    echo "Building docker image for '${SERVICE_NAME}'..."
                    sh "docker build -t ${GCR_IMAGE}:${IMAGE_VERSION} ."
                }
            }
        }
        stage('Push Image') {
            when {
                expression {
                    return env.BRANCH_NAME == "${PUBLISH_BRANCH}";
                }
            }
            steps {
                script {
                    echo "Pushing '${GCR_IMAGE}:${IMAGE_VERSION}' to GCR..."
                    withCredentials([file(credentialsId: "${GCLOUD_AUTH_CREDENTIALS}", variable: 'GCLOUD_SERVICE_KEY')]) {
                        sh '''
                            # Login to docker and push image to GCR
                            cat "${GCLOUD_SERVICE_KEY}" | docker login -u _json_key --password-stdin https://${GCR_HOST}
                            docker push ${GCR_IMAGE}:${IMAGE_VERSION}
                            docker logout https://${GCR_HOST}
                        '''
                    }
                }
            }
        }
        stage('Deploy') {
            when {
                expression {
                    return env.BRANCH_NAME == "${PUBLISH_BRANCH}";
                }
            }
            steps {
                script {
                    withCredentials([file(credentialsId: "${GCLOUD_AUTH_CREDENTIALS}", variable: 'GCLOUD_SERVICE_KEY')]) {
                        sh '''
                            docker run --rm -v "${GCLOUD_SERVICE_KEY}:/root/auth.json" ${GCLOUD_SDK_IMAGE} /bin/bash -c "\
                                gcloud auth activate-service-account --key-file=/root/auth.json && \
                                gcloud run deploy ${SERVICE_NAME} \
                                    --project=${CLOUDRUN_PROJECT} \
                                    --image=${GCR_IMAGE}:${IMAGE_VERSION} \
                                    --region=${CLOUDRUN_REGION} \
                                    --service-account=\"${CLOUDRUN_SERVICE_ACCOUNT}@${CLOUDRUN_PROJECT}.iam.gserviceaccount.com\" \
                                    --port=${SERVICE_PORT}
                            "
                        '''
                    }
                }
            }
        }
    }
    post {
        always {
            script {
                echo "Cleaning up..."
                sh '''
                    docker rmi ${GCR_IMAGE}:${IMAGE_VERSION} || true
                    docker logout https://${GCR_HOST} || true
                '''
            }
        }
    }
}
