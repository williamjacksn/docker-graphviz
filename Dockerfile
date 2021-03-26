FROM alpine:3.13.3

ARG GRAPHVIZ_VERSION="2.44.0-r1"

RUN /sbin/apk add --no-cache "graphviz=${GRAPHVIZ_VERSION}" ttf-freefont \
 && /sbin/apk add --no-cache --repository=http://dl-cdn.alpinelinux.org/alpine/v3.12/community ttf-roboto

LABEL org.opencontainers.image.authors="William Jackson <william@subtlecoolness.com>" \
      org.opencontainers.image.version="${GRAPHVIZ_VERSION}"
