FROM python:3.6
ADD . /realty_sprider
WORKDIR /realty_sprider
COPY pip.conf /root/.pip/
COPY docker-entrypoint.sh /usr/local/bin
RUN mkdir -p /root/.pip && chmod +x /usr/local/bin/docker-entrypoint.sh && ln -s /usr/local/bin/docker-entrypoint.sh /docker-entrypoint.sh
RUN pip3 install -r requirements.txt
EXPOSE 6800
CMD ["docker-entrypoint.sh"]