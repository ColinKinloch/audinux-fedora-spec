# Global variables for github repository
%global commit0 a41c6d32d9f74257c7de11dc4aebbc20dea16ef4
%global gittag0 1.0.0
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})

# Disable production of debug package.
%global debug_package %{nil}

Name:    rack-v1-ParableInstruments
Version: 1.0.0
Release: 3%{?dist}
Summary: ParableInstruments plugin for Rack
License: GPLv2+
URL:     https://github.com/adbrant/ArableInstruments

# ./rack-source.sh <tag>
# ./rack-source.sh v1.1.6

# git clone --recursive --branch v1 https://github.com/adbrant/ArableInstruments.git
# find ArableInstruments -name ".git" -exec rm -rf {} \;
# tar cvfz ArableInstruments.tar.gz ArableInstruments/*

Source0: Rack.tar.gz
Source1: ArableInstruments.tar.gz
Source2: ParableInstruments_plugin.json

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
BuildRequires: rtaudio-devel
BuildRequires: rtmidi-devel
BuildRequires: speex-devel
BuildRequires: speexdsp-devel
BuildRequires: jq

%description
ParableInstruments plugin for Rack.

%prep
%autosetup -n Rack

CURRENT_PATH=`pwd`

sed -i -e "s/-march=core2//g" compile.mk
sed -i -e "s/-march=nocona//g" compile.mk
sed -i -e "s/-ffast-math//g" compile.mk
sed -i -e "s/-fno-finite-math-only//g" compile.mk
sed -i -e "s/-O3/-O2/g" compile.mk

# %{build_cxxflags}
echo "CXXFLAGS += -I$CURRENT_PATH/include -I$CURRENT_PATH/dep/nanovg/src -I$CURRENT_PATH/dep/nanovg/example -I$CURRENT_PATH/dep/nanosvg/src -I/usr/include/rtaudio -I/usr/include/rtmidi -I$CURRENT_PATH/dep/oui-blendish -I$CURRENT_PATH/dep/osdialog -I$CURRENT_PATH/dep/jpommier-pffft-29e4f76ac53b -I$CURRENT_PATH/dep/include" >> compile.mk

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

mkdir ParableInstruments_plugin
tar xvfz %{SOURCE1} --directory=ParableInstruments_plugin --strip-components=1 

cp -n %{SOURCE2} ParableInstruments_plugin/plugin.json

%build

cd ParableInstruments_plugin
%make_build RACK_DIR=.. PREFIX=/usr LIBDIR=%{_lib} dist

%install 

mkdir -p %{buildroot}%{_libexecdir}/Rack1/plugins-v1/ParableInstruments/
cp -r ParableInstruments_plugin/dist/ParableInstruments/* %{buildroot}%{_libexecdir}/Rack1/plugins-v1/ParableInstruments/

%files
%{_libexecdir}/*

%changelog
* Tue Feb 11 2020 Yann Collette <ycollette.nospam@free.fr> - 1.0.0-3
- initial specfile