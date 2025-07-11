# Use a minimal base
FROM alpine:latest

LABEL maintainer="kieukhang1805@gmail.com"
WORKDIR /backup

# Copy in the pre-created tarball
COPY backup/mongodb_data.tar_$(date +%F).gz /backup/

# Default: list the archive so you can verify it’s there
CMD ["ls", "-lh", "/backup"]

