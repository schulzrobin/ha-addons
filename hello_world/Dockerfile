ARG BUILD_FROM
FROM $BUILD_FROM

SHELL ["/bin/bash", "-o", "pipefail", "-c"]

RUN apk add update && apt-get install -y --no-install-recommends python3 python3-pip
    #&& pip3 install --no-cache-dir -U \
    #&& pip3 install Flask, requests

COPY run.sh /
COPY gen1_update.py /
RUN chmod a+x /run.sh

CMD [ "/run.sh" ]