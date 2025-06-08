
CURR_DIR=$(dirname $0)

docker-compose -f ${CURR_DIR}/MongoDB/docker-compose.yml down

docker ps -a