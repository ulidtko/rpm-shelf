FROM centos:latest
MAINTAINER Max <ulidtko@gmail.com>

# docker build -t docker.visonic.com/rpmbuild:latest - < rpmbuild.dockerfile

RUN yum --noplugins install -y \
    tree htop vim less \
    gcc make \
    rpmdevtools yum-utils \
    sudo \
    ; yum clean all

#-- Æ·S·T·H·E·T·I·C·S --
RUN sed -i -e'$iif [ "$PS1" ]; then PS1="{docker|rpmbuild} [\\W]⚓  "; fi' /etc/bashrc

#-- build unprivileged
RUN adduser --uid 1000 builder ; \
    { echo; echo '#1000 ALL=(ALL) NOPASSWD:ALL'; } >> /etc/sudoers ; \
    chown -R 1000:1000 /usr/local ; \
    sed -i -e'$icat /etc/motd 2>/dev/null || :' /etc/bashrc ; \
    {   echo '==== Welcome to Visonic rpmbuild environment ===='; \
        echo; \
        echo 'Introductory how-to: https://rpm-packaging-guide.github.io/' ; \
        echo 'Reference: http://ftp.rpm.org/max-rpm/index.html' ; \
        echo; \
        echo 'To create a new specfile from template:' ; \
        echo '    $ rpmdev-newspec -t minimal NEWPKG.spec' ; \
        echo; \
        echo 'To download tarballs and patches:' ; \
        echo '    $ spectool -g MYPKG.spec' ; \
        echo; \
        echo 'To build binary RPM:' ; \
        echo '    $ rpmbuild --define "_topdir $PWD" -bb SPECS/MYPKG.spec' ; \
        echo; \
    } > /etc/motd

#-- drop root & default login as user
USER 1000
