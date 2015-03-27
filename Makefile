GNOME_VERSION=3.16

all:
	true

deps rpm-dependencies.P: makedeps.sh
	./makedeps.sh org.gnome.Sdk ${GNOME_VERSION}  > rpm-dependencies.P

-include rpm-dependencies.P
