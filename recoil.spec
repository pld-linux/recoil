# TODO:
# - finish html5 (BR: vnu.jar)
# - webapp config for -html5? (optional, may be used also locally)
#
# Conditional build:
%bcond_with	html5	# HTML5 viewer
%bcond_without	magick	# ImageMagick coder
#
# html5 requires cito that requires mono that is not available yet on x32
%ifarch x32
%undefine	with_html5
%endif

Summary:	RECOIL - Retro Computer Image Library
Summary(pl.UTF-8):	RECOIL (Retro Computer Image Library) - biblioteka do obrazów w formatach komputerów retro
Name:		recoil
Version:	6.1.1
Release:	3
License:	GPL v2+
Group:		Applications/Graphics
Source0:	https://downloads.sourceforge.net/recoil/%{name}-%{version}.tar.gz
# Source0-md5:	844d34c62064c8123a4179133493246e
URL:		http://recoil.sourceforge.net/
%{?with_magick:BuildRequires:	ImageMagick-devel >= 1:6.8}
%{?with_html5:BuildRequires:	asciidoc}
%{?with_html5:BuildRequires:	cito}
BuildRequires:	libpng-devel
BuildRequires:	libxslt-progs
BuildRequires:	zlib-devel
#Obsoletes:	fail < 3
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%if %{with magick}
%define		im_coders_dir	%(pkg-config --variable moduledir MagickCore)/coders
%endif

%description
RECOIL is a viewer of pictures in native formats of vintage computers:
Amiga, Amstrad CPC, Apple II, Atari 8-bit, Atari Portfolio, Atari
ST/TT/Falcon, BBC Micro, Commodore VIC-20, Commodore 16, Commodore 64,
Commodore 128, Electronika BK, FM Towns, Macintosh 128K, MSX,
NEC PC-80/88/98, Oric, Psion Series 3, SAM Coupe, Sharp X68000, Tandy
1000, Timex 2048, TRS-80, TRS-80 Color Computer, ZX81 and ZX Spectrum.

%description -l pl.UTF-8
RECOIL to przeglądarka obrazów w natywnych formatach klasycznych
komputerów: Amiga, Amstrad CPC, Apple II, Atari 8-bitowe, Atari
Portfolio, Atari ST/TT/Falcon, BBC Micro, Commodore VIC-20, Commodore
16, Commodore 64, Commodore 128, Electronika BK, FM Towns, Macintosh
128K, MSX, NEC PC-80/88/98, Oric, Psion Series 3, SAM Coupé, Sharp
X68000, Tandy 1000, Timex 2048, TRS-80, TRS-80 Color Computer, ZX81
oraz ZX Spectrum.

%package gnome
Summary:	RECOIL support for viewing retro computer files in GNOME
Summary(pl.UTF-8):	Wsparcie RECOIL do oglądania plików z komputerów retro w GNOME
Group:		X11/Applications/Graphics
Requires:	%{name} = %{version}-%{release}
Requires:	shared-mime-info
Obsoletes:	fail-gnome < 3

%description gnome
RECOIL support for viewing retro computer files in GNOME.

%description gnome -l pl.UTF-8
Wsparcie RECOIL do oglądania plików z komputerów retro w GNOME.

%package html5
Summary:	HTML5 RECOIL viewer for retro computer files
Summary(pl.UTF-8):	Przeglądarka RECOIL do plików z komputerów retro w HTML5
Group:		Applications/WWW
#Obsoletes:	fail-html5 < 3

%description html5
HTML5 RECOIL viewer for retro computer files.

%description html5 -l pl.UTF-8
Przeglądarka RECOIL do plików z komputerów retro w HTML5.

%package -n ImageMagick-coder-recoil
Summary:	RECOIL coder for ImageMagick
Summary(pl.UTF-8):	Koder RECOIL dla ImageMagicka
Group:		Libraries
%requires_ge_to	ImageMagick ImageMagick-devel
#Obsoletes:	ImageMagick-coder-fail < 3

%description -n ImageMagick-coder-recoil
RECOIL coder for ImageMagick to read retro computer formats.

%description -n ImageMagick-coder-recoil -l pl.UTF-8
Koder RECOIL dla ImageMagicka, czytający formaty komputerów retro.

%prep
%setup -q

%build
%{__make} \
	CC="%{__cc}" \
	CFLAGS="%{rpmcflags} -Wall -I. -DMAGICK7" \
%if %{with magick}
	MAGICK_INCLUDE_PATH=/usr/include/ImageMagick-7/private \
	CAN_INSTALL_MAGICK=1
%endif

%if %{with html5}
%{__make} -C www
%endif

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install-recoil2png install-mime install-thumbnailer \
	BUILDING_PACKAGE=1 \
	PREFIX=$RPM_BUILD_ROOT%{_prefix}

# install-thumbnailer is ugly; for now, install only this one
#install -D recoil-mime.xml $RPM_BUILD_ROOT%{_datadir}/mime/packages/recoil-mime.xml

%if %{with magick}
install -D imagemagick/recoil.so $RPM_BUILD_ROOT%{im_coders_dir}/recoil.so
echo "dlname='recoil.so'" >$RPM_BUILD_ROOT%{im_coders_dir}/recoil.la
%endif

%if %{with html5}
install -d $RPM_BUILD_ROOT%{_datadir}/recoil-html5
cp -p www/*.{js,html} $RPM_BUILD_ROOT%{_datadir}/recoil-html5
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post	gnome
%update_mime_database

%postun	gnome
%update_mime_database

%files
%defattr(644,root,root,755)
%doc README
%attr(755,root,root) %{_bindir}/recoil2png
%{_mandir}/man1/recoil2png.1*

%files gnome
%defattr(644,root,root,755)
%{_datadir}/mime/packages/recoil-mime.xml
%{_datadir}/thumbnailers/recoil.thumbnailer

%if %{with html5}
%files html5
%defattr(644,root,root,755)
%{_datadir}/recoil-html5
%endif

%if %{with magick}
%files -n ImageMagick-coder-recoil
%defattr(644,root,root,755)
%attr(755,root,root) %{im_coders_dir}/recoil.so
%{im_coders_dir}/recoil.la
%endif
