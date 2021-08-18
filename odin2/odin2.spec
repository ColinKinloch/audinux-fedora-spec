# Tag: Jack, Alsa
# Type: Plugin, Standalone, VST3
# Category: Audio, Synthesizer

Name:    odin2
Version: 2.3.1
Release: 3%{?dist}
Summary: A VST3 Synthesizer
License: GPLv2+
URL:     https://github.com/TheWaveWarden/odin2

Vendor:       Audinux
Distribution: Audinux

# Usage: ./odin-source.sh <TAG>
# ./odin-source.sh v2.3.1

Source0: odin2.tar.gz
Source1: odin-sources.sh
Patch0:  odin2-0001-soundbanks-in-share.patch

BuildRequires: gcc gcc-c++
BuildRequires: python2
BuildRequires: cairo-devel
BuildRequires: fontconfig-devel
BuildRequires: freetype-devel
BuildRequires: libX11-devel
BuildRequires: xcb-util-keysyms-devel
BuildRequires: xcb-util-devel
#BuildRequires: JUCE == 6.0.1
BuildRequires: JUCE
BuildRequires: libXrandr-devel
BuildRequires: xcb-util-cursor-devel
BuildRequires: libxkbcommon-x11-devel
BuildRequires: libXinerama-devel
BuildRequires: libcurl-devel
BuildRequires: alsa-lib-devel
BuildRequires: jack-audio-connection-kit-devel
BuildRequires: mesa-libGL-devel
BuildRequires: libXcursor-devel

%description
Odin 2 Synthesizer Plugin

%package -n vst3-%{name}
Summary:  VST3 version of %{name}
License:  GPLv2+
Requires: %{name}

%description -n vst3-%{name}
VST3 version of %{name}

%prep
%autosetup -p1 -n %{name}

%build

%set_build_flags

Projucer --set-global-search-path linux defaultJuceModulePath /usr/src/JUCE/modules/
Projucer --resave Odin.jucer

export HOME=`pwd`
mkdir -p .vst3
mkdir -p .lv2
mkdir -p .local/share/Odin2

cd Builds/LinuxMakefile
%make_build CONFIG=Release STRIP=true

%install 

install -m 755 -d %{buildroot}%{_libdir}/vst3/Odin2.vst3/
install -m 755 -d %{buildroot}%{_bindir}/
install -m 755 -d %{buildroot}%{_datadir}/odin2/Soundbanks/

cp -r Soundbanks/* %{buildroot}%{_datadir}/odin2/Soundbanks/
rm %{buildroot}%{_datadir}/odin2/Soundbanks/User\ Patches/.gitignore 

install -m 755 -p Builds/LinuxMakefile/build/Odin2 %{buildroot}/%{_bindir}/
cp -ra Builds/LinuxMakefile/build/Odin2.vst3/* %{buildroot}/%{_libdir}/vst3/Odin2.vst3/
chmod a+x %{buildroot}/%{_libdir}/vst3/Odin2.vst3/Contents/x86_64-linux/Odin2.so

%files
%doc README.md change_log.md
%license LICENSE
%{_bindir}/*
%{_datadir}/*

%files -n vst3-%{name}
%{_libdir}/vst3/*

%changelog
* Wed Aug 18 2021 Yann Collette <ycollette.nospam@free.fr> - 2.3.1-2
- update to 2.3.1-2

* Mon Oct 26 2020 Yann Collette <ycollette.nospam@free.fr> - 2.2.4-2
- fix install

* Sat Oct 24 2020 Yann Collette <ycollette.nospam@free.fr> - 2.2.4-1
- Initial spec file
