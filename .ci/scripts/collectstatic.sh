#!/bin/bash
docker run --rm  \
--env-file $env \
--network db-net \
--mount source=static_volume,target=/app/static \
${CI_REGISTRY_IMAGE} -m manage collectstatic --noinput;
