# install-modflow-action

[![CI](https://github.com/modflowpy/install-modflow-action/actions/workflows/commit.yml/badge.svg?branch=develop)](https://github.com/modflowpy/install-modflow-action/actions/workflows/commit.yml)

An action to install executables for MODFLOW and related programs from the [executables distribution repository](https://github.com/MODFLOW-USGS/executables).

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->

- [Usage](#usage)
- [Inputs](#inputs)
  - [Path](#path)
  - [GitHub API token](#github-api-token)
- [MODFLOW Resources](#modflow-resources)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

## Usage

To use this action, add a step like the following to your workflow:

```yaml
- name: Install executables
  uses: modflowpy/install-modflow-action@v1
  with:
      path: ~/.local/bin
      github_token: ${{ secrets.GITHUB_TOKEN }}
```

## Inputs

The action requires 2 inputs:

- `path`
- `github_token`

### Path

The `path` input is the location to install executables, e.g. a local bin directory.

**Note**: tilde expansion only works on Linux and Mac runners. The example above is suitable for Linux and Mac &mdash; on Windows the corresponding location is `C:\Users\runneradmin\.local\bin`.

### GitHub API token

Because composite GitHub Actions [do not have access to secrets](https://stackoverflow.com/a/70111134/6514033), a GitHub API token must be provided via the `github_token` input.

The example above uses the [automatically provided](https://docs.github.com/en/actions/security-guides/automatic-token-authentication#about-the-github_token-secret) `GITHUB_TOKEN` secret, but a personal access token may be provided as well.

## MODFLOW Resources

- [MODFLOW and related programs](https://water.usgs.gov/ogw/modflow/)
- [Online guide for MODFLOW-2000](https://water.usgs.gov/nrp/gwsoftware/modflow2000/Guide/)
- [Online guide for MODFLOW-2005](https://water.usgs.gov/ogw/modflow/MODFLOW-2005-Guide/)
- [Online guide for MODFLOW-NWT](https://water.usgs.gov/ogw/modflow-nwt/MODFLOW-NWT-Guide/)
