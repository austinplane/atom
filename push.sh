#!/bin/bash

if [ -z "$1" ]; then
	echo "Usage: $0 <commit_message>"
	exit 1
fi

COMMIT_MESSAGE=$1
git add .
git commit -m "$COMMIT_MESSAGE"
git push
