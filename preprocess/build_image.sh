#!/bin/bash -e
image_name=gcr.io/ideate-2021/gcp-kubeflow-rul/process_data
image_tag=latest
full_image_name=${image_name}:${image_tag}

cd "$(dirname "$0")"
docker build  -t "${full_image_name}" .
docker push "$full_image_name"

#--no-cache
# Output the strict image name, which contains the sha256 image digest
#docker inspect --format="{{index .RepoDigests 0}}" "${full_image_name}"
