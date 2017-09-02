import os, ConfigParser, codecs
from optparse import OptionParser
from photo_collage_pkg.app import process_images
from photo_collage_pkg.config import constants

directory_path = ""
def parseParams():
    global directory_path
    parser = OptionParser()
    (options, args) = parser.parse_args()
    if len(args) != 1:
        print "Please specify directory with images"
        return False
    if len(args) == 1 and not os.path.isdir(args[0]):
        print "The directory with images doesn't exist"
        return False
    directory_path = args[0]
    return True

if parseParams():
    user_config = ConfigParser.ConfigParser()
    # Don't convert keys to lowercase
    user_config.optionxform = lambda option: option
    user_config.readfp(codecs.open(constants.FILE_USERCONFIG, 'r', 'utf8'))
    process_images.createCollage(directory_path, user_config)
else:
    print "Try again"
