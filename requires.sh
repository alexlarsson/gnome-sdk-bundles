#!/bin/sh

RPM=$1

REQUIRES=
DONE=

SDK=org.freedesktop.Sdk
VERSION=1.2

mkdir -p build
BUILDDIR=`mktemp -d build/XXXXXX`
xdg-app build-init ${BUILDDIR} -v ${SDK}.Var org.gnome.TempBuild ${SDK} ${SDK} ${VERSION}

function finish {
    rm -rf ${BUILDDIR}
}
trap finish EXIT

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
        DEPS=$(xdg-app build ${BUILDDIR} rpm -qp --requires $i.rpm | awk "{ print \$1}" | grep -v "^/" | grep -v \()
        for j in $DEPS; do
            if not_in_list "$DONE" "$j"; then
                echo -n "$j.rpm "
                NEW="$NEW $j"
            fi
        done
    done
    TODO="$NEW"
done
