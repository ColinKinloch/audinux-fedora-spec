# Tag: Jack, Alsa
# Type: Plugin, Standalone, VST3
# Category: Audio, Synthesizer

Name:    obxd
Version: 2.9
Release: 2%{?dist}
Summary: A VST3 Synthesizer
License: GPLv3
URL:     https://github.com/reales/OB-Xd

Vendor:       Audinux
Distribution: Audinux

Source0: https://github.com/reales/OB-Xd/archive/refs/tags/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
Source1: obxd-makefiles.tar.gz
Source2: vst3sdk.tar.gz
Source3: vst3-source.sh
Patch0:  obxd_file_install_resources.patch

BuildRequires: gcc gcc-c++
BuildRequires: make
BuildRequires: cairo-devel
BuildRequires: fontconfig-devel
BuildRequires: freetype-devel
BuildRequires: libX11-devel
BuildRequires: xcb-util-keysyms-devel
BuildRequires: xcb-util-devel
BuildRequires: JUCE61
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
Virtual Analog Oberheim VST / VST3 based synthesizer

%package -n vst-%{name}
Summary:  VST2 version of %{name}
License:  GPLv3
Requires: %{name}

%description -n vst-%{name}
VST2 version of %{name}

%package -n vst3-%{name}
Summary:  VST3 version of %{name}
License:  GPLv3
Requires: %{name}

%description -n vst3-%{name}
VST3 version of %{name}

%prep
%autosetup -p1 -n OB-Xd-%{version}

tar xvfz %{SOURCE1}
tar xvfz %{SOURCE2}

sed -i -e "s|-DJucePlugin_Build_Standalone=0|-DJucePlugin_Build_Standalone=1|g" Builds/LinuxMakefile/Makefile

%build

%set_build_flags

CWD=`pwd`

export CPPFLAGS="-I/usr/src/JUCE61/modules -I$CWD/VST_SDK/VST2_SDK -I$CWD/VST_SDK/VST3_SDK -include utility $CPPFLAGS"

cd Builds/LinuxMakefile
%make_build VST Standalone CONFIG=Release64 STRIP=true

%install 

#install -m 755 -d %{buildroot}%{_libdir}/vst3/OB-Xd.vst3/
install -m 755 -d %{buildroot}%{_libdir}/vst/
install -m 755 -d %{buildroot}%{_bindir}/
install -m 755 -d %{buildroot}%{_datadir}/discoDSP/OB-Xd/

cp -r Documents/discoDSP/* %{buildroot}%{_datadir}/discoDSP/

install -m 755 -p Builds/LinuxMakefile/build/OB-Xd %{buildroot}/%{_bindir}/
install -m 755 -p Builds/LinuxMakefile/build/OB-Xd.so %{buildroot}/%{_libdir}/vst/
#cp -ra Builds/LinuxMakefile/build/OB-Xd.vst3/* %{buildroot}/%{_libdir}/vst3/OB-Xd.vst3/
#chmod a+x %{buildroot}/%{_libdir}/vst3/OB-Xd.vst3/Contents/x86_64-linux/OB-Xd.so

%files
%doc README.md
%license license.txt
%{_bindir}/*
%{_datadir}/*

#%files -n vst3-%{name}
#%{_libdir}/vst3/*

%files -n vst-%{name}
%{_libdir}/vst/*

%changelog
* Mon Jul 25 2022 Yann Collette <ycollette.nospam@free.fr> - 2.9-2
- update to 2.9-2

* Sun Jun 26 2022 Yann Collette <ycollette.nospam@free.fr> - 2.8-2
- update to 2.8-2

* Sun Jan 09 2022 Yann Collette <ycollette.nospam@free.fr> - 2.6-2
- update to 2.6-2

* Fri Oct 01 2021 Yann Collette <ycollette.nospam@free.fr> - 2.4-2
- Fix for Fedora 35

* Wed Jun 02 2021 Yann Collette <ycollette.nospam@free.fr> - 2.4-1
- Initial spec file
