SDK=org.gnome.Sdk
SDK_VERSION=3.18

all:
	true

deps rpm-dependencies.P: makedeps.sh
	./makedeps.sh > rpm-dependencies.P

-include rpm-dependencies.P
