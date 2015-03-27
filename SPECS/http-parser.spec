# we use the upstream version from http_parser.h as the SONAME
%global somajor 2
%global sominor 0

Name:           http-parser
Version:        %{somajor}.%{sominor}
Release:        1%{?dist}
Summary:        HTTP request/response parser for C

Group:          System Environment/Libraries
License:        MIT
URL:            http://github.com/joyent/http-parser
# download from https://github.com/joyent/http-parser/tarball/%%{version}
Source0:        https://github.com/joyent/http-parser/archive/v%{version}.tar.gz?/joyent-http-parser-%{version}.tar.gz
BuildRoot:      %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

%description
This is a parser for HTTP messages written in C. It parses both requests and
responses. The parser is designed to be used in performance HTTP applications.
It does not make any syscalls nor allocations, it does not buffer data, it can
be interrupted at anytime. Depending on your architecture, it only requires
about 40 bytes of data per message stream (in a web server that is per
connection).


%package dev
Group:          Development/Libraries
Summary:        Development headers and libraries for http-parser
Requires:       %{name} = %{version}-%{release}

%description dev
Development headers and libraries for http-parser.


%prep
%setup -q -n http-parser-%{version}


%build
make %{?_smp_mflags} BUILDTYPE=Release library


%install
rm -rf %{buildroot}

install -d %{buildroot}%{_includedir}
install -d %{buildroot}%{_libdir}

install -pm644 http_parser.h %{buildroot}%{_includedir}

#install regular variant
install libhttp_parser.so %{buildroot}%{_libdir}/libhttp_parser.so


%clean
rm -rf %{buildroot}


%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%{_libdir}/libhttp_parser.so
%doc AUTHORS CONTRIBUTIONS LICENSE-MIT README.md


%files dev
%defattr(-,root,root,-)
%{_includedir}/*


%changelog
* Fri Mar 27 2015 Alexander Larsson <alexl@redhat.com> - 2.%{sominor}-1
- Initial version

