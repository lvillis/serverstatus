FROM lvillis/alpine:3.14-python3.10.0 AS base

COPY /server/requirements.txt .

FROM lvillis/alpine:python-builder AS builder

COPY /server/requirements.txt .

RUN python3 -m pip wheel --wheel-dir=/root/wheels -r requirements.txt


FROM base AS runtime

COPY --from=builder /root/wheels /root/wheels

RUN python3 -m pip install -r requirements.txt --no-index --find-links=/root/wheels

COPY /server /root/src
WORKDIR /root/src/

CMD python3 main.py