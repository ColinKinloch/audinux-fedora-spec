%global commit0 1916d46a2823d0f091edf545666058456c93b004

Name: boomer
Version: 0.0.1
Release: 1%{?dist}
Summary: A drum synth
License: GPLv2	
URL: https://github.com/clearly-broken-software/boomer

# Usage: ./boomer-source.sh <TAG>
# ./boomer-source.sh 1916d46a2823d0f091edf545666058456c93b004

Source0: boomer.tar.gz
Source1: boomer-source.sh

BuildRequires: gcc gcc-c++
BuildRequires: make
BuildRequires: mesa-libGL-devel
BuildRequires: libsndfile-devel
BuildRequires: rubberband-devel
BuildRequires: jack-audio-connection-kit-devel
BuildRequires: libX11-devel
BuildRequires: lv2-devel

%description
A drum synth

%package -n vst-%{name}
Summary:  VST version of %{name}
License:  GPLv2+
Requires: %{name}

%description -n vst-%{name}
VST version of %{name}

%package -n lv2-%{name}
Summary:  LV2 version of %{name}
License:  GPLv2+
Requires: %{name}

%description -n lv2-%{name}
LV2 version of %{name}

%prep
%autosetup -n boomer

%build
%set_build_flags
export CXXFLAGS="$CXXFLAGS -include limits"
%make_build SKIP_STRIPPING=true

%install

install -m 755 -d %{buildroot}/%{_bindir}/
install -m 755 -d %{buildroot}/%{_libdir}/lv2/boomer.lv2/
install -m 755 -d %{buildroot}/%{_libdir}/vst/

install -m 755 -p bin/boomer %{buildroot}%{_bindir}/
install -m 755 -p bin/boomer-vst.so %{buildroot}%{_libdir}/vst/
cp -ra bin/boomer.lv2/* %{buildroot}%{_libdir}/lv2/boomer.lv2/

%files
%doc README.md
%license LICENSE.md
%{_bindir}/*

%files -n vst-%{name}
%{_libdir}/vst/*

%files -n lv2-%{name}
%{_libdir}/lv2/*

%changelog
* Tue Aug 02 2022 Yann Collette <ycollette.nospam@free.fr> - 0.0.1-1
- initial spec file
