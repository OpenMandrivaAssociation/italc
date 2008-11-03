%define name italc
%define libname %mklibname italc
%define version 1.0.9
%define release %mkrel 1

Name:		%name
Version:	%version
Release:	%release
Summary:	Intelligent Teaching And Learning with Computers
License:	GPLv2+
Group:		Networking/Remote access
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
URL:		http://italc.sourceforge.net/
Source:		%{name}-%{version}.tar.bz2
Patch0:		italc-1.0.9-detect-qt-libdir.patch
Patch1:		italc-1.0.9-fix-setup-build.patch
Patch2:		italc-1.0.9-fix-zh_cn_filename.patch
BuildRequires:	qt4-devel
BuildRequires:  zlib-devel
BuildRequires:  jpeg-devel
BuildRequires:  qt4-linguist
BuildRequires:  libxtst-devel
BuildRequires:  openssl-devel

%description
iTALC is a use- and powerful didactical tool for teachers. It lets you
view and control other computers in your network in several ways. It
supports Linux and Windows 2000/XP/Vista and it even can be used
transparently in mixed environments!

iTALC has been designed for usage in school. Therefore it offers a lot
of possibilities to teachers, such as
    * see what's going on in computer-labs by using overview mode and
      make snapshots
    * remote-control computers to support and help other people
    * show a demo (either in fullscreen or in a window) - the teacher's
      screen is shown on all student's computers in realtime
    * lock workstations for moving undivided attention to teacher
    * send text-messages to students
    * powering on/off and rebooting computers per remote
    * remote logon and logoff and remote execution of arbitrary
      commands/scripts
    * home-schooling - iTALC's network-technology is not restricted to
      a subnet and therefore students at home can join lessons via
      VPN-connections just by installing iTALC client

Furthermore iTALC is optimized for usage on multi-core systems (by
making heavy use of threads). No matter how many cores you have, iTALC
can make use of all of them. 

%package client
Summary:	ITALC client
Group:		Networking/Remote access

%description client
iTALC is a use- and powerful didactical tool for teachers. It lets you
view and control other computers in your network in several ways. It
supports Linux and Windows 2000/XP/Vista and it even can be used
transparently in mixed environments!

iTALC has been designed for usage in school. Therefore it offers a lot
of possibilities to teachers, such as
    * see what's going on in computer-labs by using overview mode and
      make snapshots
    * remote-control computers to support and help other people
    * show a demo (either in fullscreen or in a window) - the teacher's
      screen is shown on all student's computers in realtime
    * lock workstations for moving undivided attention to teacher
    * send text-messages to students
    * powering on/off and rebooting computers per remote
    * remote logon and logoff and remote execution of arbitrary
      commands/scripts
    * home-schooling - iTALC's network-technology is not restricted to
      a subnet and therefore students at home can join lessons via
      VPN-connections just by installing iTALC client

Furthermore iTALC is optimized for usage on multi-core systems (by
making heavy use of threads). No matter how many cores you have, iTALC
can make use of all of them.

This package is the client that is run on each client on the network.

%package master
Summary:	Intelligent Teaching And Learning with Computers
Group:		Networking/Remote access
Requires:	%{libname} = %{version}-%{release}
Requires:	%{name}-client = %{version}

%description master
iTALC is a use- and powerful didactical tool for teachers. It lets you
view and control other computers in your network in several ways. It
supports Linux and Windows 2000/XP/Vista and it even can be used
transparently in mixed environments!

iTALC has been designed for usage in school. Therefore it offers a lot
of possibilities to teachers, such as
    * see what's going on in computer-labs by using overview mode and
      make snapshots
    * remote-control computers to support and help other people
    * show a demo (either in fullscreen or in a window) - the teacher's
      screen is shown on all student's computers in realtime
    * lock workstations for moving undivided attention to teacher
    * send text-messages to students
    * powering on/off and rebooting computers per remote
    * remote logon and logoff and remote execution of arbitrary
      commands/scripts
    * home-schooling - iTALC's network-technology is not restricted to
      a subnet and therefore students at home can join lessons via
      VPN-connections just by installing iTALC client

Furthermore iTALC is optimized for usage on multi-core systems (by
making heavy use of threads). No matter how many cores you have, iTALC
can make use of all of them.

%post master
if [ ! -d /etc/italc/keys ] ; then
	ica -role teacher -createkeypair ;
fi

%package -n %libname
Summary:	Library used by ITALC
Group:		Networking/Remote access

%description -n %libname
iTALC is a use- and powerful didactical tool for teachers. It lets you
view and control other computers in your network in several ways. It
supports Linux and Windows 2000/XP/Vista and it even can be used
transparently in mixed environments!

This is a library used by %{name}-master and %{name}-client.

%prep
%setup -q
%patch0 -p0
%patch1 -p0
%patch2 -p0 -b .zh

(
mv lib/resources/zh.qm lib/resources/zh_cn.qm
mv ima/resources/qt_zh_CN.qm ima/resources/qt_zh_cn.qm
mv ima/resources/zh.qm ima/resources/zh_cn.qm
mv ica/resources/zh.qm ica/resources/zh_cn.qm
)

%build
%configure2_5x --with-qtdir=%{qt4dir} --disable-static
%make
%{__chmod} -x AUTHORS COPYING ChangeLog INSTALL README TODO

%install
rm -fr %buildroot
%makeinstall_std docdir=/tmp/doc
%{__rm} -Rf %{buildroot}/tmp/doc

%files client
%doc AUTHORS COPYING ChangeLog INSTALL README TODO
%{_bindir}/ica
%{_mandir}/man1/ica.1.*

%files master
%doc AUTHORS COPYING ChangeLog INSTALL README TODO
%{_bindir}/%{name}
%{_mandir}/man1/%{name}.1.*
%{_datadir}/icons/%{name}.png
%{_datadir}/menu/%{name}
%{_datadir}/pixmaps/%{name}.xpm
%{_datadir}/applications/%{name}.desktop

%files -n %libname
%doc AUTHORS COPYING ChangeLog INSTALL README TODO
%{_libdir}/%name
