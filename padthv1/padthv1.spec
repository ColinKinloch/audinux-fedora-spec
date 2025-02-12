# Tag: MIDI
# Type: Plugin, LV2
# Category: Audio, Synthesizer
# LastSourceUpdate: 2021

Summary: Old-school all-digital 4-oscillator subtractive polyphonic synthesizer with stereo fx.
Name:    padthv1
Version: 0.9.26
Release: 1%{?dist}
URL:     https://sourceforge.net/projects/%{name}
License: GPLv2+

Vendor:       Audinux
Distribution: Audinux

Source0: https://download.sourceforge.net/%{name}/%{name}-%{version}.tar.gz
Patch0:  padthv1-0001-disable-strip.patch

BuildRequires: gcc-c++
BuildRequires: cmake
BuildRequires: alsa-lib-devel
BuildRequires: jack-audio-connection-kit-devel
BuildRequires: qt5-qtbase-devel
BuildRequires: qt5-linguist
BuildRequires: lv2-devel >= 1.2.0
BuildRequires: desktop-file-utils
BuildRequires: libsndfile-devel
BuildRequires: fftw-devel
BuildRequires: liblo-devel
BuildRequires: qt5-qtsvg-devel
BuildRequires: libappstream-glib

Requires: hicolor-icon-theme

%description
Based on the PADsynth algorithm, by Paul Nasca (ZynAddSubFX), 
as a special variant of additive synthesis.

%package -n lv2-%{name}
Summary:  An LV2 port of synthv1
Requires: lv2
Requires: %{name}%{?_isa} = %{version}-%{release}

%description -n lv2-%{name}
An LV2 plugin of the padthv1 synthesizer

%prep
%autosetup -p1

%build

%cmake -DCONFIG_QT6=OFF
%cmake_build

%install

%cmake_install

install -m 755 -d %{buildroot}/%{_datadir}/mime/packages/
install -m 755 -d %{buildroot}/%{_datadir}/metainfo/

install -m 644 src/mimetypes/org.rncbc.padthv1.xml %{buildroot}%{_datadir}/mime/packages/padthv1.xml
install -m 644 src/appdata/org.rncbc.padthv1.metainfo.xml %{buildroot}%{_datadir}//metainfo/org.rncbc.padthv1.xml

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/org.rncbc.padthv1.desktop
#appstream-util validate-relax --nonet %{buildroot}%{_metainfodir}/org.rncbc.padthv1.xml

%files
%doc README
%license LICENSE
%{_datadir}/applications/org.rncbc.padthv1.desktop
%{_datadir}/icons/hicolor/*/*/*
%{_bindir}/%{name}_jack
%{_datadir}/man/man1/%{name}*
%{_datadir}/man/*/man1/%{name}*
%{_datadir}/mime/packages/*.xml
%{_datadir}/metainfo/*.xml

%files -n lv2-%{name}
%{_libdir}/lv2/%{name}.lv2/

%changelog
* Tue Jun 07 2022 Yann Collette <ycollette.nospam@free.fr> - 0.9.26-1
- update to 0.9.26-1

* Wed Jan 26 2022 Yann Collette <ycollette.nospam@free.fr> - 0.9.24-1
- update to 0.9.24-1

* Fri Oct 23 2020 Yann Collette <ycollette.nospam@free.fr> - 0.9.17-1
- update to 0.9.17-1 + fix debug build

* Fri Mar 27 2020 Yann Collette <ycollette.nospam@free.fr> - 0.9.13-1
- update to 0.9.13-1

* Sun Mar 15 2020 Yann Collette <ycollette.nospam@free.fr> - 0.9.12-1
- Initial spec file
