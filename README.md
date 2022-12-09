# install-modflow-action

[![GitHub tag](https://img.shields.io/github/tag/modflowpy/install-modflow-action.svg)](https://github.com/modflowpy/install-modflow-action/tags/latest)
[![CI](https://github.com/modflowpy/install-modflow-action/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/modflowpy/install-modflow-action/actions/workflows/ci.yml)
[![Project Status: Active – The project has reached a stable, usable state and is being actively developed.](https://www.repostatus.org/badges/latest/active.svg)](https://www.repostatus.org/#active)

An action to install MODFLOW 6 and related programs.

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->

- [Overview](#overview)
- [Usage](#usage)
- [Environment variables](#environment-variables)
- [Inputs](#inputs)
  - [`github_token`](#github_token)
  - [`path`](#path)
  - [`repo`](#repo)
- [Outputs](#outputs)
  - [`cache-hit`](#cache-hit)
- [MODFLOW Resources](#modflow-resources)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

## Overview

This action uses [FloPy's](https://github.com/modflowpy/flopy) [`get-modflow`](https://github.com/modflowpy/flopy/blob/develop/docs/get_modflow.md) utility to install MODFLOW 6 and a number of related binaries. The `get-modflow` utility is invoked directly if the `flopy` Python package is installed, otherwise it is retrieved as a standalone, dependency-free script compatible with Python >= 3.6.

By default, the action will install the standard [executables distribution](https://github.com/MODFLOW-USGS/executables/releases), including MODFLOW 6 and 20+ related programs to the path. Independent MODFLOW 6 [releases](https://github.com/MODFLOW-USGS/modflow6/releases) or [nightly builds](https://github.com/MODFLOW-USGS/modflow6-nightly-build/releases) can also be selected, which only contain:

- `mf6[.exe]`
- `mf5to6[.exe]`
- `zbud6[.exe]`
- `libmf6.[so/dylib/dll]`

## Usage

To use this action, add a step like the following to your workflow:

```yaml
- name: Install MODFLOW 6
  uses: modflowpy/install-modflow-action@v1
```

## Environment variables

This action sets the following environment variables:

- `MODFLOW_BIN_PATH`: The path to the directory containing MODFLOW 6 and other binaries

## Inputs

The action accepts the following optional inputs:

- `github_token`
- `path`
- `repo`

### `github_token`

By default, the action uses the [automatically provided](https://docs.github.com/en/actions/security-guides/automatic-token-authentication#about-the-github_token-secret) `GITHUB_TOKEN` secret, but an access token may be explicitly provided as well.

### `path`

The `path` input is the location to install executables. The path may be absolute or relative to the workflow's working directory. Tilde expansion is also supported on all three major platforms. The resolved path is stored in the `MODFLOW_BIN_PATH` environment variable, which is then available to subsequent workflow steps.

The default path, shared on all three platforms, is `~/.local/bin/modflow`.

### `repo`

The `repo` input allows selecting which MODFLOW 6 executable distribution to install. The following values are accepted:

- `executables` (default)
- `modflow6`
- `modflow6-nightly-build`

## Outputs

The action has the following outputs:

- `cache-hit`

### `cache-hit`

The `cache-hit` output forwards the internal `actions/cache` output of the same name, and is `true` if a matching entry was found and `false` if not.

Cache keys follow pattern:

```
modflow-${{ runner.os }}-${{ inputs.repo }}-${{ hashFiles('code.json') }}
```

`code.json` is a version metadata JSON file released with all three distributions. Separate caches are maintained for each combination of platform and distribution, and the cache is invalidated if versions change.

## MODFLOW Resources

- [MODFLOW and related programs](https://water.usgs.gov/ogw/modflow/)
- [Online guide for MODFLOW-2000](https://water.usgs.gov/nrp/gwsoftware/modflow2000/Guide/)
- [Online guide for MODFLOW-2005](https://water.usgs.gov/ogw/modflow/MODFLOW-2005-Guide/)
- [Online guide for MODFLOW-NWT](https://water.usgs.gov/ogw/modflow-nwt/MODFLOW-NWT-Guide/)
