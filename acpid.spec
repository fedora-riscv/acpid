Summary: ACPI Event Daemon
Name: acpid
Version: 1.0.2
Release: 6
Copyright: GPL
Group: System Environment/Daemons
Source: http://prdownloads.sourceforge.net/acpid/acpid-%{version}.tar.gz
Source2: acpid.init
Patch: acpid-1.0.1-pm1.diff
Patch2: acpid-1.0.1-conf.patch
BuildRoot: %{_tmppath}/%{name}-%{version}-root
ExclusiveArch: ia64 x86_64 i386
URL: http://acpid.sourceforge.net/
Prereq: /sbin/chkconfig, /sbin/service


%description
acpid is a daemon that dispatches ACPI events to user-space programs.


%prep
%setup
%patch -p1
%patch2 -p1

%build
make


%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT
make install INSTPREFIX=$RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT/etc/acpi/events
mkdir -p $RPM_BUILD_ROOT/etc/acpi/actions
chmod 755 $RPM_BUILD_ROOT/etc/acpi/events
install -m 644 samples/sample.conf $RPM_BUILD_ROOT/etc/acpi/events

mkdir -p $RPM_BUILD_ROOT/var/log
touch $RPM_BUILD_ROOT/var/log/acpid
chmod 640 $RPM_BUILD_ROOT/var/log/acpid

mkdir -p $RPM_BUILD_ROOT/etc/rc.d/init.d
install -m 755 %{SOURCE2} $RPM_BUILD_ROOT/etc/rc.d/init.d/acpid
chmod 755 $RPM_BUILD_ROOT/etc/rc.d/init.d/acpid


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root)
%dir /etc/acpi
%dir /etc/acpi/events
%dir /etc/acpi/actions
%config %attr(0644,root,root) /etc/acpi/events/sample.conf
/var/log/acpid
/usr/sbin/acpid
%attr(0755,root,root) /etc/rc.d/init.d/acpid
/usr/share/man/man8/acpid.8.gz


%post
/sbin/chkconfig --add acpid

%preun
if [ "$1" = "0" ]; then
	service acpid stop >/dev/null 2>&1
	/sbin/chkconfig --del acpid
fi

%changelog
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

