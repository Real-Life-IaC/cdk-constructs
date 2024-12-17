#!/bin/bash

set -e

# Check if INPUT_MACHINE_USER_PAT is set
if [[ -z "${INPUT_MACHINE_USER_PAT}" ]]; then
  echo 'Missing input "machine_user_pat: ${{ secrets.MACHINE_USER_PAT }}".'
  exit 1
fi

# Display Commitizen version
echo "Commitizen version: $(cz version)"


# GitHub authentication setup
echo "Setting up git..."
echo "${INPUT_MACHINE_USER_PAT}" | gh auth login --with-token
gh auth status

mkdir _bump
cd _bump

git init

# Configure git settings to avoid dubious ownership error
git config user.name "${GITHUB_ACTOR}"
git config user.email "${GITHUB_ACTOR}@users.noreply.github.com"
git config --global init.defaultBranch main
git remote add origin "https://x-access-token:${INPUT_MACHINE_USER_PAT}@github.com/${GITHUB_REPOSITORY}.git"

# Set up repository and checkout main branch
echo "Repository: ${GITHUB_REPOSITORY}"
git fetch
git checkout main

echo "Git name: $(git config --get user.name)"
echo "Git email: $(git config --get user.email)"

# Get the current version tag using Commitizen
TAG="$(cz version --project)"
echo "Current tag: ${TAG}"

# Run Commitizen to bump the version and update changelog, ignoring specific errors
echo "Running Commitizen"
cz --no-raise 21,3 bump --yes --changelog

# Push changes to the main branch and tags
echo "Pushing to main branch..."
git push origin "HEAD:main" --force
git push --tags

# Get the new tag (this assumes that the version bump creates a new tag)
NEW_TAG="$(cz version --project)"
echo "New tag: ${NEW_TAG}"

# Compare old and new tags, update if necessary
if [[ "${TAG}" != "${NEW_TAG}" ]]; then
  echo "Updating latest tag..."
  git tag -f latest
  git push origin latest --force

  MAJOR_VERSION=$(echo "${NEW_TAG}" | grep -oE '^[0-9]+')
  echo "Creating or updating major version tag: ${MAJOR_VERSION}"
  git tag -f "${MAJOR_VERSION}"
  git push origin "${MAJOR_VERSION}" --force

  echo "Creating release ${NEW_TAG}..."
  gh release create "${NEW_TAG}" --title "${NEW_TAG}" --notes-file CHANGELOG.md
else
  echo "No new tag to create release for."
fi

echo "Done."
