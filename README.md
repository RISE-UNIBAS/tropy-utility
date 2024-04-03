# tropy-utility

A collection of utility tools for [Tropy](https://tropy.org/).

## Creator

This software was created by the University of Basel's Research and Infrastructure Support RISE (rise@unibas.ch) in 2023 and 2024.

## File structure and data overview

Note that there are [different versions of this software](https://github.com/RISE-UNIBAS/tropy-utility/releases), see the [changelog](https://github.com/RISE-UNIBAS/tropy-utility/blob/main/CHANGELOG.md) for details.

- Python package in [`/tropy-utility`](https://github.com/RISE-UNIBAS/tropy-utility/tree/main/metagrapho_tropy)
- documentation [here](https://rise-unibas.github.io/tropy-utility/) and in [`/docs`](https://github.com/RISE-UNIBAS/tropy-utility/tree/main/docs)
- sample scripts and data for each tool in [`/samples`](https://github.com/RISE-UNIBAS/tropy-utility/tree/main/samples)

## Tools

The different tools are accessible via the `Client` class.

### selections2images

Use `Client.selections2images` to save selections of images as new images.
- Documentation [here](https://rise-unibas.github.io/tropy-utility/html/index.html#tropy_utility.client.Client.selections2images).
- Sample script [here](https://github.com/RISE-UNIBAS/tropy-utility/tree/main/samples/selections2images).

### items2transkribus

Use `Client.items2transkribus` to create folders for Tropy items that can be ingested into Transkribus as documents.
- Documentation [here](https://rise-unibas.github.io/tropy-utility/html/index.html#tropy_utility.client.Client.items2transkribus).
- Sample script [here](https://github.com/RISE-UNIBAS/tropy-utility/tree/main/samples/items2transkribus).

## To dos

 - [ ] set up Zenodo integration
 - [ ] initial release
