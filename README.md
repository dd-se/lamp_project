# How to Set Up a Development Environment

Follow these steps to set up your development environment:

1. **Run the Ansible Playbook**
   - Ensure you have [Ansible](https://docs.ansible.com/ansible/latest/installation_guide/intro_installation.html#installing-and-upgrading-ansible), [Docker](https://docs.docker.com/get-docker/), and [Docker Compose](https://docs.docker.com/compose/install/) installed.
   - Execute the following command:
     ```bash
     sudo ansible-playbook setup_dev_env.yml
     ```

2. **Set Up a Python Virtual Environment**
   - Navigate to the `app` folder:
     ```bash
     cd app
     ```
   - Create a virtual environment:
     ```bash
     python3 -m venv .virtualenv
     ```

3. **Activate the Virtual Environment**
   - Run the following command:
     ```bash
     source .virtualenv/bin/activate
     ```

4. **Install Dependencies**
   - With the virtual environment activated, install the required dependencies:
     ```bash
     pip install -r requirements.txt
     ```

5. **Run the Application**
   - To run the application using Uvicorn:
     ```bash
     uvicorn main:app --reload --port 12345
     ```

6. **Read the Documentation**
   - Familiarize yourself with the [FastAPI documentation](https://fastapi.tiangolo.com/tutorial/).
---
**Diagram**

![Alt text](https://i.imgur.com/TEmIcCI.png "Diagram")
