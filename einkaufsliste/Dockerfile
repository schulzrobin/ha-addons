ARG BUILD_FROM
FROM $BUILD_FROM

RUN apk add --no-cache python3 py3-pip

WORKDIR /opt/einkaufsliste
COPY rootfs/opt/einkaufsliste/ /opt/einkaufsliste/

RUN pip3 install --no-cache-dir -r /opt/einkaufsliste/requirements.txt

COPY run.sh /run.sh
RUN chmod a+x /run.sh

EXPOSE 8099
CMD [ "/run.sh" ]
