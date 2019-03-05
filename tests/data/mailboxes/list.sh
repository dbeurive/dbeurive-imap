#!/usr/bin/env bash

SOURCE="${BASH_SOURCE[0]}"
while [ -h "$SOURCE" ] ; do SOURCE="$(readlink "$SOURCE")"; done
readonly __DIR__="$( cd -P "$( dirname "$SOURCE" )" && pwd )"

for f in "${__DIR__}"/*.raw; do
    declare isp=$(echo "${f}" | sed 's/.*\///; s/\-lst.raw$//')
    echo "${isp}:"
    echo
    "${__DIR__}"/dump.py "${f}"
    echo
done
