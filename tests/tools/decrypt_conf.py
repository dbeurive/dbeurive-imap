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
import re
from pathlib import Path
from shutil import copyfile

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), os.path.pardir, os.path.pardir))
from dbeurive.imap.config import Config


def find_backup_name(dir_path: str, backup_name: str) -> str:
    """ Find the name of the backup.

    :param dir_path: path to the directory used to store the backups.
    :param backup_name: basename of the backup file.
    :return: The function returns a suitable backup name.
    """
    index = 1
    r = re.compile('\.(\d+)$')
    for entry in os.listdir(dir_path):
        if os.path.isfile(os.path.join(data_path, entry)):
            if len(entry) <= len(backup_name):
                continue
            if backup_name != entry[0:len(backup_name)]:
                continue
            m = r.match(entry[len(backup_name):])
            if m is not None:
                i = int(m.group(1))
                index = i if i > index else index
    index += 1
    return f'{backup_name}.{index}'


data_path: str = os.path.join(os.path.dirname(os.path.abspath(__file__)), os.path.pardir, 'data')
config_path_clear: str = os.path.join(data_path, 'isp.yaml')
config_path_clear_backup: str = find_backup_name(data_path, 'isp.yaml.backup')
config_path_cyphered: str = os.path.join(data_path, 'isp.yaml.aes')

print(f"Decrypt the configuration file:\n\n"
      f"\t{config_path_cyphered}\n\n"
      "and store the result into the file\n\n"
      f"\t{config_path_clear}\n")

path = Path(config_path_clear)
if path.is_file():
    print(f"Make a backup copy of the clear configuration...")
    try:
        copyfile(config_path_clear, config_path_clear_backup)
    except Exception as e:
        print(f'Cannot backup the configuration file {config_path_clear}: {e}')
        sys.exit(1)
    print(f'Done. Path to the backup: "{config_path_clear_backup}"' + "\n")

cyphered_conf: Config = Config.get_conf_from_file(config_path_cyphered, False)

with open(config_path_clear, 'w') as fd:
    fd.write(cyphered_conf.dump())

print('Done. Test that we can load it...')



