Name:    loudness-scanner
Version: 0.5.1
Release: 3%{?dist}
Summary: A loudness scanner (according to the EBU R128 standard)
URL:     https://github.com/jiixyj/loudness-scanner
License: MIT

Vendor:       Audinux
Distribution: Audinux

# ./loudness-scanner-source.sh <tag>
# ./loudness-scanner-source.sh v0.5.1

Source0: loudness-scanner.tar.gz
Source1: loudness-scanner-source.sh

BuildRequires: gcc gcc-c++
BuildRequires: cmake
BuildRequires: chrpath
BuildRequires: qt-devel
BuildRequires: glib2-devel
BuildRequires: libsndfile-devel
BuildRequires: taglib-devel
BuildRequires: mpg123-devel
BuildRequires: libmpcdec-devel
%if 0%{?fedora} >= 32
BuildRequires: gstreamer1-devel
BuildRequires: gstreamer1-plugins-base-devel
%else
BuildRequires: gstreamer-devel
BuildRequires: gstreamer-plugins-base-devel
%endif
BuildRequires: ffmpeg-devel
BuildRequires: librsvg2-devel
BuildRequires: gtk2-devel
BuildRequires: harfbuzz-devel
BuildRequires: speexdsp-devel
BuildRequires: libebur128-devel

%description
loudness-scanner is a tool that scans your music files according to the EBU
R128 standard for loudness normalisation. It optionally adds ReplayGain
compatible tags to the files.

%prep
%autosetup -n %{name}

%ifarch x86_64
sed -i -e "s/DESTINATION lib/DESTINATION lib64/g" ebur128/ebur128/CMakeLists.txt
%endif

# Remove the build of ebur128, it's a Fedora package
sed -i -e "s/add_subdirectory(ebur128\/ebur128)/#add_subdirectory(ebur128\/ebur128)/g" CMakeLists.txt

%build

%set_build_flags

%cmake -DEBUR128_INCLUDE_DIR=/usr/include 
%make_build

%install

install -d -m 755 %{buildroot}/%{_bindir}
install -pm 755 %{__cmake_builddir}/loudness          %{buildroot}/%{_bindir}/
install -pm 755 %{__cmake_builddir}/loudness-drop-gtk %{buildroot}/%{_bindir}/
install -pm 755 %{__cmake_builddir}/loudness-drop-qt  %{buildroot}/%{_bindir}/

install -d -m 755 %{buildroot}/%{_libdir}
%if 0%{?fedora} < 32
install -pm 755 %{__cmake_builddir}/libinput_gstreamer.so %{buildroot}/%{_libdir}/
%endif
install -pm 755 %{__cmake_builddir}/libinput_mpg123.so    %{buildroot}/%{_libdir}/
install -pm 755 %{__cmake_builddir}/libinput_sndfile.so   %{buildroot}/%{_libdir}/

chrpath --delete $RPM_BUILD_ROOT/usr/bin/*

%files
%doc README.md
%license COPYING
%{_bindir}/*
%{_libdir}/*

%changelog
* Fri Oct 23 2020 Yann Collette <ycollette.nospam@free.fr> - 0.5.1-4
- fix debug build

* Thu May 28 2020 Yann Collette <ycollette.nospam@free.fr> - 0.5.1-3
- fix install

* Thu May 28 2020 Yann Collette <ycollette.nospam@free.fr> - 0.5.1-2
- disable the build of libebur128

* Wed Nov 6 2019 Yann Collette <ycollette.nospam@free.fr> - 0.5.1-1
- fix for Fedora 31

* Thu Sep 12 2019 Yann Collette <ycollette.nospam@free.fr> - 0.5.1-1
- Initial spec file
