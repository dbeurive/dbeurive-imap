# Description

This directory contains scripts used to setup the data for the unit tests execution.

# cypher_conf.py

This script takes the configuration file "`../data/isp.yaml`" and cyphers it.
The cyphered file will be "`../data/isp.yaml.aes`".

Please note that you must provide the cypher key and the cypher IV.

* The cypher key is set through the environment variable "`CYPHER_KEY`".
* The cypher IV is set through the environment variable "`CYPHER_IV`".

# decrypt_conf.py

This script takes a cyphered configuration file "`../data/isp.yaml.aes`" and decrypts it.
The decrypted file will be "`../data/isp.yaml`".

Please note that you must provide the cypher key and the cypher IV.

* The cypher key is set through the environment variable "`CYPHER_KEY`".
* The cypher IV is set through the environment variable "`CYPHER_IV`".

# get_lists.py

This script connects to all configured ISP and lists the mailboxes located in the top directories.
The lists of mailboxes are stored into files, within the directory "`../data`".
These files have names suffixed by "`-lst.raw`". For examples:

* `laposte.net-lst.raw`
* `mail.com-lst.raw`
* `net-c.com-lst.raw`
* `vivaldi.net-lst.raw`
* `yandex.ru-lst.raw`

# conf_validator.py

Validate the configuration file.

# list_mailboxes.py

The script was used to check the way mailbox listing must be performed.


