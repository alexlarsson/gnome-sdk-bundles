%global release_version %%(echo %{version} | awk -F. '{print $1"."$2}')

Name:           libgit2-glib
Version:        0.0.24
Release:        1%{?dist}
Summary:        Git library for GLib

License:        LGPLv2+
URL:            https://wiki.gnome.org/Projects/Libgit2-glib
Source0:        http://download.gnome.org/sources/libgit2-glib/%{release_version}/libgit2-glib-%{version}.tar.xz

BuildRequires:  http-parser
BuildRequires:  libgit2
BuildRequires:  libgit2-dev

%description
libgit2-glib is a glib wrapper library around the libgit2 git access library.

%package        dev
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    dev
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%setup -q


%build
%configure --disable-static
make %{?_smp_mflags}


%install
%make_install
# Remove unwanted la files
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%doc AUTHORS COPYING NEWS
%{_libdir}/libgit2-glib-1.0.so.*
%{_libdir}/girepository-1.0/Ggit-1.0.typelib
%{_libdir}/python3.3/site-packages/gi/overrides/*

%files dev
%{_includedir}/libgit2-glib-1.0/
%{_libdir}/libgit2-glib-1.0.so
%{_libdir}/pkgconfig/libgit2-glib-1.0.pc
%{_datadir}/gir-1.0/Ggit-1.0.gir
%{_datadir}/vala/
%doc %{_datadir}/gtk-doc/


%changelog
* Fri Mar 27 2015 Alexander Larsson <alexl@redhat.com> - 0.0.24-1
- Initial version
