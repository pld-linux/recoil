# TODO: register gnome thumbnailer in more package-friendly way (not multiple gconftool runs)
Summary:	FAIL - First Atari Image Library
Summary(pl.UTF-8):	FAIL (First Atari Image Library) - biblioteka do obrazów w formatach Atari
Name:		fail
Version:	2.0.0
Release:	1
License:	GPL v2+
Group:		Applications/Graphics
Source0:	http://downloads.sourceforge.net/fail/%{name}-%{version}.tar.gz
# Source0-md5:	de3592b78144ef3c6b2e98377522df69
URL:		http://fail.sourceforge.net/
BuildRequires:	ImageMagick-devel >= 6.8
BuildRequires:	libpng-devel
BuildRequires:	libxslt-progs
BuildRequires:	zlib-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		magick_ver	%(MagickCore-config --version)
%define		im_coders_dir	%{_libdir}/%(MagickCore-config --version | sed -e 's,^\\([.0-9]\\+\\) \\+\\(Q[0-9]\\+\\)\\( \\+\\(HDRI\\)\\)\\?.*,ImageMagick-\\1/modules-\\2\\4,')/coders

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

%package -n ImageMagick-coder-fail
Summary:	FAIL coder for ImageMagick
Summary(pl.UTF-8):	Koder FAIL dla ImageMagicka
Group:		Libraries
Requires:	ImageMagick >= %{magick_ver}

%description -n ImageMagick-coder-fail
FAIL coder for ImageMagick to read Atari formats.

%description -n ImageMagick-coder-fail -l pl.UTF-8
Koder FAIL dla ImageMagicka, czytający formaty Atari.

%prep
%setup -q

%build
%{__make} all fail-mime.xml \
	CC="%{__cc}" \
	CFLAGS="%{rpmcflags} -Wall" \
	MAGICK_INCLUDE_PATH=/usr/include/ImageMagick-6/private \
	CAN_INSTALL_MAGICK=1

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install-fail2png \
	PREFIX=$RPM_BUILD_ROOT%{_prefix}

# install-thumbnailer is ugly; for now, install only this one
install -D fail-mime.xml $RPM_BUILD_ROOT%{_datadir}/mime/packages/fail-mime.xml

install -D fail.so $RPM_BUILD_ROOT%{im_coders_dir}/fail.so
echo "dlname='fail.so'" >$RPM_BUILD_ROOT%{im_coders_dir}/fail.la

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

%files -n ImageMagick-coder-fail
%defattr(644,root,root,755)
%attr(755,root,root) %{im_coders_dir}/fail.so
%{im_coders_dir}/fail.la
