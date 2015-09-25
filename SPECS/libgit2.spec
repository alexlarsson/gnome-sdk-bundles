Name:           libgit2
Version:        0.23.2
Release:        1%{?dist}
Summary:        C implementation of the Git core methods as a library with a solid API
License:        GPLv2 with exceptions
URL:            http://libgit2.github.com/
Source0:        https://github.com/libgit2/libgit2/archive/v%{version}.tar.gz?/%{name}-%{version}.tar.gz

BuildRequires:  http-parser-dev libssh2-dev

Requires: http-parser libssh2

%description
libgit2 is a portable, pure C implementation of the Git core methods
provided as a re-entrant linkable library with a solid API, allowing
you to write native speed custom Git applications in any language
with bindings.

%package        dev
Summary:        Development files for %{name}
Requires:       %{name} = %{version}-%{release}
Requires:       libssh2-dev

%description    dev
This package contains libraries and header files for
developing applications that use %{name}.

%prep
%setup -q

# Remove VCS files from examples
find examples -name ".gitignore" -delete -print

# Fix pkgconfig generation
sed -i 's|@CMAKE_INSTALL_PREFIX@/||' libgit2.pc.in

# Don't test network
sed -i 's/ionline/xonline/' CMakeLists.txt

# Remove bundled libraries
rm -frv deps

%build
CFLAGS="${CFLAGS:-%optflags}" ; export CFLAGS ; \
CXXFLAGS="${CXXFLAGS:-%optflags}" ; export CXXFLAGS ; \
%{?__global_ldflags:LDFLAGS="${LDFLAGS:-%__global_ldflags}" ; export LDFLAGS ;} \
/usr/bin/cmake \
        -DCMAKE_C_FLAGS_RELEASE:STRING="-DNDEBUG" \
        -DCMAKE_CXX_FLAGS_RELEASE:STRING="-DNDEBUG" \
        -DCMAKE_VERBOSE_MAKEFILE:BOOL=ON \
        -DCMAKE_INSTALL_PREFIX:PATH=%{_prefix} \
        -DINCLUDE_INSTALL_DIR:PATH=%{_includedir} \
        -DLIB_INSTALL_DIR:PATH=%{_libdir} \
        -DSYSCONF_INSTALL_DIR:PATH=%{_sysconfdir} \
        -DSHARE_INSTALL_PREFIX:PATH=%{_datadir} \
        -DBUILD_SHARED_LIBS:BOOL=ON \
        -DTHREADSAFE=ON \
        .

make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%doc COPYING
%{_libdir}/libgit2.so.*

%files dev
%doc AUTHORS docs examples README.md
%{_libdir}/libgit2.so
%{_libdir}/pkgconfig/libgit2.pc
%{_includedir}/git2.h
%{_includedir}/git2/

%changelog
* Fri Mar 27 2015 Alexander Larsson <alexl@redhat.com> - 0.21.3-1
- Initial version

