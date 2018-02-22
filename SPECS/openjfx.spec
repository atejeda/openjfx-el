Name:		java-1.8.0-openjfx
Version:	8u161_b12
Release:	1%{?dist}
Summary:	OpenJFX runtime libraries and documentation
Group:		Development/Languages
License:	GPL with the class path exception
URL:		https://wiki.openjdk.java.net/dashboard.action

%global openjfx_version 8u161-b12
Source0: http://services.gradle.org/distributions/gradle-1.8-bin.zip
Source1: http://hg.openjdk.java.net/openjfx/8u/rt/archive/%{openjfx_version}.tar.gz

BuildRequires: java-1.8.0-openjdk java-1.8.0-openjdk-devel mercurial bison flex gperf ksh pkgconfig libpng12-devel libjpeg-devel libxml2-devel libxslt-devel systemd-devel glib2-devel gtk2-devel libXtst-devel pango-devel freetype-devel alsa-lib-devel glib2-devel qt-devel gstreamer-devel perl perl-version perl-Digest perl-Digest-MD5 ruby gcc-c++
Requires:	java-1.8.0-openjdk

%description
OpenJFX is an open source, next generation client application platform for desktop and embedded systems based on JavaSE. It is a collaborative effort by many individuals and companies with the goal of producing a modern, efficient, and fully featured toolkit for developing rich client applications. This is the open source project where we develop JavaFX.

%global openjdk8_version %(rpm -q java-1.8.0-openjdk)
%global openjdk8_install_dir %{buildroot}/usr/lib/jvm/%{openjdk8_version}

# There is no need for a debug package (for now)
%global debug_packages %{nil}

%prep
rpm -q %{name} && echo "You need to uninstall the previously built openjfx package before proceeding (this sounds stupid, but it actually makes sense!)"
chmod -R +x %{_builddir}
[ -d %{buildroot} ] && chmod -R +x %{buildroot}
%autosetup -n gradle-1.8
%setup -b 1 -n rt-%{openjfx_version}
#%setup -T -q -n gradle-1.8 -b 1
#%setup -q -T

%define gradle_properties gradle.properties
echo "COMPILE_WEBKIT = false" >> %{gradle_properties}
# We cannot compile media for now, as the code relies on FFmpeg, whose distributions
echo "COMPILE_MEDIA = false" >> %{gradle_properties}
echo "BUILD_JAVADOC = true" >> %{gradle_properties}
echo "BUILD_SRC_ZIP = true" >> %{gradle_properties}
echo "libav" = "true" >> %{gradle_properties}

%build
%define qmake_symlink %{_builddir}/bin/qmake
#export JAVA_HOME="/usr/lib/jvm/%{openjdk8_version}"
export CXXFLAGS="$CXXFLAGS -fPIC"
export CFLAGS="$CFLAGS -fPIC"
mkdir -p %{_builddir}/bin
[[ -f %{qmake_symlink} ]] || ln -s /usr/bin/qmake-qt4 %{qmake_symlink}
PATH=%{_builddir}/bin:$PATH %{_builddir}/gradle-1.8/bin/gradle

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

# JDK libraries
install -m644 %{sdkdir}/lib/* %{openjdk8_install_dir}/lib/
install -m755 %{sdkdir}/bin/* %{openjdk8_install_dir}/bin/
install -m644 %{sdkdir}/man/man1/* %{openjdk8_install_dir}/man/man1/

# JRE libraries
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
