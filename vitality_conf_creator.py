# -*- coding: utf-8 -*-
import yaml
import io

# Define data
data = {
    'pus': [
        '',
        '',
        '',
        '',
        '',
    ],
    'base_url_server_part': 'https://localhost:8443',
    'base_url_path': '/posts',
    'cert_file_path': 'certs/keyStore.p12' ,
    'read_time_out_seconds': 1.2,
    'connection_time_out_seconds': 1.1
}

# Write YAML file
with io.open('./vitality_conf.yaml', 'w', encoding='utf8') as outfile:
    yaml.dump(data, outfile, default_flow_style=False, allow_unicode=True)

# Read YAML file
with open('./vitality_conf.yaml', 'r') as stream:
    data_loaded = yaml.safe_load(stream)

print(data == data_loaded)

