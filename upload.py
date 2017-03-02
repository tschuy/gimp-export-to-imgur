#!/usr/bin/python

from gimpfu import *
import time
import base64
import json
import os
import tempfile

client_id = "75272777892320e"

def upload_image(path):
    """
    Upload an image from a given path to Imgur. Uses the urllib2 library
    to ensure we don't need third-party dependencies for this package.
    """
    import urllib
    import urllib2

    with open(path, "rb") as image_file:
        args = { 'image': base64.b64encode(image_file.read()) }

    request = urllib2.Request('https://api.imgur.com/3/image')
    request.add_header('Authorization', "Client-ID " + client_id)

    request.add_data(urllib.urlencode(args))
    return json.loads(urllib2.urlopen(request).read())['data']


def plugin_main(image, layer):
    image = pdb.gimp_image_duplicate(image)
    layer = pdb.gimp_image_merge_visible_layers(image, CLIP_TO_IMAGE)
    file  = tempfile.NamedTemporaryFile(suffix='.png')
    file.close()
    pdb.file_png_save2(image, layer, file.name, os.path.basename(file.name), 0,5,0,0,0,0,0,0,0)
    imgur = upload_image(file.name)
    clean = os.remove(file.name)
    print imgur['link']
    gimp.message("Sucessfully uploaded!\n{}".format(imgur['link']))


register(
        "imgur_uploader",
        "Save and upload the image to Imgur",
        "Save and upload the image to Imgur",
        "Evan Tschuy",
        "MIT License",
        "2015",
        "<Image>/File/Upload to Imgur",
        "RGB*, GRAY*",
        [],
        [],
        plugin_main)

main()
