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
