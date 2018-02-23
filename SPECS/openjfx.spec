# https://github.com/atejeda/openjfx-el7

Name:    java-1.8.0-openjfx
Version: 8u161_b12
Release: 1%{?dist}
Summary: OpenJFX runtime libraries and javadoc
Group:   Development/Languages
License: Refer to https://wiki.openjdk.java.net/display/OpenJFX/Main
URL:     https://wiki.openjdk.java.net/display/OpenJFX/Main

%global openjfx_version 8u161-b12
Source0: http://hg.openjdk.java.net/openjfx/8u/rt/archive/%{openjfx_version}.tar.gz

BuildRequires: java-1.8.0-openjdk java-1.8.0-openjdk-devel mercurial bison flex gperf ksh pkgconfig libpng12-devel libjpeg-devel libxml2-devel libxslt-devel systemd-devel glib2-devel gtk2-devel libXtst-devel pango-devel freetype-devel alsa-lib-devel glib2-devel qt-devel gstreamer-devel perl perl-version perl-Digest perl-Digest-MD5 ruby gcc-c++
Requires:      java-1.8.0-openjdk

%description
OpenJFX is an open source, next generation client application platform for desktop and embedded systems based on JavaSE. It is a collaborative effort by many individuals and companies with the goal of producing a modern, efficient, and fully featured toolkit for developing rich client applications. This is the open source project where we develop JavaFX.

%global openjdk8_version %(rpm -q java-1.8.0-openjdk)
%global openjdk8_install_dir %{buildroot}/usr/lib/jvm/%{openjdk8_version}

%global debug_packages %{nil}

%prep
# stop if
rpm -q %{name} && echo "A version already exists, remove before proceding"
# check for gradle
chmod -R +x %{_builddir}
[ -d %{buildroot} ] && chmod -R +x %{buildroot}
%setup 

%define gradle_properties gradle.properties
echo "COMPILE_WEBKIT = false" >> %{gradle_properties}
echo "COMPILE_MEDIA = false" >> %{gradle_properties}
echo "BUILD_JAVADOC = true" >> %{gradle_properties}
echo "BUILD_SRC_ZIP = true" >> %{gradle_properties}
echo "libav" = "true" >> %{gradle_properties}

%build
%define qmake_symlink %{_builddir}/bin/qmake
export JAVA_HOME="/usr/lib/jvm/%{openjdk8_version}"
export CXXFLAGS="$CXXFLAGS -fPIC"
export CFLAGS="$CFLAGS -fPIC"
mkdir -p %{_builddir}/bin
[[ -f %{qmake_symlink} ]] || ln -s /usr/bin/qmake-qt4 %{qmake_symlink}

%install
%global sdkdir build/sdk
mkdir -p build/sdk
chmod -R +x %{sdkdir}
mkdir -p %{openjdk8_install_dir}/{lib,bin,man/man1,jre/lib/ext}
%ifarch %{ix86}
mkdir -p %{openjdk8_install_dir}/jre/lib/i386
%endif
%ifarch x86_64
mkdir -p %{openjdk8_install_dir}/jre/lib/amd64
%endif

# jdk libraries
install -m644 %{sdkdir}/lib/* %{openjdk8_install_dir}/lib/
install -m755 %{sdkdir}/bin/* %{openjdk8_install_dir}/bin/
install -m644 %{sdkdir}/man/man1/* %{openjdk8_install_dir}/man/man1/

# jre libraries
install -m644 %{sdkdir}/rt/lib/ext/* %{openjdk8_install_dir}/jre/lib/ext/
%ifarch %{ix86}
install -m644 %{sdkdir}/rt/lib/i386/* %{openjdk8_install_dir}/jre/lib/i386/
%endif
%ifarch x86_64
install -m644 %{sdkdir}/rt/lib/amd64/* %{openjdk8_install_dir}/jre/lib/amd64/
%endif

%files
%defattr(-,root,root,-)
%doc build/javadoc
/usr/lib/jvm/%{openjdk8_version}/lib/*
/usr/lib/jvm/%{openjdk8_version}/bin/*
/usr/lib/jvm/%{openjdk8_version}/man/man1/*
/usr/lib/jvm/%{openjdk8_version}/jre/lib/*
