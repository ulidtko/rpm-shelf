Name:           upx
Version:        3.94
Release:        VIS0.3
Summary:        The Ultimate Packer for eXecutables
License:        GPL-2.0+ WITH binary-stub-exception
Group:          Development/Tools/Other

URL:            https://upx.github.io/

%define ucl_ver 1.03

Source0:        https://github.com/upx/upx/archive/v%{version}.tar.gz#save-as/%{name}-%{version}.tar.gz
Source2:        https://github.com/upx/upx-lzma-sdk/archive/v%{version}.tar.gz#save-as/upx-lzma-sdk-%{version}.tar.gz
Source1:        http://www.oberhumer.com/opensource/ucl/download/ucl-%{ucl_ver}.tar.gz

Patch0:         00-ucl-static-assert.patch

BuildRequires: gcc-c++
#BuildRequires: clang
BuildRequires:  make
BuildRequires:  zlib-devel
# BuildRequires:  lzma-sdk457-devel

AutoReq: yes

%define make make %{?_smp_mflags} --no-print-dir
%define _pkgdocdir %{_docdir}/%{name}-%{version}

%description
UPX is a free, portable, extendable, high-performance executable packer
for several executable formats.

%prep
%setup -b 0
%setup -b 1
%setup -b 2

cd %{_builddir}/ucl-%{ucl_ver}
%patch0 -p1

%build

cd %{_builddir}/ucl-%{ucl_ver}
%configure && %make || exit 1

cd %{_builddir}/upx-%{version}
rmdir   src/lzma-sdk && \
    mv %{_builddir}/upx-lzma-sdk-%{version} \
        src/lzma-sdk

%make all \
    UPX_UCLDIR=%{_builddir}/ucl-%{ucl_ver} \
    LIBS="%{_builddir}/ucl-%{ucl_ver}/src/.libs/libucl.a -lz" \
    CHECK_WHITESPACE=': skipping "whitespace check"' \
    ;

%install
rm -rf $RPM_BUILD_ROOT

#%make_install -C %{_builddir}/ucl-%{ucl_ver}

install -m755 -D %{_builddir}/upx-%{version}/src/upx.out %{buildroot}%{_bindir}/upx
install -m755 -d %{buildroot}%{_pkgdocdir}
install -m644 -t %{buildroot}%{_pkgdocdir} \
    BUGS \
    COPYING \
    LICENSE \
    NEWS \
    PROJECTS \
    README \
    README.1ST \
    README.SRC \
    THANKS \
    doc/elf-to-mem.txt \
    doc/filter.txt \
    doc/loader.txt \
    doc/selinux.txt \
    ;
install -m755 -d %{buildroot}%{_mandir}
install -m644 -t %{buildroot}%{_mandir} \
    doc/upx.1

%files
%{_bindir}/upx
#%{_includedir}/ucl/
#%{_libdir}/libucl*
%doc %{_mandir}/upx.1*
%doc %{_pkgdocdir}/


%changelog
* Wed Jan 3 2018 Max <ulidtko@gmail.com> 3.94-VIS0.3
- RPMlint fixed (except for the licensing exception). UCL binaries not packaged now.

* Tue Jan 2 2018 Max <ulidtko@gmail.com> 3.94-VIS0.2
- UCL static assert patch added; lint fixed, can build on OpenSUSE now.

* Tue Dec 26 2017 Max <ulidtko@gmail.com> 3.94-VIS0.1
- Initial RPM packaging written from scratch.
