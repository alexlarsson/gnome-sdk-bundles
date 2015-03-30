Summary:        A freely licensed alternative to the GLUT library
Name:           freeglut
Version:        2.8.1
Release:        1%{?dist}
URL:            http://freeglut.sourceforge.net
Source0:        http://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.gz
License:        MIT
Group:          System Environment/Libraries

BuildRequires:  libGLU-dev
Requires:       libGLU

%description
freeglut is a completely open source alternative to the OpenGL Utility Toolkit
(GLUT) library with an OSI approved free software license. GLUT was originally
written by Mark Kilgard to support the sample programs in the second edition
OpenGL 'RedBook'. Since then, GLUT has been used in a wide variety of practical
applications because it is simple, universally available and highly portable.

freeglut allows the user to create and manage windows containing OpenGL
contexts on a wide range of platforms and also read the mouse, keyboard and
joystick functions.


%package dev
Summary:        Freeglut developmental libraries and header files
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}
Requires:       libGLU-dev

%description dev
Developmental libraries and header files required for developing or compiling
software which links to the freeglut library, which is an open source
alternative to the popular GLUT library, with an OSI approved free software
license.

%prep
%setup -q

%build
# --disable-warnings -> don't add -Werror to CFLAGS
%configure --disable-static --disable-warnings
make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT
rm $RPM_BUILD_ROOT/%{_libdir}/*.la

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING INSTALL NEWS README TODO doc/*.png doc/*.html
# don't include contents of doc/ directory as it is mostly obsolete
%{_libdir}/libglut*.so.*

%files dev
%defattr(-,root,root,-)
%{_includedir}/GL/*.h
%{_libdir}/libglut.so

%changelog
* Mon Mar 30 2015 Alexander Larsson <alexl@redhat.com> - 2.8.1-1
- Initial
