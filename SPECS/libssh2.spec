# Define %%{__isa_bits} for old releases
%{!?__isa_bits: %global __isa_bits %((echo '#include <bits/wordsize.h>'; echo __WORDSIZE) | cpp - | grep -Ex '32|64')}

Name:		libssh2
Version:	1.6.0
Release:	1%{?dist}
Summary:	A library implementing the SSH2 protocol
Group:		System Environment/Libraries
License:	BSD
URL:		http://www.libssh2.org/
Source0:	http://libssh2.org/download/libssh2-%{version}.tar.gz
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(id -nu)

%description
libssh2 is a library implementing the SSH2 protocol as defined by
Internet Drafts: SECSH-TRANS(22), SECSH-USERAUTH(25),
SECSH-CONNECTION(23), SECSH-ARCH(20), SECSH-FILEXFER(06)*,
SECSH-DHGEX(04), and SECSH-NUMBERS(10).

%package	dev
Summary:	Development files for libssh2
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description	dev
The libssh2-devel package contains libraries and header files for
developing applications that use libssh2.

%package	docs
Summary:	Documentation for libssh2
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description	docs
The libssh2-docs package contains man pages and examples for
developing applications that use libssh2.

%prep
%setup -q

%build
%configure --disable-static --enable-shared
make %{?_smp_mflags}

# Avoid polluting libssh2.pc with linker options (#947813)
sed -i -e 's|[[:space:]]-Wl,[^[:space:]]*||' libssh2.pc

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot} INSTALL="install -p"
find %{buildroot} -name '*.la' -exec rm -f {} \;

# clean things up a bit for packaging
make -C example clean
rm -rf example/.deps
find example/ -type f '(' -name '*.am' -o -name '*.in' ')' -exec rm -v {} \;

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%doc COPYING
%doc docs/AUTHORS ChangeLog NEWS README RELEASE-NOTES
%{_libdir}/libssh2.so.1
%{_libdir}/libssh2.so.1.*

%files docs
%doc docs/BINDINGS docs/HACKING docs/TODO
%{_mandir}/man3/libssh2_*.3*

%files dev
%doc example/
%{_includedir}/libssh2.h
%{_includedir}/libssh2_publickey.h
%{_includedir}/libssh2_sftp.h
%{_libdir}/libssh2.so
%{_libdir}/pkgconfig/libssh2.pc

%changelog
* Fri Sep 25 2015 Alexander Larsson <alexl@redhat.com> - 1.6.0-1
- import from fedora
