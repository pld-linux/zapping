#
# Conditional build:
# _without_lirc - disables LIRC
#

%define		snap	20021011

%ifarch sparc sparcv9 sparc64
%define		_without_lirc		1
%endif


Summary:	A TV viewer for Gnome2
Summary(pl):	Program do ogl±dania telewizji dla GNOME2
Name:		zapping
Version:	0.7
Release:	0.%{snap}
License:	GPL
Group:		X11/Applications/Multimedia
Source0:	%{name}-%{version}-%{snap}.tar.bz2
Patch0:		%{name}-suid.patch
Patch1:		%{name}-lirc.patch
Patch2:		%{name}-desktop.patch
URL:		http://zapping.sourceforge.net/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libglade2 >= 2.0.1
BuildRequires:	libgnomeui >= 2.1.0
BuildRequires:	libjpeg-devel
BuildRequires:	libpng-devel
BuildRequires:	libtool
BuildRequires:	libunicode-devel >= 0.4
%{!?_without_lirc:BuildRequires: lirc-devel}
%ifarch %{ix86}
BuildRequires:	rte-devel >= 0.5
%endif
BuildRequires:	zvbi-devel >= 0.2.2
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_prefix		/usr/X11R6
%define		_mandir		%{_prefix}/man
%define		_localedir	/usr/share/locale
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
Requires:	%{name} = %{version}

%description alirc-plugin
This package allows you to control Zapping with a LIRC-supported
remote control.

%description alirc-plugin -l pl
Ten pakiet pozwala na obs³ugê Zappingu pilotem zdalnego sterowania
obs³ugiwanym przez LIRC.

%package lirc-plugin
Summary:	Zapping plugin for infrared control
Summary(pl):	Wtyczka Zappingu do kontroli podczerwieni±
Group:		X11/Applications/Multimedia
Requires:	%{name} = %{version}
Requires:	lirc

%description lirc-plugin
This package allows you to control Zapping with a LIRC-supported
remote control.

%description lirc-plugin -l pl
Ten pakiet pozwala na obs³ugê Zappingu pilotem zdalnego sterowania
obs³ugiwanym przez LIRC.

%package mpeg-plugin
Summary:	Zapping plugin for infrared control
Summary(pl):	Wtyczka Zappingu do kontroli podczerwieni±
Group:		X11/Applications/Multimedia
Requires:	%{name} = %{version}

%description mpeg-plugin
This package allows you to control Zapping with a LIRC-supported
remote control.

%description mpeg-plugin -l pl
Ten pakiet pozwala na obs³ugê Zappingu pilotem zdalnego sterowania
obs³ugiwanym przez LIRC.

%package screenshot-plugin
Summary:	Zapping plugin for taking screenshots
Summary(pl):	Wtyczka Zappinga do robienia zrzutów ekranu
Group:		X11/Applications/Multimedia
Requires:	%{name} = %{version}

%description screenshot-plugin
You can use this plugin to take screenshots of what you are actually
watching in TV. It will save the screenshots in JPEG format.

%description screenshot-plugin -l pl
Ta wtyczka pozwala na zrzucanie aktualnie ogl±danego obrazu
telewizyjnego do pliku JPEG.

%prep -n %{name}
%setup -q -n %{name}
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build

echo 'all install:' > plugins/template/Makefile.am
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
install -d $RPM_BUILD_ROOT{%{_sbindir},%{_datadir}/applications,%{_pixmapsdir}}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	localedir=%{_localedir}

ln -sf zapping $RPM_BUILD_ROOT%{_bindir}/zapzilla

cp -f plugins/alirc/README{.alirc,}
cp zapping.desktop $RPM_BUILD_ROOT%{_datadir}/applications
mv $RPM_BUILD_ROOT%{_datadir}/zapping/gnome-television.png \
   $RPM_BUILD_ROOT%{_pixmapsdir}

%find_lang %{name} --with-gnome

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS THANKS NEWS README* TODO BUGS
%attr(0755,root,root) %{_bindir}/zapping
%attr(0755,root,root) %{_bindir}/zapzilla
%attr(0755,root,root) %{_bindir}/zapping_fix_overlay
%attr(4755,root,root) %{_sbindir}/zapping_setup_fb
%dir %{_libdir}/zapping
%dir %{_libdir}/zapping/plugins
%{_pixmapsdir}/*
%{_datadir}/zapping
%{_datadir}/applications/zapping.desktop
%{_mandir}/man?/*

%if %{!?_without_lirc:1}%{?_without_lirc:0}
%files alirc-plugin
%defattr(644,root,root,755)
%attr(0755,root,root) %{_libdir}/zapping/plugins/libalirc.zapping.so.*.*
%doc plugins/alirc/README
%endif

%files lirc-plugin
%defattr(644,root,root,755)
%attr(0755,root,root) %{_libdir}/zapping/plugins/liblirc.zapping.so.*.*
%doc plugins/lirc/README

#%files mpeg-plugin
#%defattr(644,root,root,755)
#%{_libdir}/zapping/plugins/libmpeg.zapping.so
#%attr(0755,root,root) %{_libdir}/zapping/plugins/libmpeg.zapping.so.*.*
#%{_datadir}/zapping/mpeg_properties.glade

%files screenshot-plugin
%defattr(644,root,root,755)
%attr(0755,root,root) %{_libdir}/zapping/plugins/libscreenshot.zapping.so.*.*
#%{_datadir}/zapping/screenshot.glade
