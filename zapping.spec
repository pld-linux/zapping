%define  prefix  /usr
%define  ver 0.5.2

Name: zapping
Version: %{ver}
Release: 1
Summary: a TV viewer for Gnome
Copyright: GPL
Group: Applications/Multimedia
Source: http://download.sourceforge.net/zapping/zapping-%{ver}.tar.gz
URL: http://zapping.sourceforge.net
Packager: I�aki Garc�a Etxebarria <garetxe@users.sourceforge.net>
Buildroot: /var/tmp/%{name}-root
BuildPrereq: libglade-devel libxml-devel
PreReq: /sbin/install-info
Docdir: 	%{prefix}/doc

Requires: gtk+ >= 1.2.6
Requires: gnome-libs >= 1.0.40
Requires: libxml >= 1.4.0
Requires: libglade >= 0.9

%description
GNOME (GNU Network Object Model Environment) is a user-friendly set of
applications and desktop tools to be used in conjunction with a window
manager for the X Window System.  GNOME is similar in purpose and scope
to CDE and KDE, but GNOME is based completely on free software.

This is a TV viewer for the GNOME desktop. It has all the needed
features, plus extensibility through a plugin system.

%prep
%setup -q

%build
./configure --prefix %prefix
make

%install
[ -n "$RPM_BUILD_ROOT" -a "$RPM_BUILD_ROOT" != / ] && rm -rf $RPM_BUILD_ROOT

make prefix=$RPM_BUILD_ROOT%{prefix} install

%clean
[ -n "$RPM_BUILD_ROOT" -a "$RPM_BUILD_ROOT" != / ] && rm -rf $RPM_BUILD_ROOT

%files

%defattr (4555, root, root)
%{prefix}/bin/zapping_setup_fb

%defattr (0555, root, root)
%{prefix}/bin/zapping
%{prefix}/share/zapping/plugins/*.zapping.so
%{prefix}/share/zapping/plugins/*.zapping.so.0.0.0

%defattr (0444, root, root, 0555)
%{prefix}/share/zapping/*.glade
%{prefix}/share/gnome/help/zapping/C/*.jpeg
%{prefix}/share/gnome/help/zapping/C/*.html
%{prefix}/share/gnome/help/zapping/C/*.dat
%{prefix}/share/pixmaps/zapping/*
%{prefix}/share/gnome/apps/Multimedia/zapping.desktop
%{prefix}/share/locale/*/*/*

%defattr (0444, root, root, 0555)
%doc AUTHORS THANKS ChangeLog README README.plugins COPYING TODO BUGS po/zapping.pot

%changelog
* Mon Jun 19 2000 I�aki Garc�a Etxebarria <garetxe@users.sourceforge.net>
	- Added the desktop entry and removed the specified --datadir

* Mon Jun 12 2000 I�aki Garc�a Etxebarria <garetxe@users.sourceforge.net>
	- Fixed, it didn't include the translations properly.

* Thu Jun 06 2000 I�aki Garc�a Etxebarria <garetxe@users.sourceforge.net>
	- Created, it works fine.
