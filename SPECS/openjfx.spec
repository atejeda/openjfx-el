# https://github.com/atejeda/openjfx-el

Name:    java-1.8.0-openjfx
Version: 8u161_b12
Release: 1%{?dist}
Summary: OpenJFX runtime libraries and javadoc
Group:   Development/Languages
License: Refer to https://wiki.openjdk.java.net/display/OpenJFX/Main
URL:     https://wiki.openjdk.java.net/display/OpenJFX/Main

%global openjfx_version 8u161-b12
Source0: http://hg.openjdk.java.net/openjfx/8u/rt/archive/%{openjfx_version}.tar.gz

BuildRequires: java-1.8.0-openjdk java-1.8.0-openjdk-devel mercurial bison flex gperf ksh pkgconfig 
BuildRequires: libpng12-devel libjpeg-devel libxml2-devel libxslt-devel systemd-devel glib2-devel 
BuildRequires: gtk2-devel libXtst-devel pango-devel freetype-devel alsa-lib-devel glib2-devel 
BuildRequires: qt-devel gstreamer-devel perl perl-version perl-Digest perl-Digest-MD5 ruby gcc-c++
BuildRequires: perl-JSON-PP ant
Requires:      java-1.8.0-openjdk

%description
OpenJFX is an open source, next generation client application platform for desktop and embedded 
systems based on JavaSE. It is a collaborative effort by many individuals and companies with the 
goal of producing a modern, efficient, and fully featured toolkit for developing rich client 
applications.

%global openjdk8_version %(rpm -q java-1.8.0-openjdk)
%global openjdk8_install_dir %{buildroot}/usr/lib/jvm/%{openjdk8_version}

%global debug_packages %{nil}

%prep
# stop if
rpm -q %{name} && echo "A version already exists, remove before proceding"
# check for gradle
chmod -R +x %{_builddir}
[ -d %{buildroot} ] && chmod -R +x %{buildroot}
%setup -b0 -q -n rt-%{openjfx_version}

%define gradle_properties gradle.properties
echo "COMPILE_WEBKIT = true" >> %{gradle_properties}
echo "COMPILE_MEDIA = false" >> %{gradle_properties}
echo "BUILD_JAVADOC = true" >> %{gradle_properties}
echo "BUILD_SRC_ZIP = true" >> %{gradle_properties}
echo "libav" = "true" >> %{gradle_properties}

%build
export JAVA_HOME="/usr/lib/jvm/%{openjdk8_version}"
export CXXFLAGS="$CXXFLAGS -fPIC"
export CFLAGS="$CFLAGS -fPIC"
gradle
gradle :base:test

%install
%global sdkdir build/sdk
mkdir -p build/sdk
tar cf %{_topdir}/%{openjfx_version}_test_reports.tar.gz %{_builddir}/rt-%{openjfx_version}/modules/base/build/reports
tar cf %{_topdir}/%{openjfx_version}_test_results.tar.gz %{_builddir}/rt-%{openjfx_version}/modules/base/build/test-results
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
