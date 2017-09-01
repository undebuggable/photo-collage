from PIL import Image
import os, subprocess, math, colorsys, shutil, mimetypes, time
from . import dominant_colors, image_crop
from ..config import constants
from collections import namedtuple

DIR_IMG = ""
TILE_SIZE = 256
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

def createCollage(directory_path):
    global DIR_IMG
    DIR_IMG = directory_path
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
    for file in os.listdir(DIR_IMG):
        if file.startswith(constants.FILE_PREFIX_TILE) or file.startswith(constants.FILE_PREFIX_TILE_DOMINANT):
            os.remove(joinPath(DIR_IMG, file))
    for file in os.listdir(DIR_IMG):
        (mimeType, encoding) = mimetypes.guess_type(file)
        if mimeType in constants.IMAGE_MIMETYPES and not file.startswith(constants.FILE_PREFIX_TILE) and not file.startswith(constants.FILE_PREFIX_TILE_DOMINANT):
            collagePath = joinPath(DIR_IMG, constants.FILE_PREFIX_TILE + os.path.splitext(file)[0] + ".png")
            dominantPath = joinPath(DIR_IMG, constants.FILE_PREFIX_TILE_DOMINANT + os.path.splitext(file)[0] + ".png")
            s = subprocess.Popen([
                "convert",
                joinPath(DIR_IMG, file),
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
        joinPath(DIR_IMG, constants.FILE_PREFIX_COLLAGE + timestamp + str(DOMINANT_COLORS) + constants.FILE_SUFFIX_RGB)
    ])
    collageYIQ.extend([
        "-geometry",
        str(TILE_SIZE) + "x" + str(TILE_SIZE) + "+0+0",
        "-tile",
        str(width) + "x" + str(height),
        joinPath(DIR_IMG, constants.FILE_PREFIX_COLLAGE + timestamp + str(DOMINANT_COLORS) + constants.FILE_SUFFIX_YIQ)
    ])
    collageHLS.extend([
        "-geometry",
        str(TILE_SIZE) + "x" + str(TILE_SIZE) + "+0+0",
        "-tile",
        str(width) + "x" + str(height),
        joinPath(DIR_IMG, constants.FILE_PREFIX_COLLAGE + timestamp + str(DOMINANT_COLORS) + constants.FILE_SUFFIX_HLS)
    ])
    collageHSV.extend([
        "-geometry",
        str(TILE_SIZE) + "x" + str(TILE_SIZE) + "+0+0",
        "-tile",
        str(width) + "x" + str(height),
        joinPath(DIR_IMG, constants.FILE_PREFIX_COLLAGE + timestamp + str(DOMINANT_COLORS) + constants.FILE_SUFFIX_HSV)
    ])
    collageRGBDominant.extend([
        "-geometry",
        str(TILE_SIZE) + "x" + str(2*TILE_SIZE) + "+0+0",
        "-tile",
        str(width) + "x" + str(height),
        joinPath(DIR_IMG, constants.FILE_PREFIX_COLLAGE + timestamp + str(DOMINANT_COLORS) + constants.FILE_SUFFIX_RGB_DOMINANT)
    ])
    collageYIQDominant.extend([
        "-geometry",
        str(TILE_SIZE) + "x" + str(2*TILE_SIZE) + "+0+0",
        "-tile",
        str(width) + "x" + str(height),
        joinPath(DIR_IMG, constants.FILE_PREFIX_COLLAGE + timestamp + str(DOMINANT_COLORS) + constants.FILE_SUFFIX_YIQ_DOMINANT)
    ])
    collageHLSDominant.extend([
        "-geometry",
        str(TILE_SIZE) + "x" + str(2*TILE_SIZE) + "+0+0",
        "-tile",
        str(width) + "x" + str(height),
        joinPath(DIR_IMG, constants.FILE_PREFIX_COLLAGE + timestamp + str(DOMINANT_COLORS) + constants.FILE_SUFFIX_HLS_DOMINANT)
    ])
    collageHSVDominant.extend([
        "-geometry",
        str(TILE_SIZE) + "x" + str(2*TILE_SIZE) + "+0+0",
        "-tile",
        str(width) + "x" + str(height),
        joinPath(DIR_IMG, constants.FILE_PREFIX_COLLAGE + timestamp + str(DOMINANT_COLORS) + constants.FILE_SUFFIX_HSV_DOMINANT)
    ])
    print "\nTotal " + str(photoCount) + " images"
    print constants.LOG_CREATING_RGB
    s = subprocess.Popen(collageRGB)
    s.wait()
    print constants.LOG_CREATING_YIQ
    s = subprocess.Popen(collageYIQ)
    s.wait()
    print constants.LOG_CREATING_HLS
    s = subprocess.Popen(collageHLS)
    s.wait()
    print constants.LOG_CREATING_HSV
    s = subprocess.Popen(collageHSV)
    s.wait()
    print constants.LOG_CREATING_RGB_DOMINANT
    s = subprocess.Popen(collageRGBDominant)
    s.wait()
    print constants.LOG_CREATING_YIQ_DOMINANT
    s = subprocess.Popen(collageYIQDominant)
    s.wait()
    print constants.LOG_CREATING_HLS_DOMINANT
    s = subprocess.Popen(collageHLSDominant)
    s.wait()
    print constants.LOG_CREATING_HSV_DOMINANT
    s = subprocess.Popen(collageHSVDominant)
    s.wait()

