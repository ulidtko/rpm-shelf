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
