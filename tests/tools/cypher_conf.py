# This script cyphers the configuration file "../data/isp.yaml".
#
# Please note that the file "../data/isp.yaml" is not keep under the GIT repository.
# Only the cyphered version of the configuration file is kept under the GIT repository.
#
# In order to use this script, you must set the following environment variables:
#
#   * CYPHER_KEY
#   * CYPHER_IV

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), os.path.pardir, os.path.pardir))

from dbeurive.imap.config import Config

data_path: str = os.path.join(os.path.dirname(os.path.abspath(__file__)), os.path.pardir, 'data')
config_path_clear: str = os.path.join(data_path, 'isp.yaml')
config_path_cyphered: str = os.path.join(data_path, 'isp.yaml.aes')

print(f"Cypher the configuration file:\n\n"
      f"\t{config_path_clear}\n\n"
      "and store the result into the file\n\n"
      f"\t{config_path_cyphered}\n")

conf: Config = Config.get_conf_from_file(config_path_clear)
cyphered_conf: bytes = Config.cypher(conf.dump())

with open(config_path_cyphered, 'wb') as fd:
    fd.write(cyphered_conf)

print('Done. Test that we can decrypt...')

dconf = Config.get_conf_from_file(config_path_cyphered, clear=False)
if Config.cmp_conf(conf.get_conf(), dconf.get_conf()):
    print("OK")
