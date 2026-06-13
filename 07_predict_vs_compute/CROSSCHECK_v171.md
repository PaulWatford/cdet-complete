# CROSSCHECK_v171 — Docker one-command deployment

**Claims.** (1) Dockerfile: python:3.12-slim + gcc/g++, `pip install -e ".[all]"`, bakes `make CC=gcc test` (194/194)
into the build, ENTRYPOINT `cdet` / default CMD `validate`. (2) .dockerignore excludes build/runtime artifacts. (3)
`docker_check.py` gates the recipe structure; the build commands are the project's real gates. (4) CI builds the image
and runs `cdet validate` in the container. (5) Frozen engine untouched.

**Honest note.** `docker build` is NOT run in this sandbox (no Docker daemon). The gate validates the recipe
structurally; every command the Dockerfile runs was verified natively (`make test` → 194/194, `cdet validate` → 5/5)
and is covered by its own gate. On GitHub the CI `docker` job performs the real build.

**Reproduce.**
```
python3 docker_check.py                 # recipe gate
docker build -t cdet-suite . && docker run --rm cdet-suite     # on a Docker host
```

**Frozen engine.** Untouched: `cd engine && make CC=gcc test` → 194/194; constants bit-identical
(−0.5082750022348369  0.44040518398732875).
