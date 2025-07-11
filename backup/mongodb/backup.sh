
workspace="backup/mongodb"

cd ${workspace}

if [[ -d backup ]]; then
    mkdir -p backup
fi

docker run --rm \
  -v flask-app_mongo_data:/data \
  -v "$(pwd)"/backup:/backup \
  busybox \
  sh -c "cd /data && tar czf /backup/mongodb_data_$(date +%F).tar.gz ."