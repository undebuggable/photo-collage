* [✓|9676db8|TASK] Implement loading the config from `photo_collage.ini`
  * [TASK] load the settings from the section `[tile]`
  * [TASK] load the settings from the section `[collage]`
* [REFACTOR] Refactor the cropping of an image:
  * [REFACTOR] rotate the image in the memory instead of having separate loops for horizontal and vertical
  * [REFACTOR] when chopping off slices, operate on ratios instead on pixels (yield the same result for the same picture with different dimensions)
* [TASK] create shell utility (or `make install`?) checking/installing required applications (ImageMagick's `convert`, Python, `find`, etc.)
* [TASK] create unit tests
* [REFACTOR] Extract ImageMagick CLI commands into parametrized strings in config file
