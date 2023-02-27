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

%package -n virtctl
Summary: CLI for Kubevirt

%package api
Summary: TODO

%package chroot
Summary: TODO

%package controller
Summary: TODO

%package exportproxy
Summary: TODO

%package exportserver
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
Requires: vim-minimal
# - base extra
Requires: coreutils
Requires: glibc-minimal-langpack
Requires: libcurl-minimal
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

%package launcher-monitor
Summary: TODO

%package launcher
Summary: TODO
# See ./hack/rpm-deps.sh to understand how this set of
# dependencies was determined.
# - base
Requires: acl
Requires: curl
Requires: vim-minimal
# - base extra
Requires: coreutils
Requires: glibc-minimal-langpack
Requires: libcurl-minimal
# - launcher base
Requires: libvirt-client
Requires: libvirt-daemon-driver-qemu
Requires: qemu-kvm-core
# - launcher x86
Requires: edk2-ovmf
Requires: qemu-kvm-hw-usbredir
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


%package operator
Summary: TODO

%package probe
Summary: TODO

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

%description exportproxy
TODO

%description exportserver
TODO

%description freezer
TODO

%description handler
TODO

%description launcher-monitor
TODO

%description launcher
TODO

%description operator
TODO

%description probe
TODO

%prep
%setup -q

%build
go build ./cmd/virt-api
go build ./cmd/virt-chroot
go build ./cmd/virt-controller
go build ./cmd/virt-exportproxy
go build ./cmd/virt-exportserver
go build ./cmd/virt-freezer
go build ./cmd/virt-handler
go build ./cmd/virt-launcher-monitor
go build ./cmd/virt-launcher
go build ./cmd/virt-operator
go build ./cmd/virt-probe
go build ./cmd/virtctl

%install
install -m 755 -d %{buildroot}/usr/bin
install -m 555 virt-api %{buildroot}/usr/bin/virt-api
install -m 555 virt-chroot %{buildroot}/usr/bin/virt-chroot
install -m 555 virt-controller %{buildroot}/usr/bin/virt-controller
install -m 555 virt-exportproxy %{buildroot}/usr/bin/virt-exportproxy
install -m 555 virt-exportserver %{buildroot}/usr/bin/virt-exportserver
install -m 555 virt-freezer %{buildroot}/usr/bin/virt-freezer
install -m 555 virt-handler %{buildroot}/usr/bin/virt-handler
install -m 555 virt-launcher-monitor %{buildroot}/usr/bin/virt-launcher-monitor
install -m 555 virt-launcher %{buildroot}/usr/bin/virt-launcher
install -m 555 virt-operator %{buildroot}/usr/bin/virt-operator
install -m 555 virt-probe %{buildroot}/usr/bin/virt-probe
install -m 555 virtctl %{buildroot}/usr/bin/virtctl

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

%files exportproxy
%license LICENSE THIRD_PARTY_LICENSES.txt
/usr/bin/virt-exportproxy

%files exportserver
%license LICENSE THIRD_PARTY_LICENSES.txt
/usr/bin/virt-exportserver

%files freezer
%license LICENSE THIRD_PARTY_LICENSES.txt
/usr/bin/virt-freezer

%files handler
%license LICENSE THIRD_PARTY_LICENSES.txt
/usr/bin/virt-handler

%files launcher-monitor
%license LICENSE THIRD_PARTY_LICENSES.txt
/usr/bin/virt-launcher-monitor

%files launcher
%license LICENSE THIRD_PARTY_LICENSES.txt
/usr/bin/virt-launcher

%files operator
%license LICENSE THIRD_PARTY_LICENSES.txt
/usr/bin/virt-operator

%files probe
%license LICENSE THIRD_PARTY_LICENSES.txt
/usr/bin/virt-probe

%changelog
* {{{.changelog_timestamp}}} - {{{$version}}}-1
- Initial Release

