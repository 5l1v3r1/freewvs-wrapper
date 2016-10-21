#!/bin/sh

dir=$(dirname "$0")
install_dir=$(cd "$dir" && pwd)

if [ -z "$1" ]; then
  echo "Usage: $0 path/to/hosting(s)"
  exit 1
fi

# update freewvs database and send output to process script
cd freewvs || exit 1
pwd
update=$(svn up "freewvsdb")
cd .. || exit 1

cd "$install_dir" || exit 1
./freewvs/freewvs -x "$1" > vulnscan.xml
python ./processResults.py "$update"

exit 0
