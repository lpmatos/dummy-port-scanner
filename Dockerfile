FROM python:3.9.6-alpine3.14 as base

FROM base as install
WORKDIR /tmp
COPY [ "requirements.txt", "."]
RUN set -ex && pip install --no-cache-dir \
  --user --no-warn-script-location \
  -r ./requirements.txt

FROM base
RUN set -ex && apk update && \
  apk add --update --no-cache \
    bash=5.1.4-r0 \
    nmap=7.91-r0
COPY --from=install [ "/root/.local", "/usr/local" ]
WORKDIR /usr/src/code
COPY [ "./src", "." ]
RUN find ./ -iname "*.py" -type f -exec chmod a+x {} \; -exec echo {} \;

ENTRYPOINT [ "python", "main.py" ]
CMD [ "google.com" ]
