Summary: ACPI Event Daemon
Name: acpid
Version: 1.0.6
Release: 3%{?dist}
License: GPL
Group: System Environment/Daemons
Source: http://prdownloads.sourceforge.net/acpid/acpid-%{version}.tar.gz
Source1: acpid.logrotate
Source2: acpid.init
Source3: acpid.video.conf
Source4: acpid.power.conf
Patch1: acpid-1.0.6-makefile.patch
Patch2: acpid-1.0.6-return.patch
Patch3: acpid-1.0.6-fd.patch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
ExclusiveArch: ia64 x86_64 %{ix86}
URL: http://acpid.sourceforge.net/
Requires(post): /sbin/chkconfig
Requires(preun): /sbin/chkconfig
Requires(preun): /sbin/service


%description
acpid is a daemon that dispatches ACPI events to user-space programs.


%prep
%setup -q
%patch1 -p1 -b .makefile
%patch2 -p1 -b .return
%patch3 -p1 -b .fd

%build
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT
make install INSTPREFIX=$RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/acpi/events
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/acpi/actions
chmod 755 $RPM_BUILD_ROOT%{_sysconfdir}/acpi/events
install -m 644 %{SOURCE3} $RPM_BUILD_ROOT%{_sysconfdir}/acpi/events/video.conf
install -m 644 %{SOURCE4} $RPM_BUILD_ROOT%{_sysconfdir}/acpi/events/power.conf

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d
install -m 644 %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d/acpid

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/rc.d/init.d
install -m 755 %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/rc.d/init.d/acpid


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root)
%doc COPYING README Changelog TODO
%dir %{_sysconfdir}/acpi
%dir %{_sysconfdir}/acpi/events
%dir %{_sysconfdir}/acpi/actions
%config(noreplace) %attr(0644,root,root) %{_sysconfdir}/acpi/events/video.conf
%config(noreplace) %attr(0644,root,root) %{_sysconfdir}/acpi/events/power.conf
%config(noreplace) %{_sysconfdir}/logrotate.d/acpid
%{_bindir}/acpi_listen
%{_sbindir}/acpid
%attr(0755,root,root) %{_sysconfdir}/rc.d/init.d/acpid
%{_mandir}/man8/acpid.8.gz
%{_mandir}/man8/acpi_listen.8.gz


%post
/sbin/chkconfig --add acpid

%preun
if [ "$1" = "0" ]; then
	/sbin/service acpid stop >/dev/null 2>&1
	/sbin/chkconfig --del acpid
fi

%postun
if [ "$1" -ge "1" ]; then
	/sbin/service acpid condrestart >/dev/null 2>&1
fi

%changelog
* Thu Oct 11 2007 Zdenek Prikryl <zprikryl@redhat.com> - 1.0.6-3.fc9
- Errors from init script are logged
- Resolves: #345611

* Wed Sep 26 2007 Zdenek Prikryl <zprikryl@redhat.com> - 1.0.6-2.fc8
- Fixed leak of a file descriptor
- Resolves: #304761

* Tue Aug 07 2007 Zdenek Prikryl <zprikryl@redhat.com> - 1.0.6-1.fc8
- Updated to version 1.0.6

* Wed Jul 25 2007 Zdenek Prikryl <zprikryl@redhat.com> - 1.0.4-8.fc8
- Fixed init script to comply with LSB standard
- Resolves: #237754

* Wed Feb 14 2007 Phil Knirsch <pknirsch@redhat.com> - 1.0.4-7.fc7
- Dropped /var/log/acpid ownership as per review (225237)

* Wed Feb 07 2007 Phil Knirsch <pknirsch@redhat.com> - 1.0.4-6.fc7
- Tons of specfile changes due to review (#225237)

* Tue Oct 10 2006 Phil Knirsch <pknirsch@redhat.com> - 1.0.4-5
- Made acpid a PIE binary (#210016)

* Thu Aug 24 2006 Phil Knirsch <pknirsch@redhat.com> - 1.0.4-4
- Made a better fix for the powerdown button which checks if g-p-m is running
- Don't install sample.conf anymore, not needed

* Thu Aug 10 2006 Phil Knirsch <pknirsch@redhat.com> - 1.0.4-3
- Disable the automatic shutdown -h via powerdown button by default due to
  conflicts with gnome-power-manager

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 1.0.4-2.1
- rebuild

* Wed Mar 01 2006 Phil Knirsch <pknirsch@redhat.com> - 1.0.4-2
- Added video.conf file to turn on DPMS when opening the laptop lid. Disabled
  by default.

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 1.0.4-1.2
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Wed Mar 16 2005 Bill Nottingham <notting@redhat.com> - 1.0.4-1
- update to 1.0.4

* Mon Aug  9 2004 Miloslav Trmac <mitr@redhat.com> - 1.0.3-2
- Update to 1.0.3 (fixes #128834)
- s/Copyright/License/
- Add logrotate config file (#110677, from Michal Jaegermann)
- Don't verify contents of /var/log/acpid (#125862)
- Use $RPM_OPT_FLAGS
- Fix and cleanup acpid-1.0.1-pm1.patch
- Add condrestart to %%postun

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Oct 22 2003  Bill Nottingham <notting@redhat.com> 1.0.2-5
- fix handling of sample.conf (#107160)
- mark for translations (#107459)

* Sun Oct 19 2003 Florian La Roche <Florian.LaRoche@redhat.de>
- add %%clean specfile target

* Wed Oct  1 2003  Bill Nottingham <notting@redhat.com> 1.0.2-3
- re-enable x86
- don't load the button module

* Thu Aug  7 2003  Bill Nottingham <notting@redhat.com> 1.0.2-2
- no x86 for now

* Mon Jul  7 2003  Bill Nottingham <notting@redhat.com> 1.0.2-1
- update to 1.0.2

* Wed Dec 11 2002  Bill Nottingham <notting@redhat.com> 1.0.1-4
- don't start if /proc/acpi/event isn't there

* Thu Nov 14 2002  Bill Nottingham <notting@redhat.com> 1.0.1-3
- build on more arches

* Mon Aug 26 2002  Bill Nottingham <notting@redhat.com> 1.0.1-2
- tweak default config to run shutdown -h now on a power button event

* Thu Aug 22 2002  Bill Nottingham <notting@redhat.com> 1.0.1-1
- initial build, bang on included specfile

* Fri Mar 15 2002  Tim Hockin <thockin@sun.com>
  - Updated RPM spec with patch from sun for chkconfig on/off
  - Add Changelog, make 'make rpm' use it.

* Wed Mar 13 2002  Tim Hockin <thockin@sun.com>
  - Fixed logging bug - not appending to log (O_APPEND needed)
  - Fix 'make install' to not need root access
  - Fix RPM spec to not need root

* Thu Sep 6 2001 Tim Hockin <thockin@sun.com>
  - 1.0.0

* Thu Aug 16 2001  Tim Hockin <thockin@sun.com>
  - Added commandline options to actions

* Wed Aug 15 2001  Tim Hockin <thockin@sun.com>
  - Added UNIX domain socket support
  - Changed /etc/acpid.d to /etc/acpid/events

* Mon Aug 13 2001  Tim Hockin <thockin@sun.com>
  - added changelog
  - 0.99.1-1

