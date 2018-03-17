• [✓|9676db8|FEATURE] Implement loading the config from `photo_collage.ini`
  • load the settings from the section `[tile]`
  • load the settings from the section `[collage]`
• [✓|9676db8|BUG] ImageMagick sometimes incorrectly interprets the image orientation and the tiles in the collage are rotated (probably related to EXIF?)
• [IMPROVEMENT] Refactor the cropping of an image:
  • rotate the image in the memory instead of having separate loops for horizontal and vertical
  • when chopping off slices, operate on ratios instead on pixels (yield the same result for the same picture with different dimensions)
• [TASK] create Python `requirements.txt` for the projects
• [TASK] create shell utility (or `make install`)? checking/installing required applications (ImageMagick's `convert`, Python, find, etc.)
