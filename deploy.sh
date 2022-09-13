#!/usr/bin/env bash
if [[ "${1}" == "insert" ]]; then
    ansible-playbook -e @secrets.yml --ask-vault-pass insert_movies.yml
    exit
fi
if [ ! -d "app/.virtualenv" ]; then
    echo "Setting up virtual enviroment for testing the application before deployment..."
    cd app && python3 -m venv .virtualenv
    .virtualenv/bin/pip3 install -r requirements.txt
    cd ..
fi
cd app && .virtualenv/bin/pytest
if [ $? -ne 0 ]; then
    echo "Tests failed, exiting!"
    exit
fi
echo "Tests passed, deploying..."
cd ../provisioner || exit
terraform apply -input=false -auto-approve >/dev/null || exit
echo "Provisioning done, creating ansible inventory."
LOADBALANCER=$(terraform output -raw loadbalancer)
DATABASE=$(terraform output -raw database)
DOCTOR=$(terraform output -raw doctor)
BACKENDS=$(terraform output -json backends | jq -r .[])
cd .. || exit
cat <<EOF >hosts
[loadbalancer]

[backend]

[database]

[doctor]

[patients:children]
loadbalancer
backend
database

[stack:children]
loadbalancer
backend
database
doctor
EOF
echo "Added loadbalancer ${LOADBALANCER}"
sed -i "/\[loadbalancer\]/a ${LOADBALANCER}" hosts
echo "Added database ${DATABASE}"
sed -i "/\[database\]/a ${DATABASE}" hosts
echo "Added doctor ${DOCTOR}"
sed -i "/\[doctor\]/a ${DOCTOR}" hosts
for backend in $BACKENDS; do
    echo "Added backend ${backend}"
    sed -i "/\[backend\]/a ${backend}" hosts
done
if [ -n "${1}" ]; then
    ansible-playbook -e @secrets.yml --tags "${1}" --ask-vault-pass playbook.yml || exit
else
    ansible-playbook -e @secrets.yml --ask-vault-pass playbook.yml || exit
fi
echo "Visit https://group-soup.duckdns.org"
