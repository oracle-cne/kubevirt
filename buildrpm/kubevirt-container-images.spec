
%if 0%{?with_debug}
# https://bugzilla.redhat.com/show_bug.cgi?id=995136#c12
%global _dwz_low_mem_die_limit 0
%else
%global debug_package   %{nil}
%endif

%{!?registry: %global registry container-registry.oracle.com/olcne}
%global _name   	kubevirt
%global _buildhost	build-ol%{?oraclelinux}-%{?_arch}.oracle.com


Name:           %{_name}-container-images
Version:        1.7.4
Release:        1%{?dist}
Summary:        Container images for Kubevirt
License:        Apache-2.0
Group:          System/Management
Url:            https://github.com/kubevirt/kubevirt
Source:         %{name}-%{version}.tar.bz2

BuildRequires: podman
BuildRequires: bash
BuildRequires: golang >= 1.20.12

%description
Container images for Kubevirt

%prep
%setup -q -n %{name}-%{version}

%build
%if %{?oraclelinux} == 9
%global base_image container-registry.oracle.com/os/oraclelinux:9-slim
%global base_image_full container-registry.oracle.com/os/oraclelinux:9
%else
%global base_image container-registry.oracle.com/os/oraclelinux:8-slim
%global base_image_full container-registry.oracle.com/os/oraclelinux:8
%endif
%global image_tag v%{version}
REGISTRY="%{registry}" \
IMAGE_TAG="%{image_tag}" \
BASE_IMAGE="%{base_image}" \
BASE_IMAGE_FULL="%{base_image_full}" \
PACKAGE_VERSION_RELEASE="%{version}-%{release}" \
bash ./olm/build-container-images.sh

%install
%__install -D -m 644 virt_api.tar %{buildroot}/usr/local/share/olcne/virt_api.tar
%__install -D -m 644 virt_controller.tar %{buildroot}/usr/local/share/olcne/virt_controller.tar
%__install -D -m 644 virt_operator.tar %{buildroot}/usr/local/share/olcne/virt_operator.tar
%__install -D -m 644 virt_exportproxy.tar %{buildroot}/usr/local/share/olcne/virt_exportproxy.tar
%__install -D -m 644 virt_exportserver.tar %{buildroot}/usr/local/share/olcne/virt_exportserver.tar
%__install -D -m 644 virt_handler.tar %{buildroot}/usr/local/share/olcne/virt_handler.tar
%__install -D -m 644 virt_launcher.tar %{buildroot}/usr/local/share/olcne/virt_launcher.tar
%__install -D -m 644 libguestfs_tools_image.tar %{buildroot}/usr/local/share/olcne/libguestfs_tools_image.tar

%files
%license LICENSE
/usr/local/share/olcne/virt_api.tar
/usr/local/share/olcne/virt_controller.tar
/usr/local/share/olcne/virt_operator.tar
/usr/local/share/olcne/virt_handler.tar
/usr/local/share/olcne/virt_launcher.tar
/usr/local/share/olcne/virt_exportproxy.tar
/usr/local/share/olcne/virt_exportserver.tar
/usr/local/share/olcne/libguestfs_tools_image.tar

%changelog
* Fri Jun 05 2026 Oracle Cloud Native Environment Authors <noreply@oracle.com> - 1.7.4-1
- Initial Release
