Summary: Additional presets for Dexed
Name:    dexed-extra-presets
Version: 1.0.1
Release: 3%{?dist}
License: GPLv2+ and GPLv3 and Green OpenMusic
URL:     https://asb2m10.github.io/dexed/

Vendor:       Audinux
Distribution: Audinux

Source0: http://ycollette.free.fr/Milkdrop/DX7_AllTheWeb.zip
Source1: http://ycollette.free.fr/Milkdrop/3221-Dexed_cart_1.0.zip
Source2: http://ycollette.free.fr/Milkdrop/SynLib_DX_TX_Marc_Bareille.zip
Source3: http://ycollette.free.fr/Milkdrop/dx7patch.zip

BuildArch: noarch

BuildRequires: p7zip

%description
A collection of additional preset for Dexed.

%prep

%build
echo "Nothing to build."

%install
rm -rf $RPM_BUILD_ROOT

# These directories are owned by hydrogen:
install -dm 0755 $RPM_BUILD_ROOT%{_datadir}/dexed/presets

7za x %{SOURCE0} -o$RPM_BUILD_ROOT%{_datadir}/dexed/presets/alltheweb
7za x %{SOURCE1} -o$RPM_BUILD_ROOT%{_datadir}/dexed/presets/cart
7za x %{SOURCE2} -o$RPM_BUILD_ROOT%{_datadir}/dexed/presets/syntlib
7za x %{SOURCE3} -o$RPM_BUILD_ROOT%{_datadir}/dexed/presets/

# Reorganisation
cd $RPM_BUILD_ROOT%{_datadir}/dexed/presets/alltheweb
mv DX7_AllTheWeb/* .
rmdir DX7_AllTheWeb

cd $RPM_BUILD_ROOT%{_datadir}/dexed/presets/syntlib
mv SynLib_DX_TX_Marc_Bareille/* .
rmdir SynLib_DX_TX_Marc_Bareille

cd $RPM_BUILD_ROOT%{_datadir}/dexed/presets/dx7patch
mv README README-dx7patch

# Change file / dir properties
cd $RPM_BUILD_ROOT%{_datadir}/dexed/presets/
find . -name "*.syx" -exec chmod a+rw {} \;
find . -type d -exec chmod u+rwx,g+rx-w,o+rx-w {} \;

%files
%{_datadir}/dexed/presets/alltheweb/*
%{_datadir}/dexed/presets/cart/*
%{_datadir}/dexed/presets/syntlib/*
%{_datadir}/dexed/presets/dx7patch/*

%changelog
* Sat Mar 21 2020 Yann Collette <ycollette dot nospam at free.fr> 1.0.1-3
- add some more files from dx7patch

* Fri Mar 20 2020 Yann Collette <ycollette dot nospam at free.fr> 1.0.1-2
- fix file / directories properties

* Wed Jan 23 2019 Yann Collette <ycollette dot nospam at free.fr> 1.0.1-1
- add SynLib_DX_TX_Marc_Bareille.zip

* Sun Sep 09 2018 Yann Collette <ycollette dot nospam at free.fr> 1.0.0-1
- Initial release
