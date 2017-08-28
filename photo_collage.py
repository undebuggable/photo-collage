import os
from optparse import OptionParser
from photo_collage_pkg.app import process_images

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
    process_images.createCollage(directory_path)
else:
    print "Try again"