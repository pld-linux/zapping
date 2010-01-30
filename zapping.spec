#
# Conditional build:
%bcond_without	lirc	# without LIRC support
#
Summary:	A TV viewer for GNOME2
Summary(pl.UTF-8):	Program do oglądania telewizji dla GNOME2
Name:		zapping
Version:	0.9.6
Release:	5
License:	GPL
Group:		X11/Applications/Multimedia
#Source0:	%{name}-%{version}-%{snap}.tar.bz2
Source0:	http://dl.sourceforge.net/zapping/%{name}-%{version}.tar.bz2
# Source0-md5:	8306775c6a11de4d72345b5eee970ea6
Patch0:		%{name}-suid.patch
Patch1:		%{name}-libdir.patch
Patch2:		%{name}-desktopfile.patch
Patch3:		%{name}-disable-altivec.patch
URL:		http://zapping.sourceforge.net/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	artsc-devel
BuildRequires:	intltool
BuildRequires:	libglade2-devel >= 1:2.5.1
BuildRequires:	libgnomeui-devel >= 2.10.0-2
BuildRequires:	libjpeg-devel
BuildRequires:	libpng-devel
%{?with_lirc:BuildRequires:	lirc-devel}
BuildRequires:	libtool
BuildRequires:	libxml2-devel
BuildRequires:	python-devel
BuildRequires:	rpmbuild(macros) >= 1.197
%ifarch %{ix86}
BuildRequires:	rte-devel >= 0.5
%endif
BuildRequires:	zvbi-devel >= 0.2.9
Requires(post,preun): GConf2
Requires(post,postun): scrollkeeper
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_plugindir	%{_libdir}/zapping/plugins

%description
GNOME (GNU Network Object Model Environment) is a user-friendly set of
applications and desktop tools to be used in conjunction with a window
manager for the X Window System. GNOME is similar in purpose and scope
to CDE and KDE, but GNOME is based completely on free software.

This is a TV viewer for the GNOME desktop. It has all the needed
features, plus extensibility through a plugin system.

%description -l pl.UTF-8
Zapping to program do oglądania telewizji dla środowiska GNOME. Ma
wszystkie potrzebne funkcje oraz oferuje możliwość rozszerzania
funkcjonalności przez system wtyczek (pluginów).

%package alirc-plugin
Summary:	Another Zapping plugin for infrared control
Summary(pl.UTF-8):	Kolejna wtyczka Zappinga do kontroli podczerwienią
Group:		X11/Applications/Multimedia
Requires:	%{name} = %{version}-%{release}
Requires:	lirc
Obsoletes:	zapping-lirc-plugin

%description alirc-plugin
This package allows you to control Zapping with a LIRC-supported
remote control.

%description alirc-plugin -l pl.UTF-8
Pakiet pozwalający na obsługę Zappinga pilotem zdalnego sterowania
obsługiwanym przez LIRC.

%package deinterlace-plugin
Summary:	Zapping plugin that deinterlaces video
Summary(pl.UTF-8):	Wtyczka Zappinga usuwajÄca przeplot obrazu
Group:		X11/Applications/Multimedia
Requires:	%{name} = %{version}-%{release}

%description deinterlace-plugin
This package allows you to deinterlace TV video.

%description deinterlace-plugin -l pl.UTF-8
Pakiet pozwalający na usunięcie przeplotu obrazu TV.

%package mpeg-plugin
Summary:	Zapping plugin that saves video in MPEG format
Summary(pl.UTF-8):	Wtyczka Zappinga do zapisu obrazu w formacie MPEG
Group:		X11/Applications/Multimedia
Requires:	%{name} = %{version}-%{release}

%description mpeg-plugin
This package allows you to save video from TV in MPEG format.

%description mpeg-plugin -l pl.UTF-8
Pakiet pozwalający na zapis obrazu z TV w formacie MPEG.

%package screenshot-plugin
Summary:	Zapping plugin for taking screenshots
Summary(pl.UTF-8):	Wtyczka Zappinga do robienia zrzutów ekranu
Group:		X11/Applications/Multimedia
Requires:	%{name} = %{version}-%{release}

%description screenshot-plugin
You can use this plugin to take screenshots of what you are actually
watching in TV. It will save the screenshots in JPEG format.

%description screenshot-plugin -l pl.UTF-8
Wtyczka pozwalająca na zapisywanie aktualnie oglądanego obrazu
telewizyjnego do pliku JPEG.

%package teletext-plugin
Summary:	Zapping plugin that displays teletext informations
Summary(pl.UTF-8):	Wtyczka Zappinga wyświetlająca strony teletekstowe
Group:		X11/Applications/Multimedia
Requires:	%{name} = %{version}-%{release}

%description teletext-plugin
This package allows you to display teletext pages.

%description teletext-plugin -l pl.UTF-8
Pakiet pozwalający na wyświetlanie stron z teletekstem.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

%build
%{__glib_gettextize}
%{__intltoolize}
%{__libtoolize}
%{__aclocal}
%{__autoheader}
%{__automake}
%{__autoconf}
%configure \
	--disable-schemas-install
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sbindir},%{_desktopdir},%{_pixmapsdir}}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	Multimediadir=%{_desktopdir}

ln -sf zapping $RPM_BUILD_ROOT%{_bindir}/zapzilla

cp -f plugins/alirc/README{.alirc,}

# Remove useless *.la files
rm -f $RPM_BUILD_ROOT%{_libdir}/%{name}/plugins/*.la

%find_lang %{name} --with-gnome

%clean
rm -rf $RPM_BUILD_ROOT

%post
%scrollkeeper_update_post
%gconf_schema_install zapping.schemas

%preun
%gconf_schema_uninstall zapping.schemas

%postun
%scrollkeeper_update_postun

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS THANKS NEWS README* TODO BUGS
%attr(755,root,root) %{_bindir}/zapping
%attr(755,root,root) %{_bindir}/zapzilla
%attr(755,root,root) %{_bindir}/zapping_fix_overlay
%attr(755,root,root) %{_bindir}/zapping_remote
%attr(4755,root,root) %{_sbindir}/zapping_setup_fb
%dir %{_libdir}/zapping
%dir %{_plugindir}
%{_pixmapsdir}/*
%{_sysconfdir}/gconf/schemas/zapping.schemas
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

# not buildable on other archs
%ifarch %{ix86}
%files deinterlace-plugin
%defattr(644,root,root,755)
%attr(755,root,root) %{_plugindir}/libdeinterlace.zapping.so*
%endif

%files mpeg-plugin
%defattr(644,root,root,755)
%attr(755,root,root) %{_plugindir}/libmpeg.zapping.so*

%files screenshot-plugin
%defattr(644,root,root,755)
%attr(755,root,root) %{_plugindir}/libscreenshot.zapping.so*

%files teletext-plugin
%defattr(644,root,root,755)
%attr(755,root,root) %{_plugindir}/libteletext.zapping.so*
