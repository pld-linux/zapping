#
# Conditional build:
%bcond_without	lirc	# without LIRC support
#
Summary:	A TV viewer for GNOME2
Summary(pl):	Program do ogl±dania telewizji dla GNOME2
Name:		zapping
Version:	0.7.0
%define	ver	0.7
%define	bver	cvs6
Release:	1.%{bver}.1
License:	GPL
Group:		X11/Applications/Multimedia
#Source0:	%{name}-%{version}-%{snap}.tar.bz2
Source0:	http://dl.sourceforge.net/zapping/%{name}-%{ver}%{bver}.tar.bz2
# Source0-md5:	cdedc0088c70f4520c37066ec05cb996
Patch0:		%{name}-suid.patch
Patch1:		%{name}-libdir.patch
Patch2:		%{name}-desktopfile.patch
Patch3:		%{name}-deprecated.patch
URL:		http://zapping.sourceforge.net/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	artsc-devel
BuildRequires:	intltool
BuildRequires:	libglade2-devel >= 2.0.1
BuildRequires:	libgnomeui-devel >= 2.4.0.1
BuildRequires:	libjpeg-devel
BuildRequires:	libpng-devel
BuildRequires:	mp1e-devel
%{?with_lirc:BuildRequires:	lirc-devel}
BuildRequires:	libtool
BuildRequires:	libxml2-devel
BuildRequires:	python-devel
%ifarch %{ix86}
BuildRequires:	rte-devel >= 0.5
%endif
BuildRequires:	zvbi-devel >= 0.2.3
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_plugindir	%{_libdir}/zapping/plugins

%description
GNOME (GNU Network Object Model Environment) is a user-friendly set of
applications and desktop tools to be used in conjunction with a window
manager for the X Window System. GNOME is similar in purpose and scope
to CDE and KDE, but GNOME is based completely on free software.

This is a TV viewer for the GNOME desktop. It has all the needed
features, plus extensibility through a plugin system.

%description -l pl
Zapping to program do ogl±dania telewizji dla ¶rodowiska GNOME. Ma
wszystkie potrzebne funkcje oraz oferuje mo¿liwo¶æ rozszerzania
funkcjonalno¶ci przez system wtyczek (pluginów).

%package alirc-plugin
Summary:	Another Zapping plugin for infrared control
Summary(pl):	Kolejna wtyczka Zappingu do kontroli podczerwieni±
Group:		X11/Applications/Multimedia
Requires:	%{name} = %{version}-%{release}
Requires:	lirc
Obsoletes:	zapping-lirc-plugin

%description alirc-plugin
This package allows you to control Zapping with a LIRC-supported
remote control.

%description alirc-plugin -l pl
Ten pakiet pozwala na obs³ugê Zappingu pilotem zdalnego sterowania
obs³ugiwanym przez LIRC.

%package mpeg-plugin
Summary:	Zapping plugin that saves video in MPEG format
Summary(pl):	Wtyczka Zappingu do zapisu obrazu w formacie MPEG
Group:		X11/Applications/Multimedia
Requires:	%{name} = %{version}-%{release}

%description mpeg-plugin
This package allows you to save video from TV in MPEG format.

%description mpeg-plugin -l pl
Ten pakiet pozwala na zapis obrazu z TV w formacie MPEG.

%package screenshot-plugin
Summary:	Zapping plugin for taking screenshots
Summary(pl):	Wtyczka Zappinga do robienia zrzutów ekranu
Group:		X11/Applications/Multimedia
Requires:	%{name} = %{version}-%{release}

%description screenshot-plugin
You can use this plugin to take screenshots of what you are actually
watching in TV. It will save the screenshots in JPEG format.

%description screenshot-plugin -l pl
Ta wtyczka pozwala na zrzucanie aktualnie ogl±danego obrazu
telewizyjnego do pliku JPEG.

%prep
%setup -q -n %{name}-%{ver}%{bver}
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

# workaround for missing file
touch common/structpr_gen.pl common/fprintf*.h

%{__perl} -pi -e "s@lib/python@%{_lib}/python@" acinclude.m4

%build
glib-gettextize --copy --force
intltoolize --copy --force
%{__libtoolize}
%{__aclocal}
%{__autoheader}
%{__automake}
%{__autoconf}
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sbindir},%{_desktopdir},%{_pixmapsdir}}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	Multimediadir=%{_desktopdir}

ln -sf zapping $RPM_BUILD_ROOT%{_bindir}/zapzilla

cp -f plugins/alirc/README{.alirc,}
#ln -s %{_pixmapsdir}/zapping/gnome-television.png $RPM_BUILD_ROOT%{_pixmapsdir}/gnome-television.png

# Remove useless *.la files
rm -f $RPM_BUILD_ROOT%{_libdir}/%{name}/plugins/*.la

%find_lang %{name} --with-gnome

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /usr/bin/scrollkeeper
%postun	-p /usr/bin/scrollkeeper

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS THANKS NEWS README* TODO BUGS
%attr(755,root,root) %{_bindir}/zapping
%attr(755,root,root) %{_bindir}/zapzilla
%attr(755,root,root) %{_bindir}/zapping_fix_overlay
%attr(4755,root,root) %{_sbindir}/zapping_setup_fb
%dir %{_libdir}/zapping
%dir %{_plugindir}
%{_pixmapsdir}/*
%{_datadir}/zapping
%{_omf_dest_dir}/zapping
%{_desktopdir}/zapping.desktop
%{_mandir}/man?/*

%if %{with lirc}
%files alirc-plugin
%defattr(644,root,root,755)
%doc plugins/alirc/README
%attr(755,root,root) %{_plugindir}/libalirc.zapping.so*
%endif

%files mpeg-plugin
%defattr(644,root,root,755)
%attr(755,root,root) %{_plugindir}/libmpeg.zapping.so*

%files screenshot-plugin
%defattr(644,root,root,755)
%attr(755,root,root) %{_plugindir}/libscreenshot.zapping.so*
