%global release_version %%(echo %{version} | awk -F. '{print $1"."$2}')

%define po_package gtksourceview-3.0

Summary: A library for viewing source files
Name: gtksourceview3
Version: 3.16.0
Release: 1%{?dist}
License: LGPLv2+
Group: System Environment/Libraries
URL: http://gtksourceview.sourceforge.net/
#VCS: git:git://git.gnome.org/gtksourceview
Source0: http://download.gnome.org/sources/gtksourceview/%{release_version}/gtksourceview-%{version}.tar.xz

%description
GtkSourceView is a text widget that extends the standard GTK+
GtkTextView widget. It improves GtkTextView by implementing
syntax highlighting and other features typical of a source code editor.

This package contains version 3 of GtkSourceView. The older version
2 is contains in the gtksourceview2 package.

%package dev
Summary: Files to compile applications that use gtksourceview3
Group: Development/Libraries
Requires: %{name}%{?_isa} = %{version}-%{release}

%description dev
gtksourceview3-devel contains the files required to compile
applications which use GtkSourceView 3.

%package tests
Summary: Tests for the gtksourceview3 package
Group: Development/Libraries
Requires: %{name}%{?_isa} = %{version}-%{release}

%description tests
The gtksourceview3-tests package contains tests that can be used to verify
the functionality of the installed gtksourceview package.

%prep
%setup -q -n gtksourceview-%{version}

%build
%configure --disable-gtk-doc --disable-static \
 --enable-installed-tests

make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT

# remove unwanted files
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la

%find_lang %{po_package}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files -f %{po_package}.lang
%doc README AUTHORS COPYING NEWS MAINTAINERS
%{_datadir}/gtksourceview-3.0
%{_libdir}/*.so.*
%{_libdir}/girepository-1.0/GtkSource-3.0.typelib

%files dev
%{_includedir}/gtksourceview-3.0
%{_datadir}/gtk-doc/html/*
%{_libdir}/pkgconfig/*.pc
%{_libdir}/*.so
%{_datadir}/gir-1.0/GtkSource-3.0.gir
%dir %{_datadir}/vala
%dir %{_datadir}/vala/vapi
%{_datadir}/vala/vapi/gtksourceview-3.0.deps
%{_datadir}/vala/vapi/gtksourceview-3.0.vapi

%files tests
%{_libexecdir}/installed-tests/gtksourceview
%{_datadir}/installed-tests

%changelog
* Fri Mar 27 2015 Alexander Larsson <alexl@redhat.com> - 3.16.0-1
- Initial version

