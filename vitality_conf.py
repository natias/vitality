# -*- coding: utf-8 -*-
import yaml
import io
import os

conf_file_name='./vitality_conf.yaml'

lupdate=0

# Define data
conf_data = {
}


def refresh_conf():
    global lupdate
    global conf_data 
    f_updata=os.path.getmtime(conf_file_name)
    if f_updata>lupdate:
       #print("reloading conf data")
       with open(conf_file_name, 'r') as stream:
          conf_data = yaml.safe_load(stream)
          #print(conf_data)
       lupdate=f_updata 
    else:
       print("not reloading")
    return

def get_conf():
    print("current conf data"+str(conf_data))
    refresh_conf()
    return conf_data


# Write YAML file
#with io.open('data.yaml', 'w', encoding='utf8') as outfile:
#    yaml.dump(data, outfile, default_flow_style=False, allow_unicode=True)

# Read YAML file
#with open("data.yaml", 'r') as stream:
#    data_loaded = yaml.safe_load(stream)

#print(data == data_loaded)

#data2 = [1,2,3,4,5]

#with io.open('dataw.yaml', 'w', encoding='utf8') as outfile:
#    yaml.dump(data2, outfile, default_flow_style=False, allow_unicode=True)

#print( data2)
