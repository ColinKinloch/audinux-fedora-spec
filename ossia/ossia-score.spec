%define _lto_cflags %{nil}

Name:    ossia-score
Version: 3.0.12
Release: 1%{?dist}
Summary: ossia score is a sequencer for audio-visual artists, designed to create interactive shows
URL:     https://github.com/OSSIA/score
License: CeCILL License v2

Vendor:       Audinux
Distribution: Audinux

Source0: https://github.com/ossia/score/releases/download/v%{version}/ossia.score-%{version}-src.tar.xz

BuildRequires: gcc gcc-c++
BuildRequires: cmake
BuildRequires: alsa-lib-devel
BuildRequires: jack-audio-connection-kit-devel
BuildRequires: boost-devel
BuildRequires: zlib-devel
BuildRequires: qt5-qtbase-devel
BuildRequires: qt5-qtbase-private-devel
BuildRequires: qt5-qtbase-gui
BuildRequires: qt5-qtwebsockets-devel
BuildRequires: qt5-qtdeclarative-devel
BuildRequires: qt5-qttools
BuildRequires: qt5-qtserialport-devel
BuildRequires: ffmpeg-devel
BuildRequires: portmidi-devel
BuildRequires: portaudio-devel
BuildRequires: lilv-devel
BuildRequires: suil-devel
BuildRequires: avahi-compat-libdns_sd-devel
BuildRequires: mesa-libGL-devel
BuildRequires: mesa-libGLU-devel
BuildRequires: fftw-devel
BuildRequires: libsndfile-devel
BuildRequires: unzip
BuildRequires: desktop-file-utils

%description
ossia score is a sequencer for audio-visual artists, designed to create interactive shows

%prep
%autosetup -cn score-v%{version}

sed -i -e "s/BOOST_MINOR 70/BOOST_MINOR 76/g" 3rdparty/libossia/cmake/OssiaDeps.cmake

%build

%cmake -DCMAKE_BUILD_TYPE=RELEASE
%cmake_build

%install

%cmake_install

# Cleanup
rm -rf %{buildroot}/usr/lib/*.a
rm -rf %{buildroot}/usr/lib/cmake/
rm -rf %{buildroot}/%{_libdir}/*.a
rm -rf %{buildroot}/%{_includedir}/
rm -rf %{buildroot}/%{_datadir}/

%files
%doc INSTALL.md README.md AUTHORS
%license LICENSE.txt
%{_bindir}/*

%changelog
* Sun Jul 24 2022 Yann Collette <ycollette.nospam@free.fr> - 3.0.12-2
- update to version 3.0.12-2

* Tue Jun 14 2022 Yann Collette <ycollette.nospam@free.fr> - 3.0.11-2
- update to version 3.0.11-2

* Mon Jun 06 2022 Yann Collette <ycollette.nospam@free.fr> - 3.0.10-2
- update to version 3.0.10-2

* Sun May 22 2022 Yann Collette <ycollette.nospam@free.fr> - 3.0.9-2
- update to version 3.0.9-2

* Tue Apr 19 2022 Yann Collette <ycollette.nospam@free.fr> - 3.0.8-2
- update to version 3.0.8-2

* Mon Apr 18 2022 Yann Collette <ycollette.nospam@free.fr> - 3.0.7-2
- update to version 3.0.7-2

* Thu Mar 24 2022 Yann Collette <ycollette.nospam@free.fr> - 3.0.6-2
- update to version 3.0.6-2

* Wed Mar 09 2022 Yann Collette <ycollette.nospam@free.fr> - 3.0.5-2
- update to version 3.0.5-2

* Thu Feb 24 2022 Yann Collette <ycollette.nospam@free.fr> - 3.0.4-2
- update to version 3.0.4-2

* Sun Jan 16 2022 Yann Collette <ycollette.nospam@free.fr> - 3.0.1-2
- update to version 3.0.1-2

* Sun Oct 25 2020 Yann Collette <ycollette.nospam@free.fr> - 2.5.2-2
- fix debug build

* Wed Oct 23 2019 Yann Collette <ycollette.nospam@free.fr> - 2.5.2-1
- initial version of the spec file
