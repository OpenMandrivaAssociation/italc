%define name italc
%define libname %mklibname italc
%define version 1.0.4
%define release %mkrel 1

Name:		%name
Version:	%version
Release:	%release
Summary:	iTALC - Intelligent Teaching And Learning with Computers
License:	GPL
Group:		Networking/Remote access
URL:		http://italc.sourceforge.net/
Source:		%{name}-%{version}.tar.bz2
BuildRequires:	qt4-devel
BuildRequires:  zlib-devel
BuildRequires:  jpeg-devel
BuildRequires:  qt4-linguist
BuildRequires:  libxtst-devel

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
Summary:	iTALC client
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
Summary:	iTALC - Intelligent Teaching And Learning with Computers
Group:		Networking/Remote access
Requires:	%{libname} = %{version}-%{release}
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

%package -n %libname
Summary:	iTALC - Intelligent Teaching And Learning with Computers
Group:		Networking/Remote access

%description -n %libname
iTALC is a use- and powerful didactical tool for teachers. It lets you
view and control other computers in your network in several ways. It
supports Linux and Windows 2000/XP/Vista and it even can be used
transparently in mixed environments!

This is a library used by %{name}-master and %{name}-client.

%prep
%setup -q


%build

%configure --with-qtdir=/usr/lib/qt4
%make
%{__chmod} -x AUTHORS COPYING ChangeLog INSTALL README TODO

%install
%makeinstall docdir=%{buildroot}/tmp/doc
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
%{_libdir}/lib%{name}_core.so
