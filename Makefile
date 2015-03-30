SDK_VERSION=3.16

all:
	true

deps rpm-dependencies.P: makedeps.sh
	./makedeps.sh org.gnome.Sdk ${SDK_VERSION}  > rpm-dependencies.P

-include rpm-dependencies.P
