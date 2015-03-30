#!/bin/sh

RPM=$1

REQUIRES=
DONE=

TODO=$RPM

not_in_list() {
  for word in $1; do
    [[ $word = $2 ]] && return 1
  done
  return 0
}

while [ "x$TODO" != "x" ]; do
    NEW=""
    for i in $TODO; do
        DONE="$DONE $i"
        DEPS=$(rpm -qp --requires $i.rpm | awk "{ print \$1}" | grep -v "^/" | grep -v \()
        for j in $DEPS; do
            if not_in_list "$DONE" "$j"; then
                echo -n "$j.rpm "
                NEW="$NEW $j"
            fi
        done
    done
    TODO="$NEW"
done
