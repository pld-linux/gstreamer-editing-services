Summary:	GStreamer Editing Services library
Summary(pl.UTF-8):	Biblioteka funkcji edycyjnych GStreamera (GStreamer Editing Services)
Name:		gstreamer-editing-services
Version:	1.1.90
Release:	1
License:	LGPL v2+
Group:		Libraries
Source0:	http://gstreamer.freedesktop.org/src/gstreamer-editing-services/%{name}-%{version}.tar.xz
# Source0-md5:	5e5448c588d1e401fae4cbceafc81e74
URL:		http://gstreamer.net/
BuildRequires:	autoconf >= 2.62
BuildRequires:	automake >= 1:1.11
BuildRequires:	glib2-devel >= 1:2.34.0
BuildRequires:	gobject-introspection-devel >= 0.9.6
BuildRequires:	gstreamer-devel >= 1.2.0
BuildRequires:	gstreamer-plugins-base-devel >= 1.2.0
BuildRequires:	gtk-doc >= 1.3
BuildRequires:	libtool
BuildRequires:	libxml2-devel >= 2.0
BuildRequires:	pkgconfig
BuildRequires:	python >= 2.3
# what version???
#BuildRequires:	python-pygobject3-devel >= 4.22
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
Requires:	glib2 >= 1:2.34.0
Requires:	gstreamer >= 1.2.0
Requires:	gstreamer-plugins-base >= 1.2.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
GStreamer Editing Services is a high-level library for facilitating
the creation of audio/video non-linear editors.

%description -l pl.UTF-8
GStreamer Editing Services to wysokopoziomowa biblioteka ułatwiająca
tworzenie nieliniowych edytorów audio/video.

%package devel
Summary:	Header files for GStreamer Editing Services library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki GStreamer Editing Services
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	glib2-devel >= 1:2.34.0
Requires:	gstreamer-devel >= 1.2.0
Requires:	gstreamer-plugins-base-devel >= 1.2.0

%description devel
Header files for GStreamer Editing Services library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki GStreamer Editing Services.

%package static
Summary:	Static GStreamer Editing Services library
Summary(pl.UTF-8):	Statyczba biblioteka GStreamer Editing Services
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static GStreamer Editing Services library.

%description static -l pl.UTF-8
Statyczba biblioteka GStreamer Editing Services.

%package apidocs
Summary:	API documentation for GStreamer Editing Services library
Summary(pl.UTF-8):	Dokumentacja API biblioteki GStreamer Editing Services
Group:		Documentation
Requires:	gtk-doc-common

%description apidocs
API documentation for GStreamer Editing Services library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki GStreamer Editing Services.

%prep
%setup -q

%build
%{__libtoolize}
%{__aclocal} -I m4 -I common/m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--disable-silent-rules \
	--enable-gtk-doc \
	--enable-static \
	--with-html-dir=%{_gtkdocdir}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# obsoleted by pkg-config
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libges-1.0.la

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README RELEASE
%attr(755,root,root) %{_bindir}/ges-launch-1.0
%attr(755,root,root) %{_libdir}/libges-1.0.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libges-1.0.so.0
%{_libdir}/girepository-1.0/GES-1.0.typelib

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libges-1.0.so
%{_includedir}/gstreamer-1.0/ges
%{_datadir}/gir-1.0/GES-1.0.gir
%{_pkgconfigdir}/gst-editing-services-1.0.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/libges-1.0.a

%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/ges-1.0
