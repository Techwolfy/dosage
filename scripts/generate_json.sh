#!/bin/sh
# Copyright (C) 2012-2014 Bastian Kleineidam
# Copyright (C) 2015-2020 Tobias Gruetzmacher
# Copyright (C) 2019-2020 Daniel Ring
set -e
set -u

d=$(dirname $0)
if [ $# -ge 1 ]; then
    list="$*"
else
    list="arcamax comicfury comicgenesis creators gocomics keenspot smackjeeves tapastic webcomicfactory webtoons"
fi
for script in $list; do
    echo "Executing ${script}.py"
    "${d}/${script}.py"
done
