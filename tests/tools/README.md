# Description

This directory contains scripts used to setup the data for the unit tests execution.

# conf_validator.py

Validate the configuration file.

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

# get_emails_id.py

This script connects to all configured ISP and gets the IDs of the emails located in INBOX directory.
The IDs are stored into files, within the directory "`../data/emails-ids`".
These files have names suffixed by "`-ids.raw`". For examples:

* `laposte.net-ids.raw`
* `mail.com-ids.raw`
* `net-c.com-ids.raw`
* `vivaldi.net-ids.raw`
* `yandex.ru-ids.raw`

# get_mailboxes_lists.py

This script connects to all configured ISP and lists the mailboxes located in the top directories.
The lists of mailboxes are stored into files, within the directory "`../data/mailboxes`".
These files have names suffixed by "`-lst.raw`". For examples:

* `laposte.net-lst.raw`
* `mail.com-lst.raw`
* `net-c.com-lst.raw`
* `vivaldi.net-lst.raw`
* `yandex.ru-lst.raw`

# pick_emails_ids.py

The script was used to check the way to get the list of emails IDs.

# pick_mailboxes_lists.py

The script was used to check the way mailbox listing must be performed.


