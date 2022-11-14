FROM alpine:3.16.3

ARG GRAPHVIZ_VERSION="3.0.0-r1"

RUN /sbin/apk add --no-cache "graphviz=${GRAPHVIZ_VERSION}" ttf-freefont

LABEL org.opencontainers.image.authors="William Jackson <william@subtlecoolness.com>" \
      org.opencontainers.image.version="${GRAPHVIZ_VERSION}"
