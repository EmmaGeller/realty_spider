docker run \
 -it  --rm --link=condescending_minsky:pg \
 -e POSTGRESQL_HOST=pg \
 -e POSTGRESQL_PORT=5432 realtyspider:1.0.1