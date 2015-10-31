#
# Conditional build:
%bcond_without	static_libs	# static library
#
%define		gst_req_ver	1.6.1
%define		gstpb_req_ver	1.6.1
Summary:	GStreamer Editing Services library
Summary(pl.UTF-8):	Biblioteka funkcji edycyjnych GStreamera (GStreamer Editing Services)
Name:		gstreamer-editing-services
Version:	1.6.1
Release:	1
License:	LGPL v2+
Group:		Libraries
Source0:	http://gstreamer.freedesktop.org/src/gstreamer-editing-services/%{name}-%{version}.tar.xz
# Source0-md5:	2e2041ef576d702014f7f6064ac75d31
URL:		http://gstreamer.net/
BuildRequires:	autoconf >= 2.62
BuildRequires:	automake >= 1:1.11
BuildRequires:	glib2-devel >= 1:2.34.0
BuildRequires:	gobject-introspection-devel >= 0.9.6
BuildRequires:	gstreamer-devel >= %{gst_req_ver}
BuildRequires:	gstreamer-plugins-base-devel >= %{gstpb_req_ver}
BuildRequires:	gstreamer-validate-devel >= 1.6.0
BuildRequires:	gtk-doc >= 1.3
BuildRequires:	libtool >= 2:2.2.6
BuildRequires:	libxml2-devel >= 2.0
BuildRequires:	pkgconfig >= 1:0.9.0
BuildRequires:	python >= 1:2.3
# what version???
#BuildRequires:	python-pygobject3-devel >= 4.22
BuildRequires:	rpmbuild(macros) >= 1.673
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
Requires:	glib2 >= 1:2.34.0
Requires:	gstreamer >= %{gst_req_ver}
Requires:	gstreamer-plugins-base >= %{gstpb_req_ver}
Obsoletes:	gstreamer-gnonlin < 1.6.0
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
Requires:	gstreamer-devel >= %{gst_req_ver}
Requires:	gstreamer-plugins-base-devel >= %{gstpb_req_ver}

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
Obsoletes:	gstreamer-gnonlin-apidocs < 1.6.0

%description apidocs
API documentation for GStreamer Editing Services library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki GStreamer Editing Services.

%package -n bash-completion-gstreamer-editing-services
Summary:	Bash completion for GStreamer Editing Services utilities
Summary(pl.UTF-8):	Bashowe uzupełnianie paramterów narzędzi GStreamer Editing Services
Group:		Applications/Shells
Requires:	%{name} = %{version}-%{release}
Requires:	bash-completion >= 2.0

%description -n bash-completion-gstreamer-editing-services
Bash completion for GStreamer Editing Services utilities (ges-launch).

%description -n bash-completion-gstreamer-editing-services -l pl.UTF-8
Bashowe uzupełnianie paramterów narzędzi GStreamer Editing Services
(ges-launch).

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
	%{?with_static_libs:--enable-static} \
	--with-bash-completion-dir=%{bash_compdir} \
	--with-html-dir=%{_gtkdocdir}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	scenariosdir=%{_datadir}/gstreamer-1.0/validate/scenarios

# obsoleted by pkg-config
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libges-1.0.la
# module loaded through glib
%{__rm} $RPM_BUILD_ROOT%{_libdir}/gstreamer-1.0/libgstnle.la

%py_comp $RPM_BUILD_ROOT%{_libdir}/gst-validate-launcher/python/launcher/apps
%py_ocomp $RPM_BUILD_ROOT%{_libdir}/gst-validate-launcher/python/launcher/apps

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
%attr(755,root,root) %{_libdir}/gstreamer-1.0/libgstnle.so
%{_libdir}/gst-validate-launcher/python/launcher/apps/geslaunch.py*
%{_datadir}/gstreamer-1.0/validate/scenarios/ges-edit-clip-while-paused.scenario

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libges-1.0.so
%{_includedir}/gstreamer-1.0/ges
%{_datadir}/gir-1.0/GES-1.0.gir
%{_pkgconfigdir}/gst-editing-services-1.0.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libges-1.0.a
%endif

%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/ges-1.0

%files -n bash-completion-gstreamer-editing-services
%defattr(644,root,root,755)
%{bash_compdir}/ges-launch-1.0
