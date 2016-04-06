%define libname %mklibname italc
%define italcgrp italc

Name:		italc
Version:	2.0.2
Release:	1
Summary:	Intelligent Teaching And Learning with Computers
License:	GPLv2+
Group:		Networking/Remote access
URL:		http://italc.sourceforge.net/
Source0:	%{name}-%{version}.tar.bz2
Source1:	italc.desktop
Source3:	ica-autostart.desktop
Source4:	ica-start
Patch0:		italc-2.0.0-mdv-fix_cmake.diff
Patch1:		harbour-3.2.0-mga-minilzo-2.8.patch
Patch2:		italc-2.0.2-mga-globalconfig.patch
BuildRequires:	cmake
BuildRequires:	qt4-devel
BuildRequires:	pkgconfig(xtst)
BuildRequires:	zlib-devel
BuildRequires:	jpeg-devel
BuildRequires:	qt4-linguist
BuildRequires:	pkgconfig(openssl)
BuildRequires:	pkgconfig(xi)
BuildRequires:	pam-devel
BuildRequires:	desktop-file-utils
BuildRequires:	java-devel

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
%patch0 -p1
pushd ica/x11/common
%patch1 -p5 -b .lzo
popd
%patch2 -p1

%build
%cmake
%make

%install
%makeinstall_std -C build

# create the directories containing the auth-keys
mkdir -p %{buildroot}%{_sysconfdir}/italc/keys/{private,public}/{teacher,admin,supporter,other}
# create pseudo key files so RPM can own them (ghost files)
for role in admin supporter teacher; do
	touch %{buildroot}%{_sysconfdir}/italc/keys/{private,public}/$role/key
done

# create the initial config
mkdir -p "%{buildroot}%{_sysconfdir}/iTALC Solutions"
cat > "%{buildroot}%{_sysconfdir}/iTALC Solutions/iTALC.conf" << EOF
[Authentication]
LogonAuthenticationEnabled=0
KeyAuthenticationEnabled=1
PublicKeyBaseDir=%{_sysconfdir}/%{name}/keys/public
PrivateKeyBaseDir=%{_sysconfdir}/%{name}/keys/private
LogonGroups=
PermissionRequiredWithKeyAuthentication=0
PermissionRequiredWithLogonAuthentication=0
SameUserConfirmationDisabled=0

[DemoServer]
Backend=0
Multithreaded=1

[Logging]
LimittedLogFileSize=0
LogFileDirectory=\$TEMP
LogFileSizeLimit=-1
LogLevel=4
LogToStdErr=1
LogToWindowsEventLog=0

[Network]
CoreServerPort=11100
DemoServerPort=11400
FirewallExceptionEnabled=1
HttpServerEnabled=0
HttpServerPort=5800

[Service]
Arguments=
Autostart=1
HideTrayIcon=0

[VNC]
CaptureLayeredWindows=0
LowAccuracy=1
PollFullScreen=1

[Paths]
PersonalConfiguration=\$APPDATA/PersonalConfig.xml
GlobalConfiguration=\$APPDATA/GlobalConfig.xml
SnapshotDirectory=\$APPDATA/Snapshots

EOF

# create GlobalConfig.xml
mkdir -p "%{buildroot}%{_sysconfdir}/skel/.%{name}"
cat > "%{buildroot}%{_sysconfdir}/skel/.%{name}/GlobalConfig.xml" << EOF
<?xml version="1.0"?>
<!DOCTYPE %{name}-config-file>
<globalclientconfig version="%{version}">
  <body/>
</globalclientconfig>
EOF

desktop-file-install --dir=%{buildroot}%{_datadir}/applications/ %{SOURCE1}
install -Dm 0644 ima/data/%{name}.png %{buildroot}%{_datadir}/icons/%{name}.png

install -dm 755 %{buildroot}%{_sysconfdir}/xdg/autostart
install -m 0644 %{SOURCE3} %{buildroot}%{_sysconfdir}/xdg/autostart/
install -dm 755 %{buildroot}%{_bindir}
install -m 755 %{SOURCE4} %{buildroot}%{_bindir}/

%pre client
%{_sbindir}/groupadd -r -f %{italcgrp} 2>/dev/null ||:

%post client
if
    getent group %{italcgrp} >/dev/null
then
    : OK group %{italcgrp} already present
else
    groupadd -r %{italcgrp} 2>/dev/null || :
fi

%post master
if
    getent group %{italcgrp} >/dev/null
then
    : OK group %{italcgrp} already present
else
    groupadd -r %{italcgrp} 2>/dev/null || :
fi

# dont run scripts on update
if [ ${1:-0} -lt 2 ]; then
# the imc command tries to start its Qt GUI if $DISPLAY is set...
  if [ ! -z ${DISPLAY+x} ]; then
   remembered_DISPLAY=$DISPLAY
  fi
  unset DISPLAY

  for role in admin supporter teacher; do
	if [ ! -f "%{_sysconfdir}/italc/keys/private/$role/key" ]; then
		/usr/bin/imc -role $role -createkeypair 1>/dev/null
		chgrp %{italcgrp} "%{_sysconfdir}/italc/keys/private/$role/key"
		chmod 0440 "%{_sysconfdir}/italc/keys/private/$role/key"
	fi
  done
  if [ ! -z "${remembered_DISPLAY+x}" ]; then
    DISPLAY=$remembered_DISPLAY
  fi
fi

%files client
%{_bindir}/ica
%{_bindir}/ica-start
%{_bindir}/italc_auth_helper
%config %{_sysconfdir}/xdg/autostart/ica-autostart.desktop
%doc AUTHORS COPYING ChangeLog INSTALL README TODO

%dir "%{_sysconfdir}/iTALC Solutions"
%config(missingok,noreplace) "%{_sysconfdir}/iTALC Solutions/iTALC.conf"

%dir %{_sysconfdir}/italc/keys/private
%defattr(0440,root,%{italcgrp},0750)
%dir %{_sysconfdir}/italc/keys/private/teacher
%dir %{_sysconfdir}/italc/keys/private/admin
%dir %{_sysconfdir}/italc/keys/private/supporter
%dir %{_sysconfdir}/italc/keys/private/other
%ghost %attr(0440,root,%{italcgrp}) %config(noreplace) %{_sysconfdir}/italc/keys/private/teacher/key
%ghost %attr(0440,root,%{italcgrp}) %config(noreplace) %{_sysconfdir}/italc/keys/private/admin/key
%ghost %attr(0440,root,%{italcgrp}) %config(noreplace) %{_sysconfdir}/italc/keys/private/supporter/key
#%ghost %attr(0440,root,%{italcgrp}) %config(noreplace) %{_sysconfdir}/italc/keys/private/other/key
%ghost %attr(0444,root,%{italcgrp}) %config(noreplace) %{_sysconfdir}/italc/keys/public/teacher/key
%ghost %attr(0444,root,%{italcgrp}) %config(noreplace) %{_sysconfdir}/italc/keys/public/admin/key
%ghost %attr(0444,root,%{italcgrp}) %config(noreplace) %{_sysconfdir}/italc/keys/public/supporter/key
#%ghost %attr(0444,root,%{italcgrp}) %config(noreplace) %{_sysconfdir}/italc/keys/public/other/key

%files master
%doc AUTHORS COPYING ChangeLog INSTALL README TODO
%{_bindir}/italc
%{_bindir}/imc
%{_datadir}/applications/italc.desktop
%{_datadir}/icons/italc.*
%{_datadir}/%{name}/JavaViewer/VncViewer.jar
%{_datadir}/%{name}/JavaViewer/index.vnc
%config %{_sysconfdir}/skel/.%{name}/GlobalConfig.xml

%files -n %{libname}
%doc AUTHORS COPYING ChangeLog INSTALL README TODO
%{_libdir}/libItalcCore.so

