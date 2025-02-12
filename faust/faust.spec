# Tag: Jack, Alsa
# Type: Standalone, Language
# Category: Audio, Programming

Name:	 faust
Version: 2.41.1
Release: 24%{?dist}
Summary: Compiled language for real-time audio signal processing
# Examples are BSD
# The rest is GPLv2+
License: GPLv2+ and BSD
URL:     http://faust.grame.fr

Vendor:       Audinux
Distribution: Audinux

Source0: https://github.com/grame-cncm/faust/releases/download/%{version}/faust-%{version}.tar.gz

BuildRequires: gcc-c++
BuildRequires: doxygen
BuildRequires: graphviz
BuildRequires: cmake
BuildRequires: unzip
BuildRequires: pandoc
BuildRequires: python2
BuildRequires: texlive-latex
BuildRequires: texlive-collection-basic
BuildRequires: texlive-collection-fontsrecommended
BuildRequires: texlive-mdwtools
BuildRequires: libmicrohttpd-devel

%description
Faust AUdio STreams is a functional programming language for real-time audio
signal processing. Its programming model combines two approaches : functional
programming and block diagram composition. You can think of FAUST as a
structured block diagram language with a textual syntax.

FAUST is intended for developers who need to develop efficient C/C++ audio
plugins for existing systems or full standalone audio applications. Thanks to
some specific compilation techniques and powerful optimizations, the C++ code
generated by the Faust compiler is usually very fast. It can generally compete
with (and sometimes outperform) hand-written C code.

Programming with FAUST is somehow like working with electronic circuits and 
signals. A FAUST program is a list of definitions that defines a signal 
processor block-diagram : a piece of code that produces output signals
according to its input signals (and maybe some user interface parameters)

%package doc
Summary:   Documentation for %{name}
License:   GPLv2+
BuildArch: noarch
Requires:  %{name} = %{version}-%{release}

%description doc
Faust AUdio STreams is a functional programming language for real-time audio
signal processing. This package provides documentation files to help with 
writing programs with faust.

%package osclib
Summary:  OSCLib Library
License:  GPLv2+ and MIT
Requires: %{name} = %{version}-%{release}

%description osclib
Faust AUdio STreams is a functional programming language for real-time audio
signal processing. This package provides osclib.

%package osclib-devel
Summary:  Headers for the OSCLib Library
License:  GPLv2+ and MIT
Requires: %{name}-osclib = %{version}-%{release}

%description osclib-devel
Faust AUdio STreams is a functional programming language for real-time audio
signal processing. This package provides the development files for osclib.

%package tools
Summary:   3rd party tools written for %{name}
License:   GPLv2+
BuildArch: noarch
Requires:  %{name}-osclib-devel = %{version}-%{release}
Requires:  python2

%description tools
Faust AUdio STreams is a functional programming language for real-time audio
signal processing. These additional tools are provided by various contributors
to help the building process of applications and plugins with Faust.

%package kate
Summary:   Kate/Kwrite plugin for %{name}
License:   GPLv2+
BuildArch: noarch
Requires:  %{name} = %{version}-%{release}

%description kate
Faust AUdio STreams is a functional programming language for real-time audio
signal processing. This package provides Faust code syntax highlighting support
for KDE's Kate/Kwrite.

%package stdlib
Summary:   standard libraries for %{name}
License:   GPLv2+
BuildArch: noarch
Requires:  %{name} = %{version}-%{release}

%description stdlib
Faust AUdio STreams is a functional programming language for real-time audio
signal processing. These libraries are part of the standard Faust libraries.

%prep
%autosetup -n faust-%{version}

# For installation in the correct location and for preserving timestamps:
# The Makefile normally puts noarch files in $prefix/lib. We change
# this to $prefix/share
# Also don't build the osclib until upstream supports shared libs
#	-e '/osclib/d'				\
sed -i	-e 's|/lib/|/share/|g'			\
	-e 's| -r | -pr |'			\
	-e 's| -m | -pm |'			\
	Makefile
sed -i 's|/lib|/share|g' compiler/parser/enrobage.cpp

# Fix optflags
sed -i 's|-O3|%{optflags} -fPIC	|' compiler/parser/Makefile \
			architecture/osclib/oscpack/Makefile

# Fix permissions
chmod -x compiler/draw/device/SVGDev.* architecture/VST/PkgInfo
chmod +x tools/faust2appls/faust2*
chmod -x tools/faust2pd/faust2*

# fix usage.sh
for Files in `grep -l usage.sh tools/faust2appls/*`
do
  sed -i -e "s/usage.sh/\/usr\/share\/faust\/usage.sh/g" $Files
done

# Fix encoding
for i in examples syntax-highlighting; do
    iconv -f iso8859-1 -t utf8 $i/README.md -o tmpfile
    touch -r $i/README.md tmpfile
    mv -f tmpfile $i/README.md
done

# To distinguish doc files
mv architecture/osclib/faust/changelog.txt architecture/osclib/faust/changelog.faustOSC.txt
mv architecture/osclib/faust/license.txt   architecture/osclib/faust/license.faustOSC.txt

for i in CHANGES LICENSE README TODO; do
    mv architecture/osclib/oscpack/$i architecture/osclib/oscpack/$i.osscpack.txt
done

# install lib in the good directory
sed -i -e "s/\$(BUILDLOCATION)\/lib/\$(BUILDLOCATION)\/%{_lib}/g" Makefile

%build

%set_build_flags

# Build the main executable
%make_build PREFIX=%{_prefix} LIBDIR=%{_libdir} MODE=SHARED
cd architecture/osclib/oscpack
%make_build PREFIX=%{_prefix} LIBDIR=%{_libdir} MODE=SHARED lib

%install
mkdir -p %{buildroot}/%{_bindir}
mkdir -p %{buildroot}/%{_datadir}/%{name}
mkdir -p %{buildroot}/%{_libdir}
%make_install PREFIX=%{_prefix} LIBDIR=%{_libdir} INCLUDEDIR=%{_includedir}

# install liboscpack manually
pushd .
cd architecture/osclib/oscpack
cp liboscpack.so.1.1.0 %{buildroot}/%{_libdir}
cd %{buildroot}/%{_libdir}
ln -s liboscpack.so.1.1.0 liboscpack.so.1
ln -s liboscpack.so.1 liboscpack.so
popd

# Install tools
cp -a tools/%{name}2sc-*/%{name}2sc %{buildroot}/%{_bindir}
mv tools/%{name}2sc-*/README README.supercollider

cp -a tools/%{name}2appls/%{name}2* %{buildroot}/%{_bindir}

# Install the kate plugin
mkdir -p %{buildroot}/%{_datadir}/kde4/apps/katepart/syntax/
cp -a syntax-highlighting/%{name}.xml %{buildroot}/%{_datadir}/kde4/apps/katepart/syntax/

# move the .a library
%ifarch x86_64 amd64
  mkdir -p %{buildroot}/%{_libdir}/
  mv %{buildroot}/usr/lib/*.a %{buildroot}/%{_libdir}/
%endif

# install library
cd libraries
export PATH=../tools/faust2appls/:$PATH

mkdir -p %{buildroot}/%{_datadir}/faust/
cp *.lib old/*.lib %{buildroot}/%{_datadir}/faust/

mkdir -p %{buildroot}/%{_datadir}/faust/doc/
cp doc/library.pdf %{buildroot}/%{_datadir}/faust/doc/

mv README.md README-stdlib.md

# remove some wasm files (not yet correctly managed by rpm):
rm %{buildroot}%{_datadir}/faust/webaudio/audioinput.wasm
rm %{buildroot}%{_datadir}/faust/webaudio/libfaust-glue.wasm
rm %{buildroot}%{_datadir}/faust/webaudio/libfaust-wasm.wasm
rm %{buildroot}%{_datadir}/faust/webaudio/mixer32.wasm
rm %{buildroot}%{_datadir}/faust/webaudio/mixer64.wasm
rm %{buildroot}%{_datadir}/faust/webaudio/noise.wasm
rm %{buildroot}%{_datadir}/faust/webaudio/organ.wasm
rm %{buildroot}%{_datadir}/faust/webaudio/osc.wasm

rm %{buildroot}/%{_libdir}/ios-libsndfile.a

rm %{buildroot}%{_datadir}/faust/android/app/lib/libsndfile/lib/*/libsndfile.so

mv %{buildroot}/%{_bindir}/usage.sh %{buildroot}/%{_datadir}/faust/

%ldconfig_scriptlets osclib

%files
%doc README.md examples
%license COPYING.txt
%{_bindir}/%{name}
%{_datadir}/%{name}/
%{_mandir}/*

%files osclib
%doc architecture/osclib/README.md
%{_libdir}/*.so.*

%files osclib-devel
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/*.a

%files doc
%doc documentation/* 

%files tools
%doc tools/README.md README.supercollider tools/%{name}2pd
%{_bindir}/%{name}2*
%{_bindir}/encoderunitypackage
%{_bindir}/faustoptflags
%{_bindir}/faustpath
%{_bindir}/sound2reader
%{_bindir}/filename2ident
%{_bindir}/faustremote
%{_bindir}/faust-config

%files kate
%doc syntax-highlighting/README.md
%{_datadir}/kde4/apps/katepart/syntax/%{name}.xml

%files stdlib
%doc libraries/README-stdlib.md
%{_datadir}/faust/doc/library.pdf
%{_datadir}/faust/*.lib

%changelog
* Mon Jul 18 2022 Yann Collette <ycollette.nospam@free.fr> - 2.41.1-24
- update to 2.41.1-24

* Thu Jun 30 2022 Yann Collette <ycollette.nospam@free.fr> - 2.41.1-23
- update to 2.41.1-23

* Mon Nov 01 2021 Yann Collette <ycollette.nospam@free.fr> - 2.37.3-23
- update to 2.37.3-23

* Wed Jul 21 2021 Yann Collette <ycollette.nospam@free.fr> - 2.33.1-23
- update to 2.33.1-23

* Sat Jan 23 2021 Yann Collette <ycollette.nospam@free.fr> - 2.30.5-23
- update to 2.30.5-23

* Fri Oct 23 2020 Yann Collette <ycollette.nospam@free.fr> - 2.27.2-23
- fix debug build

* Mon Aug 17 2020 Yann Collette <ycollette.nospam@free.fr> - 2.27.2-22
- Update to 2.27.2-22. Fix python in faust2appl tools

* Thu Aug 6 2020 Yann Collette <ycollette.nospam@free.fr> - 2.27.2-21
- Update to 2.27.2-21.

* Wed Jul 22 2020 Yann Collette <ycollette.nospam@free.fr> - 2.27.1-21
- Update to 2.27.1-21. Fix install

* Tue Jul 21 2020 Yann Collette <ycollette.nospam@free.fr> - 2.27.1-20
- Update to 2.27.1-20

* Tue May 12 2020 Yann Collette <ycollette.nospam@free.fr> - 2.20.2-20
- Update to 2.20.2-20. Fix libraries installation

* Sat Apr 25 2020 Yann Collette <ycollette.nospam@free.fr> - 2.20.2-19
- Update to 2.20.2-19. 

* Wed Apr 22 2020 Yann Collette <ycollette.nospam@free.fr> - 2.14.4-19
- Update to 2.14.4-19. Fix for Fedora 32

* Wed Jan 15 2020 Yann Collette <ycollette.nospam@free.fr> - 2.14.4-18
- Update to 2.14.4-18. Add stdlib

* Mon Jan 13 2020 Yann Collette <ycollette.nospam@free.fr> - 2.14.4-17
- Update to 2.14.4-17

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.46-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.46-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.46-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.46-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.46-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.46-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon May 15 2017 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.46-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.46-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sun Jul 10 2016 Jon Ciesla <limburgher@gmail.com> - 0.9.46-9
- Drop kdesdk Requires, retired.

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.46-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.46-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat May 02 2015 Kalev Lember <kalevlember@gmail.com> - 0.9.46-6
- Rebuilt for GCC 5 C++11 ABI change

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.46-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.46-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.46-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.46-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Aug 31 2012 Jon Ciesla <limburgher@gmail.com> - 0.9.46-1
- New upstream.

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.43-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Feb 28 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.43-4
- Rebuilt for c++ ABI breakage

* Tue Jan 10 2012 Orcan Ogetbil <oget [DOT] fedora [AT] gmail [DOT] com> - 0.9.43-3
- gcc-4.7 compile fix

* Sun Nov 27 2011 Orcan Ogetbil <oget [DOT] fedora [AT] gmail [DOT] com> - 0.9.43-2
- Drop executable permission on faust2pd.pure to avoid an unavailable dependency.

* Fri Nov 25 2011 Orcan Ogetbil <oget [DOT] fedora [AT] gmail [DOT] com> - 0.9.43-1
- Update to 0.9.43

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.30-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Nov 25 2010 Orcan Ogetbil <oget [DOT] fedora [AT] gmail [DOT] com> - 0.9.30-1
- Update to 0.9.30

* Mon May 31 2010 Orcan Ogetbil <oget [DOT] fedora [AT] gmail [DOT] com> - 0.9.24-1
- Update to 0.9.24
- Don't bundle the source documentation. It is only needed by faust developers, not users.

* Sat May 15 2010 Orcan Ogetbil <oget [DOT] fedora [AT] gmail [DOT] com> - 0.9.22-1
- Update to 0.9.22

* Sun Jan 31 2010 Orcan Ogetbil <oget [DOT] fedora [AT] gmail [DOT] com> - 0.9.10-1
- Update to 0.9.10

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.9.4-3.b
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sat Mar 21 2009 Orcan Ogetbil <oget [DOT] fedora [AT] gmail [DOT] com> - 0.9.9.4-2.b
- Fix the year of the previous changelog entry
- Install the nonbinary files in %%{_datadir}/%%{name}/
- Add Requires: %%{name}=%%{version}-%%{release} to the doc subpackage

* Mon Mar 16 2009 Orcan Ogetbil <oget [DOT] fedora [AT] gmail [DOT] com> - 0.9.9.4-1.b
- Initial build
