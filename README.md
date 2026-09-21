# PolymerLit

The data repo for polymer image recognition

### PolymerLit-MT

This is the subset containing 300 images with corresponding molblocks from the BigSMILES Machine Translation (MT) paper by Deagen et al [[1](https://doi.org/10.1021/acs.macromol.3c01378)]. The raw data have been [made available publicly](https://observablehq.com/d/f40e5de68a2dd177) by the authors. There were some minor inconsistencies in the molblocks where aromatic bonds were recorded as type 4 (i.e., non-kekulized) but the images actually displayed alternating single and double bonds (i.e., kekulized). We have manually corrected all these blocks.

### PolymerLit-Olsen

This is the subset containing 468 images with corresponding molblocks from 3 publications by the Olsen group at MIT [[2](https://doi.org/10.1021/acscentsci.9b00476),[3](https://doi.org/10.1021/acspolymersau.2c00009),[4](https://doi.org/10.1039/D2SC02257E)]. These manuscripts and SIs are all open-access, but the images were originally unlabeled. We used our PolymerScribe model to predict the molblocks which were manually corrected afterward.

### PolymerLit-OA

This is the subset containing 1,000 images with corresponding molblocks from Open-Access (OA) articles. We have carefully chosen the images to be from only articles with CC-BY-NC-ND and less restrictive licenses. Because of the ND clause (Non-Derivative) for some, we decided to release the images exactly as how they appear originally, together with the coordinates of the bounding polygons surrounding the polymer structures. These bounding polygons were also drawn manually with the help of the open-source tool [CVAT.ai](https://app.cvat.ai/), and the "cropped" images can be easily reconstructed with the provided script,

```shell
$ pip install pillow
$ python generate_cropped_images.py
```

The "cropped" images will be populated under `PolymerLit-OA_processed`, whose filenames should match the provided molblocks (`doi_suffix.corrected.mol`) which were predicted by PolymerScribe and manually corrected in a similar manner. The references for all images and their licenses are recorded in `PolymerLit-OA_refs.xlsx`.

### Canonical BigSMILES

`canonical_bigsmiles.tsv` holds the BigSMILES ground truth for every
`*.corrected.mol` in this repo, one row per molblock:

| column | meaning |
|---|---|
| `path` | the `*.corrected.mol` path, relative to the repo root |
| `bigsmiles` | BigSMILES converted from the molblock |
| `canonical_bigsmiles` | its canonical form |
| `status` | how the canonicalization went (below) |

| `status` | meaning | count |
|---|---|---:|
| `SUCCESS` | canonicalized, and the string changed | 1524 |
| `NOOP` | already canonical | 9 |
| `FAIL` | canonicalization failed | 188 |
| `BIGSMILES_FAILED` | no BigSMILES could be obtained at all | 47 |

Only `SUCCESS` and `NOOP` carry a usable canonical form (1533 of 1768). The
`status` column exists because a failed canonicalization returns its input
unchanged, exactly as an already-canonical molecule does -- so
`canonical_bigsmiles == bigsmiles` alone cannot tell the two apart.

Atoms that are placeholders rather than real chemistry -- an atom carrying an
`A` alias record (an abbreviation such as `Ph`, `CF3` or `TEG`), or one drawn
as a bare `R` -- are normalized to a single wildcard element, `[Y]`, before
conversion. Without this the same structure converts differently depending on
whether it was drawn in ChemDraw (carbon + alias) or produced by a model
(element `R`), and `[R]` cannot be parsed as an atom at all, so it never
canonicalizes. `*` atoms are left alone: here they are polymer attachment
points and become bonding descriptors.
