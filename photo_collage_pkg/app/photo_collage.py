from PIL import Image
from optparse import OptionParser
import os, subprocess, math, colorsys, dominant_colors, image_crop, shutil, mimetypes, time
from collections import namedtuple

IMAGE_MIMETYPES = [
  'image/png',
  'image/jpg',
  'image/jpeg'
]
COLLAGE_PHOTOS = ""
TILE_SIZE = 256
COLLAGE_PREFIX = "collage-"
DOMINANT_PREFIX = "dominant-"
DOMINANT_COLORS = 1
LABEL_POINTSIZE = 18
colors = []
byRGB = []
byYIQ = []
byHLS = []
byHSV = []

def joinPath(p1, p2):
    return p1 + "/" + p2

def strToFraction(str):
    return float(int(str, 16))/float(int("ff", 16))

class BreakIt( Exception ):
     pass

def insert(item, itemType):
    i = 0
    collection = globals()["by" + itemType]
    try:
        while(i < len(collection)):
            for c in collection:
                if item[itemType][0] < c[itemType][0]:
                    i = i + 1
                elif item[itemType][0] == c[itemType][0]:
                    if item[itemType][1] < c[itemType][1]:
                        i = i + 1
                    elif item[itemType][1] == c[itemType][1]:
                        if item[itemType][2] < c[itemType][2]:
                            i = i + 1
                        else:
                            raise BreakIt
                    else:
                        raise BreakIt
                else:
                    raise BreakIt
    except BreakIt:
        pass
    collection.insert(i, item)

def sortColors():
    for c in colors:
        insert(c, "RGB")
        insert(c, "YIQ")
        insert(c, "HLS")
        insert(c, "HSV")

def drawColors(path, colors):
    print "\nDrawing dominant colors\n" + path + "\n" + str(colors)
    sectionHeight = TILE_SIZE*1/len(colors)
    rectangles = []
    for i in range(len(colors)):
        rectangles.append("fill " + str(colors[i]) + " rectangle 0," + str(TILE_SIZE + i * sectionHeight) + " " + str(TILE_SIZE) + "," + str(TILE_SIZE + (i + 1) * sectionHeight))
    s = subprocess.Popen([
        "convert",
        path,
        "-gravity",
        "North",
        "-background",
        str(colors[0]),
        "-extent",
        str(TILE_SIZE) + "x" + str(2*TILE_SIZE),
        "-draw",
        "\n".join(rectangles),
        path
    ])
    s.wait()

def printLabels(path, colors):
    print "\nPrinting labels\n" + path + "\n" + str(colors)
    sectionHeight = TILE_SIZE*1/len(colors)
    labels = []
    printCommand = [
        "convert",
        path,
        "-gravity",
        "south",
        "-pointsize",
        str(LABEL_POINTSIZE)
    ]
    for i in range(len(colors)):
        labels.extend([
            "-stroke",
            "#000C",
            "-strokewidth",
            "2",
            "-annotate",
            "+0+" + str((len(colors) - i - 1) * sectionHeight + 35),
            str(colors[i]),
            "-stroke",
            "none",
            "-fill",
            "white",
            "-annotate",
            "+0+" + str((len(colors) - i - 1) * sectionHeight + 35),
            str(colors[i]),
        ])
    printCommand.extend(labels)
    printCommand.append(path)
    s = subprocess.Popen(printCommand)
    s.wait()

def createCollage():
    photoCount = 0
    collageRGB = [
        "montage"
    ]
    collageYIQ = [
        "montage"
    ]
    collageHLS = [
        "montage"
    ]
    collageHSV = [
        "montage"
    ]
    collageRGBDominant = [
        "montage"
    ]
    collageYIQDominant = [
        "montage"
    ]
    collageHLSDominant = [
        "montage"
    ]
    collageHSVDominant = [
        "montage"
    ]
    for file in os.listdir(COLLAGE_PHOTOS):
        if file.startswith(COLLAGE_PREFIX) or file.startswith(DOMINANT_PREFIX):
            os.remove(joinPath(COLLAGE_PHOTOS, file))
    for file in os.listdir(COLLAGE_PHOTOS):
        (mimeType, encoding) = mimetypes.guess_type(file)
        if mimeType in IMAGE_MIMETYPES and not file.startswith(COLLAGE_PREFIX) and not file.startswith(DOMINANT_PREFIX):
            collagePath = joinPath(COLLAGE_PHOTOS, COLLAGE_PREFIX + os.path.splitext(file)[0] + ".png")
            dominantPath = joinPath(COLLAGE_PHOTOS, DOMINANT_PREFIX + os.path.splitext(file)[0] + ".png")
            s = subprocess.Popen([
                "convert",
                joinPath(COLLAGE_PHOTOS, file),
                "-resize",
                str(TILE_SIZE) + "x" + str(TILE_SIZE) + "^",
#                "-gravity",
#                "center",
#                "-extent",
#                str(TILE_SIZE) + "x" + str(TILE_SIZE),
                collagePath
            ])
            s.wait()
            cropped = image_crop.image_square(Image.open(collagePath))
            cropped.save(collagePath)
            shutil.copyfile(collagePath, dominantPath)
            colorz = dominant_colors.colorz(collagePath, DOMINANT_COLORS)
            drawColors(dominantPath, colorz)
            printLabels(dominantPath, colorz)
            rgb = [
                strToFraction("".join([colorz[0][1], colorz[0][2]])),
                strToFraction("".join([colorz[0][3], colorz[0][4]])),
                strToFraction("".join([colorz[0][5], colorz[0][6]]))
            ]
            colors.append({
                "dominantPath": dominantPath,
                "collagePath": collagePath,
                "RGB_string": colorz[0],
                "RGB": rgb,
                "YIQ": colorsys.rgb_to_yiq(rgb[0], rgb[1], rgb[2]),
                "HSV": colorsys.rgb_to_hsv(rgb[0], rgb[1], rgb[2]),
                "HLS": colorsys.rgb_to_hls(rgb[0], rgb[1], rgb[2])
            })
            photoCount = photoCount + 1 
    width = math.ceil(photoCount ** 0.5)
    height = math.ceil(photoCount/width)
    timestamp = str(int(time.time()))
    sortColors()
    for c in byRGB:
        collageRGB.append(c.get("collagePath"))
    for c in byYIQ:
        collageYIQ.append(c.get("collagePath"))
    for c in byHLS:
        collageHLS.append(c.get("collagePath"))
    for c in byHSV:
        collageHSV.append(c.get("collagePath"))
    for c in byRGB:
        collageRGBDominant.append(c.get("dominantPath"))
    for c in byYIQ:
        collageYIQDominant.append(c.get("dominantPath"))
    for c in byHLS:
        collageHLSDominant.append(c.get("dominantPath"))
    for c in byHSV:
        collageHSVDominant.append(c.get("dominantPath"))
    collageRGB.extend([
        "-geometry",
        str(TILE_SIZE) + "x" + str(TILE_SIZE) + "+0+0",
        "-tile",
        str(width) + "x" + str(height),
        joinPath(COLLAGE_PHOTOS, "all-" + timestamp + str(DOMINANT_COLORS) +"-RGB.png")
    ])
    collageYIQ.extend([
        "-geometry",
        str(TILE_SIZE) + "x" + str(TILE_SIZE) + "+0+0",
        "-tile",
        str(width) + "x" + str(height),
        joinPath(COLLAGE_PHOTOS, "all-" + timestamp + str(DOMINANT_COLORS) +"-YIQ.png")
    ])
    collageHLS.extend([
        "-geometry",
        str(TILE_SIZE) + "x" + str(TILE_SIZE) + "+0+0",
        "-tile",
        str(width) + "x" + str(height),
        joinPath(COLLAGE_PHOTOS, "all-" + timestamp + str(DOMINANT_COLORS) +"-HLS.png")
    ])
    collageHSV.extend([
        "-geometry",
        str(TILE_SIZE) + "x" + str(TILE_SIZE) + "+0+0",
        "-tile",
        str(width) + "x" + str(height),
        joinPath(COLLAGE_PHOTOS, "all-" + timestamp + str(DOMINANT_COLORS) +"-HSV.png")
    ])
    collageRGBDominant.extend([
        "-geometry",
        str(TILE_SIZE) + "x" + str(2*TILE_SIZE) + "+0+0",
        "-tile",
        str(width) + "x" + str(height),
        joinPath(COLLAGE_PHOTOS, "all-" + timestamp + str(DOMINANT_COLORS) +"-RGB-dominant.png")
    ])
    collageYIQDominant.extend([
        "-geometry",
        str(TILE_SIZE) + "x" + str(2*TILE_SIZE) + "+0+0",
        "-tile",
        str(width) + "x" + str(height),
        joinPath(COLLAGE_PHOTOS, "all-" + timestamp + str(DOMINANT_COLORS) +"-YIQ-dominant.png")
    ])
    collageHLSDominant.extend([
        "-geometry",
        str(TILE_SIZE) + "x" + str(2*TILE_SIZE) + "+0+0",
        "-tile",
        str(width) + "x" + str(height),
        joinPath(COLLAGE_PHOTOS, "all-" + timestamp + str(DOMINANT_COLORS) +"-HLS-dominant.png")
    ])
    collageHSVDominant.extend([
        "-geometry",
        str(TILE_SIZE) + "x" + str(2*TILE_SIZE) + "+0+0",
        "-tile",
        str(width) + "x" + str(height),
        joinPath(COLLAGE_PHOTOS, "all-" + timestamp + str(DOMINANT_COLORS) +"-HSV-dominant.png")
    ])
    print "\nTotal " + str(photoCount) + " images"
    print "\nCreating collage sorted by RGB"
    s = subprocess.Popen(collageRGB)
    s.wait()
    print "\nCreating collage sorted by YIQ"
    s = subprocess.Popen(collageYIQ)
    s.wait()
    print "\nCreating collage sorted by HLS"
    s = subprocess.Popen(collageHLS)
    s.wait()
    print "\nCreating collage sorted by HSV"
    s = subprocess.Popen(collageHSV)
    s.wait()
    print "\nCreating collage sorted by RGB with dominant colors"
    s = subprocess.Popen(collageRGBDominant)
    s.wait()
    print "\nCreating collage sorted by YIQ with dominant colors"
    s = subprocess.Popen(collageYIQDominant)
    s.wait()
    print "\nCreating collage sorted by HLS with dominant colors"
    s = subprocess.Popen(collageHLSDominant)
    s.wait()
    print "\nCreating collage sorted by HSV with dominant colors"
    s = subprocess.Popen(collageHSVDominant)
    s.wait()

def parseParams():
    global COLLAGE_PHOTOS
    parser = OptionParser()
    (options, args) = parser.parse_args()
    if len(args) != 1:
        print "Please specify directory with images"
        return False
    if len(args) == 1 and not os.path.isdir(args[0]):
        print "The directory with images doesn't exist"
        return False
    COLLAGE_PHOTOS = args[0]
    return True

if parseParams():
    createCollage()
else:
    print "Try again"
