
%global debug_package %{nil}
%global _buildhost build-ol%{?oraclelinux}-%{?_arch}.oracle.com
%global build_handler 1

Name:		kubevirt
Version:	1.6.2
Release:	1%{?dist}
Summary:	KubeVirt 

License:	Apache License 2.0
URL:		https://github.com/kubevirt/kubevirt
Source0:	%{name}-%{version}.tar.bz2

%if %{?oraclelinux} == 9
BuildRequires:	libvirt-devel == 9.0.0
%else
BuildRequires:	libvirt-devel
%endif
BuildRequires:  gcc
BuildRequires:  glibc-static
BuildRequires:  golang >= 1.20.12

%package -n virtctl
Summary: CLI for KubeVirt

%package api
Summary: KubeVirt API Server

%package chroot
Summary: Chroot utility for KubeVirt

%package controller
Summary: KubeVirt Kubernetes controller

%package freezer
Summary: VM freezing utility for KubeVirt

%package exportserver
Summary: The KubeVirt export server daemon

%package exportproxy
Summary: The KubeVirt export proxy daemon

%package handler
Summary: KubeVirt Handler daemon
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
Summary: KubeVirt Launcher daemon
# See ./hack/rpm-deps.sh to understand how this set of
# dependencies was determined.
# - base
Requires: acl
Requires: curl
# - base extra
Requires: coreutils
Requires: glibc-minimal-langpack
# - launcher base
%if %{?oraclelinux} == 9
Requires: libvirt-client == 9.0.0
Requires: libvirt-daemon-driver-qemu == 9.0.0
%else
Requires: libvirt-client
Requires: libvirt-daemon-driver-qemu
%endif
Requires: qemu-kvm-core
# - launcher x86
%ifarch %{arm} arm64 aarch64
Requires: edk2-aarch64
%else
Requires: edk2-ovmf
Requires: seabios
%endif
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
Requires: kubevirt-launcher-monitor = %{version}-%{release}

%package launcher-monitor
Summary: Monitor service for the KubeVirt Launcher

%package operator
Summary: KubeVirt Operator

%package probe
Summary: Utility use by KubeVirt to probe VM status

%package container-disk
Summary: Container disk utility for KubeVirt

%package libguestfs-appliance
Summary: A set of useful utilities for interacting with VM filesystems
Requires: libguestfs-appliance
# - base
Requires: libguestfs-tools
%if %{?oraclelinux} == 9
Requires: libvirt-daemon-driver-qemu == 9.0.0
%else
Requires: libvirt-daemon-driver-qemu
%endif
Requires: qemu-kvm-core
%ifarch %{arm} arm64 aarch64
Requires: edk2-aarch64
%else
Requires: edk2-ovmf
Requires: seabios
%endif

%description
Managed virtualized infrastructure within Kubernetes.

%description -n virtctl
The CLI for KubeVirt.  virtctl makes it easy to manage virtualized workloads in
a Kubernetes cluster using KubeVirt.

%description api
The KubeVirt API Server.  It serves requests from other KubeVirt components.

%description chroot
A utility used by KubeVirt to do chroot-like operations in mount namespaces.

%description controller
The KubeVirt Kubernetes controller.  It implements the logic required to service
the kubevirt.io/v1 family of Kubernetes custom resources.

%description exportproxy
The KubeVirt export proxy

%description exportserver
The KubeVirt export server

%description freezer
A VM freexing utility used by KubeVirt

%description handler
The KubeVirt Handler service.  It listens for virtual workloads destined for the
host it is running on and manages the local set of workloads.

%description launcher
The KubeVirt Launcer service.  Each VM pod uses this utility to launch the VM
that is running within the pod.

%description launcher-monitor
A monitor service for the KubeVirt Launcher

%description operator
The KubeVirt Operator.

%description probe
A utility used by KubeVirt to probe the health of VMs.

%description container-disk
A utility used by KubeVirt to manage container disks.

%description libguestfs-appliance
A set of useful tools for interacting with VM filesystems.

%prep
%setup -q

%build
go build -trimpath=false -tags selinux -ldflags="-X main.version=v%{version}" ./cmd/virt-api
go build -trimpath=false -tags selinux -ldflags="-X main.version=v%{version}" ./cmd/virt-chroot
go build -trimpath=false -tags selinux -ldflags="-X main.version=v%{version}" ./cmd/virt-controller
go build -trimpath=false -tags selinux -ldflags="-X main.version=v%{version}" ./cmd/virt-exportproxy
go build -trimpath=false -tags selinux -ldflags="-X main.version=v%{version}" ./cmd/virt-exportserver
go build -trimpath=false -tags selinux -ldflags="-X main.version=v%{version}" ./cmd/virt-freezer
%if 0%{?build_handler}
go build -trimpath=false -tags selinux -ldflags="-X main.version=v%{version}" ./cmd/virt-handler
%endif
go build -trimpath=false -tags selinux -ldflags="-X main.version=v%{version}" ./cmd/virt-launcher-monitor
go build -trimpath=false -tags selinux -ldflags="-X main.version=v%{version}" ./cmd/virt-launcher
go build -trimpath=false -tags selinux -ldflags="-X main.version=v%{version}" ./cmd/virt-operator
go build -trimpath=false -tags selinux -ldflags="-X main.version=v%{version}" ./cmd/virt-probe
go build -trimpath=false -tags selinux -ldflags="-X main.version=v%{version}" ./cmd/virt-tail
go build -trimpath=false -tags selinux -ldflags="-X main.version=v%{version}" ./cmd/virtctl
cc -o container-disk -static ./cmd/container-disk-v2alpha/main.c

%install
install -m 755 -d %{buildroot}/usr/bin
install -m 555 virt-api %{buildroot}/usr/bin/virt-api
install -m 555 virt-chroot %{buildroot}/usr/bin/virt-chroot
install -m 555 virt-controller %{buildroot}/usr/bin/virt-controller
install -m 555 virt-exportproxy %{buildroot}/usr/bin/virt-exportproxy
install -m 555 virt-exportserver %{buildroot}/usr/bin/virt-exportserver
install -m 555 virt-freezer %{buildroot}/usr/bin/virt-freezer
%if 0%{?build_handler}
install -m 555 virt-handler %{buildroot}/usr/bin/virt-handler
%endif
install -m 555 virt-launcher-monitor %{buildroot}/usr/bin/virt-launcher-monitor
install -m 555 virt-launcher %{buildroot}/usr/bin/virt-launcher
install -m 555 virt-operator %{buildroot}/usr/bin/virt-operator
install -m 555 virt-probe %{buildroot}/usr/bin/virt-probe
install -m 555 virt-tail %{buildroot}/usr/bin/virt-tail
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
%if 0%{?build_handler}
/usr/bin/virt-handler
%endif

%files launcher-monitor
%license LICENSE THIRD_PARTY_LICENSES.txt
/usr/bin/virt-launcher-monitor
%caps(cap_net_bind_service=pe) /usr/bin/virt-launcher-monitor

%files launcher
%license LICENSE THIRD_PARTY_LICENSES.txt
/usr/bin/virt-launcher
/usr/bin/node-labeller.sh
/usr/bin/virt-tail
%caps(cap_net_bind_service=pe) /usr/bin/virt-launcher

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
* Wed Oct 08 2025 Prasad Shirodkar <prasad.shirodkar@oracle.com> - 1.6.2-1
- Initial Release

