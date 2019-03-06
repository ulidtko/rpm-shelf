%define upstream_version 2.1.1

#-- read here https://github.com/semver/semver/issues/145
%define unhyphenize(v) %(echo %1 | sed -e s:-:~:g)

Name:    dart-sdk
Version: %unhyphenize %upstream_version
Release: VIS0
Summary: Dart is an open-source, scalable programming language for web, server, and mobile.
Group: Development/Languages

License: BSD-3-Clause
URL:     https://www.dartlang.org/

#-- The tarballs they publish aren't really buildable. Pity!
# Source0: https://github.com/dart-lang/sdk/archive/%{upstream_version}.tar.gz#/dart-%{version}.tar.gz

Patch1: 0001-Fix-wrong-port-in-Dart-SocketError-messages.patch
Patch2: 0002-more-explicit-error-reporting.patch

#-- Google depot_tools
%define DEPOT_TOOLS_GIT https://chromium.googlesource.com/chromium/tools/depot_tools.git
BuildRequires: git, python >= 2.7
BuildRequires: curl

# it builds with its own clang
# BuildRequires: gcc-c++ >= 4.8

BuildArchitectures: x86_64

# Requires:

%description
The Dart SDK, including the VM, dart2js, core libraries, and more.


%prep
# depot_tools is distributed only via git
[[ -d depot_tools ]] || git clone --branch master %{DEPOT_TOOLS_GIT}
export PATH="$PATH:$PWD/depot_tools"

mkdir -p dart-%{version} && cd dart-%{version}
[[ -d sdk ]] || fetch dart

cd sdk
gclient sync --no-history --revision %{upstream_version}
%patch1 -p1
%patch2 -p1

%build

#-- workaround 4GiB OOM on CI (by ditching dart2js)
if [[ ! -z $DART_NO_FULL_SDK ]]
then TARGET=create_platform_sdk
else TARGET=create_full_sdk
fi

export PATH="$PATH:$PWD/depot_tools"
cd dart-%{version}/sdk
./tools/build.py \
    --verbose \
    --mode release \
    --arch x64 \
    $TARGET

%check
echo 'The test suite takes ~10 hours -- uncomment in the .spec first'
# cd dart-%{version}/sdk
# ninja -C out/ReleaseX64 run_vm_tests
# ./tools/test.py \
#     --mode release \
#     --arch x64 \
#     --compiler none,dart2js \
#     --runtime none,vm,d8,dart_precompiled

%install

%define outdir dart-%{version}/sdk/out/ReleaseX64/dart-sdk
%define prefix /opt/dart-sdk

install -d %{buildroot}%{prefix}
cp -a %outdir/* %{buildroot}%{prefix}
find %{buildroot}%{prefix} -type d | xargs chmod 755
find %{buildroot}%{prefix} -type f | xargs chmod 644
chmod a+x %{buildroot}%{prefix}/bin/*

install -d %{buildroot}%{_bindir}
for bin in {dart,dart2js,dartanalyzer,dartdevc,dartdevk,dartdoc,dartfmt,pub}; do
    ln -s %{prefix}/bin/$bin %{buildroot}%{_bindir}/$bin
done

rm -f dart-%{version}/samples/.gitignore

%files
%{_bindir}/*
%{prefix}
%doc dart-%{version}/sdk/{AUTHORS,CHANGELOG.md,CONTRIBUTING.md,PATENTS,README.md}
%doc dart-%{version}/sdk/docs/*
%doc dart-%{version}/sdk/{samples,samples-dev}


%changelog
* Mon Feb 25 2019 Max <ulidtko@gmail.com> - 2.1.1-VIS0
- Update onto a stable version.
- https://github.com/dart-lang/sdk/blob/2.1.1/CHANGELOG.md
- Add test running section.
- Add a patch for wrong port numbers in SocketError logs.

* Wed Oct 17 2018 Max <ulidtko@gmail.com> - 2.1.0~dev.7.1-VIS0
- Initial packaging written from scratch.
