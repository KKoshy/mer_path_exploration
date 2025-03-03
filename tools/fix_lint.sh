#!/bin/bash -x

# directory/directories where the auto-linting will be executed
SRC_DIRS=${1:-"lib rvf_analysis svf_analysis"}

echo "Running auto-linting for source code in ${SRC_DIRS}."
echo "NOTE: Code duplication issues canot be fixed by auto linting."

for src_dir in ${SRC_DIRS}
do
    [[ ! -d ./${src_dir} ]] \
        && echo "Running lint fix with incorrect directory context. Directory ${src_dir} not present" \
        && exit 1
done

autoflake --remove-all-unused-imports --recursive --remove-unused-variables --in-place --exclude=__init__.py \
    ${SRC_DIRS}

black \
    ${SRC_DIRS}


isort \
    --profile=black \
    ${SRC_DIRS}