FROM alpine

RUN apk update && \
    apk add --no-cache build-base && \
    apk add --no-cache python3-dev && \
    apk add --no-cache python3 && \
    apk add --no-cache python2 && \
    apk add --no-cache bash && \
    python3 -m ensurepip && \
    python2 -m ensurepip && \
    rm -r /usr/lib/python*/ensurepip && \
    pip3 install --upgrade pip setuptools && \
    if [ ! -e /usr/bin/pip ]; then ln -s pip3 /usr/bin/pip ; fi && \
    if [[ ! -e /usr/bin/python ]]; then ln -sf /usr/bin/python3 /usr/bin/python; fi && \
    rm -r /root/.cache && \
    pip2 install supervisor

COPY . /crypto
WORKDIR /crypto

RUN python3 setup.py develop
CMD ["bash"]