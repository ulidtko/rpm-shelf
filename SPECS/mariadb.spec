Name:           mariadb
Version:        10.1.14
Epoch:          1
Release:        VIS0.1
Summary:        A community developed fork of MySQL
Group:          Applications/Databases

License:        GPL2
URL:            http://mariadb.org
Source0:        %{name}-%{version}.tar.gz
Source1:        my.cnf
Source15:       mariadb.service
Source16:       mariadb.target
Source17:       mysql-systemd-helper
Source18:       mysql.logrotate.conf
Source50:       mariadb-wait-ready

BuildRequires:  jemalloc-devel, xz-devel, lzo-devel, readline-devel, libaio-devel
AutoReq: on

%description
MariaDB is a community developed branch of MySQL.
MariaDB is a multi-user, multi-threaded SQL database server.
It is a client/server implementation consisting of a server daemon (mysqld)
and many different client programs and libraries. The base package
contains the standard MariaDB/MySQL client programs and generic MySQL files.

The Visonic release also bundles the mysqld server in this package.

%prep
%setup -q

%define make make --no-print-dir

%build
cmake . -DBUILD_CONFIG=mysql_release \
        -DFEATURE_SET="community" \
        -DINSTALL_LAYOUT=RPM \
        -DSECURITY_HARDENED=ON \
        -DWITH_JEMALLOC=ON \
        -DWITH_READLINE=ON \
        -DPLUGINS_DAMON_EXAMPLE=NO \
        -DCMAKE_INSTALL_PREFIX="%{_prefix}"


%{make} %{?_smp_mflags}

# debuginfo extraction scripts fail to locate several source files
# get around this by moving these files into where scripts expect them
mkdir -vp storage/include
ls -1 \
    storage/{innobase,xtradb}/pars/{pars0grm.cc,pars0grm.y,pars0lex.l,lexyy.cc} \
    storage/{innobase,xtradb}/fts/{fts0blex.cc,fts0blex.l,fts0pars.cc,fts0pars.y,fts0tlex.cc,fts0tlex.l} \
    storage/innobase/include/fts0[bt]lex.h `#-- xtradb headers are the same` \
    | sed -re 'h; s|/pars/|/|; s|/fts/|/|; s|innobase/include|include|; H; x; s|\n| |' \
    | xargs -L1 cp -v \
    ;

%check
%{make} test

%install
%{make} DESTDIR=%{buildroot} install

unlink %{buildroot}/usr/sbin/rcmysql
rm -f %{buildroot}/usr/lib64/mysql/plugin/daemon_example.ini
rm -rf %{buildroot}/etc/init.d

mkdir -vp %{buildroot}/var/lib/mysql/tmp
mkdir -vp %{buildroot}/var/log/mysql

# Package config
install -D -m 644 %{_sourcedir}/my.cnf '%{buildroot}'/etc/my.cnf

# Overwrite stock logrotate config with ours
install -D -m 644 %{_sourcedir}/mysql.logrotate.conf '%{buildroot}'/etc/logrotate.d/mysql

# Systemd
install -D -m 755 %{_sourcedir}/mysql-systemd-helper '%{buildroot}'%{_libexecdir}/mysql/mysql-systemd-helper
install -D -m 755 %{_sourcedir}/mariadb-wait-ready '%{buildroot}'%{_libexecdir}/mariadb-wait-ready
sed -i 's|@MYSQLVER@|%{version}|' '%{buildroot}'%{_libexecdir}/mysql/mysql-systemd-helper
# ln -sf service '%{buildroot}'%{_sbindir}/rcmysql
install -D -m 644 %{_sourcedir}/mariadb.service '%{buildroot}'/usr/lib/systemd/system/mariadb.service
install -D -m 644 %{_sourcedir}/mariadb.target '%{buildroot}'/usr/lib/systemd/system/mariadb.target

%files
%{_bindir}/my_print_defaults
%{_bindir}/mysql
%{_bindir}/mysql_config
%{_bindir}/mysql_convert_table_format
%{_bindir}/mysql_embedded
%{_bindir}/mysql_find_rows
%{_bindir}/mysql_waitpid
%{_bindir}/mysql_zap
%{_bindir}/mysqlaccess
%{_bindir}/mysqladmin
%{_bindir}/mysqlbinlog
%{_bindir}/mysqldump
%{_bindir}/mysqldumpslow
%{_bindir}/mysqlhotcopy
%{_bindir}/mysqlimport
%{_bindir}/mysqlshow
%{_bindir}/mysqlslap
%{_bindir}/mytop
%{_bindir}/perror
%{_bindir}/replace
%{_bindir}/resolveip

%{_mandir}/man1/my_print_defaults.1*
%{_mandir}/man1/mysql.1*
%{_mandir}/man1/mysql_config.1*
%{_mandir}/man1/mysql_convert_table_format.1*
%{_mandir}/man1/mysql_find_rows.1*
%{_mandir}/man1/mysql_waitpid.1*
%{_mandir}/man1/mysql_zap.1*
%{_mandir}/man1/mysqlaccess.1*
%{_mandir}/man1/mysqladmin.1*
%{_mandir}/man1/mysqlbinlog.1*
%{_mandir}/man1/mysqldump.1*
%{_mandir}/man1/mysqldumpslow.1*
%{_mandir}/man1/mysqlhotcopy.1*
%{_mandir}/man1/mysqlimport.1*
%{_mandir}/man1/mysqlshow.1*
%{_mandir}/man1/mysqlslap.1*
%{_mandir}/man1/perror.1*
%{_mandir}/man1/replace.1*
%{_mandir}/man1/resolveip.1*

%config(noreplace) /etc/my.cnf.d/client.cnf
%config(noreplace) /etc/my.cnf.d/mysql-clients.cnf

%doc /usr/share/doc/README
%doc /usr/share/doc/README.md
%doc /usr/share/doc/CREDITS
%doc /usr/share/doc/COPYING
%doc /usr/share/doc/COPYING.AGPLv3
%doc /usr/share/doc/COPYING.GPLv2
%doc /usr/share/doc/COPYING.LESSER
%doc /usr/share/doc/COPYING.thirdparty
%doc /usr/share/doc/EXCEPTIONS-CLIENT
%doc /usr/share/doc/INSTALL-BINARY
%doc /usr/share/doc/README-wsrep
%doc /usr/share/doc/PATENTS
%doc VERSION KNOWN_BUGS.txt
%doc EXCEPTIONS-CLIENT


%package libs
Summary: The shared libraries required for MariaDB/MySQL clients
Group: Applications/Databases
Requires: /sbin/ldconfig
Provides: mysql-libs = 1:%{version}

%description libs
The mariadb-libs package provides the essential shared libraries for any
MariaDB/MySQL client program or interface. You will need to install this
package to use any other MariaDB package or any clients that need to connect
to a MariaDB/MySQL server. MariaDB is a community developed branch of MySQL.

%files libs
%doc README COPYING CREDITS COPYING.LESSER
%doc storage/innobase/COPYING.Percona storage/innobase/COPYING.Google
%config %{_sysconfdir}/my.cnf
%config(noreplace) %{_sysconfdir}/my.cnf.d/mysql-clients.cnf
%dir %{_sysconfdir}/my.cnf.d
%dir %{_libdir}/mysql
/usr/lib64/*.so
/usr/lib64/*.so.*
/usr/share/mysql


%post libs -p /sbin/ldconfig
%postun libs -p /sbin/ldconfig


%package  server
Summary:  The MariaDB server and related files
Group:    Development/Databases
Requires: mariadb-libs = 1:%{version}-%{release}
Requires: mariadb = 1:%{version}-%{release}
Requires(pre): /sbin/useradd

%description server
This package contains the mysqld server daemon, configuration, systemd service files and other support files for running the MariaDB server.

%files server
/usr/sbin/mysqld
%{_bindir}/aria_chk
%{_bindir}/aria_dump_log
%{_bindir}/aria_ftdump
%{_bindir}/aria_pack
%{_bindir}/aria_read_log
%{_bindir}/innochecksum
%{_bindir}/myisam_ftdump
%{_bindir}/myisamchk
%{_bindir}/myisamlog
%{_bindir}/myisampack
%{_bindir}/mysqld_multi
%{_bindir}/mysqld_safe
%{_bindir}/mysql_fix_extensions
%{_bindir}/mysql_install_db
%{_bindir}/mysql_plugin
%{_bindir}/mysql_secure_installation
%{_bindir}/mysql_setpermission
%{_bindir}/mysql_tzinfo_to_sql
%{_bindir}/mysql_upgrade
%{_bindir}/mysqlbug
%{_bindir}/mysqlcheck
%{_bindir}/tokuft_logprint
%{_bindir}/tokuftdump
%{_bindir}/wsrep_sst_common
%{_bindir}/wsrep_sst_mysqldump
%{_bindir}/wsrep_sst_rsync
%{_bindir}/wsrep_sst_xtrabackup
%{_bindir}/wsrep_sst_xtrabackup-v2

%{_libdir}/mysql/plugin/*.so

%{_mandir}/man1/aria_chk.1*
%{_mandir}/man1/aria_dump_log.1*
%{_mandir}/man1/aria_ftdump.1*
%{_mandir}/man1/aria_pack.1*
%{_mandir}/man1/aria_read_log.1*
%{_mandir}/man1/innochecksum.1*
%{_mandir}/man1/myisam_ftdump.1*
%{_mandir}/man1/myisamchk.1*
%{_mandir}/man1/myisamlog.1*
%{_mandir}/man1/myisampack.1*
%{_mandir}/man1/mysql.server.1*
%{_mandir}/man1/mysql_fix_extensions.1*
%{_mandir}/man1/mysql_install_db.1*
%{_mandir}/man1/mysql_plugin.1*
%{_mandir}/man1/mysql_secure_installation.1*
%{_mandir}/man1/mysql_setpermission.1*
%{_mandir}/man1/mysql_tzinfo_to_sql.1*
%{_mandir}/man1/mysql_upgrade.1*
%{_mandir}/man1/mysqlbug.1*
%{_mandir}/man1/mysqlcheck.1*
%{_mandir}/man1/mysqld_multi.1*
%{_mandir}/man1/mysqld_safe.1*
%{_mandir}/man8/mysqld.8*

%config(noreplace) /etc/logrotate.d/mysql
%config(noreplace) /etc/my.cnf.d/enable_encryption.preset
%config(noreplace) /etc/my.cnf.d/server.cnf
%config(noreplace) /etc/my.cnf.d/tokudb.cnf

%dir %attr(755, mysql, mysql) /var/lib/mysql/tmp
%dir %attr(755, mysql, mysql) /var/log/mysql

%{_libexecdir}/mysql/mysql-systemd-helper
%{_libexecdir}/mariadb-wait-ready
/usr/lib/systemd/system/mariadb.service
/usr/lib/systemd/system/mariadb.target

%pre server
/usr/sbin/groupadd -g 27 -o -r mysql || echo "(that's OK)"
/usr/sbin/useradd -M -N -g mysql -o -r -d /var/lib/mysql -s /bin/bash \
	-c "MariaDB Server" -u 27 mysql || echo "(that's OK too)"

%post server
mkdir -p /var/run/mariadb
chown mysql:mysql /var/run/mariadb
mysql_install_db --user=mysql

%systemd_post mysql.service mysql@.service mysql.target mysql@default.service

%preun server
%systemd_preun mysql.service mysql@.service mysql.target mysql@default.service

%postun server
/sbin/ldconfig
%systemd_postun mysql.service mysql@.service mysql.target mysql@default.service


%package  devel
Summary:  Header files for MariaDB
Group:    Development/Libraries
Requires: openssl-devel%{?_isa}

%description devel
This package contains development files for compiling against MariaDB.

%files devel
/usr/include/mysql
/usr/lib64/*.a
/usr/share/aclocal/mysql.m4
/usr/share/pkgconfig/mariadb.pc
%{_bindir}/msql2mysql
%{_bindir}/resolve_stack_dump
%{_mandir}/man1/msql2mysql.1*
%{_mandir}/man1/resolve_stack_dump.1*


%package test
Summary: Test files for MariaDB
Group:   Development/Testing

%description test
This package contains MariaDB test files.

%files test
%{_bindir}/mysqltest
%{_bindir}/mysqltest_embedded
%{_bindir}/mysql_client_test
%{_bindir}/mysql_client_test_embedded
/usr/share/mysql-test
%{_mandir}/man1/mysqltest.1*
%{_mandir}/man1/mysqltest_embedded.1*
%{_mandir}/man1/mysql_client_test.1*
%{_mandir}/man1/mysql_client_test_embedded.1*

%{_mandir}/man1/mysql-stress-test.pl.1*
%{_mandir}/man1/mysql-test-run.pl.1*


%clean
exit 0 #-- noclean


%changelog
* Tue Aug 16 2016 Maxim Ivanov <ulidtko@gmail.com> - 10.1.14-VIS0.1
- Logrotate config corrected, logs locations adjusted

* Wed Jun 15 2016 Maxim Ivanov <ulidtko@gmail.com>
- Latest stable version 10.1.14 packaged from scratch
