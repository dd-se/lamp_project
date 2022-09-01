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
    exit
fi
echo "Tests passed, deploying..."
cd ../provisioner || exit
terraform apply --auto-approve || exit
echo "Provisioning done, creating ansible inventory."
ips=$(terraform output -json public_ip | jq -r .[])
cd .. || exit
cat <<EOF >hosts
[frontend]

[backend]

[db]

[stack:children]
frontend
backend
db
EOF
count=0
for ip in $ips; do
    echo "Added IP ${ip}"
    case $count in
    0)
        sed -i "/\[frontend\]/a ${ip}" hosts
        ;;
    1)
        sed -i "/\[db\]/a ${ip}" hosts
        ;;
    *)
        sed -i "/\[backend\]/a ${ip}" hosts
        ;;
    esac
    count=$((count + 1))
done
ansible-playbook -e @secrets.yml --ask-vault-pass playbook.yml
