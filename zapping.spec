Summary:	a TV viewer for Gnome
Name:		zapping
Version:	0.5.4
Release:	3
License:	GPL
Group:		X11/Applications/Multimedia
Group(de):	X11/Applikationen/Multimedia
Group(pl):	X11/Aplikacje/Multimedia
Source0:	ftp://download.sourceforge.net/pub/sourceforge/zapping/%{name}-%{version}.tar.bz2
URL:		http://zapping.sourceforge.net
BuildRequires:	gettext-devel
BuildRequires:	gnome-libs-devel >= 1.0.40
BuildRequires:	gtk+-devel >= 1.2.6
BuildRequires:	libjpeg-devel
BuildRequires:	libxml-devel >= 1.4.0
BuildRequires:	libglade-devel >= 0.9
Buildroot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_prefix		/usr/X11R6

%description
GNOME (GNU Network Object Model Environment) is a user-friendly set of
applications and desktop tools to be used in conjunction with a window
manager for the X Window System. GNOME is similar in purpose and scope
to CDE and KDE, but GNOME is based completely on free software.

This is a TV viewer for the GNOME desktop. It has all the needed
features, plus extensibility through a plugin system.

%prep
%setup -q

%build
gettextize --copy --force
autoconf
%configure \
	--without-included-gettext
%{__make} plugindir=%{_libdir}/zapping

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	INSTALL_PROGRAM="install" \
	DESTDIR=$RPM_BUILD_ROOT \
	plugindir=%{_libdir}/zapping \
	Multimediadir=%{_applnkdir}/Multimedia

gzip -9nf AUTHORS THANKS ChangeLog README README.plugins TODO BUGS

%find_lang %{name} --with-gnome

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc *.gz
%attr(0755,root,root) %{_bindir}/zapping
%attr(4755,root,root) %{_bindir}/zapping_setup_fb
%attr(0755,root,root) %{_libdir}/zapping/lib*so*

%{_datadir}/zapping/*.glade
%{_datadir}/pixmaps/zapping
%{_applnkdir}/Multimedia/zapping.desktop
