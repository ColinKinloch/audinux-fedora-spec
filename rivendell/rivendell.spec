Summary: A radio automation system
Name:    rivendell
Version: 3.6.5
Release: 1%{?dist}
License: LGPL
URL:     https://github.com/ElvishArtisan/rivendell

Vendor:       Audinux
Distribution: Audinux

Source0: https://github.com/ElvishArtisan/rivendell/archive/refs/tags/v%{version}.tar.gz#/rivendell-%{version}.tar.gz
Patch0: rivendell-0001-use-nullptr.patch
Patch1: rivendell-0001-use-nullptr-2.patch
Patch2: rivendell-0001-use-nullptr-3.patch

BuildRequires: gcc gcc-c++
BuildRequires: alsa-lib-devel jack-audio-connection-kit-devel
BuildRequires: cdparanoia-devel
BuildRequires: id3lib-devel
BuildRequires: taglib-devel
BuildRequires: pam-devel
BuildRequires: soundtouch-devel
BuildRequires: gtk-update-icon-cache
BuildRequires: qt5-qtbase-devel
BuildRequires: qt-devel
BuildRequires: docbook-style-xsl
BuildRequires: autoconf automake libtool
BuildRequires: python3
BuildRequires: sed
BuildRequires: openssl-devel
BuildRequires: libcurl-devel
BuildRequires: expat-devel
BuildRequires: lame-devel
BuildRequires: libvorbis-devel
BuildRequires: libmad-devel
BuildRequires: libsamplerate-devel
BuildRequires: libsndfile-devel
BuildRequires: flac-devel
BuildRequires: libmusicbrainz5-devel
BuildRequires: libdiscid-devel
BuildRequires: libcoverart-devel
BuildRequires: libmp4v2-devel
BuildRequires: twolame-devel
#BuildRequires: faad2-devel

Requires: madplay, autofs
Requires: python3, python3-pycurl, python3-requests, python3-pyserial, python3-mysql

%description
Rivendell is a complete radio broadcast automation solution, with
facilities for the acquisition, management, scheduling and playout of
audio content.  Modules for the production and management of podcast
audio are also included.

%prep
%autosetup -p1 -n %{name}-%{version}

sed -i -e "s/instdir = @LOCAL_PREFIX@\/lib/instdir = @LOCAL_PREFIX@\/%{_lib}/g" lib/Makefile.am

%build

./autogen.sh

# -Werror=format-security

CFLAGS='-O2 -g -pipe -Wall -Wp,-D_FORTIFY_SOURCE=2 -Wp,-D_GLIBCXX_ASSERTIONS -fexceptions -fstack-protector-strong -grecord-gcc-switches -specs=/usr/lib/rpm/redhat/redhat-hardened-cc1 -specs=/usr/lib/rpm/redhat/redhat-annobin-cc1 -m64 -mtune=generic -fasynchronous-unwind-tables -fstack-clash-protection -fcf-protection'
export CFLAGS
CXXFLAGS='-O2 -g -pipe -Wall -Wp,-D_FORTIFY_SOURCE=2 -Wp,-D_GLIBCXX_ASSERTIONS -fexceptions -fstack-protector-strong -grecord-gcc-switches -specs=/usr/lib/rpm/redhat/redhat-hardened-cc1 -specs=/usr/lib/rpm/redhat/redhat-annobin-cc1 -m64 -mtune=generic -fasynchronous-unwind-tables -fstack-clash-protection -fcf-protection'
export CXXFLAGS
FFLAGS='-O2 -g -pipe -Wall -Wp,-D_FORTIFY_SOURCE=2 -Wp,-D_GLIBCXX_ASSERTIONS -fexceptions -fstack-protector-strong -grecord-gcc-switches -specs=/usr/lib/rpm/redhat/redhat-hardened-cc1 -specs=/usr/lib/rpm/redhat/redhat-annobin-cc1 -m64 -mtune=generic -fasynchronous-unwind-tables -fstack-clash-protection -fcf-protection -I/usr/lib64/gfortran/modules'
export FFLAGS
FCFLAGS='-O2 -g -pipe -Wall -Wp,-D_FORTIFY_SOURCE=2 -Wp,-D_GLIBCXX_ASSERTIONS -fexceptions -fstack-protector-strong -grecord-gcc-switches -specs=/usr/lib/rpm/redhat/redhat-hardened-cc1 -specs=/usr/lib/rpm/redhat/redhat-annobin-cc1 -m64 -mtune=generic -fasynchronous-unwind-tables -fstack-clash-protection -fcf-protection -I/usr/lib64/gfortran/modules'
export FCFLAGS
LDFLAGS='-Wl,-z,relro  -Wl,-z,now -specs=/usr/lib/rpm/redhat/redhat-hardened-ld'
export LDFLAGS

%configure --prefix=%{_prefix} --libdir=%{_libdir} --disable-docbook
%make_build

%install

%make_install

install -m 755 -d %{buildroot}/usr/lib/systemd/system/
mv %{buildroot}/lib/systemd/system/rivendell.service %{buildroot}/usr/lib/systemd/system/rivendell.service

for Files in %{buildroot}/%{_libdir}/rivendell/pypad/*.py
do
    sed -i -e "s/bin\/python/bin\/python2/g" $Files
done

%post
update-desktop-database -q
touch --no-create %{_datadir}/icons/hicolor >&/dev/null || :

/sbin/ldconfig
/bin/systemctl daemon-reload
/usr/sbin/groupadd -r -g 150 %{name} &>/dev/null || :
/usr/sbin/useradd -o -u 150 -g %{name} -s /bin/false -r -c "Rivendell radio automation system" -d /var/snd %{name} &>/dev/null || :
if test ! -e /var/snd ; then
  mkdir -p /var/snd
  chown rivendell:rivendell /var/snd
  chmod 775 /var/snd
fi
if test ! -d /etc/rivendell.d ; then
  mkdir -p /etc/rivendell.d
  chmod 775 /etc/rivendell.d
fi
if test ! -e /etc/rd.conf ; then
  cp /usr/share/doc/rivendell-%{version}/rd.conf-sample /etc/rivendell.d/rd-default.conf
  ln -s /etc/rivendell.d/rd-default.conf /etc/rd.conf
fi
if test ! -h /etc/rd.conf ; then
  mv /etc/rd.conf /etc/rivendell.d/rd-default.conf
  ln -s /etc/rivendell.d/rd-default.conf /etc/rd.conf
fi
if test ! -e /etc/asound.conf ; then
  cp /usr/share/doc/rivendell-%{version}/asound.conf-sample /etc/asound.conf
fi
/usr/sbin/rddbmgr --modify
/bin/systemctl restart rivendell
/bin/systemctl enable rivendell
/bin/systemctl restart httpd
/bin/systemctl enable httpd
if [ -x %{_bindir}/gtk-update-icon-cache ] ; then
  %{_bindir}/gtk-update-icon-cache -f --quiet %{_datadir}/icons/hicolor || :
fi
if test ! -e ${exec_prefix}/libexec/logos ; then
    mkdir -p ${exec_prefix}/libexec/logos
fi
if test ! -f ${exec_prefix}/libexec/logos/webget_logo.png ; then
    cp /usr/share/doc/rivendell-%{version}/logos/webget_logo.png ${exec_prefix}/libexec/logos/webget_logo.png
fi
mkdir -p /var/log/rivendell
if test ! -e /etc/rsyslog.d/rivendell.conf ; then
    cp /usr/share/doc/rivendell-%{version}/syslog.conf-sample /etc/rsyslog.d/rivendell.conf
fi
/bin/systemctl restart rsyslog
exit 0

%preun
if test "$1" = "0" ; then
  /bin/systemctl stop rivendell
  /bin/systemctl disable rivendell
  /bin/systemctl stop rivendell
fi
exit 0

%files
%doc AUTHORS INSTALL NEWS README ChangeLog UPGRADING
%license COPYING
%{_datadir}/*
%{_libdir}/*
%{_libexecdir}/*
%{_bindir}/*
%{_sbindir}/*
%{_sysconfdir}/*
%{_includedir}/*
%{_unitdir}/*

%changelog
* Sun Mar 20 2022 Yann Collette <ycollette.nospam@free.fr> - 3.6.5-1
- update to 3.6.5-1

* Tue Feb 22 2022 Yann Collette <ycollette.nospam@free.fr> - 3.6.4-1
- update to 3.6.4-1

* Wed Aug 04 2021 Yann Collette <ycollette.nospam@free.fr> - 3.6.2-1
- update to 3.6.2-1

* Sun Jun 06 2021 Yann Collette <ycollette.nospam@free.fr> - 3.6.1-1
- update to 3.6.1-1

* Sat May 15 2021 Yann Collette <ycollette.nospam@free.fr> - 3.6.0-1
- update to 3.6.0

* Sun Dec 13 2020 Yann Collette <ycollette.nospam@free.fr> - 3.5.0-1
- update to 3.5.0

* Wed Jul 22 2020 Yann Collette <ycollette.nospam@free.fr> - 3.4.1-1
- update to 3.4.1

* Sat May 23 2020 Yann Collette <ycollette.nospam@free.fr> - 3.4.0-1
- update to 3.4.0

* Sat Jan 25 2020 Yann Collette <ycollette.nospam@free.fr> - 3.2.1-1
- update to 3.2.1

* Sun Nov 3 2019 Yann Collette <ycollette.nospam@free.fr> - 3.2.0-1
- update to 3.2.0 + some fixes from the rivendell spec file

* Sat Sep 21 2019 Yann Collette <ycollette.nospam@free.fr> - 3.1.0-1
- initial release of the spec file
