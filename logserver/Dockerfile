FROM ubuntu:20.04

ADD ./ /usr/local/services/log-converter

RUN apt-get update; \
    apt-get install -y --no-install-recommends python3 python3-pip vim; \
    pip3 install -r /usr/local/services/log-converter/requirements.txt; \
    apt-get autoremove -y python3-pip; \
    rm -rf /var/lib/apt/lists/*;

CMD ["/usr/local/services/log-converter/start.sh"]