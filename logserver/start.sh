#!/bin/sh

script_path=$(cd `dirname $0`; pwd)

python3 ${script_path}/src/app.py worker -l info -f ${script_path}/logs/app.log -p 6066
