
APP_CONTAINER="flask-app"
APP_PATH=$(sudo find $HOME -type d -name "$APP_CONTAINER")
# APP_PATH="/home/ubuntu/project/flask-app"

# echo $APP_PATH

WORKSPACE="${APP_PATH}/backup/mongodb"
# cd ${WORKSPACE}

if docker ps --filter "name=${APP_CONTAINER}" --filter "status=running" --format '{{.Names}}' | grep -q "^${APP_CONTAINER}"; then
    BACKUP_DIR="${WORKSPACE}/backup"     # e.g. /var/backups/mongo
    if [ -d "${BACKUP_DIR}" ]; then
        mkdir -p ${BACKUP_DIR}
    fi
fi
cd ${WORKSPACE}
DATE=$(date +%F)
docker run --rm \
  -v flask-app_mongo_data:/data \
  -v "${BACKUP_DIR}:/backup" \
  busybox \
  sh -c "cd /data && tar czf /backup/mongodb_data_$DATE.tar.gz ."

IMAGE_TAG="0.0.1" #TODO: create a function to get currrent tag and create  a new tag for image and store in a file

docker build --build-arg DATE=$(date +%F) -t hunterbxb/monggodb_backup:0.0.1 . --rm

# docker push hunterbxb/monggodb_backup:0.0.1