#
# Conditional build:
# _without_lirc - disables LIRC
#
%ifarch sparc sparcv9 sparc64
%define		_without_lirc		1
%endif

Summary:	A TV viewer for Gnome
Summary(pl):	Program do ogl±dania telewizji dla GNOME
Name:		zapping
Version:	0.6.4
Release:	5
License:	GPL
Group:		X11/Applications/Multimedia
Source0:	ftp://ftp.sourceforge.net/pub/sourceforge/zapping/%{name}-%{version}.tar.bz2
Patch0:		%{name}-make.patch
Patch1:		%{name}-lirc-path.patch
Patch2:		%{name}-am15.patch
URL:		http://zapping.sourceforge.net/
BuildRequires:	gettext-devel
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	gdk-pixbuf-devel >= 0.8
BuildRequires:	gnome-libs-devel >= 1.0.40
BuildRequires:	gtk+-devel >= 1.2.6
BuildRequires:	libglade-gnome-devel >= 0.9
BuildRequires:	libjpeg-devel
BuildRequires:	libpng-devel
BuildRequires:	libtool
BuildRequires:	libunicode-devel >= 0.4
BuildRequires:	libxml-devel >= 1.7.3
%{!?_without_lirc:BuildRequires: lirc-devel}
BuildRequires:	pam-devel
%ifarch %{ix86}
BuildRequires:	rte-devel >= 0.4
%endif
BuildRequires:	zvbi-devel
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

%prep
%setup -q
%patch0 -p1
%patch1 -p0
%patch2 -p1

%build
rm -f missing
%{__libtoolize}
%{__aclocal} -I %{_aclocaldir}/gnome
# Temporary hack for autoheader
echo 'AH_OUTPUT([HAVE_LIBSM], [#undef HAVE_LIBSM])' >> configure.in
%{__autoconf}
%{__automake}
# We don't want dummy plugins
echo 'all install:' > plugins/template/Makefile.in
%configure \
	AS='${CC}' \
	--without-included-gettext
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	localedir=%{_localedir}

ln -sf zapping $RPM_BUILD_ROOT%{_bindir}/zapzilla

mv -f plugins/alirc/README{.alirc,}

%find_lang %{name} --with-gnome

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS THANKS NEWS README* TODO BUGS
%attr(0755,root,root) %{_bindir}/zapping
%attr(0755,root,root) %{_bindir}/zapzilla
%attr(4755,root,root) %{_bindir}/zapping_setup_fb
%dir %{_libdir}/zapping
%dir %{_libdir}/zapping/plugins
%dir %{_datadir}/zapping
%{_datadir}/zapping/zapping.glade
%{_pixmapsdir}/zapping
%{_applnkdir}/Multimedia/zapping.desktop
%{_mandir}/man?/*

%if %{!?_without_lirc:1}%{?_without_lirc:0}
%files alirc-plugin
%defattr(644,root,root,755)
%{_libdir}/zapping/plugins/libalirc.zapping.so
%attr(0755,root,root) %{_libdir}/zapping/plugins/libalirc.zapping.so.*.*
%doc plugins/alirc/README
%endif

%files lirc-plugin
%defattr(644,root,root,755)
%{_libdir}/zapping/plugins/liblirc.zapping.so
%attr(0755,root,root) %{_libdir}/zapping/plugins/liblirc.zapping.so.*.*
%doc plugins/lirc/README

%files mpeg-plugin
%defattr(644,root,root,755)
%{_libdir}/zapping/plugins/libmpeg.zapping.so
%attr(0755,root,root) %{_libdir}/zapping/plugins/libmpeg.zapping.so.*.*
%{_datadir}/zapping/mpeg_properties.glade

%files screenshot-plugin
%defattr(644,root,root,755)
%{_libdir}/zapping/plugins/libscreenshot.zapping.so
%attr(0755,root,root) %{_libdir}/zapping/plugins/libscreenshot.zapping.so.*.*
%{_datadir}/zapping/screenshot.glade
