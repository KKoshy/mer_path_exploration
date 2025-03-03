#!/bin/bash -ex

# directory/directories where the auto-linting will be executed
SRC_DIRS=${1:-"lib rvf_analysis svf_analysis"}

echo "Running linting checks for source code in ${SRC_DIRS} with directory context $(pwd)"

for src_dir in ${SRC_DIRS}
do
    [ ! -d ./${src_dir} ] \
        && echo "Running lint check with incorrect directory context. Directory ${src_dir} not present" \
        && exit 1
done

autoflake \
    --remove-all-unused-imports \
    --recursive \
    --remove-unused-variables \
    --in-place \
    --exclude=__init__.py \
    --check-diff \
    ${SRC_DIRS}

black \
    --check \
    --diff \
    ${SRC_DIRS}

isort \
    --profile=black \
    --check-only \
    ${SRC_DIRS}
