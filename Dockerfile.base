FROM arm32v7/debian:stretch

# need git to use custom git repo until SoCo fixes breaking Sonos API change issues in v0.16
RUN apt-get update && apt-get install -y git
# python3-pygame - package does not exist on this platform at the time, so we use python2.7 version
RUN apt-get update && apt-get install -y python-pygame python-pip

##### SDL 2.x and SDL 1.2.15-10 have issues with the touchscreen...must force SDL1.2
##### otherwise touchscreen will provide wonky values

# enable wheezy package sources
RUN echo "deb http://archive.debian.org/debian/ wheezy main" > /etc/apt/sources.list.d/wheezy.list

# set stable as default package source (currently stretch)
RUN echo "APT::Default-release \"stable\";" > /etc/apt/apt.conf.d/10defaultRelease

# set the priority for libsdl from wheezy higher
RUN echo "Package: libsdl1.2debian\
Pin: release n=stretch\
Pin-Priority: -10\
Package: libsdl1.2debian\
Pin: release n=wheezy\
Pin-Priority: 900\
" > /etc/apt/preferences.d/libsdl

# install
RUN apt-get update
RUN apt-get -y --allow-downgrades install libsdl1.2debian/wheezy
