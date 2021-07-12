# STAR-HEPdata

This repository helps coordinate preparations of STAR published data for submission to HEPdata.net

You will find the following directory structure:

- `oldhepdata` a list of single-file submissions, all based on the old hepdb data format
- `tools` a collection of tools/scripts that were used for some of these submissions
- `tools/xml` scripts to (re-)generate STAR's xml-based publication database
- `yaml` directories (named according to STAR's publication ID) that contain yaml-based HEPDB submission files.

Each directory in `STAR-HEPdata/yaml`  should have a basic readme.md file that looks as follows:
```
# Dielectron Mass Spectra from Au+Au Collisions at $\sqrt{s_{NN}}$ = 200 GeV

Reference	: Phys. Rev. Lett. 113 (2014) 22301 \
e-Print Archives: http://arxiv.org/abs/1312.7397 \
STAR pubID	: 208 \
Inspire ID	: 1275614\
  ```
where the various fields should be updated according to the information found in STAR's publication records.

Each submission should include thumbnail picture files that are appropriately referenced in the associated yaml files. For multi-panel pictures, it is fine to repeatedly refer to the same thumbnail picture. Make sure that each thumbnail picture's name starts with `thumb_`.


For HEPdata submission **all** files, except for `readme.md` should be combined in a single tarball or zip file.


A few more useful links:
- [STAR data in HEPdata](https://www.hepdata.net/search/?collaboration=STAR)
- [STAR Publications](https://drupal.star.bnl.gov/STAR/publications/)
- [Documentation of the HEPdata yaml format](https://hepdata-submission.readthedocs.io/en/latest/)
