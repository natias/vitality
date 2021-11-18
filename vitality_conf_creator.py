# -*- coding: utf-8 -*-
import yaml
import io

# Define data
data = {
    'pus_suffixes': [
        'PU1', 
        'PU22'
    ],
    'base_url': 'https://address_of_apigee/path_to_ods',
    'cert_file_path': './cert.pfx' ,
    'read_time_out_seconds': 0.8,
    'connection_time_out_seconds': 0.3
}

# Write YAML file
with io.open('./vitality_conf.yaml', 'w', encoding='utf8') as outfile:
    yaml.dump(data, outfile, default_flow_style=False, allow_unicode=True)

# Read YAML file
with open('./vitality_conf.yaml', 'r') as stream:
    data_loaded = yaml.safe_load(stream)

print(data == data_loaded)

