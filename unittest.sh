#!/usr/bin/env bash

SOURCE="${BASH_SOURCE[0]}"
while [ -h "$SOURCE" ] ; do SOURCE="$(readlink "$SOURCE")"; done
readonly __DIR__="$( cd -P "$( dirname "$SOURCE" )" && pwd )"

if [ -z "${CYPHER_KEY}" ]; then
    echo "Environment variable CYPHER_KEY is not defined. Abort."
    exit 1
fi

if [ -z "${CYPHER_IV}" ]; then
    echo "Environment variable CYPHER_IV is not defined. Abort."
    exit 1
fi

echo "Run relatively to \"${__DIR__}\""
python3 -m unittest discover -s "${__DIR__}/tests" "$@" -p *_test.py