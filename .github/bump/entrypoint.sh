#!/bin/bash

set -e

if [[ -z "${INPUT_GITHUB_TOKEN}" ]]; then
  echo 'Missing input "github_token: ${{ secrets.PERSONAL_ACCESS_TOKEN }}".'
  exit 1
fi

echo "Commitizen version: $(cz version)"

echo "Configuring Git username and email..."

mkdir _bump
cd _bump

git init

git config user.name "${GITHUB_ACTOR}"
git config user.email "${GITHUB_ACTOR}@users.noreply.github.com"

git remote add origin "https://x-access-token:${INPUT_GITHUB_TOKEN}@github.com/${GITHUB_REPOSITORY}.git"
git fetch
echo "Git name: $(git config --get user.name)"
echo "Git email: $(git config --get user.email)"


echo "Repository: ${GITHUB_REPOSITORY}"

git checkout main

echo "Running Commitizen"
cz --no-raise 21 bump --yes --changelog

REV="$(cz version --project)"
echo "version=${REV}" >> $GITHUB_OUTPUT

echo "Pushing to branch..."
git push origin "HEAD:main" --force
git push --tags

SHA="$(git rev-parse HEAD)"
echo "new_sha=${SHA}" >> $GITHUB_OUTPUT

echo "Done."
