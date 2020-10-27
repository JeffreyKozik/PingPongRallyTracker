# Jeffrey Kozik

# Thanks to the following resources:
# https://www.youtube.com/watch?v=sghglbXyjHc
    # Learned how to template match -> much of the code comes from video
# https://www.youtube.com/watch?v=MkcUgPhOlP8
    # Learned how to track movement -> much of the code comes from video
# https://www.pyimagesearch.com/2015/09/14/ball-tracking-with-opencv/
    # imutils and resizing frames

# Program to track how many hits in a row in a videotaped rally
import cv2
import numpy as np
import imutils
import matplotlib.pyplot as plt

cap = cv2.VideoCapture('OneRallyClip2.mov')
ret, frame1 = cap.read()
ret, frame2 = cap.read()
frame1 = imutils.resize(frame1, width=600)
frame2 = imutils.resize(frame2, width=600)
template = cv2.imread("snippetpong.png", 0)
w, h = template.shape[::-1]
# returns rows, columns, channels
side = -1 # current side the ball is on -1 is left, 1 is right
prevSide = -1 # the previous side the ball was on
realcounter = 0; # the number of hits in a row

while cap.isOpened():
    diff = cv2.absdiff(frame1, frame2)
    # cv2.imshow("diff", diff)
    # cv2.waitKey(0)
    gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    # cv2.imshow("gray", gray)
    # cv2.waitKey(0)
    # OpenCV represents in BGR colorspace
    blur = cv2.GaussianBlur(gray, (5,5), 0)
    # cv2.imshow("blur", blur)
    # cv2.waitKey(0)
    # a kernel of 5 by 5, deviation is 0
    _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY) # alternative to canny edge detection?
    # 20 is the threshold, so if it is greater than 20 (somewhat white), it is turned into white (255)
    # cv2.imshow("thresh",thresh)
    # cv2.waitKey(0)
    dilated = cv2.dilate(thresh, None, iterations=3)
    # dilation distance, number of iterations -> sort of pixelizes it
    # cv2.imshow("dilation", dilated)
    # cv2.waitKey(0)
    contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # countour retrieval mode, contour approximation method
    cv2.putText(frame1, "Counter: {}".format(realcounter), (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
    # Counter: realcounter, located at x=10, y=20, that font, fontscale (this is 1x original font size), color (bgr), thickness
    for contour in contours:
        (x, y, w, h) = cv2.boundingRect(contour)

        if cv2.contourArea(contour) < 700 or cv2.contourArea(contour) > 1500 or (w < 50) or (w > 90) or (h < 15) or (h > 55):
            continue

        roi = frame1[y: y+h, x: x+w]
        # numpy array, top left corner and bottom right corner of cropped square
        # ^ https://stackoverflow.com/questions/15589517/how-to-crop-an-image-in-opencv-using-python
        roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
        res = cv2.matchTemplate(roi, template, cv2.TM_CCOEFF_NORMED)
        threshold = 0.6;
        loc = np.where(res >= threshold)

        if(len(loc[0]) == 0):
            continue

        if (x > 100) and (x < 450):
            cv2.rectangle(frame1, (x, y), (x+w, y+h), (0, 255, 0), 2)
            # draws a rectangle on frame 1 with the upper left corner at x,y and lower right at x+w, y+h, color green, thickness 2
            if(x > 300):
                side = 1
            if(x <= 300):
                side = -1
            if(prevSide != side):
                realcounter = realcounter + 1
                prevSide = side

    # cv2.drawContours(frame1, contours, -1, (0,255,0), 2) # draws all contours (-1 position meaning), green color, thickness 2
    cv2.imshow("Rally", frame1)
    frame1 = frame2
    ret, frame2 = cap.read()
    frame1 = imutils.resize(frame1, width=600)
    frame2 = imutils.resize(frame2, width=600)
    if cv2.waitKey(1) & 0xFF == ord('q'): # if q is pressed it pauses
        cv2.waitKey(-1) #If a key is pressed it starts again

cv2.destroyAllWindows()
cap.release()

# maybe do something where if it senses movement on one side at a certain time, then wait a certain amount of seconds
# if it senses movement on the other side after that certain amount of seconds, then it counts as a hit

# or could also do something where it looks through each of the proposed areas. And if a certain color is present in that area
# then it's a yes. Would still need something similar to the above idea, but would be simpler
# just a matter of tracking position and keep track of left or right side. If it switches side then it's a hit.

# also this will be my last day (at least for a little bit) working on this project -> I want to start analyzing some fluid
# and marble movements next

# maybe don't do a bounding rectangle?
