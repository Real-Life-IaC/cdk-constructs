# Release Package

Bump a Python project version using Commitizen and release a new version in GitHub.

## Usage

Example Workflow using:

```yaml
name: Release Package

on:
  push:
    branches:
      - main

jobs:
  release:
    name: Release
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Bump Version and Release
        uses: ./.github/actions/release
        with:
          machine_user_pat: ${{ secrets.MACHINE_USER_PAT }}
```

## Inputs

| name | type | default | description |
| ---- | ----- | ------- | ----------- |
| machine_user_pat | string | | Personal Access Token (PAT) for the GitHub Machine User. Can be passed in using `${{ secrets.MACHINE_USER_PAT }}`. |
