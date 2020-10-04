from pathlib import Path


def getKeyFrames(videoPath):
    import subprocess
    import pkg_resources
    import shutil
    import cv2
    import numpy
    import os
    import re
    from PIL import Image
    import PIL
    import videokf as vf
    import sys

    videoPath = Path(videoPath)

    required = {'opencv-python', 'numpy', 'video-kf'}
    installed = {pkg.key for pkg in pkg_resources.working_set}
    missing = required - installed

    if missing:
        python = sys.executable
        subprocess.check_call(
            [python, '-m', 'pip', 'install', *missing], stdout=subprocess.DEVNULL)
    else:
        print("Requirements Fulfilled")

    if not os.path.exists('unique'):
        os.makedirs('unique')

    if(os.path.exists(os.path.dirname(videoPath)+"/keyframes")):
        shutil.rmtree(os.path.dirname(videoPath)+"/keyframes",
                      ignore_errors=False, onerror=None)

    print("It should take a few minutes have patience :)")

    vf.extract_keyframes(videoPath)

    folder = os.path.dirname(videoPath)+"/keyframes"
    read = os.listdir(folder)
    read.sort(key=lambda f: int(re.sub('\D', '', f)))
    i = 0

    while(i < len(read)):

        img1 = cv2.imread(os.path.join(folder, read[i-1]))
        img2 = cv2.imread(os.path.join(folder, read[i]))
        res = cv2.absdiff(img1, img2)
        res = res.astype(numpy.uint8)
        percentage = (numpy.count_nonzero(res) * 100) / res.size
        if(percentage > 50):
            shutil.move(os.path.join(
                folder, read[i-1]), os.path.join("unique", read[i-1]))
            print(read[i-1])

        i += 1

    i = 0
    while(i < len(read)):

        os.remove(os.path.join(folder, read[i]))

        i += 1


print("Enter the address of your video file output will be in a folder unique : ")
vidPath = Path(input())
getKeyFrames(vidPath)
