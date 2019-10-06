Installation
---------------
Install Python dependencies:

`pip install -r requirements.txt`

[ImageMagick](https://en.wikipedia.org/wiki/ImageMagick) is required. To verify whether it's installed run from the command line:
```bash
convert --version
```

Usage
---------------
Create a collage in a PNG format from all images in the directory `/home/user1/Photos/my-holidays-in-exotic-place/`: 
```
make collage-jpg DIR_IMG=/home/user1/Photos/my-holidays-in-exotic-place/
```
