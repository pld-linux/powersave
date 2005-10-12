Summary:	Powermanagment deamon
Summary(pl):	Demon zarz±dzania energi±
Name:		powersave
Version:	0.10.10
Release:	0.1
Epoch:		0
License:	GPL
Group:		Daemons
Source0:	http://forgeftp.novell.com/powersave/powersave/0.10.10-rc/%{name}-%{version}.tar.bz2
# Source0-md5:	170db6ee365dee08adbc5a8cb477bfc0
URL:		http://forge.novell.com/modules/xfmod/project/?powersave
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	hal-devel
BuildRequires:	libtool
BuildRequires:	rpmbuild(macros) >= 1.228
Requires(post,preun):	/sbin/chkconfig
Requires:	%{name}-libs = %{version}-%{release}
Requires:	acpid
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The powersave package provides global power management tasks.
It supports battery monitoring, userspace workarounds for proper
suspend/standby functionality and more.

%description -l pl
Paczka powersave ¶wiadczy globalne us³ugi zarz±dzania energi±.
Wspiera monitorowanie stanu baterii, prowizorycznie rozwi±zuje
problemy usypiania/wstrzymywania w przestrzeni u¿ytkownika
i inne.

%package libs
Summary:	Powersave libraries
Summary(pl):	Biblioteki powersave
Group:		Libraries

%description libs
Powersave libraries.

%description libs -l pl
Biblioteki powersave.

%package devel
Summary:	Header files for powersave library
Summary(pl):	Pliki nag³ówkowe biblioteki powersave
Group:		Development/Libraries

%description devel
This is the package containing header files for powersave
libraries.

%description devel -l pl
Paczka ta zawiera pliki nag³ówkowe dla bibliotek powersave.

%package static
Summary:	Static powersave libraries
Summary(pl):	Biblioteki statyczne powersave
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static powersave library.

%description static -l pl
Statyczne biblioteki powersave.

%prep
%setup -q
# translations disabled (terrible mess)
sed -i -e 's|translations||' Makefile.am

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

rm -rf $RPM_BUILD_ROOT%{_sysconfdir}/init.d

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
%doc BUGS README

%dir %{_sysconfdir}/sysconfig/powersave
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/sysconfig/powersave/*
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/dbus-1/system.d/powersave.conf

%dir %{_sysconfdir}/acpi/events.ignore
%{_sysconfdir}/acpi/events.ignore/events.ignore

#%%attr(754,root,root) /etc/rc.d/init.d/powersaved

%attr(755,root,root) %{_bindir}/*
%dir %{_libdir}/powersave
%dir %{_libdir}/powersave/scripts
%attr(755,root,root) %{_libdir}/powersave/scripts/*
%attr(755,root,root) %{_libdir}/powersave/do_*
%{_includedir}/*.h
%{_sbindir}/powersaved

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/*.so.*.*.*

%files devel
%defattr(644,root,root,755)
%{_includedir}/*.h
%{_libdir}/*.so
%{_libdir}/*.la

%files static
%defattr(644,root,root,755)
%{_libdir}/*.a
