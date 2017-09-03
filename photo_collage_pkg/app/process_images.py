from PIL import Image
import os, subprocess, math, colorsys, shutil, mimetypes, time
from . import dominant_colors, image_crop
from ..config import constants
from collections import namedtuple

DIR_IMG = None
TILE_SIZE = None
DOMINANT_COLORS = None
LABEL_POINTSIZE = None
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
    print constants.LOG_DRAWING_COLORS + path + "\n" + str(colors)
    sectionHeight = TILE_SIZE*1/len(colors)
    rectangles = []
    for i in range(len(colors)):
        rectangles.append(
          "fill " + str(colors[i]) + " rectangle 0," + str(TILE_SIZE + i * sectionHeight) + " " + str(TILE_SIZE) + "," + str(TILE_SIZE + (i + 1) * sectionHeight)
        )
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
    print constants.LOG_DRAWING_LABELS + path + "\n" + str(colors)
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

def createCollageForColoModel (
        key_color_model, command_collage, count_tile_rows, count_tile_columns
    ):
    collageRGB = [
        "montage"
    ]
    string_by_color_model = {
        "RGB": [
          constants.FILE_SUFFIX_RGB, constants.LOG_CREATING_RGB
        ],
        "YIQ": [
          constants.FILE_SUFFIX_YIQ, constants.LOG_CREATING_YIQ
        ],
        "HLS": [
          constants.FILE_SUFFIX_HLS, constants.LOG_CREATING_HLS
        ],
        "HSV": [
          constants.FILE_SUFFIX_HSV, constants.LOG_CREATING_HSV
        ],
        "RGB_dominant": [
          constants.FILE_SUFFIX_RGB_DOMINANT, constants.LOG_CREATING_RGB_DOMINANT
        ],
        "YIQ_dominant": [
          constants.FILE_SUFFIX_YIQ_DOMINANT, constants.LOG_CREATING_YIQ_DOMINANT
        ],
        "HLS_dominant": [
          constants.FILE_SUFFIX_HLS_DOMINANT, constants.LOG_CREATING_HLS_DOMINANT
        ],
        "HSV_dominant": [
          constants.FILE_SUFFIX_HSV_DOMINANT, constants.LOG_CREATING_HSV_DOMINANT
        ]
    }
    timestamp = str(int(time.time()))
    for c in byRGB:
        collageRGB.append(c.get("path_collage"))
    command_collage.extend([
        "-geometry",
        str(TILE_SIZE) + "x" + str(
            TILE_SIZE * 2 if key_color_model.endswith('_dominant') else TILE_SIZE
        ) + "+0+0",
        "-tile",
        str(count_tile_columns) + "x" + str(count_tile_rows),
        joinPath(
            DIR_IMG,
            constants.FILE_PREFIX_COLLAGE + timestamp + str(DOMINANT_COLORS) + string_by_color_model[key_color_model][0]
        )
    ])
    print string_by_color_model[key_color_model][1]
    s = subprocess.Popen(command_collage)
    s.wait()

def loadUserConfig (user_config):
    global USER_CONFIG
    global TILE_SIZE
    global DOMINANT_COLORS
    global LABEL_POINTSIZE
    is_correct = True
    USER_CONFIG = user_config
    if USER_CONFIG.has_option(constants.CONFIG_TILE, constants.CONFIG_TILE_SIZE) and
    USER_CONFIG.has_option(constants.CONFIG_TILE, constants.CONFIG_TILE_DOMINANT_COLORS) and
    USER_CONFIG.has_option(constants.CONFIG_TILE, constants.CONFIG_TILE_POINTSIZES):
        TILE_SIZE = int(USER_CONFIG.get(constants.CONFIG_TILE, constants.CONFIG_TILE_SIZE))
        DOMINANT_COLORS = int(USER_CONFIG.get(constants.CONFIG_TILE, constants.CONFIG_TILE_DOMINANT_COLORS))
        LABEL_POINTSIZE = int(USER_CONFIG.get(constants.CONFIG_TILE, constants.CONFIG_TILE_POINTSIZES))
    else:
        is_correct = False
    return is_correct

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
        (mimeType, encoding) = mimetypes.guess_type(file)
        if mimeType in constants.IMAGE_MIMETYPES and not file.startswith(constants.FILE_PREFIX_TILE) and not file.startswith(constants.FILE_PREFIX_TILE_DOMINANT):
            path_collage = joinPath(DIR_IMG, constants.FILE_PREFIX_TILE + os.path.splitext(file)[0] + ".png")
            path_dominant = joinPath(DIR_IMG, constants.FILE_PREFIX_TILE_DOMINANT + os.path.splitext(file)[0] + ".png")
            s = subprocess.Popen([
                "convert",
                joinPath(DIR_IMG, file),
                "-resize",
                str(TILE_SIZE) + "x" + str(TILE_SIZE) + "^",
#                "-gravity",
#                "center",
#                "-extent",
#                str(TILE_SIZE) + "x" + str(TILE_SIZE),
                path_collage
            ])
            s.wait()
            cropped = image_crop.image_square(Image.open(path_collage))
            cropped.save(path_collage)
            shutil.copyfile(path_collage, path_dominant)
            colorz = dominant_colors.colorz(path_collage, DOMINANT_COLORS)
            drawColors(path_dominant, colorz)
            printLabels(path_dominant, colorz)
            rgb = [
                strToFraction("".join([colorz[0][1], colorz[0][2]])),
                strToFraction("".join([colorz[0][3], colorz[0][4]])),
                strToFraction("".join([colorz[0][5], colorz[0][6]]))
            ]
            colors.append({
                "path_dominant": path_dominant,
                "path_collage": path_collage,
                "RGB_string": colorz[0],
                "RGB": rgb,
                "YIQ": colorsys.rgb_to_yiq(rgb[0], rgb[1], rgb[2]),
                "HSV": colorsys.rgb_to_hsv(rgb[0], rgb[1], rgb[2]),
                "HLS": colorsys.rgb_to_hls(rgb[0], rgb[1], rgb[2])
            })
            photoCount = photoCount + 1
    count_tile_columns = math.ceil(photoCount ** 0.5)
    count_tile_rows = math.ceil(photoCount/count_tile_columns)
    sortColors()

    for c in byRGB:
        collageRGB.append(c.get("path_collage"))
    for c in byYIQ:
        collageYIQ.append(c.get("path_collage"))
    for c in byHLS:
        collageHLS.append(c.get("path_collage"))
    for c in byHSV:
        collageHSV.append(c.get("path_collage"))
    for c in byRGB:
        collageRGBDominant.append(c.get("path_dominant"))
    for c in byYIQ:
        collageYIQDominant.append(c.get("path_dominant"))
    for c in byHLS:
        collageHLSDominant.append(c.get("path_dominant"))
    for c in byHSV:
        collageHSVDominant.append(c.get("path_dominant"))

    for key_color_model, command_collage in [
        ("RGB", collageRGB),
        ("YIQ", collageYIQ),
        ("HLS", collageHLS),
        ("HSV", collageHSV),
        ("RGB_dominant", collageRGBDominant),
        ("YIQ_dominant", collageYIQDominant),
        ("HLS_dominant", collageHLSDominant),
        ("HSV_dominant", collageHSVDominant),
    ]:
        createCollageForColoModel(
            key_color_model, command_collage, count_tile_rows, count_tile_columns
        )

    print "\nTotal " + str(photoCount) + " images"
