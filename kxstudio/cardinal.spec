Name:    cardinal
Version: 22.02
Release: 1%{?dist}
Summary:  Virtual modular synthesizer plugin
License: GPLv2+
URL:     https://github.com/DISTRHO/Cardinal

Vendor:       Audinux
Distribution: Audinux

Source0: https://github.com/DISTRHO/Cardinal/releases/download/%{version}/%{name}-%{version}.tar.xz

BuildRequires: gcc gcc-c++ make
BuildRequires: python-qt5-devel
BuildRequires: liblo-devel
BuildRequires: alsa-lib-devel
BuildRequires: pulseaudio-libs-devel
BuildRequires: gtk2-devel
BuildRequires: gtk3-devel
BuildRequires: qt-devel
BuildRequires: qt5-qtbase-devel
BuildRequires: fluidsynth-devel
BuildRequires: fftw-devel
BuildRequires: mxml-devel
BuildRequires: zlib-devel
BuildRequires: mesa-libGL-devel
BuildRequires: non-ntk-fluid
BuildRequires: non-ntk-devel
BuildRequires: jack-audio-connection-kit-devel
BuildRequires: linuxsampler-devel
BuildRequires: wget

Requires(pre): python3-qt5

%description
Cardinal, the Rack!

Cardinal is a free and open-source virtual modular synthesizer plugin,
available as JACK standalone and LV2, VST2 and VST3 audio plugin
for FreeBSD, Linux, macOS and Windows.
It is based on the popular VCV Rack but with a focus on being a fully
self-contained plugin version.

%package -n lv2-%{name}
Summary:  LV2 version of %{name}
License:  GPLv2+
Requires: %{name}-common

%description -n lv2-%{name}
LV2 version of %{name}

%package -n vst3-%{name}
Summary:  VST3 version of %{name}
License:  GPLv2+
Requires: %{name}-common

%description -n vst3-%{name}
VST3 version of %{name}

%package -n vst-%{name}
Summary:  VST2 version of %{name}
License:  GPLv2+
Requires: %{name}-common

%description -n vst-%{name}
VST2 version of %{name}

%prep
%autosetup -n %{name}-%{version}

%build
%make_build PREFIX=/usr LIBDIR=%{_libdir} SKIP_STRIPPING=true

%install 
%make_install PREFIX=/usr LIBDIR=%{_libdir} SKIP_STRIPPING=true
%ifarch x86_64 amd64
mv %buildroot/usr/lib %buildroot/usr/lib64
%endif

%files
%license LICENSE
%{_bindir}/*
%{_datadir}/%{name}/*
%{_datadir}/doc/%{name}/*

%files -n lv2-%{name}
%{_libdir}/lv2/*

%files -n vst-%{name}
%{_libdir}/vst/*

%files -n vst3-%{name}
%{_libdir}/vst3/*

%changelog
* Fri Feb 18 2022 Yann Collette <ycollette.nospam@free.fr> - 22.02-1
- Initial build