#!/usr/bin/env bash

param=""


if [ -n "$POSTGRESQL_HOST" ];then
    param="$param --set POSTGRESQL_HOST=$POSTGRESQL_HOST "
    echo "POSTGRESQL_HOST: $POSTGRESQL_HOST"
fi

if [ -n "$POSTGRESQL_DBNAME" ];then
   param="$param --set POSTGRESQL_DBNAME=$POSTGRESQL_DBNAME "
   echo "POSTGRESQL_DBNAME: $POSTGRESQL_DBNAME"
fi

if [ -n "$POSTGRESQL_PASSWD" ];then
   param="$param --set POSTGRESQL_PASSWD=$POSTGRESQL_PASSWD "
   echo "POSTGRESQL_PASSWD: $POSTGRESQL_PASSWD"
fi


if [ -n "$POSTGRESQL_PASSWD" ];then
   param="$param --set POSTGRESQL_PASSWD=$POSTGRESQL_PASSWD "
   echo "POSTGRESQL_PASSWD: $POSTGRESQL_PASSWD"
fi

if [ -n "$POSTGRESQL_USER" ];then
   param="$param --set POSTGRESQL_USER=$POSTGRESQL_USER "
   echo "POSTGRESQL_USER: $POSTGRESQL_USER"
fi

if [ -n "$POSTGRESQL_PORT" ];then
   param="$param --set POSTGRESQL_PORT=$POSTGRESQL_PORT "
   echo "POSTGRESQL_PORT: $POSTGRESQL_PORT"
fi


if [ -n "$REDIS_HOST" ];then
   param="$param  --set REDIS_HOST=$REDIS_HOST "
   echo "REDIS_HOST: $REDIS_HOST"
fi


if [ -n "$REDIS_PORT" ];then
   param="$param --set REDIS_HOST=$REDIS_PORT "
   echo "REDIS_PORT: $REDIS_PORT"
fi

scrapy crawl realtySpider $param