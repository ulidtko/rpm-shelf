[![PackageCloud.io](https://img.shields.io/badge/rpm-packagecloud.io-844fec.svg)](https://packagecloud.io/rpm-shelf/main)
<!-- Disabled: CircleCI badge style doesn't blend [![CircleCI](https://circleci.com/gh/ulidtko/rpm-shelf.svg?style=svg&circle-token=5cbd95be6f7f4776743310365f197910bb447004)](https://circleci.com/gh/ulidtko/rpm-shelf) -->
[![CircleCI](https://img.shields.io/circleci/token/37cb3ba63d9711b861d52a440e0712898e7fcf3a/project/github/ulidtko/rpm-shelf/master.svg?label=CircleCI%20build)](https://circleci.com/gh/ulidtko/rpm-shelf)

# ???

1. [RHEL](https://redhat.com/rhel)

2. [CentOS](https://centos.org)

3. [RPM](http://rpm.org)

4. [`rpmbuild`](https://rpm-packaging-guide.github.io/)

**TL;DR** can loot linux softwares here.

# How?

Most better with [Docker](https://www.docker.com). Feed it the [blessed +2 trendy dockerfile](rpmbuild.dockerfile), get an
image, run a container from it. RTFM! (srsly)

LMDTFY:

                        [docker build]               [docker run -it]
    rpmbuild.dockerfile --------------> {image hash} ----------------> {centos shell}
                                                                           |
                                                                           |
                                                     thing.spec ----> $ rpmbuild
                                                                           |
                                                                           V
                                                                       thing.rpm

And then, an installable RPM appears. Nice huh!

# Binary RPM download
https://packagecloud.io/rpm-shelf/main
