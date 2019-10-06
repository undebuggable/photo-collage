DIR_IMG=''
IMG_QUALITY=90
collage-png:
	python photo_collage.py $(DIR_IMG)
	rm -f $(DIR_IMG)/collage-*.[pP][nN][gG] $(DIR_IMG)/dominant-*.[pP][nN][gG]
collage-jpg: collage-png
	find $(DIR_IMG)/ -name all-*.[pP][nN][gG] -print0 -exec convert -quality $(IMG_QUALITY) {} {}.jpg \;
	rm -f $(DIR_IMG)/all-*.[pP][nN][gG]
