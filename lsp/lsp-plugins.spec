# Tag: Jack, Equalizer, Compressor, Convolution, Gate, Analyzer, Reverb, Delay, MIDI
# Type: Plugin, LV2
# Category: Audio, Effect

%global debug_package %{nil}

Name:    lsp-plugins
Summary: Linux Studio Plugins collection
Version: 1.2.2
Release: 1%{?dist}
License: GPL
URL:     https://github.com/sadko4u/lsp-plugins

Vendor:       Audinux
Distribution: Audinux

# ./lsp-sources.sh 1.2.2

Source0: lsp-plugins.tar.gz
Source1: lsp-sources.sh

BuildRequires: gcc gcc-c++ make
BuildRequires: lv2-devel
BuildRequires: ladspa-devel
BuildRequires: jack-audio-connection-kit-devel
BuildRequires: libsndfile-devel
BuildRequires: cairo-devel
BuildRequires: expat-devel
BuildRequires: mesa-libGLU-devel
BuildRequires: mesa-libGL-devel
BuildRequires: libXrandr-devel
BuildRequires: php-cli
BuildRequires: chrpath

%description
LSP (Linux Studio Plugins) is a collection of open-source plugins
currently compatible with LADSPA, LV2 and LinuxVST formats.

%package -n ladspa-%{name}
Summary: LADSPA version of %{name} plugins

%description -n ladspa-%{name}
LADSPA version of %{name} plugins

%package -n vst-%{name}
Summary: VST2 version of %{name} plugins

%description -n vst-%{name}
VST2 version of %{name} plugins

%package -n lv2-%{name}
Summary: LV2 version of %{name} plugins

%description -n lv2-%{name}
LV2 version of %{name} plugins

%prep
%autosetup -n lsp-plugins

%build
%set_build_flags
export CXXFLAGS="-std=c++98 $CXXFLAGS"

%make_build PREFIX=%{_usr} LIBDIR=%{_libdir} config
%make_build PREFIX=%{_usr} LIBDIR=%{_libdir} VERBOSE=1

%install

%make_install PREFIX=%{_usr} LIBDIR=%{_libdir}

chrpath --delete %{buildroot}/usr/bin/*
chrpath --delete %{buildroot}/usr/%{_lib}/ladspa/*.so
chrpath --delete %{buildroot}/usr/%{_lib}/lsp-plugins/*.so
chrpath --delete %{buildroot}/usr/%{_lib}/lv2/lsp-plugins.lv2/*.so
chrpath --delete %{buildroot}/usr/%{_lib}/vst/lsp-plugins/*.so

mkdir -p %{buildroot}/usr/share/lsp-plugins/
mv %{buildroot}/usr/share/doc/lsp-plugins %{buildroot}/usr/share/lsp-plugins/doc

%files
%doc CHANGELOG README.md
%license COPYING
%{_bindir}/*
%{_datadir}/*
%{_libdir}/pkgconfig/*
%{_libdir}/*.so
%{_libdir}/lsp-plugins/*.so
%exclude %{_libdir}/*.a

%files -n lv2-%{name}
%{_libdir}/lv2/* 

%files -n ladspa-%{name}
%{_libdir}/ladspa/* 

%files -n vst-%{name}
%{_libdir}/vst/* 


%changelog
* Thu Jun 23 2022 Yann Collette <ycollette dot nospam at free.fr> 1.2.2-1
- update to 1.2.2-1

* Wed May 04 2022 Yann Collette <ycollette dot nospam at free.fr> 1.2.1-1
- update to 1.2.1-1

* Sat Mar 26 2022 Yann Collette <ycollette dot nospam at free.fr> 1.2.0-1
- update to 1.2.0-1

* Tue Dec 21 2021 Yann Collette <ycollette dot nospam at free.fr> 1.1.31-1
- update to 1.1.31-1

* Thu Apr 01 2021 Yann Collette <ycollette dot nospam at free.fr> 1.1.30-1
- update to 1.1.30-1

* Tue Jan 19 2021 Yann Collette <ycollette dot nospam at free.fr> 1.1.29-1
- update to 1.1.29-1

* Mon Dec 21 2020 Yann Collette <ycollette dot nospam at free.fr> 1.1.28-1
- update to 1.1.28-1

* Wed Sep 16 2020 Yann Collette <ycollette dot nospam at free.fr> 1.1.26-1
- update to 1.1.26-1

* Thu Jul 16 2020 Yann Collette <ycollette dot nospam at free.fr> 1.1.24-1
- update to 1.1.24-1

* Sun May 31 2020 Yann Collette <ycollette dot nospam at free.fr> 1.1.22-1
- update to 1.1.22-1

* Sun May 17 2020 Yann Collette <ycollette dot nospam at free.fr> 1.1.21-1
- update to 1.1.21-1

* Sun Apr 19 2020 Yann Collette <ycollette dot nospam at free.fr> 1.1.19-1
- update to 1.1.19-1

* Sun Apr 5 2020 Yann Collette <ycollette dot nospam at free.fr> 1.1.17-1
- update to 1.1.17-1

* Sun Mar 29 2020 Yann Collette <ycollette dot nospam at free.fr> 1.1.15-1
- update to 1.1.15-1

* Tue Dec 24 2019 Yann Collette <ycollette dot nospam at free.fr> 1.1.13-1
- update to 1.1.13-1

* Sun Dec 22 2019 Yann Collette <ycollette dot nospam at free.fr> 1.1.11-1
- update to 1.1.11-1

* Tue Jul 23 2019 Yann Collette <ycollette dot nospam at free.fr> 1.1.10-1
- update to 1.1.10-1

* Mon Mar 18 2019 Yann Collette <ycollette dot nospam at free.fr> 1.1.7-1
- update to 1.1.7-1

* Fri Dec 21 2018 Yann Collette <ycollette dot nospam at free.fr> 1.1.5-1
- update to 1.1.5-1

* Mon Oct 15 2018 Yann Collette <ycollette dot nospam at free.fr> 1.1.4-1
- update for Fedora 29

* Sun Sep 30 2018 Yann Collette <ycollette dot nospam at free.fr> 1.1.4-1
- Initial release of the spec file
