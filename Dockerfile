FROM alpine:3.17.0

ARG GRAPHVIZ_VERSION="7.0.2-r0"

RUN /sbin/apk add --no-cache "graphviz=${GRAPHVIZ_VERSION}" ttf-liberation

LABEL org.opencontainers.image.authors="William Jackson <william@subtlecoolness.com>" \
      org.opencontainers.image.version="${GRAPHVIZ_VERSION}"
