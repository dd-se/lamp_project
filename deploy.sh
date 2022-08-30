#!/usr/bin/env bash
if [ ! -d "app/.virtualenv" ]; then
    echo "You have not set up a virtual enviroment for testing the application"
    echo "Step 1: CD into app folder and run 'python3 -m venv .virtualenv'"
    echo "Step 2: Run 'source .virtualenv/bin/activate' to activate virtual enviroment"
    echo "Step 3: Run 'pip install -r requirements.txt'"
    exit
fi
cd app && .virtualenv/bin/pytest
if [ $? -ne 0 ]; then
    echo "Tests failed, exiting!"
else
    echo "Tests passed, deploying..."
    cd ..
    ansible-playbook -e @secrets.yml --ask-vault-pass playbook.yml
fi
