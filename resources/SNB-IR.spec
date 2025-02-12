Summary: Impulse response from SNB studio
Name:    SNB-IR
Version: 1.0.0
Release: 2%{?dist}
License: GPLv2+ and GPLv3
URL:     http://www.grgr.de/IR/

Vendor:       Audinux
Distribution: Audinux

Source0: IR.zip

BuildArch: noarch

BuildRequires: unzip

%description
A collection of impulse responses from SNB studio

%prep

%build
echo "Nothing to build."

%install
rm -rf $RPM_BUILD_ROOT

# These directories are owned by hydrogen:
install -dm 0755 $RPM_BUILD_ROOT%{_datadir}/IR/SNB

cd $RPM_BUILD_ROOT%{_datadir}/IR/SNB
unzip %{SOURCE0}

%files
%{_datadir}/IR/SNB/

%changelog
* Sat Nov 30 2019 Yann Collette <ycollette dot nospam at free.fr> 1.0.0-1
- Initial release
