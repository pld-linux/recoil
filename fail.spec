# TODO:
# - register gnome thumbnailer in more package-friendly way (not multiple gconftool runs)
# - webapp config for -html5? (optional, may be used also locally)
#
# Conditional build:
%bcond_without	html5	# HTML5 viewer
%bcond_without	magick	# ImageMagick coder
#
# html5 requires cito that requires mono that is not available yet on x32
%ifarch x32
%undefine	with_html5
%endif

Summary:	FAIL - First Atari Image Library
Summary(pl.UTF-8):	FAIL (First Atari Image Library) - biblioteka do obrazów w formatach Atari
Name:		fail
Version:	2.0.1
Release:	20
License:	GPL v2+
Group:		Applications/Graphics
Source0:	http://downloads.sourceforge.net/fail/%{name}-%{version}.tar.gz
# Source0-md5:	b9362106f9a23a1f99ff7bece94d9aa7
Patch0:		imagemagick7.patch
URL:		http://fail.sourceforge.net/
%{?with_magick:BuildRequires:	ImageMagick-devel >= 1:6.8}
%{?with_html5:BuildRequires:	asciidoc}
%{?with_html5:BuildRequires:	cito}
BuildRequires:	libpng-devel
BuildRequires:	libxslt-progs
BuildRequires:	zlib-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%if %{with magick}
%define		im_coders_dir	%(pkg-config --variable moduledir MagickCore)/coders
%endif

%description
FAIL is a viewer of pictures in native formats of Atari 8-bit, Atari
ST, Atari Falcon and Atari Portfolio computers.

%description -l pl.UTF-8
FAIL to narzędzia do przeglądania obrazów w natywnych formatach
komputerów Atari 8-bitowych, Atari ST, Atari Falcon oraz Atari
Portfolio.

%package gnome
Summary:	FAIL support for viewing Atari files in GNOME
Summary(pl.UTF-8):	Wsparcie FAIL do oglądania plików z Atari w GNOME
Group:		X11/Applications/Graphics
Requires:	%{name} = %{version}-%{release}

%description gnome
FAIL support for viewing Atari files in GNOME.

%description gnome -l pl.UTF-8
Wsparcie FAIL do oglądania plików z Atari w GNOME.

%package html5
Summary:	HTML5 FAIL viewer for Atari files
Summary(pl.UTF-8):	Przeglądarka FAIL do plików z Atari w HTML5
Group:		Applications/WWW

%description html5
HTML5 FAIL viewer for Atari files.

%description html5 -l pl.UTF-8
Przeglądarka FAIL do plików z Atari w HTML5.

%package -n ImageMagick-coder-fail
Summary:	FAIL coder for ImageMagick
Summary(pl.UTF-8):	Koder FAIL dla ImageMagicka
Group:		Libraries
%requires_ge_to	ImageMagick ImageMagick-devel

%description -n ImageMagick-coder-fail
FAIL coder for ImageMagick to read Atari formats.

%description -n ImageMagick-coder-fail -l pl.UTF-8
Koder FAIL dla ImageMagicka, czytający formaty Atari.

%prep
%setup -q
%patch0 -p1

%build
%{__make} all fail-mime.xml \
	CC="%{__cc}" \
	CFLAGS="%{rpmcflags} -Wall" \
%if %{with magick}
	MAGICK_INCLUDE_PATH=/usr/include/ImageMagick-7/private \
	CAN_INSTALL_MAGICK=1
%endif

%if %{with html5}
%{__make} -C html5
%endif

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install-fail2png \
	PREFIX=$RPM_BUILD_ROOT%{_prefix}

# install-thumbnailer is ugly; for now, install only this one
install -D fail-mime.xml $RPM_BUILD_ROOT%{_datadir}/mime/packages/fail-mime.xml

%if %{with magick}
install -D fail.so $RPM_BUILD_ROOT%{im_coders_dir}/fail.so
echo "dlname='fail.so'" >$RPM_BUILD_ROOT%{im_coders_dir}/fail.la
%endif

%if %{with html5}
install -d $RPM_BUILD_ROOT%{_datadir}/fail-html5
cp -p html5/*.{js,html} $RPM_BUILD_ROOT%{_datadir}/fail-html5
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README.html
%attr(755,root,root) %{_bindir}/fail2png

%files gnome
%defattr(644,root,root,755)
%{_datadir}/mime/packages/fail-mime.xml
# TODO: gconf files?

%if %{with html5}
%files html5
%defattr(644,root,root,755)
%{_datadir}/fail-html5
%endif

%if %{with magick}
%files -n ImageMagick-coder-fail
%defattr(644,root,root,755)
%attr(755,root,root) %{im_coders_dir}/fail.so
%{im_coders_dir}/fail.la
%endif
