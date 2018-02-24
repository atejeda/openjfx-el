# OpenJFX 1.8 x86_64 EL7 packaging scripts

This repo is a set of scripts to package OpenJFX 1.8 in RPM packages for EL7 GNU/Linux flavors. Refer to the artifacts section for versions.

A docker image file is provided to easily setup and build the RPM, this image is based on Centos 7 and contains a few extra packages like gradle 1.8, qmake, cmake 3.6 and some devtoolset-3 tools (gcc 4.9 is needed to build webkit). 

Is worth to mention that FFmpeg is being included as well as it is needed to have media support, if you want to distribute software using the RPM package produced from this repository please refer to https://www.ffmpeg.org/legal.html to see if you software qualify for your purposes, as long you software license is compatible with GPL or LGPL 2.1 you are good (see https://video.stackexchange.com/questions/14802/can-i-use-ffmpeg-in-a-commercial-product).

## RPM build

To build the RPM a Makefile is provided:
```
make deps # retrieves the needed sources (openjfx)
make info # print to the stdout info about the environment
make all  # create the RPM using a relative rpmbuild directory
make info deps all # will excersise the build process
```

# Artifacts

OpenJFX will be built provide with webkit support, media support and javadocs as well. The build is based on OpenJDK 1.8 b161u14 using OpenJFX b161u12-1 official sources, this is the current combination of versions being currently used by Oracle JDK 1.8.

The build will generate the test reports and test results at the top of the rpmbuild directory, RPMs, SRPMs intended for x86_64 architectures.

Webkit library info, being 4.8.5 installed by default on EL7 (at least 7.4) environments.

```
valhalla rt-8u161-b12 [master] $ strings -a build/sdk/rt/lib/amd64/libjfxwebkit.so | grep "GCC: ("
GCC: (GNU) 4.9.2 20150212 (Red Hat 4.9.2-6)
GCC: (GNU) 4.8.5 20150623 (Red Hat 4.8.5-16)
```

There is some smoke test under test to manually check if FXML and WebView both of them work with no issues.

## TLDR

Pull up the docker image and enable devtoolset-3 enviroment to trigger a build, webkit takes almost around 70% of the build time 

```
docker pull atejeda/openjfx-el
git clone https://github.com/atejeda/openjfx-el.git
cd openjfx-el
docker run --rm -w /root/workspace -v $PWD:/root/workspace atejeda/openjfx-el scl enable devtoolset-3 'make info deps all' 2>&1 | tee build.log
```

## Issues?

Open a ticket in https://github.com/atejeda/openjfx-el or provide a pull request.

## Legal

I do not own any of the technologies used in this repo, for licenses refer to each technology license being used. Use at your own risk.
