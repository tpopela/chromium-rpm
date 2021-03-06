# %%{nil} for Stable; -beta for Beta; -dev for Devel
# dash in -beta and -dev is intentional !
%global chromium_channel %{nil}
%global chromium_browser_channel chromium-browser%{chromium_channel}
%global chromium_path %{_libdir}/chromium-browser%{chromium_channel}
%global crd_path %{_libdir}/chrome-remote-desktop
%global tests 0
# Try to not use the Xvfb as it is slow..
%global tests_force_display 0
# If we build with shared on, then chrome-remote-desktop depends on chromium libs.
# If we build with shared off, then users cannot swap out libffmpeg (and i686 gets a lot harder to build)
%global shared 1
# We should not need to turn this on. The app in the webstore _should_ work.
%global build_remoting_app 0

# TODO: Try arm (nacl disabled)
%if 0%{?fedora}
 %ifarch i686
 %global nacl 0
 %global nonacl 1
 %else
 %global nacl 1
 %global nonacl 0
 %endif
%endif

%if 0%{?fedora} >= 22 && 0%{?fedora} < 24
# Chromium needs icu 5.4 now, which isn't in older Fedora.
# And F24+ is "too new". Sigh.
BuildRequires:  libicu-devel >= 5.4
%global bundleicu 0
%else
%global bundleicu 1
%endif

### Google API keys (see http://www.chromium.org/developers/how-tos/api-keys)
### Note: These are for Fedora use ONLY.
### For your own distribution, please get your own set of keys.
### http://lists.debian.org/debian-legal/2013/11/msg00006.html
%global api_key AIzaSyDUIXvzVrt5OkVsgXhQ6NFfvWlA44by-aw
%global default_client_id 449907151817.apps.googleusercontent.com
%global default_client_secret miEreAep8nuvTdvLums6qyLK
%global chromoting_client_id 449907151817-8vnlfih032ni8c4jjps9int9t86k546t.apps.googleusercontent.com 

Name:		chromium%{chromium_channel}
Version:	48.0.2564.116
Release:	1%{?dist}
Summary:	A WebKit (Blink) powered web browser
Url:		http://www.chromium.org/Home
License:	BSD and LGPLv2+ and ASL 2.0 and IJG and MIT and GPLv2+ and ISC and OpenSSL and (MPLv1.1 or GPLv2 or LGPLv2)
Group:		Applications/Internet

### Chromium Fedora Patches ###
Patch0:		chromium-46.0.2490.71-gcc5.patch
Patch1:		chromium-45.0.2454.101-linux-path-max.patch
Patch2:		chromium-48.0.2564.103-addrfix.patch
# Google patched their bundled copy of icu 54 to include API functionality that wasn't added until 55.
# :P
Patch3:		chromium-45.0.2454.101-system-icu-54-does-not-have-detectHostTimeZone.patch
Patch4:		chromium-46.0.2490.71-notest.patch
Patch5:		chromium-46.0.2490.80-cast_link_zlib.patch
# In file included from ../linux/directory.c:21:
# In file included from ../../../../native_client/src/nonsfi/linux/abi_conversion.h:20:
# ../../../../native_client/src/nonsfi/linux/linux_syscall_structs.h:44:13: error: GNU-style inline assembly is disabled
#     __asm__ __volatile__("mov %%gs, %0" : "=r"(gs));
#             ^
# 1 error generated.
Patch6:		chromium-47.0.2526.80-pnacl-fgnu-inline-asm.patch
# Ignore broken nacl open fd counter
Patch7:		chromium-47.0.2526.80-nacl-ignore-broken-fd-counter.patch
# Fixups for gcc6
Patch8:		chromium-48.0.2564.103-gcc6.patch
# Use libusb_interrupt_event_handler from current libusbx (1.0.21-0.1.git448584a)
Patch9:		chromium-48.0.2564.116-libusb_interrupt_event_handler.patch


### Chromium Tests Patches ###
Patch100:	chromium-46.0.2490.86-use_system_opus.patch
Patch101:	chromium-46.0.2490.86-use_system_harfbuzz.patch
Patch102:	chromium-46.0.2490.86-sync_link_zlib.patch

# Use chromium-latest.py to generate clean tarball from released build tarballs, found here:
# http://build.chromium.org/buildbot/official/
# For Chromium Fedora use chromium-latest.py --stable --ffmpegclean --ffmpegarm
# If you want to include the ffmpeg arm sources append the --ffmpegarm switch
# https://commondatastorage.googleapis.com/chromium-browser-official/chromium-%%{version}.tar.xz
Source0:	chromium-%{version}-clean.tar.xz
%if 0%{tests}
Source1:	https://commondatastorage.googleapis.com/chromium-browser-official/chromium-%{version}-testdata.tar.xz
%endif
# https://chromium.googlesource.com/chromium/tools/depot_tools.git/+archive/7e7a454f9afdddacf63e10be48f0eab603be654e.tar.gz
Source2:	depot_tools.git-master.tar.gz
Source3:	chromium-browser.sh
Source4:	%{chromium_browser_channel}.desktop
# Also, only used if you want to reproduce the clean tarball.
Source5:	clean_ffmpeg.sh
Source6:	chromium-latest.py
Source7:	get_free_ffmpeg_source_files.py
# Get the names of all tests (gtests) for Linux
# Usage: get_linux_tests_name.py chromium-%%{version} --spec
Source8:	get_linux_tests_names.py
# GNOME stuff
Source9:	chromium-browser.xml
Source10:	https://dl.google.com/dl/edgedl/chrome/policy/policy_templates.zip
Source11:	chrome-remote-desktop.service

BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

# We can assume gcc and binutils.
BuildRequires:	gcc-c++

BuildRequires:	alsa-lib-devel
BuildRequires:	atk-devel
BuildRequires:	bison
BuildRequires:	cups-devel
BuildRequires:	dbus-devel
BuildRequires:	desktop-file-utils
BuildRequires:	expat-devel
BuildRequires:	flex
BuildRequires:	fontconfig-devel
BuildRequires:	GConf2-devel
BuildRequires:	glib2-devel
BuildRequires:	gnome-keyring-devel
BuildRequires:	gtk2-devel
BuildRequires:	glibc-devel
BuildRequires:	gperf
BuildRequires:	libcap-devel
BuildRequires:	libdrm-devel
BuildRequires:	libexif-devel
BuildRequires:	libgcrypt-devel
BuildRequires:	libudev-devel
BuildRequires:	libusb-devel
BuildRequires:	libXdamage-devel
BuildRequires:	libXScrnSaver-devel
BuildRequires:	libXtst-devel
BuildRequires:	nss-devel
BuildRequires:	pciutils-devel
BuildRequires:	pulseaudio-libs-devel
%if 0%{?tests}
BuildRequires:	pam-devel
# Tests needs X
BuildRequires:	Xvfb
BuildRequires:	liberation-sans-fonts
# For sandbox initialization
BuildRequires:	sudo
%endif

# Fedora turns on NaCl
# NaCl needs these
BuildRequires:	libstdc++-devel, openssl-devel
%if 0%{?nacl}
BuildRequires:	nacl-gcc, nacl-binutils, nacl-newlib
BuildRequires:	nacl-arm-gcc, nacl-arm-binutils, nacl-arm-newlib
# pNaCl needs this monster
BuildRequires:	native_client >= 47.0.2526.73
%ifarch x86_64
BuildRequires:  glibc-devel(x86-32) libgcc(x86-32)
%endif
%endif
# Fedora tries to use system libs whenever it can.
BuildRequires:	bzip2-devel
BuildRequires:	dbus-glib-devel
BuildRequires:	elfutils-libelf-devel
BuildRequires:	flac-devel
BuildRequires:	hwdata
BuildRequires:	jsoncpp-devel
BuildRequires:	kernel-headers
BuildRequires:	libevent-devel
BuildRequires:	libexif-devel
%if 0%{?bundleicu}
# If this is true, we're using the bundled icu.
# We'd like to use the system icu every time, but we cannot always do that.
%else
# Not newer than 5.4 (at least not right now)
BuildRequires:	libicu-devel = 5.4
%endif
BuildRequires:	libjpeg-devel
BuildRequires:	libpng-devel
%if 0
# see https://code.google.com/p/chromium/issues/detail?id=501318
BuildRequires:	libsrtp-devel >= 1.4.4
%endif
BuildRequires:	libudev-devel
Requires:	libusbx >= 1.0.21-0.1.git448584a
BuildRequires:	libusbx-devel >= 1.0.21-0.1.git448584a
# We don't use libvpx anymore because Chromium loves to
# use bleeding edge revisions here that break other things
# ... so we just use the bundled libvpx.
# Same is true for libwebp.
BuildRequires:	libxslt-devel
# Same here, it seems.
# BuildRequires:	libyuv-devel
BuildRequires:	minizip-devel
BuildRequires:	nspr-devel
BuildRequires:	opus-devel
BuildRequires:	perl(Switch)
BuildRequires:	pulseaudio-libs-devel
BuildRequires:	python-beautifulsoup4
BuildRequires:	python-BeautifulSoup
BuildRequires:	python-html5lib
BuildRequires:	python-jinja2
BuildRequires:	python-markupsafe
BuildRequires:	python-ply
BuildRequires:	python-simplejson
Requires:	re2 >= 20131024
BuildRequires:	re2-devel >= 20131024
BuildRequires:	speech-dispatcher-devel
BuildRequires:	speex-devel = 1.2
BuildRequires:	yasm
BuildRequires:	pkgconfig(gnome-keyring-1)
# remote desktop needs this
BuildRequires:	pam-devel
BuildRequires:	systemd

# We pick up an automatic requires on the library, but we need the version check
# because the nss shared library is unversioned.
# This is to prevent someone from hitting http://code.google.com/p/chromium/issues/detail?id=26448
Requires:	nss%{_isa} >= 3.12.3
Requires:	nss-mdns%{_isa}

# GTK modules it expects to find for some reason.
Requires:	libcanberra-gtk2%{_isa}

# Once upon a time, we tried to split these out... but that's not worth the effort anymore.
Provides:	chromium-ffmpegsumo = %{version}-%{release}
Obsoletes:	chromium-ffmpegsumo <= 35.0.1916.114
# This is a lie. v8 has its own version... but I'm being lazy and not using it here.
# Barring Google getting much faster on the v8 side (or much slower on the Chromium side)
# the true v8 version will be much smaller than the Chromium version that it came from.
Provides:	chromium-v8 = %{version}-%{release}
Obsoletes:	chromium-v8 <= 3.25.28.18
# This is a lie. webrtc never had any real version. 0.2 is greater than 0.1
Provides:	webrtc = 0.2
Obsoletes:	webrtc <= 0.1
%if 0%{?shared}
Requires:       chromium-libs%{_isa} = %{version}-%{release}
# Nothing to do here. chromium-libs is real.
%else
Provides:	chromium-libs = %{version}-%{release}
Obsoletes:	chromium-libs <= %{version}-%{release}
%endif

ExclusiveArch:	x86_64 i686

# Bundled bits (I'm sure I've missed some)
Provides: bundled(angle) = 2422
Provides: bundled(bintrees) = 1.0.1
# This is a fork of openssl.
Provides: bundled(boringssl)
Provides: bundled(brotli)
Provides: bundled(bspatch)
Provides: bundled(cacheinvalidation) = 20150720
Provides: bundled(cardboard) = 0.5.4
Provides: bundled(colorama) = 799604a104
Provides: bundled(crashpad)
Provides: bundled(dmg_fp)
Provides: bundled(expat) = 2.1.0
Provides: bundled(fdmlibm) = 5.3
# Don't get too excited. MPEG and other legally problematic stuff is stripped out.
Provides: bundled(ffmpeg) = 2.6
Provides: bundled(fips181) = 2.2.3
Provides: bundled(fontconfig) = 2.11.0
Provides: bundled(gperftools) = svn144
Provides: bundled(gtk3) = 3.1.4
Provides: bundled(hunspell) = 1.3.2
Provides: bundled(iccjpeg)
%if 0%{?bundleicu}
Provides: bundled(icu) = 54.1
%endif
Provides: bundled(kitchensink) = 1
Provides: bundled(leveldb) = r80
Provides: bundled(libaddressinput) = 0
Provides: bundled(libjingle) = 9564
Provides: bundled(libphonenumber) = svn584
Provides: bundled(libsrtp) = 1.5.2
Provides: bundled(libvpx) = 1.4.0
Provides: bundled(libwebp) = 0.4.3
Provides: bundled(libXNVCtrl) = 302.17
Provides: bundled(libyuv) = 1444
Provides: bundled(lzma) = 9.20
Provides: bundled(libudis86) = 1.7.1
Provides: bundled(mesa) = 9.0.3
Provides: bundled(NSBezierPath) = 1.0
Provides: bundled(mozc)
Provides: bundled(mt19937ar) = 2002.1.26
Provides: bundled(ots) = 767d6040439e6ebcdb867271fcb686bd3f8ac739
Provides: bundled(protobuf) = r476
Provides: bundled(qcms) = 4
Provides: bundled(sfntly) = svn111
Provides: bundled(skia)
Provides: bundled(SMHasher) = 0
Provides: bundled(snappy) = r80
Provides: bundled(speech-dispatcher) = 0.7.1
Provides: bundled(sqlite) = 3.8.7.4
Provides: bundled(superfasthash) = 0
Provides: bundled(talloc) = 2.0.1
Provides: bundled(usrsctp) = 0
Provides: bundled(v8) = 4.5.103.35
Provides: bundled(webrtc) = 90usrsctp
Provides: bundled(woff2) = 445f541996fe8376f3976d35692fd2b9a6eedf2d
Provides: bundled(xdg-mime)
Provides: bundled(xdg-user-dirs)
Provides: bundled(x86inc) = 0
Provides: bundled(zlib) = 1.2.5

%description
Chromium is an open-source web browser, powered by WebKit (Blink).

%if 0%{?shared}
%package libs
Summary: Shared libraries used by chromium (and chrome-remote-desktop)

%description libs
Shared libraries used by chromium (and chrome-remote-desktop).
%endif

%package -n chrome-remote-desktop
Requires(pre): shadow-utils
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd
%if 0%{?shared}
Requires: chromium-libs%{_isa} = %{version}-%{release}
%endif
Summary: Remote desktop support for google-chrome & chromium

%description -n chrome-remote-desktop
Remote desktop support for google-chrome & chromium.

%prep
%setup -q -T -c -n %{name}-policies -a 10
%setup -q -T -c -n depot_tools -a 2
%if 0%{tests}
%setup -q -n chromium-%{version} -b 1
%else
%setup -q -n chromium-%{version}
%endif

### Chromium Fedora Patches ###
%patch0 -p1 -b .gcc5
%patch1 -p1 -b .pathmax
%patch2 -p1 -b .addrfix
%patch3 -p1 -b .system-icu
%patch4 -p1 -b .notest
%patch5 -p1 -b .cast_link_zlib
%patch6 -p1 -b .gnu-inline
%patch7 -p1 -b .ignore-fd-count
%patch8 -p1 -b .gcc6
%patch9 -p1 -b .modern-libusbx

### Chromium Tests Patches ###
%patch100 -p1 -b .use_system_opus
%patch101 -p1 -b .use_system_harfbuzz
%patch102 -p1 -b .sync_link_zlib


export CC="gcc"
export CXX="g++"
export AR="ar"
export RANLIB="ranlib"

%if 0%{?nacl}
# prep the nacl tree
mkdir -p out/Release/gen/sdk/linux_x86/nacl_x86_newlib
cp -a --no-preserve=context /usr/%{_arch}-nacl/* out/Release/gen/sdk/linux_x86/nacl_x86_newlib

mkdir -p out/Release/gen/sdk/linux_x86/nacl_arm_newlib
cp -a --no-preserve=context /usr/arm-nacl/* out/Release/gen/sdk/linux_x86/nacl_arm_newlib

# Not sure if we need this or not, but better safe than sorry.
pushd out/Release/gen/sdk/linux_x86
ln -s nacl_x86_newlib nacl_x86_newlib_raw
ln -s nacl_arm_newlib nacl_arm_newlib_raw
popd

mkdir -p out/Release/gen/sdk/linux_x86/nacl_x86_newlib/bin
pushd out/Release/gen/sdk/linux_x86/nacl_x86_newlib/bin
ln -s /usr/bin/x86_64-nacl-gcc gcc
ln -s /usr/bin/x86_64-nacl-gcc x86_64-nacl-gcc
ln -s /usr/bin/x86_64-nacl-g++ g++
ln -s /usr/bin/x86_64-nacl-g++ x86_64-nacl-g++
# ln -s /usr/bin/x86_64-nacl-ar ar
ln -s /usr/bin/x86_64-nacl-ar x86_64-nacl-ar
# ln -s /usr/bin/x86_64-nacl-as as
ln -s /usr/bin/x86_64-nacl-as x86_64-nacl-as
# ln -s /usr/bin/x86_64-nacl-ranlib ranlib
ln -s /usr/bin/x86_64-nacl-ranlib x86_64-nacl-ranlib
# Cleanups
rm addr2line
ln -s /usr/bin/x86_64-nacl-addr2line addr2line
rm c++filt
ln -s /usr/bin/x86_64-nacl-c++filt c++filt
rm gprof
ln -s /usr/bin/x86_64-nacl-gprof gprof
rm readelf
ln -s /usr/bin/x86_64-nacl-readelf readelf
rm size
ln -s /usr/bin/x86_64-nacl-size size
rm strings
ln -s /usr/bin/x86_64-nacl-strings strings
popd

mkdir -p out/Release/gen/sdk/linux_x86/nacl_arm_newlib/bin
pushd out/Release/gen/sdk/linux_x86/nacl_arm_newlib/bin
ln -s /usr/bin/arm-nacl-gcc gcc
ln -s /usr/bin/arm-nacl-gcc arm-nacl-gcc
ln -s /usr/bin/arm-nacl-g++ g++
ln -s /usr/bin/arm-nacl-g++ arm-nacl-g++
ln -s /usr/bin/arm-nacl-ar arm-nacl-ar
ln -s /usr/bin/arm-nacl-as arm-nacl-as
ln -s /usr/bin/arm-nacl-ranlib arm-nacl-ranlib
popd

touch out/Release/gen/sdk/linux_x86/nacl_x86_newlib/stamp.untar out/Release/gen/sdk/linux_x86/nacl_x86_newlib/stamp.prep
touch out/Release/gen/sdk/linux_x86/nacl_x86_newlib/nacl_x86_newlib.json
touch out/Release/gen/sdk/linux_x86/nacl_arm_newlib/stamp.untar out/Release/gen/sdk/linux_x86/nacl_arm_newlib/stamp.prep
touch out/Release/gen/sdk/linux_x86/nacl_arm_newlib/nacl_arm_newlib.json

pushd out/Release/gen/sdk/linux_x86/
mkdir -p pnacl_newlib pnacl_translator
# Might be able to do symlinks here, but eh.
cp -a --no-preserve=context /usr/pnacl_newlib/* pnacl_newlib/
cp -a --no-preserve=context /usr/pnacl_translator/* pnacl_translator/
for i in lib/libc.a lib/libc++.a lib/libg.a lib/libm.a; do
	/usr/pnacl_newlib/bin/pnacl-ranlib pnacl_newlib/x86_64_bc-nacl/$i
	/usr/pnacl_newlib/bin/pnacl-ranlib pnacl_newlib/i686_bc-nacl/$i
	/usr/pnacl_newlib/bin/pnacl-ranlib pnacl_newlib/le32-nacl/$i
done

for i in lib/clang/3.7.0/lib/x86_64_bc-nacl/libpnaclmm.a lib/clang/3.7.0/lib/i686_bc-nacl/libpnaclmm.a; do
	/usr/pnacl_newlib/bin/pnacl-ranlib pnacl_newlib/$i
done

for i in lib/clang/3.7.0/lib/le32-nacl/libpnaclmm.a lib/clang/3.7.0/lib/le32-nacl/libgcc.a; do
	/usr/pnacl_newlib/bin/pnacl-ranlib pnacl_newlib/$i
done

popd

mkdir -p native_client/toolchain/.tars/linux_x86
touch native_client/toolchain/.tars/linux_x86/pnacl_translator.json

pushd native_client/toolchain
ln -s ../../out/Release/gen/sdk/linux_x86 linux_x86
popd
%endif

export CHROMIUM_BROWSER_GYP_DEFINES="\
%ifarch x86_64
	-Dtarget_arch=x64 \
	-Dsystem_libdir=lib64 \
%endif
	-Dgoogle_api_key="%{api_key}" \
	-Dgoogle_default_client_id="%{default_client_id}" \
	-Dgoogle_default_client_secret="%{default_client_secret}" \
	\
	-Ddisable_glibc=1 \
	-Ddisable_sse2=1 \
%if 0%{?nonacl}
	-Ddisable_nacl=1 \
%else
	-Ddisable_newlib_untar=1 \
	-Ddisable_pnacl_untar=1 \
	-Dpnacl_newlib_toolchain=out/Release/gen/sdk/linux_x86/pnacl_newlib/ \
	-Dpnacl_translator_dir=/usr/pnacl_translator \
%endif
	\
	-Duse_gconf=0 \
	-Duse_gio=1 \
	-Duse_gnome_keyring=1 \
	-Duse_pulseaudio=1 \
	-Duse_system_bzip2=1 \
	-Duse_system_flac=1 \
	-Duse_system_harfbuzz=1 \
%if 0%{?bundleicu}
%else
	-Duse_system_icu=1 \
%endif
	-Dicu_use_data_file_flag=0 \
	-Duse_system_jsoncpp=1 \
	-Duse_system_libevent=1 \
	-Duse_system_libexif=1 \
	-Duse_system_libjpeg=1 \
	-Duse_system_libpng=1 \
	-Duse_system_libusb=1 \
	-Duse_system_libxml=1 \
	-Duse_system_libxslt=1 \
	-Duse_system_minizip=1 \
	-Duse_system_nspr=1 \
	-Duse_system_opus=1 \
	-Duse_system_protobuf=0 \
	-Duse_system_re2=1 \
	-Duse_system_speex=1 \
	-Duse_system_libsrtp=0 \
	-Duse_system_xdg_utils=1 \
	-Duse_system_yasm=1 \
	-Duse_system_zlib=0 \
	-Duse_system_libevent=1 \
	\
	-Dlinux_link_libspeechd=1 \
	-Dlinux_link_gnome_keyring=1 \
	-Dlinux_link_gsettings=1 \
	-Dlinux_link_libpci=1 \
	-Dlinux_link_libgps=0 \
	-Dlinux_sandbox_path=%{chromium_path}/chrome-sandbox \
	-Dlinux_sandbox_chrome_path=%{chromium_path}/chromium-browser \
	-Dlinux_strip_binary=1 \
	-Dlinux_use_bundled_binutils=0 \
	-Dlinux_use_bundled_gold=0 \
	-Dlinux_use_gold_binary=0 \
	-Dlinux_use_gold_flags=0 \
	-Dlinux_use_libgps=0 \
	\
	-Dusb_ids_path=/usr/share/hwdata/usb.ids \
	-Dlibspeechd_h_prefix=speech-dispatcher/ \
	\
	-Dffmpeg_branding=Chromium \
	-Dproprietary_codecs=0 \
%if 0%{?shared}
	-Dbuild_ffmpegsumo=1 \
	-Dffmpeg_component=shared_library \
%else
	-Dffmpeg_component=static_library \
%endif
	\
	-Dno_strict_aliasing=1 \
	-Dv8_no_strict_aliasing=1 \
	-Dclang=0 \
	-Dhost_clang=0 \
	\
	-Dremove_webcore_debug_symbols=1 \
	-Dlogging_like_official_build=1 \
	-Denable_hotwording=0 \
	-Dbuildtype=Official \
	\
%if 0%{?shared}
	-Dcomponent=shared_library \
%endif
	-Dwerror="

# Remove most of the bundled libraries. Libraries specified below (taken from
# Gentoo's Chromium ebuild) are the libraries that needs to be preserved.
build/linux/unbundle/remove_bundled_libraries.py \
	'third_party/ffmpeg' \
	'third_party/adobe' \
	'third_party/flac' \
	'third_party/harfbuzz-ng' \
	'third_party/icu' \
	'third_party/libevent' \
	'third_party/libjpeg_turbo' \
	'third_party/libpng' \
	'third_party/libsrtp' \
	'third_party/libwebp' \
	'third_party/libxml' \
	'third_party/libxslt' \
	'third_party/re2' \
	'third_party/snappy' \
	'third_party/speech-dispatcher' \
	'third_party/usb_ids' \
	'third_party/xdg-utils' \
	'third_party/yasm' \
	'third_party/zlib' \
	'base/third_party/dmg_fp' \
	'base/third_party/dynamic_annotations' \
	'base/third_party/icu' \
	'base/third_party/nspr' \
	'base/third_party/superfasthash' \
	'base/third_party/symbolize' \
	'base/third_party/valgrind' \
	'base/third_party/xdg_mime' \
	'base/third_party/xdg_user_dirs' \
	'breakpad/src/third_party/curl' \
	'chrome/third_party/mozilla_security_manager' \
	'courgette/third_party' \
	'crypto/third_party/nss' \
	'native_client/src/third_party/dlmalloc' \
	'net/third_party/mozilla_security_manager' \
	'net/third_party/nss' \
	'third_party/WebKit' \
	'third_party/analytics' \
	'third_party/angle' \
	'third_party/angle/src/third_party/compiler' \
	'third_party/angle/src/third_party/murmurhash' \
	'third_party/angle/src/third_party/trace_event' \
	'third_party/boringssl' \
	'third_party/brotli' \
	'third_party/cacheinvalidation' \
	'third_party/catapult' \
	'third_party/catapult/tracing/third_party/components/polymer' \
	'third_party/catapult/tracing/third_party/d3' \
	'third_party/catapult/tracing/third_party/gl-matrix' \
	'third_party/catapult/tracing/third_party/jszip' \
	'third_party/catapult/third_party/py_vulcanize' \
	'third_party/catapult/third_party/py_vulcanize/third_party/rcssmin' \
	'third_party/catapult/third_party/py_vulcanize/third_party/rjsmin' \
	'third_party/cld_2' \
	'third_party/cros_system_api' \
	'third_party/cython/python_flags.py' \
	'third_party/devscripts' \
	'third_party/dom_distiller_js' \
	'third_party/dom_distiller_js/dist/proto_gen/third_party/dom_distiller_js' \
	'third_party/fips181' \
	'third_party/flot' \
	'third_party/google_input_tools' \
	'third_party/google_input_tools/third_party/closure_library' \
	'third_party/google_input_tools/third_party/closure_library/third_party/closure' \
	'third_party/hunspell' \
	'third_party/iccjpeg' \
	'third_party/jstemplate' \
	'third_party/khronos' \
	'third_party/leveldatabase' \
	'third_party/libXNVCtrl' \
	'third_party/libaddressinput' \
	'third_party/libjingle' \
	'third_party/libphonenumber' \
	'third_party/libsecret' \
	'third_party/libudev' \
	'third_party/libusb' \
	'third_party/libvpx_new' \
	'third_party/libvpx_new/source/libvpx/third_party/x86inc' \
	'third_party/libxml/chromium' \
	'third_party/libwebm' \
	'third_party/libyuv' \
	'third_party/lss' \
	'third_party/lzma_sdk' \
	'third_party/mesa' \
	'third_party/modp_b64' \
	'third_party/mojo' \
	'third_party/mt19937ar' \
	'third_party/npapi' \
	'third_party/openmax_dl' \
	'third_party/opus' \
	'third_party/ots' \
	'third_party/pdfium' \
	'third_party/pdfium/third_party/agg23' \
	'third_party/pdfium/third_party/base' \
	'third_party/pdfium/third_party/bigint' \
	'third_party/pdfium/third_party/freetype' \
	'third_party/pdfium/third_party/lcms2-2.6' \
	'third_party/pdfium/third_party/libjpeg' \
	'third_party/pdfium/third_party/libopenjpeg20' \
	'third_party/pdfium/third_party/zlib_v128' \
	'third_party/polymer' \
	'third_party/protobuf' \
	'third_party/ply' \
	'third_party/qcms' \
	'third_party/sfntly' \
	'third_party/skia' \
	'third_party/smhasher' \
	'third_party/sqlite' \
	'third_party/tcmalloc' \
	'third_party/usrsctp' \
	'third_party/web-animations-js' \
	'third_party/webdriver' \
	'third_party/webrtc' \
	'third_party/widevine' \
	'third_party/x86inc' \
	'third_party/zlib/google' \
	'url/third_party/mozilla' \
	'v8/src/third_party/fdlibm' \
	'v8/src/third_party/valgrind' \
	--do-remove

# Look, I don't know. This package is spit and chewing gum. Sorry.
rm -rf third_party/jinja2
ln -s %{python_sitelib}/jinja2 third_party/jinja2
rm -rf third_party/markupsafe
ln -s %{python_sitearch}/markupsafe third_party/markupsafe
# We should look on removing other python packages as well i.e. ply

# Fix hardcoded path in remoting code
sed -i 's|/opt/google/chrome-remote-desktop|%{crd_path}|g' remoting/host/setup/daemon_controller_delegate_linux.cc

# Update gyp files according to our configuration
# If you will change something in the configuration please update it
# for build/gyp_chromium as well (and vice versa).
build/linux/unbundle/replace_gyp_files.py $CHROMIUM_BROWSER_GYP_DEFINES

build/gyp_chromium \
	--depth . \
	$CHROMIUM_BROWSER_GYP_DEFINES

# hackity hack hack
rm -rf third_party/libusb/src/libusb/libusb.h

%build

%if %{?tests}
# Tests targets taken from testing/buildbot/chromium.linux.json and obtained with
# get_linux_tests_name.py PATH_TO_UNPACKED_CHROMIUM_SOURCES --spec
# You can also check if you have to update the tests in SPEC file by running
# get_linux_tests_name.py PATH_TO_UNPACKED_CHROMIUM_SOURCES --check PATH_TO_SPEC_FILE
export CHROMIUM_BROWSER_UNIT_TESTS="\
	accessibility_unittests \
	app_list_unittests \
	app_shell_unittests \
	aura_unittests \
	base_unittests \
	browser_tests \
	cacheinvalidation_unittests \
	cast_unittests \
	cc_unittests \
	chromedriver_unittests \
	components_browsertests \
	components_unittests \
	compositor_unittests \
	content_browsertests \
	content_unittests \
	crypto_unittests \
	dbus_unittests \
	device_unittests \
	display_unittests \
	events_unittests \
	extensions_browsertests \
	extensions_unittests \
	gcm_unit_tests \
	gfx_unittests \
	gl_unittests \
	gn_unittests \
	google_apis_unittests \
	gpu_unittests \
	interactive_ui_tests \
	ipc_mojo_unittests \
	ipc_tests \
	jingle_unittests \
	media_unittests \
	midi_unittests \
	mojo_common_unittests \
	mojo_public_bindings_unittests \
	mojo_public_environment_unittests \
	mojo_public_system_unittests \
	mojo_public_utility_unittests \
	mojo_system_unittests \
%if 0%{?nacl}
	nacl_loader_unittests \
%endif
	net_unittests \
	ppapi_unittests \
	printing_unittests \
	remoting_unittests \
	sandbox_linux_unittests \
	skia_unittests \
	sql_unittests \
	sync_integration_tests \
	sync_unit_tests \
	ui_base_unittests \
	ui_touch_selection_unittests \
	unit_tests \
	url_unittests \
	views_unittests \
	wm_unittests \
	"
%else
export CHROMIUM_BROWSER_UNIT_TESTS=
%endif


%global target out/Release

../depot_tools/ninja -C %{target} -vvv chrome chrome_sandbox policy_templates $CHROMIUM_BROWSER_UNIT_TESTS

# remote client
pushd remoting
../../depot_tools/ninja -C ../%{target} -vvv remoting_me2me_host remoting_start_host remoting_it2me_native_messaging_host remoting_me2me_native_messaging_host remoting_native_messaging_manifests remoting_resources
%if 0%{?build_remoting_app}
%if 0%{?nacl}
GOOGLE_CLIENT_ID_REMOTING_IDENTITY_API=%{chromoting_client_id} ../../depot_tools/ninja -vv -C ../out/Release/ remoting_webapp
%endif
%endif
popd


%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{chromium_path}
cp -a %{SOURCE3} %{buildroot}%{chromium_path}/%{chromium_browser_channel}.sh
export BUILDTARGET=`cat /etc/redhat-release`
export CHROMIUM_PATH=%{chromium_path}
export CHROMIUM_BROWSER_CHANNEL=%{chromium_browser_channel}
sed -i "s|@@BUILDTARGET@@|$BUILDTARGET|g" %{buildroot}%{chromium_path}/%{chromium_browser_channel}.sh
sed -i "s|@@CHROMIUM_PATH@@|$CHROMIUM_PATH|g" %{buildroot}%{chromium_path}/%{chromium_browser_channel}.sh
sed -i "s|@@CHROMIUM_BROWSER_CHANNEL@@|$CHROMIUM_BROWSER_CHANNEL|g" %{buildroot}%{chromium_path}/%{chromium_browser_channel}.sh
%if "%{chromium_channel}" == "%%{nil}"
# Enable debug outputs for beta and dev channels
export EXTRA_FLAGS="--enable-logging=stderr --v=2"
sed -i "s|@@EXTRA_FLAGS@@|$EXTRA_FLAGS|g" %{buildroot}%{chromium_path}/%{chromium_browser_channel}.sh
%else
sed -i "s|@@EXTRA_FLAGS@@||g" %{buildroot}%{chromium_path}/%{chromium_browser_channel}.sh
%endif

ln -s %{chromium_path}/%{chromium_browser_channel}.sh %{buildroot}%{_bindir}/%{chromium_browser_channel}
mkdir -p %{buildroot}%{_mandir}/man1/

pushd %{target}
cp -a *.pak locales resources %{buildroot}%{chromium_path}
%if 0%{?nacl}
cp -a nacl_helper* *.nexe pnacl tls_edit %{buildroot}%{chromium_path}
chmod -x %{buildroot}%{chromium_path}/nacl_helper_bootstrap* *.nexe
%endif
cp -a protoc pseudo_locales pyproto %{buildroot}%{chromium_path}
cp -a chrome %{buildroot}%{chromium_path}/%{chromium_browser_channel}
cp -a chrome_sandbox %{buildroot}%{chromium_path}/chrome-sandbox
cp -a chrome.1 %{buildroot}%{_mandir}/man1/%{chromium_browser_channel}.1
# V8 initial snapshots
# https://code.google.com/p/chromium/issues/detail?id=421063
cp -a natives_blob.bin %{buildroot}%{chromium_path}
cp -a snapshot_blob.bin %{buildroot}%{chromium_path}
%if 0%{?shared}
cp -a lib %{buildroot}%{chromium_path}
%endif

# Remote desktop bits
mkdir -p %{buildroot}%{crd_path}

%if 0%{?shared}
pushd %{buildroot}%{crd_path}
ln -s %{chromium_path}/lib lib
popd
%endif

# See remoting/host/installer/linux/Makefile for logic
cp -a native_messaging_host %{buildroot}%{crd_path}/native-messaging-host
cp -a remote_assistance_host %{buildroot}%{crd_path}/remote-assistance-host
cp -a remoting_locales %{buildroot}%{crd_path}/
cp -a remoting_me2me_host %{buildroot}%{crd_path}/chrome-remote-desktop-host
cp -a remoting_start_host %{buildroot}%{crd_path}/start-host

# chromium
mkdir -p %{buildroot}%{_sysconfdir}/chromium/native-messaging-hosts
# google-chrome
mkdir -p %{buildroot}%{_sysconfdir}/opt/chrome/
cp -a remoting/* %{buildroot}%{_sysconfdir}/chromium/native-messaging-hosts/
for i in %{buildroot}%{_sysconfdir}/chromium/native-messaging-hosts/*.json; do
	sed -i 's|/opt/google/chrome-remote-desktop|%{crd_path}|g' $i
done
pushd %{buildroot}%{_sysconfdir}/opt/chrome/
ln -s ../../chromium/native-messaging-hosts native-messaging-hosts
popd

mkdir -p %{buildroot}/var/lib/chrome-remote-desktop
touch %{buildroot}/var/lib/chrome-remote-desktop/hashes

mkdir -p %{buildroot}%{_sysconfdir}/pam.d/
pushd %{buildroot}%{_sysconfdir}/pam.d/
ln -s system-auth chrome-remote-desktop
popd

%if 0%{?build_remoting_app}
%if 0%{?nacl}
cp -a remoting_client_plugin_newlib.* %{buildroot}%{chromium_path}
%endif
%endif
popd

cp -a remoting/host/linux/linux_me2me_host.py %{buildroot}%{crd_path}/chrome-remote-desktop
cp -a remoting/host/installer/linux/is-remoting-session %{buildroot}%{crd_path}/

mkdir -p %{buildroot}%{_unitdir}
cp -a %{SOURCE11} %{buildroot}%{_unitdir}/
sed -i 's|@@CRD_PATH@@|%{crd_path}|g' %{buildroot}%{_unitdir}/chrome-remote-desktop.service

# Add directories for policy management
mkdir -p %{buildroot}%{_sysconfdir}/chromium/policies/managed
mkdir -p %{buildroot}%{_sysconfdir}/chromium/policies/recommended
cp -a ../%{name}-policies/common/html/en-US/*.html .

# linux json files no longer in .zip file
#cp -a ../%{name}-policies/linux/examples/*.json .
cp -a out/Release/gen/chrome/app/policy/linux/examples/chrome.json .

mkdir -p %{buildroot}%{_datadir}/icons/hicolor/256x256/apps
cp -a chrome/app/theme/chromium/product_logo_256.png %{buildroot}%{_datadir}/icons/hicolor/256x256/apps/%{chromium_browser_channel}.png

mkdir -p %{buildroot}%{_datadir}/applications/
desktop-file-install --dir %{buildroot}%{_datadir}/applications %{SOURCE4}

mkdir -p %{buildroot}%{_datadir}/gnome-control-center/default-apps/
cp -a %{SOURCE9} %{buildroot}%{_datadir}/gnome-control-center/default-apps/

%check
%if 0%{tests}
%if 0%{?tests_force_display}
	export DISPLAY=:0
%else
	Xvfb :9 -screen 0 1024x768x24 &

	export XVFB_PID=$!
	export DISPLAY=:9
%endif
	export LC_ALL="en_US.utf8"

	sleep 5

	# Run tests and disable the failed ones
	pushd %{target}
	(
	cp -f chrome_sandbox chrome-sandbox
	echo "Test sandbox needs to be owned by root and have the suid set"
	if [ "$(id -u)" != "0" ]; then
		sudo chown root:root chrome-sandbox && sudo chmod 4755 chrome-sandbox
	else
		chown root:root chrome-sandbox && chmod 4755 chrome-sandbox
	fi

	# Example of failed or timed-out test annotation
	# ./browser_tests \
	#	--gtest_filter=-"\
	#		`#failed`\
	#		SandboxStatusUITest.testBPFSandboxEnabled:`#failed - not using BPF sandbox`\
	#		:\
	#		`#timed-out`\
	#		CalculatorBrowserTest.Model:\
	#		WebRtcBrowserTest.RunsAudioVideoWebRTCCallInTwoTabs\
	#	" \

	./accessibility_unittests && \
	./app_list_unittests && \
	./app_shell_unittests && \
	./aura_unittests && \
	./base_unittests \
		--gtest_filter=-"\
			`#failed`\
			ICUStringConversionsTest.ConvertToUtf8AndNormalize\
		" \
	&& \
	./browser_tests \
		--gtest_filter=-"\
			`#failed`\
			DevToolsSanityTest.TestNetworkRawHeadersText:\
			DevToolsSanityTest.TestNetworkSize:\
			DevToolsSanityTest.TestNetworkSyncSize:\
			ExtensionWebstoreGetWebGLStatusTest.Allowed:\
			InlineLoginUISafeIframeBrowserTest.Basic:\
			InlineLoginUISafeIframeBrowserTest.ConfirmationRequiredForNonsecureSignin:\
			InlineLoginUISafeIframeBrowserTest.NoWebUIInIframe:\
			InlineLoginUISafeIframeBrowserTest.TopFrameNavigationDisallowed:\
			OutOfProcessPPAPITest.Graphics3D:\
			PolicyTest.Disable3DAPIs:\
			WebRtcWebcamBrowserTests/WebRtcWebcamBrowserTest.TestAcquiringAndReacquiringWebcam/0:\
			:\
			`#timed-out`\
			CalculatorBrowserTest.Model:\
			ImageFetcherImplBrowserTest.MultipleFetch:\
			ProfileManagerBrowserTest.DeletePasswords:\
			TabCaptureApiPixelTest.EndToEndThroughWebRTC:\
			WebRtcBrowserTest.RunsAudioVideoWebRTCCallInTwoTabs:\
			WebRtcSimulcastBrowserTest.TestVgaReturnsTwoSimulcastStreams\
		" \
	&& \
	./cacheinvalidation_unittests && \
	./cast_unittests && \
	./cc_unittests && \
	./chromedriver_unittests && \
	./components_unittests \
		--gtest_filter=-"\
			`#failed`\
			AutocompleteMatchTest.Duplicates:\
			BookmarkIndexTest.GetBookmarksMatchingWithURLs:\
			BookmarkIndexTest.MatchPositionsURLs:\
			InMemoryURLIndexTypesTest.StaticFunctions:\
			ScoredHistoryMatchTest.GetTopicalityScore:\
			ScoredHistoryMatchTest.Inlining:\
			ScoredHistoryMatchTest.ScoringTLD:\
			UrlFormatterTest.FormatUrlWithOffsets:\
			UrlFormatterTest.IDNToUnicodeFast:\
			UrlFormatterTest.IDNToUnicodeSlow\
		" \
	&& \
	./components_browsertests \
		--gtest_filter=-"\
			`#failed`\
			AutofillRiskFingerprintTest.GetFingerprint\
		" \
	&& \
	./compositor_unittests && \
	./content_browsertests \
		--gtest_filter=-"\
			`#failed`\
			BrowserGpuChannelHostFactoryTest.:\
			BrowserGpuChannelHostFactoryTest.AlreadyEstablished:\
			BrowserGpuChannelHostFactoryTest.Basic:\
			ImageTransportFactoryBrowserTest.TestLostContext:\
			ImageTransportFactoryTearDownBrowserTest.LoseOnTearDown:\
			RenderViewImplTest.GetCompositionCharacterBoundsTest:\
			SignalTest.BasicSignalQueryTest:\
			SignalTest.BasicSignalSyncPointTest:\
			SignalTest.InvalidSignalQueryUnboundTest:\
			SignalTest.InvalidSignalSyncPointTest:\
			SignalTest.SignalQueryUnboundTest:\
			WebRtcBrowserTest.*:\
			:\
			`#timed-out`\
			WebRtcAecDumpBrowserTest.CallWithAecDump:\
			WebRtcAecDumpBrowserTest.CallWithAecDumpEnabledThenDisabled\
		" \
	&& \
	./content_unittests && \
	./crypto_unittests && \
	./dbus_unittests \
		--gtest_filter=-"\
			`#crashed`\
			EndToEndAsyncTest.InvalidObjectPath:\
			EndToEndAsyncTest.InvalidServiceName:\
			EndToEndSyncTest.InvalidObjectPath:\
			EndToEndSyncTest.InvalidServiceName:\
			MessageTest.SetInvalidHeaders\
		" \
	&& \
	./device_unittests && \
	./display_unittests && \
	./events_unittests && \
	./extensions_browsertests && \
	./extensions_unittests && \
	./gcm_unit_tests && \
	./gfx_unittests \
		--gtest_filter=-"\
			`#failed - missing Microsoft TrueType fonts`\
			FontListTest.Fonts_GetHeight_GetBaseline:\
			FontRenderParamsTest.Default:\
			FontRenderParamsTest.MissingFamily:\
			FontRenderParamsTest.Size:\
			FontRenderParamsTest.Style:\
			FontRenderParamsTest.SubstituteFamily:\
			FontRenderParamsTest.UseBitmaps:\
			FontTest.GetActualFontNameForTesting:\
			FontTest.LoadArial:\
			FontTest.LoadArialBold:\
			PlatformFontLinuxTest.DefaultFont:\
			RenderTextTest.HarfBuzz_FontListFallback:\
			RenderTextTest.SetFontList:\
			RenderTextTest.StringSizeRespectsFontListMetrics\
			:\
			`#crashed`\
			FontRenderParamsTest.Default:\
			FontRenderParamsTest.ForceFullHintingWhenAntialiasingIsDisabled:\
			FontRenderParamsTest.MissingFamily:\
			FontRenderParamsTest.NoFontconfigMatch:\
			FontRenderParamsTest.OnlySetConfiguredValues:\
			FontRenderParamsTest.Scalable:\
			FontRenderParamsTest.Size:\
			FontRenderParamsTest.Style:\
			FontRenderParamsTest.SubstituteFamily:\
			FontRenderParamsTest.UseBitmaps:\
			PlatformFontLinuxTest.DefaultFont\
		" \
	&& \
	./gl_unittests && \
	./gn_unittests \
		--gtest_filter=-"\
			`#failed`\
			Format.004:\
			Format.007:\
			Format.012:\
			Format.013:\
			Format.014:\
			Format.015:\
			Format.017:\
			Format.019:\
			Format.020:\
			Format.021:\
			Format.023:\
			Format.031:\
			Format.033:\
			Format.038:\
			Format.043:\
			Format.046:\
			Format.048:\
			Format.056:\
			Format.057:\
			Format.062:\
			ParseTree.SortRangeExtraction:\
			Parser.CommentsAtEndOfBlock:\
			Parser.CommentsConnectedInList:\
			Parser.CommentsEndOfBlockSingleLine:\
			Parser.CommentsLineAttached:\
			Parser.CommentsSuffix:\
			Parser.CommentsSuffixDifferentLine:\
			Parser.CommentsSuffixMultiple\
		" \
	&& \
	./google_apis_unittests && \
	./gpu_unittests && \
	./interactive_ui_tests \
		--gtest_filter=-"\
			`#failed`\
			AshNativeCursorManagerTest.CursorChangeOnEnterNotify:\
			BookmarkBarViewTest5.DND:\
			OmniboxViewViewsTest.DeactivateTouchEditingOnExecuteCommand:\
			OmniboxViewViewsTest.SelectAllOnTap:\
			StartupBrowserCreatorTest.LastUsedProfileActivated:\
			X11TopmostWindowFinderTest.Basic:\
			X11TopmostWindowFinderTest.Menu:\
			:\
			`#timed-out`\
			BookmarkBarViewTest9.ScrollButtonScrolls:\
			DockedPanelBrowserTest.CloseSqueezedPanels:\
			DockedPanelBrowserTest.MinimizeSqueezedActive:\
			GlobalCommandsApiTest.GlobalCommand\
		" \
	&& \
	./ipc_mojo_unittests && \
	./ipc_tests && \
	./jingle_unittests && \
	./midi_unittests && \
	./media_unittests && \
	./mojo_common_unittests && \
	./mojo_public_bindings_unittests && \
	./mojo_public_environment_unittests && \
	./mojo_public_system_unittests && \
	./mojo_public_utility_unittests && \
	./mojo_system_unittests && \
%if 0%{?nacl}
	./nacl_loader_unittests && \
%endif
	./net_unittests \
		--gtest_filter=-"\
			`#failed`\
			CertVerifyProcTest.TestKnownRoot\
		" \
	&& \
	./ppapi_unittests && \
	./printing_unittests && \
	./remoting_unittests && \
	./sandbox_linux_unittests && \
	./skia_unittests && \
	./sql_unittests && \
	./ui_base_unittests && \
	./ui_touch_selection_unittests && \
	./sync_unit_tests && \
	./unit_tests \
		--gtest_filter=-"\
			`#failed - some need https://chromium.googlesource.com/chromium/deps/hunspell_dictionaries/+/master`\
			BookmarkProviderTest.StripHttpAndAdjustOffsets:\
			HQPOrderingTest.TEAMatch:\
			HistoryQuickProviderTest.ContentsClass:\
			LimitedInMemoryURLIndexTest.Initialization:\
			MultilingualSpellCheckTest.MultilingualSpellCheckParagraph:\
			MultilingualSpellCheckTest.MultilingualSpellCheckSuggestions:\
			MultilingualSpellCheckTest.MultilingualSpellCheckWord:\
			MultilingualSpellCheckTest.MultilingualSpellCheckWordEnglishSpanish:\
			SpellCheckTest.CreateTextCheckingResultsKeepsMarkers:\
			SpellCheckTest.DictionaryFiles:\
			SpellCheckTest.EnglishWords:\
			SpellCheckTest.GetAutoCorrectionWord_EN_US:\
			SpellCheckTest.LogicalSuggestions:\
			SpellCheckTest.MisspelledWords:\
			SpellCheckTest.NoSuggest:\
			SpellCheckTest.SpellCheckParagraphLongSentenceMultipleMisspellings:\
			SpellCheckTest.SpellCheckParagraphMultipleMisspellings:\
			SpellCheckTest.SpellCheckParagraphSingleMisspellings:\
			SpellCheckTest.SpellCheckStrings_EN_US:\
			SpellCheckTest.SpellCheckSuggestions_EN_US:\
			SpellCheckTest.SpellingEngine_CheckSpelling:\
			SpellcheckWordIteratorTest.FindSkippableWordsKhmer:\
			:\
			`#crashed`\
			ListChangesTaskTest.UnderTrackedFolder:\
			ListChangesTaskTest.UnrelatedChange:\
			SpellCheckTest.RequestSpellCheckWithMisspellings:\
			SpellCheckTest.RequestSpellCheckWithMultipleRequests:\
			SpellCheckTest.RequestSpellCheckWithSingleMisspelling\
		" \
	&& \
	./url_unittests && \
	./views_unittests \
		--gtest_filter=-"\
			`#failed`\
			DesktopWindowTreeHostX11HighDPITest.LocatedEventDispatchWithCapture:\
			LabelTest.FontPropertySymbol:\
			WidgetTest.WindowMouseModalityTest\
		" \
	&& \
	./wm_unittests \
	)
	popd

	if [ -n "$XVFB_PID" ]; then
		kill $XVFB_PID
		unset XVFB_PID
		unset DISPLAY
	fi
%endif

%clean
rm -rf %{buildroot}

%post
# Set SELinux labels - semanage itself will adjust the lib directory naming
semanage fcontext -a -t bin_t /usr/lib/%{chromium_browser_channel}
semanage fcontext -a -t bin_t /usr/lib/%{chromium_browser_channel}/%{chromium_browser_channel}.sh
semanage fcontext -a -t chrome_sandbox_exec_t /usr/lib/chrome-sandbox
restorecon -R -v %{chromium_path}/%{chromium_browser_channel}

touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :
update-desktop-database &> /dev/null || :

%postun
if [ $1 -eq 0 ] ; then
	touch --no-create %{_datadir}/icons/hicolor &>/dev/null
	gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi
update-desktop-database &> /dev/null || :

%posttrans
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :

%pre -n chrome-remote-desktop
getent group chrome-remote-desktop >/dev/null || groupadd -r chrome-remote-desktop

%post -n chrome-remote-desktop
%systemd_post chrome-remote-desktop.service

%preun -n chrome-remote-desktop
%systemd_preun chrome-remote-desktop.service

%postun -n chrome-remote-desktop
%systemd_postun_with_restart chrome-remote-desktop.service

%files
%defattr(-,root,root,-)
%{_bindir}/%{chromium_browser_channel}
%dir %{chromium_path}
%{chromium_path}/*.bin
%{chromium_path}/*.pak
%{chromium_path}/%{chromium_browser_channel}
%{chromium_path}/%{chromium_browser_channel}.sh
%if 0%{?nacl}
%{chromium_path}/nacl_helper*
%{chromium_path}/*.nexe
%{chromium_path}/pnacl/
%{chromium_path}/tls_edit
%endif
%{chromium_path}/protoc
# %%{chromium_path}/remoting_locales/
%{chromium_path}/pseudo_locales/
# %%{chromium_path}/plugins/
%{chromium_path}/pyproto/
%attr(4755, root, root) %{chromium_path}/chrome-sandbox
%{chromium_path}/locales/
%{chromium_path}/resources/
%{_mandir}/man1/%{chromium_browser_channel}.*
%{_datadir}/icons/hicolor/256x256/apps/%{chromium_browser_channel}.png
%{_datadir}/applications/*.desktop
%{_datadir}/gnome-control-center/default-apps/chromium-browser.xml

%dir %{_sysconfdir}/chromium/policies/managed
%dir %{_sysconfdir}/chromium/policies/recommended
%doc chrome_policy_list.html *.json

%if 0%{?shared}
%files libs
%{chromium_path}/lib/
%endif

%files -n chrome-remote-desktop
%{crd_path}/chrome-remote-desktop
%{crd_path}/chrome-remote-desktop-host
%{crd_path}/is-remoting-session
%if 0%{?shared}
%{crd_path}/lib
%endif
%{crd_path}/native-messaging-host
%{crd_path}/remote-assistance-host
%{_sysconfdir}/pam.d/chrome-remote-desktop
%{_sysconfdir}/chromium/native-messaging-hosts/
%{_sysconfdir}/opt/chrome/
%{crd_path}/remoting_locales/
%{crd_path}/start-host
%{_unitdir}/chrome-remote-desktop.service
/var/lib/chrome-remote-desktop/
%if 0%{?build_remoting_app}
%if 0%{?nacl}
%{chromium_path}/remoting_client_plugin_newlib.*
%endif
%endif

%changelog
* Wed Feb 24 2016 Tom Callaway <spot@fedoraproject.org> 48.0.2564.116-1
- Update to 48.0.2564.116
- conditionalize icu properly
- fix libusbx handling (bz1270324)

* Wed Feb 17 2016 Tom Callaway <spot@fedoraproject.org> 48.0.2564.103-2
- fixes for gcc6

* Mon Feb  8 2016 Tom Callaway <spot@fedoraproject.org> 48.0.2564.103-1
- update to 48.0.2564.103
- use bundled libsrtp (because upstream has coded themselves into an ugly corner)

* Fri Jan 22 2016 Tom Callaway <spot@fedoraproject.org> 48.0.2564.82-1
- update to 48.0.2564.82

* Fri Jan 15 2016 Tom Callaway <spot@fedoraproject.org> 47.0.2526.111-1
- update to 47.0.2526.111

* Thu Jan 07 2016 Tomas Popela <tpopela@redhat.com> 47.0.2526.106-2
- compare hashes when downloading the tarballs
- Google started to include the Debian sysroots in tarballs - remove them while
  processing the tarball
- add a way to not use the system display server for tests instead of Xvfb
- update the depot_tools checkout to get some GN fixes
- use the remove_bundled_libraries script
- update the clean_ffmpeg script to print errors when some files that we are
  processing are missing
- update the clean_ffmpeg script to operate on tarball's toplevel folder
- don't show comments as removed tests in get_linux_tests_names script
- rework the process_ffmpeg_gyp script (also rename it to
  get_free_ffmpeg_source_files) to use the GN files insted of GYP (but we still
  didn't switched to GN build)

* Wed Dec 16 2015 Tom Callaway <spot@fedoraproject.org> 47.0.2526.106-1
- update to 47.0.2526.106

* Tue Dec 15 2015 Tom Callaway <spot@fedoraproject.org> 47.0.2526.80-4
- entirely patch out the broken fd counter from the nacl loader code
  killing it with fire would be better, but then chromium is on fire
  and that somehow makes it worse.

* Mon Dec 14 2015 Tom Callaway <spot@fedoraproject.org> 47.0.2526.80-3
- revert nacl fd patch (now we see 6 fds! 6 LIGHTS!)

* Fri Dec 11 2015 Tom Callaway <spot@fedoraproject.org> 47.0.2526.80-2
- build everything shared, but when we do shared builds, make -libs subpackage
- make chrome-remote-desktop dep on -libs subpackage in shared builds

* Wed Dec  9 2015 Tom Callaway <spot@fedoraproject.org> 47.0.2526.80-1
- update to 47.0.2526.80
- only build ffmpeg shared, not any other libs
  this is because if we build the other libs shared, then our
  chrome-remote-desktop build deps on those libs and we do not want that

* Tue Dec  8 2015 Tom Callaway <spot@fedoraproject.org> 47.0.2526.73-2
- The nacl loader claims it sees 7 fds open ALL THE TIME, and fails
  So, we tell it that it is supposed to see 7.
  I suspect building with shared objects is causing this disconnect.

* Wed Dec  2 2015 Tom Callaway <spot@fedoraproject.org> 47.0.2526.73-1
- update to 47.0.2526.73
- rework chrome-remote-desktop subpackage to work for google-chrome and chromium

* Wed Dec  2 2015 Tomas Popela <tpopela@redhat.com> 47.0.2526.69-1
- Update to 47.0.2526.69

* Tue Dec  1 2015 Tom Callaway <spot@fedoraproject.org> 46.0.2490.86-4
- still more remote desktop changes

* Mon Nov 30 2015 Tom Callaway <spot@fedoraproject.org> 46.0.2490.86-3
- lots of remote desktop cleanups

* Thu Nov 12 2015 Tom Callaway <spot@fedoraproject.org> 46.0.2490.86-2
- re-enable Requires/BuildRequires for libusbx
- add remote-desktop subpackage

* Wed Nov 11 2015 Tomas Popela <tpopela@redhat.com> 46.0.2490.86-1
- update to 46.0.2490.86
- clean the SPEC file
- add support for policies: https://www.chromium.org/administrators/linux-quick-start
- replace exec_mem_t SELinux label with bin_t - see rhbz#1281437
- refresh scripts that are used for processing the original tarball

* Fri Oct 30 2015 Tom Callaway <spot@fedoraproject.org> 46.0.2490.80-5
- tls_edit is a nacl thing. who knew?

* Thu Oct 29 2015 Tom Callaway <spot@fedoraproject.org> 46.0.2490.80-4
- more nacl fixups for i686 case

* Thu Oct 29 2015 Tom Callaway <spot@fedoraproject.org> 46.0.2490.80-3
- conditionalize nacl/nonacl, disable nacl on i686, build for i686

* Mon Oct 26 2015 Tom Callaway <spot@fedoraproject.org> 46.0.2490.80-2
- conditionalize shared bits (enable by default)

* Fri Oct 23 2015 Tom Callaway <spot@fedoraproject.org> 46.0.2490.80-1
- update to 46.0.2490.80

* Thu Oct 15 2015 Tom Callaway <spot@fedoraproject.org> 46.0.2490.71-1
- update to 46.0.2490.71

* Thu Oct 15 2015 Tom Callaway <spot@fedoraproject.org> 45.0.2454.101-2
- fix icu handling for f21 and older

* Mon Oct  5 2015 Tom Callaway <spot@fedoraproject.org> 45.0.2454.101-1
- update to 45.0.2454.101

* Thu Jun 11 2015 Tom Callaway <spot@fedoraproject.org> 43.0.2357.124-1
- update to 43.0.2357.124

* Tue Jun  2 2015 Tom Callaway <spot@fedoraproject.org> 43.0.2357.81-1
- update to 43.0.2357.81

* Thu Feb 26 2015 Tom Callaway <spot@fedoraproject.org> 40.0.2214.115-1
- update to 40.0.2214.115

* Thu Feb 19 2015 Tom Callaway <spot@fedoraproject.org> 40.0.2214.111-1
- update to 40.0.2214.111

* Mon Feb  2 2015 Tom Callaway <spot@fedoraproject.org> 40.0.2214.94-1
- update to 40.0.2214.94

* Tue Jan 27 2015 Tom Callaway <spot@fedoraproject.org> 40.0.2214.93-1
- update to 40.0.2214.93

* Sat Jan 24 2015 Tom Callaway <spot@fedoraproject.org> 40.0.2214.91-1
- update to 40.0.2214.91

* Wed Jan 21 2015 Tom Callaway <spot@fedoraproject.org> 39.0.2171.95-3
- use bundled icu on Fedora < 21, we need 5.2

* Tue Jan  6 2015 Tom Callaway <spot@fedoraproject.org> 39.0.2171.95-2
- rebase off Tomas's spec file for Fedora

* Fri Dec 12 2014 Tomas Popela <tpopela@redhat.com> 39.0.2171.95-1
- Update to 39.0.2171.95
- Resolves: rhbz#1173448

* Wed Nov 26 2014 Tomas Popela <tpopela@redhat.com> 39.0.2171.71-1
- Update to 39.0.2171.71
- Resolves: rhbz#1168128

* Wed Nov 19 2014 Tomas Popela <tpopela@redhat.com> 39.0.2171.65-2
- Revert the chrome-sandbox rename to chrome_sandbox
- Resolves: rhbz#1165653

* Wed Nov 19 2014 Tomas Popela <tpopela@redhat.com> 39.0.2171.65-1
- Update to 39.0.2171.65
- Use Red Hat Developer Toolset for compilation
- Set additional SELinux labels
- Add more unit tests
- Resolves: rhbz#1165653

* Fri Nov 14 2014 Tomas Popela <tpopela@redhat.com> 38.0.2125.122-1
- Update to 38.0.2125.122
- Resolves: rhbz#1164116

* Wed Oct 29 2014 Tomas Popela <tpopela@redhat.com> 38.0.2125.111-1
- Update to 38.0.2125.111
- Resolves: rhbz#1158347

* Fri Oct 24 2014 Tomas Popela <tpopela@redhat.com> 38.0.2125.104-2
- Fix the situation when the return key (and keys from numpad) does not work
  in HTML elements with input
- Resolves: rhbz#1153988
- Dynamically determine the presence of the PepperFlash plugin
- Resolves: rhbz#1154118

* Thu Oct 16 2014 Tomas Popela <tpopela@redhat.com> 38.0.2125.104-1
- Update to 38.0.2125.104
- Resolves: rhbz#1153012

* Thu Oct 09 2014 Tomas Popela <tpopela@redhat.com> 38.0.2125.101-2
- The boringssl is used for tests, without the possibility of using
  the system openssl instead. Remove the openssl and boringssl sources
  when not building the tests.
- Resolves: rhbz#1004948

* Wed Oct 08 2014 Tomas Popela <tpopela@redhat.com> 38.0.2125.101-1
- Update to 38.0.2125.101
- System openssl is used for tests, otherwise the bundled boringssl is used
- Don't build with clang
- Resolves: rhbz#1004948

* Wed Sep 10 2014 Tomas Popela <tpopela@redhat.com> 37.0.2062.120-1
- Update to 37.0.2062.120
- Resolves: rhbz#1004948

* Wed Aug 27 2014 Tomas Popela <tpopela@redhat.com> 37.0.2062.94-1
- Update to 37.0.2062.94
- Include the pdf viewer library

* Wed Aug 13 2014 Tomas Popela <tpopela@redhat.com> 36.0.1985.143-1
- Update to 36.0.1985.143
- Use system openssl instead of bundled one
- Resolves: rhbz#1004948

* Thu Jul 17 2014 Tomas Popela <tpopela@redhat.com> 36.0.1985.125-1
- Update to 36.0.1985.125
- Add libexif as BR
- Resolves: rhbz#1004948

* Wed Jun 11 2014 Tomas Popela <tpopela@redhat.com> 35.0.1916.153-1
- Update to 35.0.1916.153
- Resolves: rhbz#1004948

* Wed May 21 2014 Tomas Popela <tpopela@redhat.com> 35.0.1916.114-1
- Update to 35.0.1916.114
- Bundle python-argparse
- Resolves: rhbz#1004948

* Wed May 14 2014 Tomas Popela <tpopela@redhat.com> 34.0.1847.137-1
- Update to 34.0.1847.137
- Resolves: rhbz#1004948

* Mon May 5 2014 Tomas Popela <tpopela@redhat.com> 34.0.1847.132-1
- Update to 34.0.1847.132
- Bundle depot_tools and switch from make to ninja
- Remove PepperFlash
- Resolves: rhbz#1004948

* Mon Feb 3 2014 Tomas Popela <tpopela@redhat.com> 32.0.1700.102-1
- Update to 32.0.1700.102

* Thu Jan 16 2014 Tomas Popela <tpopela@redhat.com> 32.0.1700.77-1
- Update to 32.0.1700.77
- Properly kill Xvfb when tests fails
- Add libdrm as BR
- Add libcap as BR

* Tue Jan 7 2014 Tomas Popela <tpopela@redhat.com> 31.0.1650.67-2
- Minor changes in spec files and scripts
- Add Xvfb as BR for tests
- Add policycoreutils-python as Requires
- Compile unittests and run them in chech phase, but turn them off by default
  as many of them are failing in Brew

* Thu Dec 5 2013 Tomas Popela <tpopela@redhat.com> 31.0.1650.67-1
- Update to 31.0.1650.63

* Thu Nov 21 2013 Tomas Popela <tpopela@redhat.com> 31.0.1650.57-1
- Update to 31.0.1650.57

* Wed Nov 13 2013 Tomas Popela <tpopela@redhat.com> 31.0.1650.48-1
- Update to 31.0.1650.48
- Minimal supported RHEL6 version is now RHEL 6.5 due to GTK+

* Fri Oct 25 2013 Tomas Popela <tpopela@redhat.com> 30.0.1599.114-1
- Update to 30.0.1599.114
- Hide the infobar with warning that this version of OS is not supported
- Polished the chromium-latest.py

* Thu Oct 17 2013 Tomas Popela <tpopela@redhat.com> 30.0.1599.101-1
- Update to 30.0.1599.101
- Minor changes in scripts

* Wed Oct 2 2013 Tomas Popela <tpopela@redhat.com> 30.0.1599.66-1
- Update to 30.0.1599.66
- Automated the script for cleaning the proprietary sources from ffmpeg.

* Thu Sep 19 2013 Tomas Popela <tpopela@redhat.com> 29.0.1547.76-1
- Update to 29.0.1547.76
- Added script for removing the proprietary sources from ffmpeg. This script is called during cleaning phase of ./chromium-latest --rhel

* Mon Sep 16 2013 Tomas Popela <tpopela@redhat.com> 29.0.1547.65-2
- Compile with Dproprietary_codecs=0 and Dffmpeg_branding=Chromium to disable proprietary codecs (i.e. MP3)

* Mon Sep 9 2013 Tomas Popela <tpopela@redhat.com> 29.0.1547.65-1
- Initial version based on Tom Callaway's <spot@fedoraproject.org> work

