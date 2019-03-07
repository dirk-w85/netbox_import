# netbox_import
This script pulls several details of prefixes from Netbox using the REST API. 
Based on Tags, it then creates files which can be used in tools linke Ansible of Prometheus (file_sd).


## Usage
Clone the Repo
```
python netbox_import.py [NETBOX-URL]

python netbox_import_zabbix.py [NETBOX-URL]

python netbox_import_prometheus.py [NETBOX-URL]
```
