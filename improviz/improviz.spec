%global debug_package %{nil}

Name:    improviz
Summary: A live-coded visual performance tool
Version: 0.9.0
Release: 2%{?dist}
License: BSD
URL:     https://github.com/rumblesan/improviz

Source0: https://github.com/rumblesan/%{name}/archive/%{version}.tar.gz#/%{name}-%{version}.tar.gz
Source1: improviz.yaml

BuildRequires: ghc
BuildRequires: ghc-network-devel
BuildRequires: stack
BuildRequires: gmp-devel
BuildRequires: libXrandr-devel
BuildRequires: libXi-devel
BuildRequires: libXinerama-devel
BuildRequires: libXcursor-devel
BuildRequires: freeglut-devel
BuildRequires: zlib-devel
BuildRequires: libGL-devel
BuildRequires: mesa-libGLU-devel
BuildRequires: glfw-devel
BuildRequires: libXxf86vm-devel
BuildRequires: desktop-file-utils

%description
Improviz is a live-coding environment built for creating visual performances of abstract shapes,
blurred shades and broken GIFs. It is built in Haskell and interacts directly with OpenGL.
It's very much a work in progress but is definitely stable enough to use for performances.

%prep
%autosetup -n %{name}-%{version}

sed -i -e "/-fwarn-unused-binds/a \ \ cxx-options:         -fPIC\n\ \ cc-options:          -fPIC" improviz.cabal
sed -i -e "s/-threaded/-threaded -fPIC/g" improviz.cabal

%build

%set_build_flags

#export CFLAGS="-fPIC $CFLAGS"
#export CXXFLAGS="-fPIC $CXXFLAGS"
#export LDFLAGS="-fPIC $LDFLAGS"

export CFLAGS="-fPIC"
export CXXFLAGS="-fPIC"
export LDFLAGS="-fPIC"

stack build

%install

IMPROVIZ=`stack path --local-install-root`/bin/improviz

install -m 755 -d %{buildroot}/%{_bindir}/
cp $IMPROVIZ %{buildroot}/%{_bindir}/

install -m 755 -d %{buildroot}/%{_datadir}/%{name}/
install -m 755 -d %{buildroot}/%{_datadir}/%{name}/config/

cp -ra docs         %{buildroot}/%{_datadir}/%{name}/
cp -ra examples     %{buildroot}/%{_datadir}/%{name}/
cp -ra geometries   %{buildroot}/%{_datadir}/%{name}/
cp -ra hellocatfood %{buildroot}/%{_datadir}/%{name}/
cp -ra materials    %{buildroot}/%{_datadir}/%{name}/
cp -ra stdlib       %{buildroot}/%{_datadir}/%{name}/
cp -ra test         %{buildroot}/%{_datadir}/%{name}/
cp -ra textures     %{buildroot}/%{_datadir}/%{name}/
cp -ra usercode     %{buildroot}/%{_datadir}/%{name}/
cp -a %{SOURCE1}    %{buildroot}/%{_datadir}/%{name}/config/

%files
%doc README.md
%license LICENSE
%{_bindir}/*
%{_datadir}/%{name}/*

%changelog
* Wed Oct 21 2020 Yann Collette <ycollette dot nospam at free.fr> 0.9.0-2
- update to 0.9.0

* Fri Oct 16 2020 Yann Collette <ycollette dot nospam at free.fr> 0.8.3-2
- update to 0.8.3

* Wed Sep 30 2020 Yann Collette <ycollette dot nospam at free.fr> 0.8.2-2
- fix build + install

* Mon Sep 28 2020 Yann Collette <ycollette dot nospam at free.fr> 0.8.2-1
- Initial release of spec file
