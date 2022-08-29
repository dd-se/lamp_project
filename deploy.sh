#!/usr/bin/env bash
ansible-playbook -e @secrets.yml --ask-vault-pass playbook.yml
