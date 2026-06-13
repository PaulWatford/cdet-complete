#!/bin/sh
# One-command Hubbard correlation pattern + animation.
cd "$(dirname "$0")/06_hubbard_pattern" && python3 hubbard_pattern.py --anim "$@"
