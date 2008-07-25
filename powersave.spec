# 
# TODO:
# - fix bashizms in po/Makefile.am
# - do something with contrib scripts
#
Summary:	Powermanagment daemon
Summary(pl.UTF-8):	Demon zarządzania energią
Name:		powersave
Version:	0.15.20
Release:	1
Epoch:		0
License:	GPL
Group:		Daemons
Source0:	http://dl.sourceforge.net/powersave/%{name}-%{version}.tar.bz2
# Source0-md5:	8c14df7f3e477ac8c1d5b955f01dcfe6
Source1:	%{name}.init
Source2:	%{name}.sysconfig
Source3:	%{name}.logrotate
Patch0:		%{name}-ipw2200.patch
Patch1:		%{name}-lib.patch
URL:		http://forge.novell.com/modules/xfmod/project/?powersave
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	cpufrequtils-devel >= 0.4
BuildRequires:	dbus-glib-devel >= 0.71
BuildRequires:	hal-devel >= 0.5.7.1
BuildRequires:	liblazy-devel
BuildRequires:	libtool
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 1.228
BuildRequires:	sed >= 4.0
BuildRequires:	sysfsutils-devel >= 1.3.0-3
Requires(post,preun):	/sbin/chkconfig
Requires:	%{name}-libs = %{version}-%{release}
Requires:	acpid
Requires:	hal >= 0.5.7.1
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The powersave package provides global power management tasks.
It supports battery monitoring, userspace workarounds for proper
suspend/standby functionality and more.

%description -l pl.UTF-8
Paczka powersave świadczy globalne usługi zarządzania energią.
Wspiera monitorowanie stanu baterii, prowizorycznie rozwiązuje
problemy usypiania/wstrzymywania w przestrzeni użytkownika
i inne.

%package libs
Summary:	Powersave libraries
Summary(pl.UTF-8):	Biblioteki powersave
Group:		Libraries

%description libs
Powersave libraries.

%description libs -l pl.UTF-8
Biblioteki powersave.

%package devel
Summary:	Header files for powersave library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki powersave
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}
Requires:	cpufrequtils-devel >= 0.4
Requires:	dbus-devel >= 0.71
Requires:	hal-devel >= 0.5.7.1
Requires:	sysfsutils-devel >= 1.3.0-3

%description devel
This is the package containing header files for powersave
libraries.

%description devel -l pl.UTF-8
Paczka ta zawiera pliki nagłówkowe dla bibliotek powersave.

%package static
Summary:	Static powersave libraries
Summary(pl.UTF-8):	Biblioteki statyczne powersave
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static powersave library.

%description static -l pl.UTF-8
Statyczne biblioteki powersave.

%prep
%setup -q
#%patch0 -p1
%patch1 -p1
# translations disabled (terrible mess, see TODO)
sed -i -e 's|translations||' Makefile.am

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--with-gnome-bindir=%{_prefix} \
	--with-kde-bindir=%{_prefix}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/etc/{rc.d/init.d,sysconfig} \
	$RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/powersave
install %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/powersaved
install %{SOURCE3} $RPM_BUILD_ROOT/etc/logrotate.d/powersave

rm -rf $RPM_BUILD_ROOT/etc/init.d
rm $RPM_BUILD_ROOT{%{_libdir}/powersave/rcpowersaved,%{_sbindir}/rcpowersaved}


%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add %{name}
%service %{name} restart

%preun
if [ "$1" = "0" ]; then
	%service -q %{name} stop
	/sbin/chkconfig --del %{name}
fi

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README docs/README.*

%dir %{_sysconfdir}/powersave
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/powersave/*
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/powersaved
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/dbus-1/system.d/powersave.conf

%dir %{_sysconfdir}/acpi/events.ignore
%{_sysconfdir}/acpi/events.ignore/events.ignore

%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/logrotate.d/powersave
%attr(754,root,root) /etc/rc.d/init.d/powersave

%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_sbindir}/powersaved
%dir %{_libdir}/powersave
%dir %{_libdir}/powersave/scripts
%attr(755,root,root) %{_libdir}/powersave/do_*
%attr(755,root,root) %{_libdir}/powersave/myecho
%attr(755,root,root) %{_libdir}/powersave/powersave-notify
%attr(755,root,root) %{_libdir}/powersave/scripts/*
%attr(755,root,root) %{_libdir}/powersave/setDefaultTrippoints.sh
%attr(755,root,root) %{_libdir}/powersave/wttyhx
%{_mandir}/man8/powersave*.8*

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/*.so.*.*.*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/*.so
%{_libdir}/*.la
%{_includedir}/*.h
%{_pkgconfigdir}/*.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/*.a
