#! /usr/bin/env bash

function run_process {

    echo "-------------------------------------"
    echo "Processing..."
    echo

    git add --all
    git commit -m "${LOCAL_VARS[0]}"
    git push

    rez-release --no-latest
    rez-build -i --symlink 1

}

# Collect all input arguments into a local array of variables
LOCAL_VARS=("$@")

if [ ! "${#LOCAL_VARS[@]}" -eq 1 ]; then
    echo "Missing commit comment"
    exit 1
fi


run_process


# How to use:
# ./rez_release_build.sh "My commit message"
