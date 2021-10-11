def run_with_pod(Closure body) {
    def label = "pingcap-com-cn-build"
    def cloud = "kubernetes"
    podTemplate(label: label,
            cloud: cloud,
            namespace: 'jenkins-tidb',
            containers: [
                    containerTemplate(
                            name: 'node', alwaysPullImage: false,
                            image: "hub.pingcap.net/jenkins/node:14.18.0", ttyEnabled: true,
                            resourceRequestCpu: '2000m', resourceRequestMemory: '4Gi',
                            resourceLimitCpu: '4000m', resourceLimitMemory: "8Gi",
                            command: '/bin/sh -c', args: 'cat',
                    ),
                    containerTemplate(
                            name: 'base', alwaysPullImage: false,
                            image: "registry-mirror.pingcap.net/instrumentisto/rsync-ssh", ttyEnabled: true,
                            resourceRequestCpu: '2000m', resourceRequestMemory: '4Gi',
                            resourceLimitCpu: '4000m', resourceLimitMemory: "8Gi",
                            command: '/bin/sh -c', args: 'cat',
                    ),
            ],
    ) {
        node(label) {
            println "debug command:\nkubectl -n jenkins-tidb exec -ti ${NODE_NAME} bash"
            body()
        }
    }

}

run_with_pod() {
    container("node") {
        stage("download code") {
            timeout(time: 10, unit: 'MINUTES') { 
                def refspec = "+refs/heads/*:refs/remotes/origin/*"
                checkout(changelog: false, poll: false, scm: [
                        $class: "GitSCM",
                        branches: [
                                [name: "XC_Web"],
                        ],
                        userRemoteConfigs: [
                                [
                                        url: "git@github.com:pingcap/pingcap.github.io.git",
                                        refspec: refspec,
                                        credentialsId: "github-sre-bot-ssh",
                                ]
                        ],
                        extensions: [
                                [$class: 'PruneStaleBranch'],
                                [$class: 'CleanBeforeCheckout'],
                        ],
                ])
            }
            
        }
        
        stage('test and build') {
            timeout(time: 10, unit: 'MINUTES') {
                sh """
                node -v
                npm -v
                sudo apt update && sudo apt install python3 python3-bs4 python3-pip -y
                timeout -s 9 300 npm install
                npm run build
                echo 'Building successful'
                """
            }
        }
    }

    container("base") {
        stage('deploy to production environment') {
            timeout(time: 10, unit: 'MINUTES') { 
                withCredentials([
                    string(credentialsId: 'pingcap.com.cn-user', variable: 'PINGCAP_COM_CN_USER'),
                    string(credentialsId: 'pingcap.com.cn-host', variable: 'PINGCAP_COM_CN_HOST'),
                    string(credentialsId: 'pingcap.com.cn-path', variable: 'PINGCAP_COM_CN_PATH')
                ]) { 
                    sh """
                    echo 'Deploying to production environment....'
                    ssh-keyscan "${PINGCAP_COM_CN_HOST}" >> ~/.ssh/known_hosts 2>/dev/null
                    rsync -avz --progress --delete dist/ ${PINGCAP_COM_CN_USER}@${PINGCAP_COM_CN_HOST}:${PINGCAP_COM_CN_PATH}
                    echo 'Deploying successful'
                    """
                }
            }
        }
    }
}
