* [✓|9676db8|TASK] Implement loading the config from `photo_collage.ini`
  * [TASK] load the settings from the section `[tile]`
  * [TASK] load the settings from the section `[collage]`
* [✓|9676db8|BUG] ImageMagick sometimes incorrectly interprets the image orientation and the tiles in the collage are rotated (probably related to EXIF?)
* [REFACTOR] Refactor the cropping of an image:
  * [REFACTOR] rotate the image in the memory instead of having separate loops for horizontal and vertical
  * [REFACTOR] when chopping off slices, operate on ratios instead on pixels (yield the same result for the same picture with different dimensions)
* [TASK] create Python `requirements.txt` for the project
* [TASK] create shell utility (or `make install`?) checking/installing required applications (ImageMagick's `convert`, Python, `find`, etc.)
* [TASK] create unit tests

