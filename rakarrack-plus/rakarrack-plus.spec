# Tag: Guitar, Amp Simul
# Type: Plugin, LV2, Standalone
# Category: Audio, Effect
# LastSourceUpdate: 2021

Summary: Guitar Amplifier emulator
Name:    rakarrack-plus
Version: 1.2.2
Release: 2%{?dist}
License: GPL
URL:     https://github.com/Stazed/rakarrack-plus

Vendor:       Audinux
Distribution: Audinux

Source0: https://github.com/Stazed/rakarrack-plus/archive/refs/tags/%{version}.tar.gz#/%{name}-%{version}.tar.gz

BuildRequires: gcc gcc-c++
BuildRequires: cmake
BuildRequires: alsa-lib-devel
BuildRequires: alsa-utils
BuildRequires: fltk-devel
BuildRequires: fltk-fluid
BuildRequires: liblo-devel
BuildRequires: libXpm-devel
BuildRequires: libsndfile-devel
BuildRequires: libsamplerate-devel
BuildRequires: fftw-devel
BuildRequires: lv2-devel
BuildRequires: jack-audio-connection-kit-devel
BuildRequires: desktop-file-utils

%description
This app was born after an informal conversation about effects for guitar using GNU/linux.
The major part of this apps are discontinued or simply not have new versions after few
years. Josep Andreu say on the IRC chat 'I can made an app based on the effects set
hiden on code of ZynAddSubFX (by Paul Nasca Octavian)'. Some time after here is the
result of our work...

This app has 42 effects:
  * EQ Lineal
  * Compressor
  * Distortion
  * Overdrive
  * Echo
  * Chorus
  * Phaser
  * Flanger
  * Reverb
  * Parametric EQ
  * Wah Wah
  * Alienwha
  * Harmonizer
  * etc.
The effects are procesed in cascade... The order of effects are configurable by the user.
The state of rack can be saved as 'presets'. Sets of presets can be stored as 'banks'.
The rack also has an integrated tuner and can receive MIDI control orders and can send MIDI
notes to MIDI devices like synthesizers.

%package -n lv2-%{name}
Summary: LV2 plugins for %{name}

%description -n lv2-%{name}
LV2 plugins for %{name}

%prep
%autosetup -n %{name}-%{version}

%build

%cmake -DLV2_PATH=%{_libdir}/lv2 -DBuildCarlaPresets=ON
%cmake_build

%install
%cmake_install

desktop-file-install --vendor '' \
        --add-category=X-Sound \
        --add-category=Midi \
        --add-category=X-Jack \
        --dir %{buildroot}/%{_datadir}/applications \
        %{buildroot}/%{_datadir}/applications/rakarrack-plus.desktop

rm %{buildroot}/%{_datadir}/doc/rakarrack-plus/COPYING

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/rakarrack-plus.desktop

%files
%doc AUTHORS ChangeLog NEWS README.md PACKAGERS.README README
%license COPYING
%{_bindir}/*
%{_datadir}/applications/*
%{_datadir}/man/*
%{_datadir}/pixmaps/*
%{_datadir}/rakarrack-plus/*
%{_datadir}/RakarrackPlus.lv2/*
%{_datadir}/doc/rakarrack-plus/html/*

%files -n lv2-%{name}
%{_libdir}/lv2/*

%changelog
* Sun Jun 19 2022 Yann Collette <ycollette dot nospam at free.fr> 1.2.2-2
- update to 1.2.2-2 

* Tue May 10 2022 Yann Collette <ycollette dot nospam at free.fr> 1.2.1-2
- update to 1.2.1-2 

* Tue Apr 19 2022 Yann Collette <ycollette dot nospam at free.fr> 1.2.0-2
- update to 1.2.0-2 

* Sun Dec 12 2021 Yann Collette <ycollette dot nospam at free.fr> 1.1.2-2
- update to 1.1.2-2 

* Mon Jul 26 2021 Yann Collette <ycollette dot nospam at free.fr> 1.1.1-2
- update to 1.1.1-2 

* Wed Jun 23 2021 Yann Collette <ycollette dot nospam at free.fr> 1.1.0-2
- put lv2 plugins in a separate package 

* Sat Jun 12 2021 Yann Collette <ycollette dot nospam at free.fr> 1.1.0-1
- initial release 
