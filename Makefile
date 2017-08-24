PHOTOS=''
collage-png:
	python photo_collage.py $(PHOTOS)
	rm $(PHOTOS)/collage-*.[pP][nN][gG] $(PHOTOS)/dominant-*.[pP][nN][gG]
collage-jpg: collage-png
	find $(PHOTOS)/ -name all-*.[pP][nN][gG] -print0 -exec convert -quality 90 {} {}.jpg \;
	rm $(PHOTOS)/all-*.[pP][nN][gG]
