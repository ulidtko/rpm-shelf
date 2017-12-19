# -*- rpm-spec -*-
Summary:        A dead simple tool to sign files and verify signatures.
Name:           minisign
Version:        0.7
Release:        VIS0.2
License:        ISC
Vendor:         Visonic
Url:            https://jedisct1.github.io/minisign/
BuildRequires:  cmake, libsodium-devel
Requires:       libsodium
Source:         https://github.com/jedisct1/minisign/archive/%{version}.tar.gz

#%define _unpackaged_files_terminate_build 0

%description

Minisign
========

Minisign is a dead simple tool to sign files and verify signatures.

For more information, please refer to the
[Minisign documentation](https://jedisct1.github.io/minisign/)

Tarballs and pre-compiled binaries can be verified with the following
public key:

    RWQf6LRCGA9i53mlYecO4IzT51TGPpvWucNSCh1CBM0QTaLn73Y7GFO3

Compilation / installation
--------------------------

Dependencies:
* [libsodium](http://doc.libsodium.org/)
* cmake

Compilation:

    $ mkdir build
    $ cd build
    $ cmake ..
    $ make
    # make install

Minisign is also available in Homebrew:

    $ brew install minisign

Minisign is also available in Scoop on Windows:

    $ scoop install minisign

Minisign is also available in chocolatey on Windows:

    $ choco install minisign

Additional tools
----------------

* [minisign-misc](https://github.com/JayBrown/minisign-misc) is a very
nice set of workflows and scripts for macOS to verify and sign files
with minisign.

Alternative implementations
---------------------------

* [rsign](https://bitbucket.org/danielrangel/rsign) is a minisign
implementation written in Rust.

Faults injections
-----------------

Minisign uses the EdDSA signature system, and deterministic signature
schemes are fragile against fault attacks. However, conducting these requires
physical access or the attacker having access to the same physical host.

More importantly, this requires a significant amount of time, and messages
being signed endlessly while the attack is being conducted.

If such a scenario ever happens to be part of your threat model,
libsodium should be compiled with the `ED25519_NONDETERMINISTIC` macro
defined. This will add random noise to the computation of EdDSA
nonces.


%prep
%setup -q

%build
cmake . -DCMAKE_INSTALL_PREFIX=%{_prefix}
make

%install
make DESTDIR=%{buildroot} install


%files
%defattr(-,root,root,-)
%{_bindir}/minisign
%{_mandir}/man1/minisign.1*


%changelog
* Tue Dec 19 2017 Max <ulidtko@gmail.com> - 0.7-VIS0.2
  Rebuild against newer libsodium 1.0.16

* Thu Dec 14 2017 Max <ulidtko@gmail.com> - 0.7-VIS0.1
  Fix failure on keypair generation when secret key path
  is specified relative to CWD (e.g. -s new.key)
  https://github.com/jedisct1/minisign/pull/35

* Tue Dec 12 2017 Max <ulidtko@gmail.com> - 0.7-VIS0
  Initial packaging from CPack RPM.
