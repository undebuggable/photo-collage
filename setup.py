from distutils.core import setup

setup(
	name = "photo_collage",
	version = "0.0.0.0",
	author = "Pawel Owczarek",
	packages = ["photo_collage_pkg", "photo_collage_pkg.app", "photo_collage_pkg.config"],
	description = "Photo collage with tiles sorted by their color models."
)
