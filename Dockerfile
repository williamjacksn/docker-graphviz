FROM alpine:3.16.0

ARG GRAPHVIZ_VERSION="3.0.0-r0"

RUN /sbin/apk add --no-cache "graphviz=${GRAPHVIZ_VERSION}"

LABEL org.opencontainers.image.authors="William Jackson <william@subtlecoolness.com>" \
      org.opencontainers.image.version="${GRAPHVIZ_VERSION}"
