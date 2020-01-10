%global	githash 38573e7d
Name:		memstomp
Version:	0.1.4
Release:	11%{?dist}
Summary:	Warns of memory argument overlaps to various functions
Group:		Development/Debuggers
# The entire source code is LGPLV3+ with the exception of backtrace-symbols.c which
# is GPLv2+ by way of being a hacked up old version of binutils's addr2line.
# backtrace-symbols.c is built into an independent .so to avoid license contamination
License:	LGPLv3+ and GPLv2+
URL:		git://fedorapeople.org/home/fedora/wcohen/public_git/memstomp
# The source for this package was pulled from upstream's vcs.  Use the
# following commands to generate the tarball:
# git glone git://fedorapeople.org/home/fedora/wcohen/public_git/memstomp
# cd memstomp
# git archive --prefix memstomp-0.1.4-38573e7d/ master | gzip > memstomp-0.1.4-3867e37d.tar.gz
Source0:	%{name}-%{version}-%{githash}.tar.gz
Requires:	util-linux
BuildRequires:	binutils-devel autoconf automake dejagnu

Patch0: memstomp-testsuite.patch
Patch1: memstomp-man.patch
Patch2: memstomp-rh961495.patch
Patch3: memstomp-rh962763.patch
Patch4: memstomp-quietmode.patch


%description 
memstomp is a simple program that can be used to identify
places in code which trigger undefined behavior due to
overlapping memory arguments to certain library calls.

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%prep
%setup -q -n %{name}-%{version}-%{githash}
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1


%build
autoreconf
%configure
make %{?_smp_mflags} CFLAGS+="-fno-strict-aliasing"
make -k check

%install
make install DESTDIR=$RPM_BUILD_ROOT

%files
%doc README LGPL3 GPL2 GPL3
%{_bindir}/memstomp
%{_libdir}/libmemstomp.so
%{_libdir}/libmemstomp-backtrace-symbols.so
%{_mandir}/man1/memstomp.1.gz

%changelog
* Fri Jan 24 2014 Daniel Mach <dmach@redhat.com> - 0.1.4-11
- Mass rebuild 2014-01-24

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 0.1.4-10
- Mass rebuild 2013-12-27

* Thu May 30 2013 Jeff Law <law@redhat.com> 0.1.4-9
- Add -q/--quiet options for quiet mode.

* Tue May 14 2013 Jeff Law <law@redhat.com> 0.1.4-8
- Link in libiberty too (#962763)

* Fri May 10 2013 Jeff Law <law@redhat.com> 0.1.4-7
- Improve man page (#961518)

* Thu May 09 2013 Jeff Law <law@redhat.com> 0.1.4-5
- Fix typo in initialization message (#961495)

* Fri Mar 15 2013 Jeff Law <law@redhat.com> 0.1.4-4
- Build tests with -fno-builtin

* Mon Mar 11 2013 Jeff Law <law@redhat.com> 0.1.4-4
- Add manpage
- Add initial testsuite

* Fri Feb 22 2013 Jeff Law <law@redhat.com> 0.1.4-3
- Change %%define to %%global for git hash
- Remove git hash from version # in changelog
- Build with -fno-strict-aliasing
- Fix minor spelling error in description

* Tue Feb 5 2013 Jeff Law <law@redhat.com> 0.1.4-2
- Remove commands/directives automatically handled by rpm
- Add comment on how to build the tarball
- Change Requires to reference package rather than file
- Add comments on licensing issues
- Add autoconf and automake to BuildRequires

* Tue Feb 5 2013 Jeff Law <law@redhat.com> 0.1.4-1
- Initial release
