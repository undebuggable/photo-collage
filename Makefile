DIR_IMG=''
collage-png:
	python photo_collage.py $(DIR_IMG)
	rm $(DIR_IMG)/collage-*.[pP][nN][gG] $(DIR_IMG)/dominant-*.[pP][nN][gG]
collage-jpg: collage-png
	find $(DIR_IMG)/ -name all-*.[pP][nN][gG] -print0 -exec convert -quality 90 {} {}.jpg \;
	rm $(DIR_IMG)/all-*.[pP][nN][gG]
