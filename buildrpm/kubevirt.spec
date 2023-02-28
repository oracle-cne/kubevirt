{{{$version := printf "%s.%s.%s" .major .minor .patch}}}
%global debug_package %{nil}

Name:		kubevirt
Version:	{{{$version}}}
Release:	1%{?dist}
Summary:	Kubevirt 

License:	Apache License 2.0
URL:		https://github.com/kubevirt/kubevirt
Source0:	%{name}-%{version}.tar.bz2

BuildRequires:	golang >= 1.18.0
BuildRequires:	libvirt-devel
BuildRequires:  gcc
BuildRequires:  glibc-static

%package -n virtctl
Summary: CLI for Kubevirt

%package api
Summary: TODO

%package chroot
Summary: TODO

%package controller
Summary: TODO

%package freezer
Summary: TODO

%package handler
Summary: TODO
# See ./hack/rpm-deps.sh to understand how this set of
# dependencies was determined.
# - base
Requires: acl
Requires: curl
# - base extra
Requires: coreutils
Requires: glibc-minimal-langpack
# - handler base
Requires: qemu-img
# - handler extra
Requires: findutils
Requires: iproute
Requires: iptables
Requires: nftables
Requires: procps-ng
Requires: selinux-policy
Requires: selinux-policy-targeted
Requires: tar
Requires: util-linux
Requires: xorriso
# - local
Requires: kubevirt-container-disk = %{version}-%{release}
Requires: kubevirt-chroot = %{version}-%{release}

%package launcher
Summary: TODO
# See ./hack/rpm-deps.sh to understand how this set of
# dependencies was determined.
# - base
Requires: acl
Requires: curl
# - base extra
Requires: coreutils
Requires: glibc-minimal-langpack
# - launcher base
Requires: libvirt-client
Requires: libvirt-daemon-driver-qemu
Requires: qemu-kvm-core
# - launcher x86
Requires: edk2-ovmf
Requires: seabios
# - launcher extra
Requires: ethtool
Requires: findutils
Requires: iptables
Requires: nftables
Requires: nmap-ncat
Requires: procps-ng
Requires: selinux-policy
Requires: selinux-policy-targeted
Requires: tar
Requires: xorriso
# - local
Requires: kubevirt-container-disk = %{version}-%{release}
Requires: kubevirt-freezer = %{version}-%{release}
Requires: kubevirt-probe = %{version}-%{release}


%package operator
Summary: TODO

%package probe
Summary: TODO

%package container-disk
Summary: TODO

%package libguestfs-appliance
Summary: TODO
Requires: libguestfs-appliance

%description
Managed virtualized infrastructure within Kubernetes.

%description -n virtctl
TODO

%description api
TODO

%description chroot
TODO

%description controller
TODO

%description freezer
TODO

%description handler
TODO

%description launcher
TODO

%description operator
TODO

%description probe
TODO

%description container-disk
TODO

%description libguestfs-appliance
TODO

%prep
%setup -q

%build
go build ./cmd/virt-api
go build ./cmd/virt-chroot
go build ./cmd/virt-controller
go build ./cmd/virt-freezer
go build ./cmd/virt-handler
go build ./cmd/virt-launcher
go build ./cmd/virt-operator
go build ./cmd/virt-probe
go build ./cmd/virtctl
cc -o container-disk -static ./cmd/container-disk-v2alpha/main.c

%install
install -m 755 -d %{buildroot}/usr/bin
install -m 555 virt-api %{buildroot}/usr/bin/virt-api
install -m 555 virt-chroot %{buildroot}/usr/bin/virt-chroot
install -m 555 virt-controller %{buildroot}/usr/bin/virt-controller
install -m 555 virt-freezer %{buildroot}/usr/bin/virt-freezer
install -m 555 virt-handler %{buildroot}/usr/bin/virt-handler
install -m 555 virt-launcher %{buildroot}/usr/bin/virt-launcher
install -m 555 virt-operator %{buildroot}/usr/bin/virt-operator
install -m 555 virt-probe %{buildroot}/usr/bin/virt-probe
install -m 555 virtctl %{buildroot}/usr/bin/virtctl
install -m 555 container-disk %{buildroot}/usr/bin/container-disk
install -m 555 ./cmd/virt-launcher/node-labeller/node-labeller.sh %{buildroot}/usr/bin/node-labeller.sh
install -m 775 ./cmd/libguestfs/entrypoint.sh %{buildroot}/entrypoint.sh

%files
%license LICENSE THIRD_PARTY_LICENSES.txt

%files -n virtctl
%license LICENSE THIRD_PARTY_LICENSES.txt
/usr/bin/virtctl

%files api
%license LICENSE THIRD_PARTY_LICENSES.txt
/usr/bin/virt-api

%files chroot
%license LICENSE THIRD_PARTY_LICENSES.txt
/usr/bin/virt-chroot

%files controller
%license LICENSE THIRD_PARTY_LICENSES.txt
/usr/bin/virt-controller

%files freezer
%license LICENSE THIRD_PARTY_LICENSES.txt
/usr/bin/virt-freezer

%files handler
%license LICENSE THIRD_PARTY_LICENSES.txt
/usr/bin/virt-handler

%files launcher
%license LICENSE THIRD_PARTY_LICENSES.txt
/usr/bin/virt-launcher
/usr/bin/node-labeller.sh

%files operator
%license LICENSE THIRD_PARTY_LICENSES.txt
/usr/bin/virt-operator

%files probe
%license LICENSE THIRD_PARTY_LICENSES.txt
/usr/bin/virt-probe

%files container-disk
%license LICENSE THIRD_PARTY_LICENSES.txt
/usr/bin/container-disk

%files libguestfs-appliance
%license LICENSE THIRD_PARTY_LICENSES.txt
/entrypoint.sh

%changelog
* {{{.changelog_timestamp}}} - {{{$version}}}-1
- Initial Release

