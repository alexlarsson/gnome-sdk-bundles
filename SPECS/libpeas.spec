%global release_version %%(echo %{version} | awk -F. '{print $1"."$2}')

Name:		libpeas
Version:	1.14.0
Release:	1%{?dist}
Summary:	Plug-ins implementation convenience library

Group:		System Environment/Libraries
License:	LGPLv2+
Source0:	https://download.gnome.org/sources/libpeas/%{release_version}/libpeas-%{version}.tar.xz

%description
libpeas is a convenience library making adding plug-ins support
to GTK+ and glib-based applications.

%package dev
Summary:	Development files for libpeas
Group:		Development/Libraries
Requires:	%{name}%{?_isa} = %{version}-%{release}

%description dev
This package contains development libraries and header files
that are needed to write applications that use libpeas.

%prep
%setup -q

%build
%configure --enable-python3 --disable-python2

make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT/%{_libdir}/libpeas-1.0/loaders
rm $RPM_BUILD_ROOT/%{_libdir}/lib*.la \
   $RPM_BUILD_ROOT/%{_libdir}/libpeas-1.0/loaders/lib*.la

%find_lang libpeas

%post
/sbin/ldconfig
touch --no-create %{_datadir}/icons/hicolor >&/dev/null || :

%postun
/sbin/ldconfig
if [ $1 -eq 0 ]; then
  touch --no-create %{_datadir}/icons/hicolor >&/dev/null || :
  gtk-update-icon-cache %{_datadir}/icons/hicolor >&/dev/null || :
fi

%posttrans
gtk-update-icon-cache %{_datadir}/icons/hicolor >&/dev/null || :

%files -f libpeas.lang
%doc AUTHORS
%{_libdir}/libpeas*-1.0.so.*
%dir %{_libdir}/libpeas-1.0/
%dir %{_libdir}/libpeas-1.0/loaders
%{_libdir}/libpeas-1.0/loaders/libpython3loader.so
%{_libdir}/girepository-1.0/*.typelib
%{_datadir}/icons/hicolor/*/actions/libpeas-plugin.*

%files dev
%{_bindir}/peas-demo
%{_includedir}/libpeas-1.0/
%{_libdir}/peas-demo/
%dir %{_datadir}/gtk-doc/
%dir %{_datadir}/gtk-doc/html/
%{_datadir}/gtk-doc/html/libpeas/
%{_libdir}/libpeas*-1.0.so
%{_datadir}/gir-1.0/*.gir
%{_libdir}/pkgconfig/*.pc

%changelog
* Fri Mar 27 2015 Alexander Larsson <alexl@redhat.com> - 1.12.1-1
- Initial version
