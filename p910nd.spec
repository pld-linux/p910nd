Summary:	Tiny non-spooling printer daemon.
Name:		p910nd
Version:	0.7
Release:	0.1
License:	GPL
Vendor:		Etherboot project
Group:		Networking/Daemons
Source0:	http://etherboot.sourceforge.net/p910nd/%{name}-%{version}.tar.bz2
#Source0-md5:	7bf752532d26c9106f8039db95df3a6b
Source1:	%{name}.init
Patch0:		%{name}-makefile.patch
URL:		http://etherboot.sourceforge.net/p910nd
BuildArch:	i386
#Icon:		.p910nd.xpm
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)


%description
Tiny non-spooling printer daemon for Linux hosts. Accepts data over a
TCP network connection from a spooling host. Useful on diskless X
terminals with local printer.

%prep
%setup -q 
%patch0 -p0

%build
%{__make} \
	CFLAGS="%{rpmcflags}" \
	CC="%{__cc}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/etc/rc.d/init.d,%{_sbindir},%{_libdir}/p910nd,%{_mandir}/man8}

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/p910nd
install p910nd $RPM_BUILD_ROOT%{_sbindir}
install *.pl $RPM_BUILD_ROOT%{_libdir}/p910nd/
install p910nd.8 $RPM_BUILD_ROOT%{_mandir}/man8/

%post
/sbin/chkconfig --add p910nd
if [ -f /var/lock/subsys/p910nd ]; then
	/etc/rc.d/init.d/p910nd restart >&2
else
	echo "Run \"/etc/rc.d/init.d/p910nd start\" to start p910nd daemon." >&2
fi

%preun
if [ "$1" = "0" ]; then
	if [ -f /var/lock/subsys/p910nd ]; then
		/etc/rc.d/init.d/p910nd stop >&2
	fi
	/sbin/chkconfig --del p910nd
fi

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(754,root,root) /etc/rc.d/init.d/p910nd
%attr(755,root,root) %{_sbindir}/p910nd
%{_libdir}/p910nd
%{_mandir}/man8/p910nd.8*
