Name:           upx
Version:        3.94
Release:        VIS0.1
Summary:        UPX - the Ultimate Packer for eXecutables
License:        GPL (with executable stub exception)

URL:            https://upx.github.io/

%define ucl_ver 1.03

Source0:        https://github.com/upx/upx/archive/v%{version}.tar.gz#save-as/%{name}-%{version}.tar.gz
Source2:        https://github.com/upx/upx-lzma-sdk/archive/v%{version}.tar.gz#save-as/upx-lzma-sdk-%{version}.tar.gz
Source1:        http://www.oberhumer.com/opensource/ucl/download/ucl-%{ucl_ver}.tar.gz

BuildRequires: gcc-c++
#BuildRequires: clang
BuildRequires:  make
BuildRequires:  zlib-devel
# BuildRequires:  lzma-sdk457-devel

AutoReq: yes

%define make make %{?_smp_mflags} --no-print-dir

%description
UPX is a free, portable, extendable, high-performance executable packer
for several executable formats.

%prep
%setup -b 0
%setup -b 1
%setup -b 2

%build

cd %{_builddir}/ucl-%{ucl_ver}
%configure && %make

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

%make_install -C %{_builddir}/ucl-%{ucl_ver}

install -D -m755 %{_builddir}/upx-%{version}/src/upx.out %{buildroot}%{_bindir}/upx
install -d %{buildroot}%{_pkgdocdir}
install -t %{buildroot}%{_pkgdocdir} \
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
install -d %{buildroot}%{_mandir}
install -t %{buildroot}%{_mandir} \
    doc/upx.1

%files
%{_bindir}/upx
%{_includedir}/ucl/
%{_libdir}/libucl*
%doc %{_mandir}/upx.1*
%doc %{_pkgdocdir}/


%changelog

* Tue Dec 26 2017 Max <ulidtko@gmail.com> 3.94-VIS0.1
- Initial RPM packaging written from scratch.
