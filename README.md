# install-modflow-action

[![CI](https://github.com/modflowpy/install-modflow-action/actions/workflows/commit.yml/badge.svg?branch=develop)](https://github.com/modflowpy/install-modflow-action/actions/workflows/commit.yml)
![Status](https://img.shields.io/badge/-under%20development-yellow?style=flat-square)

An action to install executables for MODFLOW and related programs from the [executables distribution repository](https://github.com/MODFLOW-USGS/executables).

## Usage

To use this action, add a step like the following to your workflow:

```yaml
- name: Install executables
  uses: modflowpy/install-modflow-action@v1
  with:
      path: ~/.local/bin
      github_token: ${{ secrets.GITHUB_TOKEN }}
```

Note that tilde expansion works on Linux and Mac runners, but not on Windows &mdash; the corresponding location on Windows is `C:\Users\runneradmin\.local\bin`.