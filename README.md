# install-modflow-action

[![CI](https://github.com/modflowpy/install-modflow-action/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/modflowpy/install-modflow-action/actions/workflows/ci.yml)

An action to install MODFLOW 6 and related programs.

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->


- [Overview](#overview)
- [Usage](#usage)
  - [Inputs](#inputs)
    - [`github_token`](#github_token)
    - [`path`](#path)
    - [`repo`](#repo)
  - [Outputs](#outputs)
    - [`cache-hit`](#cache-hit)
- [MODFLOW Resources](#modflow-resources)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

## Overview

This action uses [FloPy's](https://github.com/modflowpy/flopy) [`get-modflow`](https://github.com/modflowpy/flopy/blob/develop/docs/get_modflow.md) utility to install MODFLOW 6 and a number of related binaries. The `get-modflow` utility is invoked directly if the `flopy` Python package is installed, otherwise it is downloaded as a standalone, dependency-free script compatible with Python >= 3.6.

By default, the action will install the standard [executables distribution](https://github.com/MODFLOW-USGS/executables/releases), downloading and adding `mf6` and over 20 other related programs to the path. Independent MODFLOW 6 [releases](https://github.com/MODFLOW-USGS/modflow6/releases) or [nightly builds](https://github.com/MODFLOW-USGS/modflow6-nightly-build/releases) can also be selected, which only contain `mf6`, `mf5to6`, `zbud6`, and the `libmf6` library.

## Usage

To use this action, add a step like the following to your workflow:

```yaml
- name: Install MODFLOW 6
  uses: modflowpy/install-modflow-action@v1
  with:
    github_token: ${{ secrets.GITHUB_TOKEN }}
    path: ~/.local/bin
```

### Inputs

The action accepts the following inputs:

- `github_token` (required)
- `path` (required)
- `repo` (optional)

#### `github_token`

Because composite GitHub Actions [do not have access to secrets](https://stackoverflow.com/a/70111134/6514033), a GitHub API token must be provided via the `github_token` input (this avoids HTTP errors due to rate-limiting).

The example above uses the [automatically provided](https://docs.github.com/en/actions/security-guides/automatic-token-authentication#about-the-github_token-secret) `GITHUB_TOKEN` secret, but a personal access token may be provided as well.

#### `path`

The `path` input is the location to install executables. The path may be absolute or relative to the workflow's working directory. Tilde expansion is also supported on all three major platforms. The resolved path is stored in the `MODFLOW_BIN_PATH` environment variable, which is then available to subsequent workflow steps.

#### `repo`

The `repo` input allows selecting which MODFLOW 6 executable distribution to install. The following values are accepted:

- `executables` (default)
- `modflow6`
- `modflow6-nightly-build`

### Outputs

The action has the following outputs:

- `cache-hit`

#### `cache-hit`

The `cache-hit` output simply forwards the internal `actions/cache` output of the same name, and is `true` if a matching entry was found and `false` if not.

Cache keys follow pattern `modflow-${{ runner.os }}-${{ inputs.repo }}-${{ hashFiles('code.json') }}`, where `code.json` is a JSON file containing version metadata. (This file is currently distributed only with the `executables` distribution, but is to be added to the others in forthcoming releases.) Thus separate caches are maintained for each combination of platform and distribution repository, and the cache is invalidated

1. when `code.json` changes, or
2. when `code.json` is added to a distribution.

## MODFLOW Resources

- [MODFLOW and related programs](https://water.usgs.gov/ogw/modflow/)
- [Online guide for MODFLOW-2000](https://water.usgs.gov/nrp/gwsoftware/modflow2000/Guide/)
- [Online guide for MODFLOW-2005](https://water.usgs.gov/ogw/modflow/MODFLOW-2005-Guide/)
- [Online guide for MODFLOW-NWT](https://water.usgs.gov/ogw/modflow-nwt/MODFLOW-NWT-Guide/)
