# https://hub.docker.com/r/atejeda/openjfx-el
# https://github.com/atejeda/openjfx-el

FROM centos:centos7

RUN yum group install -y "Development Tools"
RUN yum install -y \
    rpmdevtools wget make vim ant \
    java-1.8.0-openjdk java-1.8.0-openjdk-devel mercurial bison flex gperf ksh \
    pkgconfig libpng12-devel libjpeg-devel libxml2-devel libxslt-devel \
    systemd-devel glib2-devel gtk2-devel libXtst-devel pango-devel \
    freetype-devel alsa-lib-devel glib2-devel qt-devel gstreamer-devel perl \
    perl-version perl-Digest perl-Digest-MD5 ruby gcc-c++ perl-JSON-PP \
    centos-release-scl-rh
RUN yum install -y devtoolset-3-gcc devtoolset-3-*c++*
RUN yum install -y http://ftp.linux.ncsu.edu/pub/epel/7/x86_64/Packages/e/epel-release-7-11.noarch.rpm
RUN yum install -y cmake3
RUN ln -s /usr/bin/cmake3 /usr/bin/cmake && ln -s /usr/bin/qmake-qt4 /usr/bin/qmake
RUN wget http://services.gradle.org/distributions/gradle-1.8-bin.zip && \
    unzip gradle-1.8-bin.zip -d /opt && \
    ln -s /opt/gradle-1.8/bin/gradle /usr/bin/ && \
    rm -f gradle-1.8-bin.zip
RUN yum install -y http://li.nux.ro/download/nux/dextop/el7/x86_64/nux-dextop-release-0-1.el7.nux.noarch.rpm
RUN yum install -y ffmpeg ffmpeg-devel
