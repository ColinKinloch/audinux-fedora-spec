# Tag: Modular, Rack
# Type: Rack
# Category: Audio, Synthesizer

# Global variables for github repository
%global commit0 c9b0feef18e7f79c444cdd62f9b0628afb354fa6
%global gittag0 1.0.0
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})

# Disable production of debug package.
%global debug_package %{nil}

Name:    rack-v1-alto777_LFSR
Version: 1.0.0
Release: 3%{?dist}
Summary: alto777_LFSR plugin for Rack
License: GPLv2+
URL:     https://github.com/alto777/LFSR

Vendor:       Audinux
Distribution: Audinux

# ./rack-source.sh <tag>
# ./rack-source.sh v1.1.6

Source0: Rack.tar.gz
Source1: https://github.com/alto777/LFSR/archive/%{commit0}.tar.gz#/%{name}-%{shortcommit0}.tar.gz
Source2: alto777_LFSR_plugin.json

BuildRequires: gcc gcc-c++
BuildRequires: cmake sed
BuildRequires: alsa-lib-devel
BuildRequires: jack-audio-connection-kit-devel
BuildRequires: libsamplerate-devel
BuildRequires: libzip-devel
BuildRequires: glew-devel
BuildRequires: glfw-devel
BuildRequires: portmidi-devel
BuildRequires: portaudio-devel
BuildRequires: libcurl-devel
BuildRequires: openssl-devel
BuildRequires: jansson-devel
BuildRequires: gtk2-devel
BuildRequires: rtmidi-devel
BuildRequires: speex-devel
BuildRequires: speexdsp-devel
BuildRequires: jq

%description
alto777_LFSR plugin for Rack.

%prep
%autosetup -n Rack

CURRENT_PATH=`pwd`

sed -i -e "s/-march=nocona//g" compile.mk
sed -i -e "s/-O3/-O2/g" compile.mk

# %{build_cxxflags}
echo "CXXFLAGS += -I$CURRENT_PATH/include -I$CURRENT_PATH/dep/include -I$CURRENT_PATH/dep/nanovg/src -I$CURRENT_PATH/dep/nanovg/example -I$CURRENT_PATH/dep/nanosvg/src -I/usr/include/rtmidi -I$CURRENT_PATH/dep/oui-blendish -I$CURRENT_PATH/dep/osdialog -I$CURRENT_PATH/dep/jpommier-pffft-29e4f76ac53b -I$CURRENT_PATH/dep/include  -I$CURRENT_PATH/dep/rtaudio" >> compile.mk

sed -i -e "s/-Wl,-Bstatic//g" Makefile
sed -i -e "s/-lglfw3/dep\/lib\/libglfw3.a/g" Makefile

sed -i -e "s/dep\/lib\/libGLEW.a/-lGLEW/g" Makefile
sed -i -e "s/dep\/lib\/libglfw3.a/dep\/%{_lib}\/libglfw3.a/g" Makefile
sed -i -e "s/dep\/lib\/libjansson.a/-ljansson/g" Makefile
sed -i -e "s/dep\/lib\/libcurl.a/-lcurl/g" Makefile
sed -i -e "s/dep\/lib\/libssl.a/-lssl/g" Makefile
sed -i -e "s/dep\/lib\/libcrypto.a/-lcrypto/g" Makefile
sed -i -e "s/dep\/lib\/libzip.a/-lzip/g" Makefile
sed -i -e "s/dep\/lib\/libz.a/-lz/g" Makefile
sed -i -e "s/dep\/lib\/libspeexdsp.a/-lspeexdsp/g" Makefile
sed -i -e "s/dep\/lib\/libsamplerate.a/-lsamplerate/g" Makefile
sed -i -e "s/dep\/lib\/librtmidi.a/-lrtmidi/g" Makefile
sed -i -e "s/dep\/lib\/librtaudio.a/-lrtaudio/g" Makefile
# We use provided RtAudio library because Rack hangs when using jack and fedora rtaudio
sed -i -e "s/dep\/lib\/librtaudio.a/dep\/%{_lib}\/librtaudio.a -lpulse-simple -lpulse/g" Makefile

mkdir alto777_LFSR_plugin
tar xvfz %{SOURCE1} --directory=alto777_LFSR_plugin --strip-components=1 

cp -n %{SOURCE2} alto777_LFSR_plugin/plugin.json

%build

cd alto777_LFSR_plugin
%make_build RACK_DIR=.. PREFIX=/usr STRIP=true LIBDIR=%{_lib} dist

%install 

mkdir -p %{buildroot}%{_libexecdir}/Rack1/plugins-v1/alto777_LFSR/
cp -r alto777_LFSR_plugin/dist/alto777_LFSR/* %{buildroot}%{_libexecdir}/Rack1/plugins-v1/alto777_LFSR/

%files
%{_libexecdir}/*

%changelog
* Tue Feb 11 2020 Yann Collette <ycollette.nospam@free.fr> - 1.0.0-3
- initial specfile
