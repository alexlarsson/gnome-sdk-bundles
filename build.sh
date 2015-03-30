#!/bin/sh

SDK=$1
VERSION=$2
SPEC=$3

SRCDIR=`pwd`

mkdir -p build
BUILDDIR=`mktemp -d build/XXXXXX`
function finish {
    rm -rf ${BUILDDIR}
}
trap finish EXIT


xdg-app build-init ${BUILDDIR} -v ${SDK}.Var ${SDK} ${SDK} ${VERSION}

for BR in `xdg-app build ${BUILDDIR} rpmspec -q ${SPEC} --buildrequires`; do
    xdg-app build ${BUILDDIR} rpm -Uvh $(./requires.sh ${BR}) ${BR}.rpm
done

xdg-app build ${BUILDDIR} rpmspec -q ${SPEC} --qf "rm -f %{NAME}.rpm\n" | sh

xdg-app build ${BUILDDIR} rpmbuild --define "_topdir ${SRCDIR}" --clean -bb ${SPEC}
rc=$?; if [ $rc != 0 ] ; then exit $rc; fi

xdg-app build ${BUILDDIR} rpmspec -q ${SPEC} --qf "ln -sf RPMS/%{ARCH}/%{NAME}-%{VERSION}-%{RELEASE}.%{ARCH}.rpm %{NAME}.rpm\n" | sh
