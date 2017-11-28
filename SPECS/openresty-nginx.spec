Name:           openresty-nginx
Version:        0.1
Release:        VIS0
Summary:        Visonic build of OpenResty Nginx with Lua scripting

BuildRequires: gcc make pcre-devel zlib-devel openssl-devel
Requires: pcre zlib openssl

%define version_nginx          1.13.4
%define version_ndk            0.3.0
%define version_luajit         2.1.0-beta3
%define version_lua_mod        0.10.10
%define version_openssl        1.0.2l

License: BSD
URL:     https://github.com/openresty
Source0: http://nginx.org/download/nginx-%{version_nginx}.tar.gz
Source1: https://github.com/simpl/ngx_devel_kit/archive/v%{version_ndk}.tar.gz
Source2: http://luajit.org/download/LuaJIT-%{version_luajit}.tar.gz
Source3: https://github.com/openresty/lua-nginx-module/archive/v%{version_lua_mod}.tar.gz

Source10: https://github.com/openresty/lua-upstream-nginx-module/archive/master.tar.gz
Source11: https://github.com/openresty/lua-resty-core/archive/v0.1.13.tar.gz
Source15: https://github.com/openresty/lua-resty-balancer/archive/v0.02rc4.tar.gz
Source16: https://github.com/openresty/lua-resty-lrucache/archive/v0.07.tar.gz
Source17: https://github.com/openresty/lua-resty-limit-traffic/archive/v0.05.tar.gz
Source18: https://github.com/openresty/lua-cjson/archive/2.1.0.6rc2.tar.gz

#-- NOTE: download all with spectool -g (package rpmdevtools) --#

%description
Turning Nginx into a Full-Fledged Scriptable Web Platform

%define prefix /usr/local
%define make make --no-print-dir

#------------------------------------------------------------------------------#
%prep
%setup -Tb 0 -n nginx-%{version_nginx}
%setup -Tb 1 -n ngx_devel_kit-%{version_ndk}
%setup -Tb 2 -n LuaJIT-%{version_luajit}
%setup -Tb 3 -n lua-nginx-module-%{version_lua_mod}

%setup -Tb 10 -n lua-upstream-nginx-module-master
%setup -Tb 11 -n lua-resty-core-0.1.13
%setup -Tb 15 -n lua-resty-balancer-0.02rc4
%setup -Tb 16 -n lua-resty-lrucache-0.07
%setup -Tb 17 -n lua-resty-limit-traffic-0.05
%setup -Tb 18 -n lua-cjson-2.1.0.6rc2

#------------------------------------------------------------------------------#
#   ====   https://github.com/openresty/lua-nginx-module#installation   ====   #
#------------------------------------------------------------------------------#
%build
#-- LuaJIT is built once, installed twice: once to stage, once more into the RPM
export LUAJIT_STAGING=%{_builddir}/luajit-staging

%make -C %{_builddir}/LuaJIT-%{version_luajit} \
    DESTDIR=$LUAJIT_STAGING \
    install

cd %{_builddir}/nginx-%{version_nginx}
export LUAJIT_LIB=$LUAJIT_STAGING%{prefix}/lib
export LUAJIT_INC=$LUAJIT_STAGING%{prefix}/include/luajit-2.1
./configure \
    --prefix=%{prefix} \
    --build=%{release} \
    --conf-path=/etc/nginx/nginx.conf \
    --http-log-path=/var/log/nginx/access.log \
    --error-log-path=/var/log/nginx/error.log \
    --pid-path=
    --with-ld-opt="-Wl,-rpath,%{prefix}/lib" \
    --with-http_ssl_module \
    --add-module=%{_builddir}/ngx_devel_kit-%{version_ndk} \
    --add-module=%{_builddir}/lua-nginx-module-%{version_lua_mod} \
    --add-module=%{_builddir}/lua-upstream-nginx-module-master \
&& %make -j3

#------------------------------------------------------------------------------#
%install
cd %{buildroot}

%make -C %{_builddir}/LuaJIT-%{version_luajit} \
    DESTDIR=%{buildroot} \
    install
ln -s luajit-%{version_luajit} %{buildroot}%{prefix}/bin/luajit

%make -C %{_builddir}/nginx-%{version_nginx} \
    DESTDIR=%{buildroot} \
    install
#------------------------------------------------------------------------------#
%files
%{prefix}/bin/luajit*
%{prefix}/lib/libluajit*
%{prefix}/lib/pkgconfig/luajit.pc
%{prefix}/include/luajit*
%{prefix}/share/luajit*/jit/*.lua
%{prefix}/share/man/man1/luajit.1

/etc/nginx
%{prefix}/sbin/nginx
%{prefix}/html
# %doc

#------------------------------------------------------------------------------#
%changelog
* Wed Nov 28 2017 Max Ivanov <ulidtko@gmail.com> 0.1-VIS0
- Initial RPM packaging written from scratch.
