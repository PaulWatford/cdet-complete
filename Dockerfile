# CDet suite -- one-command deployment.
#   docker build -t cdet-suite .
#   docker run --rm cdet-suite                 # default: runs `cdet validate` (all gates)
#   docker run --rm cdet-suite converge        # any subcommand
#   docker run --rm -v "$PWD/out:/opt/cdet/out" cdet-suite export docc --format all --out out
FROM python:3.12-slim

# build tools for the frozen C reference engine (and the optional native bindings)
RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc g++ make libc6-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /opt/cdet
COPY . /opt/cdet

# install the suite with all optional extras (rich tables, matplotlib figures, HDF5 export)
RUN pip install --no-cache-dir -e ".[all]"

# bake validation into the image: it will not build unless the frozen engine passes 194/194
RUN cd engine && make CC=gcc test

# default entrypoint is the unified CLI; default command runs the validation gates
ENTRYPOINT ["cdet"]
CMD ["validate"]
