#
# Conditional build:
%bcond_without	apidocs		# API documentation
%bcond_without	python3		# CPython 3.x binding
%bcond_without	static_libs	# static library

%define		gstmver		1.0
%define		gst_ver		1.24.0
%define		gstpb_ver	1.24.0
%define		gstdevtools_ver	1.24.0
Summary:	GStreamer Editing Services library
Summary(pl.UTF-8):	Biblioteka funkcji edycyjnych GStreamera (GStreamer Editing Services)
Name:		gstreamer-editing-services
Version:	1.24.4
Release:	1
License:	LGPL v2+
Group:		Libraries
Source0:	https://gstreamer.freedesktop.org/src/gstreamer-editing-services/gst-editing-services-%{version}.tar.xz
# Source0-md5:	5b1f167dfc6463f9a7cf627038111429
URL:		https://gstreamer.freedesktop.org/
BuildRequires:	bash-completion-devel >= 1:2.0
BuildRequires:	flex >= 2.5.31
BuildRequires:	glib2-devel >= 1:2.67.4
BuildRequires:	gobject-introspection-devel >= 0.9.6
BuildRequires:	gstreamer-devel >= %{gst_ver}
BuildRequires:	gstreamer-plugins-base-devel >= %{gstpb_ver}
# for tests/check only
#BuildRequires:	gstreamer-plugins-bad-devel >= %{gstpb_ver}
BuildRequires:	gstreamer-validate-devel >= %{gstdevtools_ver}
%{?with_apidocs:BuildRequires:	hotdoc >= 0.11.0}
BuildRequires:	meson >= 1.1
BuildRequires:	ninja >= 1.5
BuildRequires:	libxml2-devel >= 2.0
BuildRequires:	pkgconfig >= 1:0.9.0
%if %{with python3}
BuildRequires:	python3 >= 1:3.4
# for proper overrides dir detection
BuildRequires:	python3-pygobject3
%endif
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.736
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
Requires:	glib2 >= 1:2.67.4
Requires:	gstreamer >= %{gst_ver}
Requires:	gstreamer-plugins-base >= %{gstpb_ver}
Requires:	gstreamer-validate >= %{gstdevtools_ver}
Obsoletes:	gstreamer-gnonlin < 1.6.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# must be consistent with python-pygobject3.spec because of "..overrides" and "..importer" imports
%define		py3_gi_overridesdir	%{py3_sitedir}/gi/overrides

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
Requires:	glib2-devel >= 1:2.67.4
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
Obsoletes:	gstreamer-gnonlin-apidocs < 1.6.0
BuildArch:	noarch

%description apidocs
API documentation for GStreamer Editing Services library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki GStreamer Editing Services.

%package -n python3-gstreamer-editing-services
Summary:	Python GI binding for GStreamer Editing Services
Summary(pl.UTF-8):	Wiązanie Pythona GI do usług GStreamer Editing Services
Group:		Libraries/Python
Requires:	%{name} = %{version}-%{release}
Requires:	python3-pygobject3 >= 3.0
Obsoletes:	python-gstreamer-editing-services < 1.18

%description -n python3-gstreamer-editing-services
Python GI binding for GStreamer Editing Services.

%description -n python3-gstreamer-editing-services -l pl.UTF-8
Wiązanie Pythona GI do usług GStreamer Editing Services.

%package -n bash-completion-gstreamer-editing-services
Summary:	Bash completion for GStreamer Editing Services utilities
Summary(pl.UTF-8):	Bashowe uzupełnianie paramterów narzędzi GStreamer Editing Services
Group:		Applications/Shells
Requires:	%{name} = %{version}-%{release}
Requires:	bash-completion >= 1:2.0
BuildArch:	noarch

%description -n bash-completion-gstreamer-editing-services
Bash completion for GStreamer Editing Services utilities (ges-launch).

%description -n bash-completion-gstreamer-editing-services -l pl.UTF-8
Bashowe uzupełnianie paramterów narzędzi GStreamer Editing Services
(ges-launch).

%prep
%setup -q -n gst-editing-services-%{version}

%build
%meson build \
	%{!?with_apidocs:-Ddoc=false} \
	-Dpygi-overrides-dir=%{py3_sitedir}/gi/overrides

%ninja_build -C build

%if %{with apidocs}
cd build/docs
for component_dir in gst-editing-services-doc plugin-ges plugin-nle ; do
	LC_ALL=C.UTF-8 hotdoc run --conf-file ${component_dir}.json
done
%endif

%install
rm -rf $RPM_BUILD_ROOT

%ninja_install -C build

%if %{with static_libs}
%{__rm} $RPM_BUILD_ROOT%{_libdir}/gstreamer-1.0/libgst*.a
%{__rm} -r $RPM_BUILD_ROOT%{_libdir}/gstreamer-1.0/pkgconfig
%endif

%if %{with python3}
%py3_comp $RPM_BUILD_ROOT%{py3_sitedir}
%py3_ocomp $RPM_BUILD_ROOT%{py3_sitedir}
%endif

%if %{with apidocs}
install -d $RPM_BUILD_ROOT%{_docdir}/gstreamer-%{gstmver}
cp -pr build/docs/{gst-editing-services-doc,plugin-ges,plugin-nle} $RPM_BUILD_ROOT%{_docdir}/gstreamer-%{gstmver}
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
%if %{with python3}
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

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%{_docdir}/gstreamer-%{gstmver}/gst-editing-services-doc
%{_docdir}/gstreamer-%{gstmver}/plugin-ges
%{_docdir}/gstreamer-%{gstmver}/plugin-nle
%endif

%if %{with python3}
%files -n python3-gstreamer-editing-services
%defattr(644,root,root,755)
%{py3_gi_overridesdir}/GES.py
%{py3_gi_overridesdir}/__pycache__/GES.cpython-*.py[co]
%endif

%files -n bash-completion-gstreamer-editing-services
%defattr(644,root,root,755)
%{bash_compdir}/ges-launch-1.0
