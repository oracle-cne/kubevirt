{{{$version := printf "%s.%s.%s" .major .minor .patch}}}
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
Version:        {{{$version}}}
Release:        1%{?dist}
BuildArch:      x86_64
Summary:        Container images for Kubevirt
License:        Apache-2.0
Group:          System/Management
Url:            https://github.com/kubevirt/kubevirt
Source:         %{name}-%{version}.tar.bz2

BuildRequires: podman

%description
Container images for Kubevirt

%prep
%setup -q -n %{name}-%{version}

%build
%global base_image container-registry.oracle.com/os/oraclelinux:9-slim
%global base_image_full container-registry.oracle.com/os/oraclelinux:9
podman build \
    --network=host \
    --build-arg BASE_IMAGE=%{base_image} \
    --build-arg PACKAGE=kubevirt-api-%{version}-%{release}\
    %{build_args} \
    -t %{registry}/virt-api:v%{version} -f ./olm/builds/Dockerfile.virt-api ./olm/builds
podman save -o virt_api.tar %{registry}/virt-api:v%{version}

podman build \
    --network=host \
    --build-arg BASE_IMAGE=%{base_image} \
    --build-arg PACKAGE=kubevirt-controller-%{version}-%{release}\
    %{build_args} \
    -t %{registry}/virt-controller:v%{version} -f ./olm/builds/Dockerfile.virt-controller ./olm/builds
podman save -o virt_controller.tar %{registry}/virt-controller:v%{version}

podman build \
    --network=host \
    --build-arg BASE_IMAGE=%{base_image} \
    --build-arg PACKAGE=kubevirt-operator-%{version}-%{release}\
    %{build_args} \
    -t %{registry}/virt-operator:v%{version} -f ./olm/builds/Dockerfile.virt-operator ./olm/builds
podman save -o virt_operator.tar %{registry}/virt-operator:v%{version}

podman build \
    --network=host \
    --build-arg BASE_IMAGE=%{base_image} \
    --build-arg PACKAGE=kubevirt-exportproxy-%{version}-%{release}\
    %{build_args} \
    -t %{registry}/virt-exportproxy:v%{version} -f ./olm/builds/Dockerfile.virt-exportproxy ./olm/builds
podman save -o virt_exportproxy.tar %{registry}/virt-exportproxy:v%{version}

podman build \
    --network=host \
    --build-arg BASE_IMAGE=%{base_image} \
    --build-arg PACKAGE=kubevirt-exportserver-%{version}-%{release}\
    %{build_args} \
    -t %{registry}/virt-exportserver:v%{version} -f ./olm/builds/Dockerfile.virt-exportserver ./olm/builds
podman save -o virt_exportserver.tar %{registry}/virt-exportserver:v%{version}

podman build \
    --network=host \
    --build-arg BASE_IMAGE=%{base_image_full} \
    --build-arg PACKAGE=kubevirt-launcher-%{version}-%{release}\
    %{build_args} \
    -t %{registry}/virt-launcher:v%{version} -f ./olm/builds/Dockerfile.virt-launcher ./cmd/virt-launcher
podman save -o virt_launcher.tar %{registry}/virt-launcher:v%{version}

podman build \
    --network=host \
    --build-arg BASE_IMAGE=%{base_image_full} \
    --build-arg PACKAGE=kubevirt-handler-%{version}-%{release}\
    %{build_args} \
    -t %{registry}/virt-handler:v%{version} -f ./olm/builds/Dockerfile.virt-handler ./cmd/virt-handler
podman save -o virt_handler.tar %{registry}/virt-handler:v%{version}

podman build \
    --network=host \
    --build-arg BASE_IMAGE=%{base_image_full} \
    --build-arg PACKAGE=kubevirt-libguestfs-appliance-%{version}-%{release}\
    %{build_args} \
    -t %{registry}/libguestfs-tools-image:v%{version} -f ./olm/builds/Dockerfile.libguestfs-tools-image ./olm/builds
podman save -o libguestfs_tools_image.tar %{registry}/libguestfs-tools-image:v%{version}

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
* {{{.changelog_timestamp}}} - {{{$version}}}-1
- Initial Release
