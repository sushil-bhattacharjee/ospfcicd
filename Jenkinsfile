pipeline {
    agent any
    environment {
        ANSIBLE_HOST_KEY_CHECKING = "False"
    }
    stages {
        stage('Setup') {
            steps {
                sh '''
                    # Using sudo for apt-get commands to resolve permission issues
                    sudo apt-get update && sudo apt-get install -y sshpass git libffi-dev gcc || true

                    # Creating and activating a Python virtual environment
                    python3 -m venv .venv
                    . .venv/bin/activate

                    # Upgrading pip and installing required Python packages
                    pip install --upgrade pip
                    pip install ansible ansible-pylibssh jinja2 paramiko pyyaml requests || true
                    
                    # Setting permissions for the workspace
                    chmod 755 $WORKSPACE
                '''
            }
        }
        stage('Show Version') {
            steps {
                sh '''
                    echo "Fetching 'show version' using REST API for R1"
                    python3 fetch_show_version.py 10.1.10.11 cisco cisco
                    echo "Fetching 'show version' using REST API for R2"
                    python3 fetch_show_version.py 10.1.10.12 cisco cisco
                    echo "Fetching 'show version' using REST API for R3"
                    python3 fetch_show_version.py 10.1.10.13 cisco cisco
                    echo "Fetching 'show version' using REST API for R5"
                    python3 fetch_show_version.py 10.1.10.15 cisco cisco
                '''
            }
        }
        stage('Connection Test') {
            steps {
                sh '''
                    echo "Testing SSH connectivity to all routers"
                    ansible all -i inventory.yml -m ping
                '''
            }
        }
        stage('Build') {
            steps {
                sh '''
                    echo "Configuring OSPF for R1 and R2"
                    ansible-playbook configure_ospf.yml -i inventory.yml --limit R1,R2 -vvv
                '''
            }
        }
        stage('Test') {
            steps {
                sh '''
                    echo "Verifying OSPF Neighborship between R1 and R2"
                    ansible-playbook verify_ospf.yml -i inventory.yml --limit R1,R2
                '''
            }
        }
        stage('Deploy') {
            steps {
                sh '''
                    echo "Configuring OSPF for R5 and R3"
                    ansible-playbook configure_ospf.yml -i inventory.yml --limit R5,R3
                    echo "Waiting for 60 seconds to allow OSPF adjacency to form"
                    sleep 60
                    echo "Verifying OSPF Neighborship between R5 and R3"
                    ansible-playbook verify_ospf.yml -i inventory.yml --limit R5,R3
                '''
            }
        }
    }
}


