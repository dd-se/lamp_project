
## HOW TO SETUP A DEV ENVIRONMENT
### 1. Run 'sudo ansible-playbook setup_dev_env.yml' (ansible, docker and docker-compose required  https://docs.ansible.com/ansible/latest/installation_guide/intro_installation.html#installing-and-upgrading-ansible - https://docs.docker.com/compose/install/)
### 2. 'cd' into app folder and run 'python3 -m venv .virtualenv'
### 3. Run 'source .virtualenv/bin/activate' to activate virtual enviroment"
### 4. Run 'pip install -r requirements.txt'"
### 5. With the environment activated, press F5 to run in the app in debug mode, else run 'uvicorn main:app --reload --port 12345'.
### 6. Read the docs https://fastapi.tiangolo.com/tutorial/


DIAGRAM

![Alt text](https://i.imgur.com/TEmIcCI.png "Optional title")


