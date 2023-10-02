#!/usr/bin/python
# -*- coding: UTF-8 -*-

import codecs
import os
import sys
import functools
import tinify
tinify.key = "07kVTh8oGbNFNHn4Fb0XU-t_ncAlJkMq"
compresswidth = 512
reload(sys)
sys.setdefaultencoding('utf8')
USE_COMPRESS_2 = False


from PIL import Image
from PIL import ImageFile
from PIL import ExifTags
ImageFile.LOAD_TRUNCATED_IMAGES = True

import imghdr

import re
global compressRate
compressRate = 0.3
global res
res = ""
global rootdir
rootdir = os.getcwd()
global head
head = ""
global headflag
headflag = False
global subcnt
subcnt = 0

def collectPicName(dir, namearr):
    # k = 0
    global head
    global headflag
    for root, dirs, files in os.walk(dir):
        for file in files:
            pos = file.find(".jpg")
            if pos == -1:
                continue
            if file == "head.jpg":
                head = os.path.join(root, file).replace(rootdir + "/", '')
                headflag = True
                continue
            # k += 1
            # os.system("mv " + os.path.join(root, file) + " " + os.path.join(root, str(k) + ".jpg"))
            fileabsdir = os.path.join(root, file).replace(rootdir+"/", '')
            namearr.append(fileabsdir)

def get_rotation_code(img):
    """
    Returns rotation code which say how much photo is rotated.
    Returns None if photo does not have exif tag information.
    Raises Exception if cannot get Orientation number from python
    image library.
    """
    if not hasattr(img, '_getexif') or img._getexif() is None:
        return None

    for code, name in ExifTags.TAGS.iteritems():
        if name == 'Orientation':
            orientation_code = code
            break
    else:
        raise Exception('Cannot get orientation code from library.')

    return img._getexif().get(orientation_code, None)


class IncorrectRotationCode(Exception):
    pass


def rotate_image(img, rotation_code):
    """
    Returns rotated image file.

    img: PIL.Image file.
    rotation_code: is rotation code retrieved from get_rotation_code.
    """
    if rotation_code == 1:
        return img
    if rotation_code == 3 or rotation_code==4:
        img = img.transpose(Image.ROTATE_180)
    elif rotation_code == 6 or rotation_code==5:
        img = img.transpose(Image.ROTATE_270)
    elif rotation_code == 8 or rotation_code==7:
        img = img.transpose(Image.ROTATE_90)
    else:
        raise IncorrectRotationCode('{} is unrecognized '
                                    'rotation code.'
                                    .format(rotation_code))
    return img

def compressSinglePic2(inputdir, outputdir):
    source = tinify.from_file(inputdir)
    print ('Resizing ' + inputdir)
    resized = source.resize(method = "scale", width = compresswidth)
    resized.to_file(outputdir)

def compressSinglePic(inputdir, outputdir, cpsrate):
    image = Image.open(inputdir)
    w,h = image.size
    if w < compresswidth or h < compresswidth:
        os.system("cp " + inputdir + " " + outputdir)
        print("Compress: "+inputdir.replace(rootdir,"") + "\nSkip: "+str(w)+"x"+str(h)+"\n")
        return
    towidth = w
    toheight = h
    while cpsrate > 0.01 and min(towidth, toheight) > compresswidth:
        cpsrate -= 0.01
        towidth = int(w * cpsrate)
        toheight = int(h * cpsrate)

    print("Compress: "+inputdir.replace(rootdir,"") + "\nsize: "+str(w)+"x"+str(h)+"\t->\t"+str(towidth)+"x"+str(toheight)+"\n")

    rotation_code = get_rotation_code(image)
    if rotation_code is not None and rotation_code != 0:
        image = rotate_image(image, rotation_code)

    image.thumbnail((towidth , toheight), Image.ANTIALIAS)


    # im.thumbnail((500, 500))

    # im.resize((towidth,toheight),Image.ANTIALIAS)

    image.save(outputdir,optimize=True,quality=100)
    return


def compressBkgQto():
    for root, dirs, files in os.walk(os.path.join(rootdir,"background")):
        for file in files:
            pos = file.find(".jpg")
            if pos == -1:
                continue
            if USE_COMPRESS_2:
                compressSinglePic2(os.path.join(root, file),
                                  os.path.join(root, file).replace(".jpg", "_cpsed.jpg"))
            else:
                compressSinglePic(os.path.join(root, file),
                                  os.path.join(root, file).replace(".jpg", "_cpsed.jpg")
                                  , compressRate)
            os.system("rm -f " + os.path.join(root, file))
            os.system("mv " + os.path.join(root, file).replace(".jpg", "_cpsed.jpg") + " " + os.path.join(root, file))
    for root, dirs, files in os.walk(os.path.join(rootdir,"QuoteImage")):
        for file in files:
            pos = file.find(".jpg")
            if pos == -1:
                continue
            if USE_COMPRESS_2:
                compressSinglePic2(os.path.join(root, file),
                                  os.path.join(root, file).replace(".jpg", "_cpsed.jpg"))
            else:
                compressSinglePic(os.path.join(root, file),
                                  os.path.join(root, file).replace(".jpg", "_cpsed.jpg")
                                  , compressRate)

            os.system("rm -f " + os.path.join(root, file))
            os.system("mv " + os.path.join(root, file).replace(".jpg", "_cpsed.jpg") + " " + os.path.join(root, file))

# def compressProcess():
#     os.system("rm -rf Galary_Compressed")
#     os.system("mkdir Galary_Compressed")
#     os.system("cp -r Galary/* Galary_Compressed")
#     for root, dirs, files in os.walk(rootdir+"/Galary_Compressed"):
#         for file in files:
#             pos = file.find(".jpg")
#             if pos == -1:
#                 continue
#             if file == "head.jpg":#compress head.jpg
#                 compressSinglePic(os.path.join(root, file),
#                                   os.path.join(root, file).replace(".jpg","_cpsed.jpg")
#                                   ,compressRate)
#                 os.system("rm -f "+os.path.join(root, file))
#                 os.system("mv " + os.path.join(root, file).replace(".jpg","_cpsed.jpg") + " " + os.path.join(root, file))
#                 continue
#             compressSinglePic(os.path.join(root, file),
#                               os.path.join(root, file).replace(".jpg", "_cpsed.jpg")
#                               , compressRate)
#             os.system("rm -f " + os.path.join(root, file))

def count(now, tot):
    return '[' + str(round(100.0 * now /float(tot), 1)) + '%]'

def compressProcess():
    tot = 0
    for root, dirs, files in os.walk(rootdir+"/Galary"):
        for file in files:
            pos = file.find(".jpg")
            if pos == -1:
                continue
            tot += 1
    now = 0
    if not os.path.exists(os.path.join(rootdir, "Galary_Compressed")):
        os.system("mkdir Galary_Compressed")
    for root, dirs, files in os.walk(rootdir+"/Galary"):
        for dir in dirs:
            if not os.path.exists(os.path.join(rootdir, "Galary_compressed", dir)):
                os.system("mkdir " + os.path.join(rootdir,"Galary_compressed", dir))
                print("Create Directory: " + os.path.join(rootdir, "Galary_compressed", dir))
    for root, dirs, files in os.walk(rootdir + "/Galary"):
        for file in files:
            pos = file.find(".txt")
            if pos != -1:
                os.system("cp " + os.path.join(root, file) + " " + os.path.join(root.replace("Galary", "Galary_compressed"), file))
                continue
            pos = file.find(".jpg")
            if pos == -1:
                continue
            now += 1
            if os.path.exists(os.path.join(root.replace("Galary", "Galary_compressed"), file.replace(".jpg", "_cpsed.jpg"))):
                print(count(now, tot) + "Compress Skip, File Already Exists:\n" + os.path.join(root.replace("Galary", "Galary_compressed"), file.replace(".jpg", "_cpsed.jpg")).replace(rootdir, "") + "\n")
                continue
            if file == "head.jpg":#compress head.jpg
                if os.path.exists(os.path.join(root.replace("Galary", "Galary_compressed"), file)):
                    print(count(now, tot) + "Compress Skip, File Already Exists:\n" + os.path.join(root.replace("Galary", "Galary_compressed"),file).replace(rootdir, "") + "\n")
                    continue
                print count(now, tot),
                if USE_COMPRESS_2:
                    compressSinglePic2(os.path.join(root, file),
                                      os.path.join(root.replace("Galary", "Galary_compressed"), file))
                else:
                    compressSinglePic(os.path.join(root, file),
                                      os.path.join(root.replace("Galary", "Galary_compressed"), file)
                                      ,compressRate)
                continue
            print count(now, tot),
            if USE_COMPRESS_2:
                compressSinglePic2(os.path.join(root, file),
                                  os.path.join(root.replace("Galary", "Galary_compressed"), file.replace(".jpg", "_cpsed.jpg")))
            else:
                compressSinglePic(os.path.join(root, file),
                                  os.path.join(root.replace("Galary", "Galary_compressed"), file.replace(".jpg", "_cpsed.jpg"))
                                  , compressRate)



def appendfile(filename):
    constantdir = os.path.join(rootdir, "IndexConstant")
    global res
    htmlhead = codecs.open(constantdir + "/" + filename, "r", "utf-8")
    while 1:
        line = htmlhead.readline()
        if line == '':
            break
        res += line

def generateBackground():
    ret = "\n"
    backgrounddir = rootdir + "/background"
    for root, dirs, files in os.walk(backgrounddir):
        for file in files:
            pos = file.find(".jpg")
            if pos == -1:
                continue
            ret += "<li style=\"background-image: url(" + "background/" \
                  + file + ");\" data-stellar-background-ratio=\"0.5\"></li>\n"
    return ret

def append(str):
    global res
    res += str

def readFromFile(filename):
    constantdir = os.path.join(rootdir, "SubIndexConstant")
    ret = ""
    htmlhead = codecs.open(constantdir + "/" + filename, "r", "utf-8")
    while 1:
        line = htmlhead.readline()
        if line == '':
            break
        ret += line
    return ret

# def generatePic(namearr):
#     ret = ''
#     for namedir in namearr:
#         ret += "\n<figure class=\"animate-box\">\n<img src=\""
#         ret += namedir
#         ret += "\" alt=\"Sorry, something wrong happened... Please refresh " \
#                "the webpage...\" class=\"img-responsive\">\n</figure>\n"
#     return ret

def generatePic(namearr, tit):
    ret = ''
    for namedir in namearr:
        ret += "<div class=\"col-md-4 col-sm-4 col-xs-6 col-xxs-12 animate-box\">\n\t<div class=\"img-grid\">\n\t<img src=\""
        ret += namedir
        ret += "\" alt=\"Something wrong happened...\" class=\"img-responsive\">\n\t<a href=\""
        ret += namedir.replace("Galary_Compressed","Galary").replace("_cpsed.jpg",".jpg")
        ret += "\" >\n\t<div>\n\t<span class=\"fh5co-meta\">Click for Original Image </span>\n\t<h2 class=\"fh5co-title\">"
        ret += tit
        ret += "</h2>\n\t</div>\n\t</a>\n\t</div>\n\t</div>\n\n"
    return ret


def buildSubIndex(namearr, title, content):
    ret = ""
    global subcnt
    subcnt += 1
    filename = "subindex" + str(subcnt) + ".html"
    output = codecs.open(filename, "w", "utf-8")
    ret += readFromFile("SubHead.txt")
    ret += title
    ret += readFromFile("SubAfterTitle.txt")
    if headflag:
        ret += head
    else:
        ret += namearr[0]
    ret += readFromFile("SubBeforePic.txt")
    ret += content
    ret += readFromFile("SubAfterContent.txt")
    ret += generatePic(namearr, title)
    ret += readFromFile("SubAfterPic.txt")
    output.write(ret)
    return filename


def generaterGalary(Galarydir):
    info = codecs.open(Galarydir + "/info.txt", "r", "utf-8")
    galarytitle = info.readline()
    galarycontent = ""
    while 1:
        line = info.readline()
        if line == '':
            break
        galarycontent += " <p> " + line + "</p>\n"
    galarycontent += " <p></p>\n"
    galarycontent += " <a>点击以下图片查看原图～</a>\n"
    ret = ""
    namearray = []
    collectPicName(Galarydir, namearray)
    ret += "<div class=\"col-md-4 col-sm-4 col-xs-6 col-xxs-12 animate-box\">\n<div class=\"img-grid\">\n<img src=\""
    if headflag:
        ret += head
    else:
        ret += namearray[0]
    ret += "\" alt=\"Something wrong happened...\" class=\"img-responsive\">" \
           "\n<a href=\"http://love.jinningli.cn/"
    ret += buildSubIndex(namearray, galarytitle, galarycontent)
    ret += "\" target=\"_blank\" class=\"transition\"><div>\n<span class=\"fh5co-meta\">"
    ret += str(namearray.__len__())
    ret +=  " images</span>\n<h2 class=\"fh5co-title\">"
    ret += galarytitle
    ret += "</h2>\n</div>\n</a>\n</div>\n</div>\n"
    return ret

def stdlizeFilename():
    for root, dirs, files in os.walk(rootdir+"/Galary"):
        for file in files:
            if file.find(".png") != -1:
                os.system("mv " + os.path.join(root, file) + " " + os.path.join(root, file.replace(".png", ".jpg")))
                print("Modified name from " + os.path.join(root,file).replace(rootdir, "") + " into jpg format.")
            if file.find(".PNG") != -1:
                os.system("mv " + os.path.join(root, file) + " " + os.path.join(root, file.replace(".PNG", ".jpg")))
                print("Modified name from " + os.path.join(root,file).replace(rootdir, "") + " into jpg format.")
            if file.find(".JPG") != -1:
                os.system("mv " + os.path.join(root, file) + " " + os.path.join(root, file.replace(".JPG", ".jpg")))
                print("Modified name from " + os.path.join(root,file).replace(rootdir, "") + " into jpg format.")
            if file.find(".JPEG") != -1:
                os.system("mv " + os.path.join(root, file) + " " + os.path.join(root, file.replace(".JPEG", ".jpg")))
                print("Modified name from " + os.path.join(root,file).replace(rootdir, "") + " into jpg format.")
            if file.find(".jpeg") != -1:
                os.system("mv " + os.path.join(root, file) + " " + os.path.join(root, file.replace(".jpeg", ".jpg")))
                print("Modified name from " + os.path.join(root,file).replace(rootdir, "") + " into jpg format.")
            if file.find(".HEIC") != -1:
                os.system("magick convert {} {}".format(
                os.path.join(root, file),
                os.path.join(root, file.replace(".HEIC", ".jpg"))
                ))
                os.system("rm " + os.path.join(root, file))
                print("Modified name from " + os.path.join(root,file).replace(rootdir, "") + " into jpg format.")

def encrypt(encrypt_subindex=True):
    # Static HTML encryption based on https://github.com/robinmoisson/staticrypt
    global subcnt
    print("Please export MY_WEBSITE_PASSWORD in system environment (e.g. .zshrc)")
    password = os.environ['MY_WEBSITE_PASSWORD']
    print("Current password is: {}".format(password))
    command = "staticrypt index.html {} -o index.html --decrypt-button Unlock".format(password)
    print(command)
    os.system(command)
    if encrypt_subindex:
        for i in range(1, subcnt + 1):
            command = "staticrypt subindex{}.html {} -o subindex{}.html --decrypt-button Unlock".format(i, password, i)
            print(command)
            os.system(command)

def main():
    print("\n-----------------------\nHTML Building Process Start\n-----------------------\n")
    print("\n-----------------------\nModifying Image Format...\n-----------------------\n")
    stdlizeFilename()
    print("\n-----------------------\nCompressing Image...\n-----------------------\n")
    compressBkgQto()
    compressProcess()
    print("\n-----------------------\nCompressing Image Finish\n-----------------------\n")
    appendfile("IndexHead.txt")
    appendfile("IndexBeforeBackground.txt")
    append(generateBackground())
    appendfile("IndexBeforeGalary.txt")
    print("\nGenerated Galary:\n-----------------------")
    for root, dirs, files in os.walk(rootdir + "/Galary_Compressed"):
        for dir in dirs:
            print("Create Directory: " + dir)
            append(generaterGalary(os.path.join(root, dir)))
    print("-----------------------\n")
    appendfile("IndexAfterGalary.txt")
    tmpout = codecs.open("index.html", "w", "utf-8")
    tmpout.write(res)
    print("\n-----------------------\nEncrypting Website...\n-----------------------\n")
    encrypt()
    print("\n-----------------------\nEncrypting Finish\n-----------------------\n")

main()

# compressProcessPro()

print("\n-----------------------\nHTML Build Success!!\n-----------------------\n")
