#!/usr/sh

cd /tmp
python /mnt/files/Coding/netbox_import/netbox_import.py docker-01:8082
sleep 1
cp --force /tmp/hosts /mnt/files/Ansible/
cp --force /tmp/hosts.yml /mnt/files/Ansible/roles/dns-dhcp-host/vars/

sleep 1
python /mnt/files/Coding/netbox_import/netbox_import_zabbix.py docker-01:8082
cp --force /tmp/zabbix_hosts.yml /mnt/files/Ansible/seclab/

sleep 1
python /mnt/files/Coding/netbox_import/netbox_import_prometheus.py docker-01:8082
cp --force /tmp/blackbox_targets.json /mnt/files/Ansible/roles/prometheus-server/files
cp --force /tmp/node_targets.json /mnt/files/Ansible/roles/prometheus-server/files