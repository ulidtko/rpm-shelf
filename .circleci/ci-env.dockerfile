FROM centos:7.3.1611
MAINTAINER Max <ulidtko@gmail.com>

ENV \
    GEM_HOME=/usr/local \
    GOPATH=/tmp/golang.cage \
    GOBIN=/usr/local/bin

RUN \
    yum --noplugins install -y \
        make gcc-c++ \
        rpmdevtools yum-utils \
        golang git \
        rubygems ruby-devel \
        epel-release \
    && \
    yum --noplugins clean all \
    ; \
    go get github.com/tcnksm/ghr \
    && \
    rm -rf $GOPATH \
    && \
    gem install package_cloud \
    ;
