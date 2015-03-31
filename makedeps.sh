#!/bin/sh

SDK=$1
VERSION=$2

mkdir -p build
BUILDDIR=`mktemp -d build/XXXXXX`
xdg-app build-init ${BUILDDIR} -v ${SDK}.Var ${SDK} ${SDK} ${VERSION}

function finish {
    rm -rf ${BUILDDIR}
}
trap finish EXIT

export LC_ALL=C
for SPEC in SPECS/*.spec; do
    URLS=`xdg-app build ${BUILDDIR} rpmspec -P ${SPEC} | grep "^Source.*:" | awk '{ print $2 }' /dev/stdin | grep 'http\|ftp'`

    for URL in $URLS; do
        FILENAME=SOURCES/`basename $URL`
        BARE_URL=`echo $URL | sed s/\?.*//`
        echo "$FILENAME:"
        echo "	mkdir -p SOURCES"
        echo "	wget -O $FILENAME $BARE_URL"
        echo
    done

    echo -n "`basename ${SPEC} .spec` "
    xdg-app build ${BUILDDIR} rpmspec -q ${SPEC} --qf "%{NAME}.rpm "
    echo -n ": $SPEC "
    for BR in `xdg-app build ${BUILDDIR} rpmspec -q ${SPEC} --buildrequires`; do
        echo -n "$BR.rpm "
    done
    for URL in $URLS; do
        FILENAME=SOURCES/`basename $URL`
        echo -n "$FILENAME "
    done
    echo
    echo "	./build.sh ${SDK} ${VERSION} ${SPEC}"
    echo


done
