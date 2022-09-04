#!/usr/bin/env bash
export TF_IN_AUTOMATION=YES
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
    exit
fi
echo "Tests passed, deploying..."
cd ../provisioner || exit
terraform apply --auto-approve || exit
echo "Provisioning done, creating ansible inventory."
LB=$(terraform output -raw loadbalancer)
DB=$(terraform output -raw database)
BACKENDS=$(terraform output -json backends | jq -r .[])
cd .. || exit
cat <<EOF >hosts
[loadbalancer]

[backend]

[database]

[stack:children]
loadbalancer
backend
database
EOF
echo "Added loadbalancer ${LB}"
sed -i "/\[loadbalancer\]/a ${LB}" hosts
echo "Added database ${DB}"
sed -i "/\[database\]/a ${LB}" hosts
for backend in $BACKENDS; do
    echo "Added backend ${backend}"
    sed -i "/\[backend\]/a ${backend}" hosts
done
ansible-playbook -e @secrets.yml --ask-vault-pass playbook.yml
