%define libname %mklibname italc
%define ver 1.0.9.1.6
%define italcgrp italc

Name:		italc
Version:	1.0.13
Release:	3
Summary:	Intelligent Teaching And Learning with Computers
License:	GPLv2+
Group:		Networking/Remote access
URL:		http://italc.sourceforge.net/
Source0:	%{name}-%{version}.tar.bz2
Source2:	italc-start_ica
Source3:	italc.sysconfig
Source5:	ica-autostart.desktop
Source6:	italc-launcher
Patch0:		italc-1.0.11-detect-qt-libdir.patch
Patch1:		italc-1.0.13-mwindows.patch
Patch2:		italc-desktop-launcher-change.patch
Patch4:		italc-1.0.11-fix-str-fmt.patch
Patch12:	%{name}-%{ver}-ubuntu-username.patch
Patch13:	%{name}-%{ver}-ubuntu-fixdemo.patch
Patch14:	%{name}-%{ver}-ubuntu-fix-ftbfs.patch
Patch15:	%{name}-%{ver}-ubuntu-ica-auto-respawn.patch
Patch16:	%{name}-%{ver}-ubuntu-fix-lock.patch
Patch40:	%{name}-%{ver}-alt-kde4-shutdown.patch
BuildRequires:	qt4-devel
BuildRequires:	zlib-devel
BuildRequires:	jpeg-devel
BuildRequires:	qt4-linguist
BuildRequires:	libxtst-devel
BuildRequires:	pkgconfig(openssl)
BuildRequires:	pkgconfig(xi)

%description
iTALC is a use- and powerful didactical tool for teachers. It lets you view
and control other computers in your network in several ways. It supports Linux
and Windows 2000/XP/Vista.

Features:

* see what's going on in computer-labs by using overview mode and
  make snapshots
* remote-control computers to support and help other people
* show a demo (either in fullscreen or in a window) - the teacher's screen
  is shown on all student's computers in realtime
* lock workstations for moving undivided attention to teacher
* send text-messages to students
* powering on/off and rebooting computers per remote
* remote logon and logoff and remote execution of arbitrary commands/scripts
* home-schooling - iTALC's network-technology is not restricted to a subnet
  and therefore students at home can join lessons via VPN-connections just
  by installing iTALC client

Furthermore iTALC is optimized for usage on multi-core systems (by making
heavy use of threads). No matter how many cores you have, iTALC can make use
of all of them.

%package client
Summary:	Software for iTALC-clients
Group:		Networking/Remote access
#Requires: italc = %version-%release

%description client
This package contains the software, needed by iTALC-clients.

See /usr/share/italc/doc/INSTALL for details on how to install and setup iTALC
in your network.

%package master
Summary:	iTALC master software
Group:		Networking/Remote access
Requires:	%{libname} = %{version}-%{release}
Requires:	%{name}-client = %{version}
Requires(post):	%{name}-client = %{version}

%description master
This package contains the actual master-software for accessing clients.

See /usr/share/italc/doc/INSTALL for details on how to install and setup iTALC
in your network.

%package -n %{libname}
Summary:	Library used by ITALC
Group:		Networking/Remote access

%description -n %{libname}
iTALC is a use- and powerful didactical tool for teachers. It lets you
view and control other computers in your network in several ways. It
supports Linux and Windows 2000/XP/Vista and it even can be used
transparently in mixed environments!

This is a library used by %{name}-master and %{name}-client.

%prep
%setup -q

%patch0 -p0
%patch1 -p1
%patch2 -p0
%patch4 -p0
%patch12 -p1
%patch13 -p1
%patch14 -p1
%patch15 -p1
%patch16 -p1
%patch40 -p1

%build
autoreconf -fi
./configure --with-qtdir=%{qt4dir} --disable-static --disable-pixmaps-files --disable-menu-files --prefix=/usr --libdir=/usr/%{_lib}

%make
chmod -x AUTHORS COPYING ChangeLog INSTALL README TODO

%install
mkdir -p %{buildroot}%{_defaultdocdir}/%{name}
%makeinstall_std
# create the directories containing the auth-keys
mkdir -p %{buildroot}%{_sysconfdir}/italc/keys/{private,public}/{teacher,admin,supporter,other}
# create pseudo key files so RPM can own them (ghost files)
for role in admin supporter teacher; do
	touch %{buildroot}%{_sysconfdir}/italc/keys/{private,public}/$role/key
done
# create the initial config
mkdir -p "%{buildroot}/%{_sysconfdir}/settings/iTALC Solutions"
cat > "%{buildroot}/%{_sysconfdir}/settings/iTALC Solutions/iTALC.conf" << EOF
[keypathsprivate]
admin=%{_sysconfdir}/italc/keys/private/admin/key
supporter=%{_sysconfdir}/italc/keys/private/supporter/key
teacher=%{_sysconfdir}/italc/keys/private/teacher/key

[keypathspublic]
admin=%{_sysconfdir}/italc/keys/public/admin/key
supporter=%{_sysconfdir}/italc/keys/public/supporter/key
teacher=%{_sysconfdir}/italc/keys/public/teacher/key
EOF
# install start script for ica client
install -D -m755 %{SOURCE2} %{buildroot}/%{_bindir}/start-ica
install -D -m644 %{SOURCE5} %{buildroot}/%{_sysconfdir}/xdg/autostart/ica-autostart.desktop
install -D -m755 %{SOURCE6} %{buildroot}/%{_bindir}/italc-launcher
# icon for the desktop file
install -Dm644 ima/data/italc.png %{buildroot}/%{_datadir}/pixmaps/italc.png
#
# Distribution specific
#
# configuration for ica

install -D -m644 %{SOURCE3} %{buildroot}/%{_sysconfdir}/sysconfig/ica

# as italc's configure doesn't understand docdir atm, create symlinks
#pushd %{buildroot}/%_datadir/%name/doc
#for i in *; do
# ln -s %_datadir/%name/doc/$i %{buildroot}%_defaultdocdir/%name/
#done
#popd

rm -rf %{buildroot}/usr/local

%pre client
%{_sbindir}/groupadd -r -f %{italkgrp} 2>/dev/null ||:

%post client
if
    getent group %{italkgrp} >/dev/null
then
    : OK group %{italkgrp} already present
else
    groupadd -r %{italkgrp} 2>/dev/null || :
fi

%post master
if
    getent group %{italkgrp} >/dev/null
then
    : OK group %{italkgrp} already present
else
    groupadd -r %{italkgrp} 2>/dev/null || :
fi

# dont run scripts on update
if [ ${1:-0} -lt 2 ]; then
  for role in admin supporter teacher; do
	if [ ! -f "%{_sysconfdir}/italc/keys/private/$role/key" ]; then
		/usr/bin/ica -role $role -createkeypair 1>/dev/null
		chgrp %{italkgrp} "%{_sysconfdir}/italc/keys/private/$role/key"
		chmod 0440 "%{_sysconfdir}/italc/keys/private/$role/key"
	fi
  done
fi

%files client
%doc %{_mandir}/man1/ica*
%{_bindir}/ica
%{_bindir}/start-ica
%config %{_sysconfdir}/xdg/autostart/ica-autostart.desktop
%config(noreplace) %{_sysconfdir}/sysconfig/ica
%doc AUTHORS COPYING ChangeLog INSTALL README TODO
%{_datadir}/%{name}/doc/

%dir %{_sysconfdir}/settings
%dir "%{_sysconfdir}/settings/iTALC Solutions"
%config(missingok,noreplace) "%{_sysconfdir}/settings/iTALC Solutions/iTALC.conf"

%dir %{_sysconfdir}/italc/keys/private
%defattr(0440,root,%{italkgrp},0750)
%dir %{_sysconfdir}/italc/keys/private/teacher
%dir %{_sysconfdir}/italc/keys/private/admin
%dir %{_sysconfdir}/italc/keys/private/supporter
%dir %{_sysconfdir}/italc/keys/private/other
%ghost %attr(0440,root,%{italkgrp}) %config(noreplace) %{_sysconfdir}/italc/keys/private/teacher/key
%ghost %attr(0440,root,%{italkgrp}) %config(noreplace) %{_sysconfdir}/italc/keys/private/admin/key
%ghost %attr(0440,root,%{italkgrp}) %config(noreplace) %{_sysconfdir}/italc/keys/private/supporter/key
#%ghost %attr(0440,root,%{italkgrp}) %config(noreplace) %{_sysconfdir}/italc/keys/private/other/key
%ghost %attr(0444,root,%{italkgrp}) %config(noreplace) %{_sysconfdir}/italc/keys/public/teacher/key
%ghost %attr(0444,root,%{italkgrp}) %config(noreplace) %{_sysconfdir}/italc/keys/public/admin/key
%ghost %attr(0444,root,%{italkgrp}) %config(noreplace) %{_sysconfdir}/italc/keys/public/supporter/key
#%ghost %attr(0444,root,%{italkgrp}) %config(noreplace) %{_sysconfdir}/italc/keys/public/other/key

%files master
%doc AUTHORS COPYING ChangeLog INSTALL README TODO
%{_bindir}/italc
%{_bindir}/italc-launcher
%doc %{_mandir}/man1/italc.*
%{_datadir}/applications/italc.desktop
%{_datadir}/icons/italc.*
%{_datadir}/pixmaps/*
%{_datadir}/menu/%{name}

%files -n %{libname}
%doc AUTHORS COPYING ChangeLog INSTALL README TODO
%{_libdir}/%{name}

