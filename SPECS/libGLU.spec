Name:           libGLU
Version:        9.0.0
Release:        1%{?dist}
Summary:        Mesa libGLU library

License:        MIT
URL:            http://mesa3d.org/
Source0:        ftp://ftp.freedesktop.org/pub/mesa/glu/glu-%{version}.tar.bz2

%description
Mesa implementation of the standard GLU OpenGL utility API.

%package        dev
Summary:        Development files for %{name}
Requires:       %{name} = %{version}-%{release}

%description    dev
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%setup -q -n glu-%{version}

%build
autoreconf -v -i -f
%configure --disable-static
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'
rm -rf $RPM_BUILD_ROOT%{_datadir}/man/man3/gl[A-Z]*

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%{_libdir}/libGLU.so.1
%{_libdir}/libGLU.so.1.3.*

%files dev
%{_includedir}/GL/glu*.h
%{_libdir}/libGLU.so
%{_libdir}/pkgconfig/glu.pc

%changelog
* Mon Mar 30 2015 Alexander Larsson <alexl@redhat.com> - 9.0.0-1
- Initial
