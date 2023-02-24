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
%global base_image container-registry.oracle.com/os/oraclelinux:8-slim
podman build \
    --build-arg BASE_IMAGE=%{base_image} \
    --build-arg PACKAGE=kubevirt-api-%{version}-%{release}\
    %{build_args} \
    -t %{registry}/virt-api:%{version} -f ./olm/builds/Dockerfile.virt-api ./olm/builds
podman save -o virt_api.tar %{registry}/virt-api:%{version}

%install
%__install -D -m 644 virt_api.tar %{buildroot}/usr/local/share/olcne/virt_api.tar

%files
%license LICENSE
/usr/local/share/olcne/virt_api.tar

%changelog
* {{{.changelog_timestamp}}} - {{{$version}}}-1
- Initial Release
