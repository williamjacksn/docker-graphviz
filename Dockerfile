FROM alpine:3.12.1

ARG GRAPHVIZ_VERSION="2.42.3-r0"

RUN /sbin/apk add --no-cache "graphviz=${GRAPHVIZ_VERSION}" ttf-freefont ttf-roboto

LABEL org.opencontainers.image.authors="William Jackson <william@subtlecoolness.com>" \
      org.opencontainers.image.version="${GRAPHVIZ_VERSION}"
