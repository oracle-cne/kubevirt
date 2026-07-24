#!/usr/bin/env bash

set -euo pipefail

log() {
    echo "build-container-images.sh: $*"
}

require_env() {
    local name="$1"
    local value="${!name:-}"

    log "checking required environment variable ${name}"
    if [[ -z "${value}" ]]; then
        log "required environment variable ${name} is not set" >&2
        exit 1
    fi
}

append_podman_build_args() {
    local raw_args="${PODMAN_BUILD_ARGS:-}"

    log "checking optional PODMAN_BUILD_ARGS"
    if [[ -z "${raw_args}" ]]; then
        log "PODMAN_BUILD_ARGS is not set"
        return
    fi

    log "using PODMAN_BUILD_ARGS: ${raw_args}"
    read -r -a podman_build_args <<< "${raw_args}"
}

has_yum_vars_mount() {
    local arg

    for arg in "${podman_build_args[@]}"; do
        if [[ "${arg}" == *":/etc/yum/vars"* ]]; then
            return 0
        fi
    done

    return 1
}

mount_yum_config() {
    local yum_repo_config_file="${YUM_REPO_CONFIG_FILE:-}"
    local yum_vars_dir="${YUM_VARS_DIR:-/etc/yum/vars}"

    log "starting yum repository configuration check"
    if [[ -z "${yum_repo_config_file}" ]]; then
        log "YUM_REPO_CONFIG_FILE is not set; using base image repository configuration"
        return
    fi

    if [[ "${yum_repo_config_file}" != /* ]]; then
        yum_repo_config_file="$(pwd)/${yum_repo_config_file}"
    fi

    log "checking yum repo config file ${yum_repo_config_file}"
    if [[ ! -s "${yum_repo_config_file}" ]]; then
        log "yum repo config file ${yum_repo_config_file} is missing or empty" >&2
        exit 1
    fi

    log "mounting yum repo config file ${yum_repo_config_file}"
    podman_build_args=(
        --volume "${yum_repo_config_file}:/etc/yum.repos.d/extra.repo:ro"
        "${podman_build_args[@]}"
    )

    log "checking yum vars directory ${yum_vars_dir}"
    if [[ ! -d "${yum_vars_dir}" ]]; then
        log "yum vars directory ${yum_vars_dir} is not present; continuing without yum vars mount"
        return
    fi

    if has_yum_vars_mount; then
        log "yum vars mount already present in podman build args"
        return
    fi

    log "mounting yum vars directory ${yum_vars_dir}"
    podman_build_args=(
        --volume "${yum_vars_dir}:/etc/yum/vars:ro"
        "${podman_build_args[@]}"
    )
}

build_container_image() {
    local image_name="$1"
    local dockerfile="$2"
    local context_dir="$3"
    local base_image="$4"
    local package_name="$5"
    local output_tar="$6"
    local image_ref="${REGISTRY}/${image_name}:${IMAGE_TAG}"

    log "starting build for ${image_ref}"
    log "using dockerfile ${dockerfile}"
    log "using context ${context_dir}"
    log "using base image ${base_image}"
    log "installing package ${package_name}"
    podman build \
        --network=host \
        --build-arg "BASE_IMAGE=${base_image}" \
        --build-arg "PACKAGE=${package_name}" \
        "${podman_build_args[@]}" \
        -t "${image_ref}" -f "${dockerfile}" "${context_dir}"

    log "saving ${image_ref} to ${output_tar}"
    podman save -o "${output_tar}" "${image_ref}"
    log "completed build for ${image_ref}"
}

main() {
    log "starting kubevirt container image RPM build"
    require_env REGISTRY
    require_env IMAGE_TAG
    require_env BASE_IMAGE
    require_env BASE_IMAGE_FULL
    require_env PACKAGE_VERSION_RELEASE

    podman_build_args=()
    append_podman_build_args
    mount_yum_config

    build_container_image virt-api ./olm/builds/Dockerfile.virt-api ./olm/builds "${BASE_IMAGE}" "kubevirt-api-${PACKAGE_VERSION_RELEASE}" virt_api.tar
    build_container_image virt-controller ./olm/builds/Dockerfile.virt-controller ./olm/builds "${BASE_IMAGE}" "kubevirt-controller-${PACKAGE_VERSION_RELEASE}" virt_controller.tar
    build_container_image virt-operator ./olm/builds/Dockerfile.virt-operator ./olm/builds "${BASE_IMAGE}" "kubevirt-operator-${PACKAGE_VERSION_RELEASE}" virt_operator.tar
    build_container_image virt-exportproxy ./olm/builds/Dockerfile.virt-exportproxy ./olm/builds "${BASE_IMAGE}" "kubevirt-exportproxy-${PACKAGE_VERSION_RELEASE}" virt_exportproxy.tar
    build_container_image virt-exportserver ./olm/builds/Dockerfile.virt-exportserver ./olm/builds "${BASE_IMAGE}" "kubevirt-exportserver-${PACKAGE_VERSION_RELEASE}" virt_exportserver.tar
    build_container_image virt-launcher ./olm/builds/Dockerfile.virt-launcher ./cmd/virt-launcher "${BASE_IMAGE_FULL}" "kubevirt-launcher-${PACKAGE_VERSION_RELEASE}" virt_launcher.tar
    build_container_image virt-handler ./olm/builds/Dockerfile.virt-handler ./cmd/virt-handler "${BASE_IMAGE_FULL}" "kubevirt-handler-${PACKAGE_VERSION_RELEASE}" virt_handler.tar
    build_container_image libguestfs-tools-image ./olm/builds/Dockerfile.libguestfs-tools-image ./olm/builds "${BASE_IMAGE_FULL}" "kubevirt-libguestfs-appliance-${PACKAGE_VERSION_RELEASE}" libguestfs_tools_image.tar

    log "completed kubevirt container image RPM build"
}

main "$@"
