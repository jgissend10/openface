# -*- coding: UTF-8 -*-

"""
@file openface.py
@brief
    Implement of img eigener in eigen_center.

Created on: 2016/1/14
"""

import numpy as np
import logging
from PIL import Image

import openface

from faceapi import openfaceutils
from faceapi import exceptions
from faceapi.utils import log_center
from faceapi.detect_center import FaceDetector

"""
8888888b.            .d888 d8b
888  "Y88b          d88P"  Y8P
888    888          888
888    888  .d88b.  888888 888 88888b.   .d88b.  .d8888b
888    888 d8P  Y8b 888    888 888 "88b d8P  Y8b 88K
888    888 88888888 888    888 888  888 88888888 "Y8888b.
888  .d88P Y8b.     888    888 888  888 Y8b.          X88
8888888P"   "Y8888  888    888 888  888  "Y8888   88888P'
"""

_DEFAULT_IMG_W = 400
_DEFAULT_IMG_H = 300


"""
.d8888b.  888
d88P  Y88b 888
888    888 888
888        888  8888b.  .d8888b  .d8888b
888        888     "88b 88K      88K
888    888 888 .d888888 "Y8888b. "Y8888b.
Y88b  d88P 888 888  888      X88      X88
 "Y8888P"  888 "Y888888  88888P'  88888P'
 """


class FaceDetectorOf(FaceDetector):
    def __init__(self):
        super(FaceDetectorOf, self).__init__()
        self._logger = log_center.make_logger(__name__, logging.INFO)

    def detect(self, image):
        if isinstance(image, basestring):
            img = Image.open(image)
            self._logger.debug("PIL image: {}".format(str(img)))
        elif isinstance(image, Image.Image):
            img = image
        else:
            raise exceptions.LibError("Don't know img type")

        buf = np.fliplr(np.asarray(img))
        rgbFrame = np.zeros(
                        (_DEFAULT_IMG_H, _DEFAULT_IMG_W, 3),
                        dtype=np.uint8)
        rgbFrame[:, :, 0] = buf[:, :, 2]
        rgbFrame[:, :, 1] = buf[:, :, 1]
        rgbFrame[:, :, 2] = buf[:, :, 0]

        face_box = openfaceutils.align.getLargestFaceBoundingBox(rgbFrame)
        # face_list = align.getAllFaceBoundingBoxes(rgbFrame)
        face_list = [face_box] if face_box is not None else []

        detected_list = []
        for face_box in face_list:
            landmarks = openfaceutils.align.findLandmarks(rgbFrame, face_box)

            alignedFace = openfaceutils.align.align(
                        openfaceutils.args.imgDim, rgbFrame, face_box,
                        landmarks=landmarks,
                        landmarkIndices=openface.AlignDlib.OUTER_EYES_AND_NOSE)
            if alignedFace is None:
                continue

            detected_list.append(alignedFace)

        return detected_list
