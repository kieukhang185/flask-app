# Use a minimal base
FROM alpine:latest

LABEL maintainer="kieukhang1805@gmail.com"
WORKDIR /backup

ARG DATE

# Copy in the pre-created tarball
COPY ./backup/mongodb_data_${DATE}.tar.gz /backup/

# Default: list the archive so you can verify it’s there
CMD ["ls", "-lh", "/backup"]

