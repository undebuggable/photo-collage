Setting up the development environment
=================
Auto formatting
--------------

Enable auto formatting of Python in PyCharm with Black or Save Actions

### Auto formatting with Black

Configure the [auto formatting](https://black.readthedocs.io/en/stable/editor_integration.html) of Python code with Black in PyCharm.

The Black configuration is stored in the file [`pyproject.toml`](https://black.readthedocs.io/en/stable/pyproject_toml.html).

### Sorting of imports with Save Actions

Install the [Save Actions plugin](https://plugins.jetbrains.com/plugin/7642-save-actions/reviews).

The Save Actions configuration stored in the file `.idea/saveactions_settings.xml`.

Update the PyCharm settings:

Preferences ➜ Save Actions ➜ Activate save actions on save

Preferences ➜ Save Actions ➜ Optimize imports

Save Actions supports auto formatting of the source code as well.

Installation
=================
Install Python dependencies:

`pip install -r requirements.txt`

[ImageMagick](https://en.wikipedia.org/wiki/ImageMagick) is required. To verify whether it's installed run from the command line:
```bash
convert --version
```
Running the application
=================
Create a collage in a PNG format from all images in the directory `/home/user1/Photos/my-holidays-in-exotic-place/`: 
```
make collage-jpg DIR_IMG=/home/user1/Photos/my-holidays-in-exotic-place/
```
