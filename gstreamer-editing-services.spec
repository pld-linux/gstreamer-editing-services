#
# Conditional build:
%bcond_without	python		# Python binding (any)
%bcond_without	python2		# CPython 2.x binding + validate launcher
%bcond_without	python3		# CPython 3.x binding
%bcond_without	static_libs	# static library

%if %{without python}
%undefine	with_python2
%undefine	with_python3
%endif

%define		gst_ver		1.16.3
%define		gstpb_ver	1.16.3
%define		gstvalidate_ver	1.12.1
Summary:	GStreamer Editing Services library
Summary(pl.UTF-8):	Biblioteka funkcji edycyjnych GStreamera (GStreamer Editing Services)
Name:		gstreamer-editing-services
Version:	1.16.3
Release:	1
License:	LGPL v2+
Group:		Libraries
Source0:	https://gstreamer.freedesktop.org/src/gstreamer-editing-services/%{name}-%{version}.tar.xz
# Source0-md5:	15e007faa8ac6c9049567f5b086d378b
URL:		https://gstreamer.freedesktop.org/
BuildRequires:	autoconf >= 2.62
BuildRequires:	automake >= 1:1.11
BuildRequires:	flex >= 2.5.31
BuildRequires:	glib2-devel >= 1:2.40.0
BuildRequires:	gobject-introspection-devel >= 0.9.6
BuildRequires:	gstreamer-devel >= %{gst_ver}
BuildRequires:	gstreamer-plugins-base-devel >= %{gstpb_ver}
BuildRequires:	gstreamer-validate-devel >= %{gstvalidate_ver}
BuildRequires:	gtk-doc >= 1.3
BuildRequires:	libtool >= 2:2.2.6
BuildRequires:	libxml2-devel >= 2.0
BuildRequires:	pkgconfig >= 1:0.9.0
%if %{with python2}
BuildRequires:	python >= 1:2.3
BuildRequires:	python-pygobject3-devel >= 3.0
%endif
%if %{with python3}
BuildRequires:	python3 >= 1:3.4
%endif
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.673
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
Requires:	glib2 >= 1:2.40.0
Requires:	gstreamer >= %{gst_ver}
Requires:	gstreamer-plugins-base >= %{gstpb_ver}
Requires:	gstreamer-validate >= %{gstvalidate_ver}
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
Requires:	glib2-devel >= 1:2.40.0
Requires:	gstreamer-devel >= %{gst_ver}
Requires:	gstreamer-plugins-base-devel >= %{gstpb_ver}

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
BuildArch:	noarch

%description apidocs
API documentation for GStreamer Editing Services library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki GStreamer Editing Services.

%package -n python-gstreamer-editing-services
Summary:	Python GI binding for GStreamer Editing Services
Summary(pl.UTF-8):	Wiązanie Pythona GI do usług GStreamer Editing Services
Group:		Libraries/Python
Requires:	%{name} = %{version}-%{release}
Requires:	python-pygobject3 >= 3.0

%description -n python-gstreamer-editing-services
Python GI binding for GStreamer Editing Services.

%description -n python-gstreamer-editing-services -l pl.UTF-8
Wiązanie Pythona GI do usług GStreamer Editing Services.

%package -n python3-gstreamer-editing-services
Summary:	Python GI binding for GStreamer Editing Services
Summary(pl.UTF-8):	Wiązanie Pythona GI do usług GStreamer Editing Services
Group:		Libraries/Python
Requires:	%{name} = %{version}-%{release}
Requires:	python3-pygobject3 >= 3.0

%description -n python3-gstreamer-editing-services
Python GI binding for GStreamer Editing Services.

%description -n python3-gstreamer-editing-services -l pl.UTF-8
Wiązanie Pythona GI do usług GStreamer Editing Services.

%package -n bash-completion-gstreamer-editing-services
Summary:	Bash completion for GStreamer Editing Services utilities
Summary(pl.UTF-8):	Bashowe uzupełnianie paramterów narzędzi GStreamer Editing Services
Group:		Applications/Shells
Requires:	%{name} = %{version}-%{release}
Requires:	bash-completion >= 2.0
BuildArch:	noarch

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
# modules loaded through glib
%{__rm} $RPM_BUILD_ROOT%{_libdir}/gstreamer-1.0/libgst*.la
%if %{with static_libs}
%{__rm} $RPM_BUILD_ROOT%{_libdir}/gstreamer-1.0/libgst*.a
%endif

%if %{with python2}
%py_comp $RPM_BUILD_ROOT%{_libdir}/gst-validate-launcher/python/launcher/apps
%py_ocomp $RPM_BUILD_ROOT%{_libdir}/gst-validate-launcher/python/launcher/apps

%py_postclean
%endif

%if %{with python3}
install -d $RPM_BUILD_ROOT%{py3_sitedir}/gstreamer-editing-services
cp -p bindings/python/gi/overrides/GES.py $RPM_BUILD_ROOT%{py3_sitedir}/gstreamer-editing-services
%py3_comp $RPM_BUILD_ROOT%{py_sitedir}/gstreamer-editing-services
%py3_ocomp $RPM_BUILD_ROOT%{py_sitedir}/gstreamer-editing-services
%endif

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
%attr(755,root,root) %{_libdir}/gstreamer-1.0/libgstges.so
%attr(755,root,root) %{_libdir}/gstreamer-1.0/libgstnle.so
%if %{with python2}
%{_libdir}/gst-validate-launcher/python/launcher/apps/geslaunch.py*
%endif
%{_datadir}/gstreamer-1.0/validate/scenarios/ges-edit-clip-while-paused.scenario
%{_mandir}/man1/ges-launch-1.0.1*

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

%if %{with python2}
%files -n python-gstreamer-editing-services
%defattr(644,root,root,755)
# must be in %{py_sitedir} because of "..overrides" and "..importer" imports
%{py_sitedir}/gstreamer-editing-services
%endif

%if %{with python3}
%files -n python3-gstreamer-editing-services
%defattr(644,root,root,755)
# must be in %{py3_sitedir} because of "..overrides" and "..importer" imports
%{py3_sitedir}/gstreamer-editing-services
%endif

%files -n bash-completion-gstreamer-editing-services
%defattr(644,root,root,755)
%{bash_compdir}/ges-launch-1.0
