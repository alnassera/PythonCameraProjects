import cv2
import numpy as np
import math

GREEN_THRESHOLD_LOW = (36, 25, 25)
GREEN_THRESHOLD_HIGH = (86, 255, 255)

YELLOW_THRESHOLD_LOW = np.array([20, 100, 100])
YELLOW_THRESHOLD_HIGH = np.array([30, 255, 255])

CAMERA_WIDTH = 320
CAMERA_HEIGHT = 240
CURR_COLOR = (0, 0, 0)

MIN_RADIUS = 2

cam = cv2.VideoCapture(0)

print("Camera initialized")
iterator = 0
iterator_1 = 0
first_pt = None
second_pt = None
erase_pt = None
has_Green = False
global erase, pen


def clear():
    ret_val, img = cam.read()
    img = cv2.flip(img, 1)
    return img


def pen(iterator, iterator_1, first_pt, second_pt, has_Green, CURR_COLOR):
    erase = False
    pen = False
    pt_L = [[]]
    while True:
        # Get image from camera
        ret_val, img = cam.read()
        img = cv2.flip(img, 1)

        # Blur image to remove noise
        img_filter = cv2.GaussianBlur(img.copy(), (3, 3), 0)

        # Convert image from BGR to HSV
        img_filter = cv2.cvtColor(img_filter, cv2.COLOR_BGR2HSV)

        #  Set pixels to white if in color range, others to black (binary bitmap)
        pen_img_binary = cv2.inRange(img_filter.copy(), GREEN_THRESHOLD_LOW, GREEN_THRESHOLD_HIGH)

        # Dilate image to make white blobs larger
        pen_img_binary = cv2.dilate(pen_img_binary, None, iterations=1)

        # Find center of object using contours instead of blob detection.
        pen_img_contours = pen_img_binary.copy()
        pen_contours = cv2.findContours(pen_img_contours, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]

        #white box main
        cv2.rectangle(img, (900, 768), (1366, 0), (255, 255, 255), -1)
        # blue box
        cv2.rectangle(img, (900 + 31, 21), (900 + 94, 64), (255, 0, 0), -1)
        # green
        cv2.rectangle(img, (900 + 157, 21), (900 + 220, 64), (0, 255, 0), -1)
        # black
        cv2.rectangle(img, (900 + 283, 21), (900 + 346, 64), (0, 0, 0), -1)
        # yellow
        cv2.rectangle(img, (900 + 31, 106), (900 + 94, 149), (255, 255, 0), -1)
        # red
        cv2.rectangle(img, (900 + 157, 106), (900 + 220, 149), (0, 0, 255), -1)
        cv2.putText(img, 'ERASE', (900 + 283, 149), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 0), 1)
        cv2.line(img, (900, 256), (1368, 256), (0, 0, 0), 5)
        erase = False

    #    Find the largest contour and use it to compute the min enclosing circle
        if len(pen_contours) > 0:
            if not has_Green:
                pt_L.append([CURR_COLOR])
                if not pen:
                    pt_L[-1].append(False)
                if pen:
                    pt_L[-1].append(True)
            c = max(pen_contours, key=cv2.contourArea)
            ((x, y), radius) = cv2.minEnclosingCircle(c)
            M = cv2.moments(c)
            if radius > 20:
                if M["m00"] > 0:
                    if iterator % 2 == 0:
                        first_pt = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
                        #   print(pt_L[-1])
                        pt_L[-1].append(first_pt)
                        has_Green = True

                    else:
                        second_pt = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
                        print(pt_L[-1])
                        pt_L[-1].append(second_pt)
                        has_Green = True
                    if first_pt and second_pt:
                        if first_pt[0] > 900 and second_pt[0] > 900:
                            cv2.line(img=img, pt1=first_pt, pt2=second_pt, color=i[0], thickness=5, lineType=8, shift=0)
                iterator += 1
            else:
                has_Green = False

        for i in pt_L:
            for j in range(3, len(i)):
                if not (i[j][0] > 900 and i[j - 1][0] > 900):
                    if i[1]:
                        cv2.line(img=img, pt1=i[j], pt2=i[j - 1], color=i[0], thickness=5, lineType=8, shift=0)
                    elif erase:
                        if i[j]:
                            if i[j][0] in range(i[j][0] - 2, i[j][0] + 2) or \
                                (i[j][1] in range(i[j][1] - 2, i[j][1] + 2)):
                                try:
                                    pt_L.remove(i)
                                except ValueError:
                                    pass
                elif 900 <= i[j][0] <= 978 and 21 <=  i[j][1] <= 64:
                    CURR_COLOR = (255, 0, 0)
                    erase = False
                    pen = True

                elif 1057 <= i[j][0] <= 1120 and 21 <= i[j][1] <= 64:
                    CURR_COLOR = (0, 255, 0)
                    erase = False
                    pen = True

                elif 1183 <= i[j][0] <= 1246 and 21 <= i[j][1] <= 64:
                    CURR_COLOR = (0, 0, 0)
                    erase = False
                    pen = True

                elif 931 <= i[j][0] <= 994 and 106 <= i[j][1] <= 149:
                    CURR_COLOR = (255, 255, 0)
                    erase = False
                    pen = True

                elif 1057 <= i[j][0] <= 1220 and 106 <= i[j][1] <= 149:
                    erase = False
                    CURR_COLOR = (0, 0, 255)
                    pen = True

                elif 1183 <= i[j][0] <= 1246 and 106 <= i[j][1] <= 149:
                    erase = True
                    pen = False

        if erase:
            cv2.imshow('webcam', clear())
            erase = False
            pen = False
            pt_L = [[]]
        else:
            cv2.imshow('webcam', img)
        cv2.imshow('countors', pen_img_contours)
        cv2.waitKey(1)


pen(iterator, iterator_1, first_pt, second_pt, has_Green, CURR_COLOR)