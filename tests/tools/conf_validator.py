import yaml
import os
import sys
from typing import Mapping, List, Any

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), os.path.pardir, os.path.pardir))

from dbeurive.imap.config import Config

DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_CONF = os.path.join(DIR, os.path.pardir, 'data', 'isp.yaml')

config_file = DEFAULT_CONF
print(f'Configuration file: {config_file}')

text = Config.load_conf(config_file)
conf: Mapping[str, Mapping[str, Mapping[str, str]]] = yaml.load(text)
if Config.validate_conf(conf):
    print("The configuration is valid.")
else:
    print("The configuration is _NOT_ valid.")
