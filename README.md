# install-modflow-action

[![GitHub tag](https://img.shields.io/github/tag/modflowpy/install-modflow-action.svg)](https://github.com/modflowpy/install-modflow-action/tags/latest)
[![CI](https://github.com/modflowpy/install-modflow-action/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/modflowpy/install-modflow-action/actions/workflows/ci.yml)
[![Project Status: Active – The project has reached a stable, usable state and is being actively developed.](https://www.repostatus.org/badges/latest/active.svg)](https://www.repostatus.org/#active)

An action to setup MODFLOW 6 and related programs.

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->


- [Overview](#overview)
- [Usage](#usage)
- [Environment variables](#environment-variables)
- [Inputs](#inputs)
  - [`github_token`](#github_token)
  - [`path`](#path)
  - [`repo`](#repo)
  - [`tag`](#tag)
  - [`subset`](#subset)
  - [`cache`](#cache)
- [Outputs](#outputs)
  - [`cache-hit`](#cache-hit)
    - [Cache key](#cache-key)
    - [`code.json`](#codejson)
- [MODFLOW Resources](#modflow-resources)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

## Overview

This action uses [FloPy's](https://github.com/modflowpy/flopy) [`get-modflow`](https://github.com/modflowpy/flopy/blob/develop/docs/get_modflow.md) utility to install MODFLOW 6 and a number of related binaries. The `get-modflow` utility is invoked directly if the `flopy` Python package is installed, otherwise it is retrieved as a standalone, dependency-free script compatible with Python >= 3.6.

By default, the action will install the standard MODFLOW [executables distribution](https://github.com/MODFLOW-USGS/executables/releases), which contains ~20 binaries. Independent MODFLOW 6 [releases](https://github.com/MODFLOW-USGS/modflow6/releases) or [nightly builds](https://github.com/MODFLOW-USGS/modflow6-nightly-build/releases) can also be selected, both of which only contain:

- `mf6[.exe]`
- `mf5to6[.exe]`
- `zbud6[.exe]`
- `libmf6.[so/dylib/dll]`

The `executables` and `modflow6-nightly-build` distributions are small (less than 100 MB) and take only a few seconds to download and extract. The `modflow6` distribution is larger and takes a bit more time.

The installation is cached by default, with the key changed daily. Daily key rotation allows the action automatically update versions when they become available, e.g. the nightly build &mdash; caching can be turned off by setting the `cache` input to `false`.

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
- `tag`
- `subset`
- `cache`

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

### `tag`

The `tag` input allows selecting a release by tag name. The default is `latest`.

For the `modflow6` distribution, releases are [tagged by semantic version number](https://github.com/MODFLOW-USGS/modflow6/tags). For the `modflow6-nightly-build` distribution, releases are [tagged by date](https://github.com/MODFLOW-USGS/modflow6-nightly-build/tags), in format `%Y%m%d`, e.g. `20230607`. For the `executables` distribution, releases are [tagged by integer version number with trailing ".0"](https://github.com/MODFLOW-USGS/executables/tags).

### `subset`

The `subset` input allows selecting which binaries to install. One or more binaries may be selected with a comma-separated string.

If this input is not provided, or if its value is an empty string, all binaries in the selected distribution are installed. This is the default behavior.

### `cache`

The `cache` input is a boolean that controls whether the action caches the MODFLOW binaries. The default is `true`.

**Note:** an [outstanding cache reservation bug in `actions/cache`](https://github.com/actions/cache/issues/144) can cause the cache to [fail to restore while simultaneously rejecting new saves](https://github.com/MODFLOW-USGS/modflow6/actions/runs/3624583228/jobs/6111766806#step:6:152). The [GitHub-endorsed workaround for this issue](https://github.com/actions/cache/issues/144#issuecomment-579323937) is currently to change keys, therefore this action rotates the cache key once daily. Rotating the key daily also allows the action to automatically update versions when they become available, e.g. so workflows can use the most recent nightly build.

## Outputs

The action has the following outputs:

- `cache-hit`

### `cache-hit`

The `cache-hit` output forwards the internal `actions/cache` output of the same name, and is `true` if a matching entry was found and `false` if not.

#### Cache key

Cache keys follow pattern:

```
modflow-${{ runner.os }}-${{ inputs.repo }}-${{ hashFiles('code.json') }}-${{ %Y%m%d }}
```

#### `code.json`

`code.json` is a version metadata JSON file released with the `executables` distribution, for instance:

```
{
  "mf6": {
    "current": true,
    "dirname": "mf6.4.1_linux",
    "double_switch": false,
    "shared_object": false,
    "srcdir": "src",
    "standard_switch": true,
    "url": "https://github.com/MODFLOW-USGS/modflow6/releases/download/6.4.1/mf6.4.1_linux.zip",
    "url_download_asset_date": "12/09/2022",
    "version": "6.4.1"
  },
  "libmf6": {
    "current": true,
    "dirname": "mf6.4.1_linux",
    "double_switch": false,
    "shared_object": true,
    "srcdir": "srcbmi",
    "standard_switch": true,
    "url": "https://github.com/MODFLOW-USGS/modflow6/releases/download/6.4.1/mf6.4.1_linux.zip",
    "url_download_asset_date": "12/09/2022",
    "version": "6.4.1"
  },
  ...
}
```

## MODFLOW Resources

- [MODFLOW and related programs](https://water.usgs.gov/ogw/modflow/)
- [Online guide for MODFLOW-2000](https://water.usgs.gov/nrp/gwsoftware/modflow2000/Guide/)
- [Online guide for MODFLOW-2005](https://water.usgs.gov/ogw/modflow/MODFLOW-2005-Guide/)
- [Online guide for MODFLOW-NWT](https://water.usgs.gov/ogw/modflow-nwt/MODFLOW-NWT-Guide/)
