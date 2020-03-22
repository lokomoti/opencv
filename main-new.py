import math
import time

import coordinatesCalc as calc
import cv2
import numpy as np
import imutils


def nothing(x):
    # any operation
    pass

angle = 5

# def distCoor(x1, y1, x2, y2):
#    a = int(pow((x2 - x1),2))
#    b = int(pow((y2 - y1),2))
#    c = math.sqrt(a + b)
#    return int(c)

# font variable
font = cv2.FONT_HERSHEY_SIMPLEX

# Setup variables:
diffTresh = 1.7

# list of video sources
path1 = "http://10.0.0.31:8080/video"
path2 = "rtsp://admin:Nedoma1126!@10.0.0.141/live2.sdp"
path3 = "http://209.206.162.230/mjpg/video.mjpg"
path4 = "http://10.0.0.26:8081"
path5 = "rtsp://admin:admin@10.0.0.232:554/h264.sdp?res=full"

# start video capture
path = "http://bctprod14:18814/video/stream/1.mjpeg"

cap = cv2.VideoCapture(path)

# try if video stream works

print("video OK!")

# set input resolution
cap.set(3, 720)
cap.set(4, 1280)
tra = int(cap.get(3))
trb = int(cap.get(4))

# create two gui windows
cv2.namedWindow("Frame")
cv2.namedWindow("Trackbars")

# create control elements
cv2.createTrackbar("L-H", "Trackbars", 0, 180, nothing)
cv2.createTrackbar("L-S", "Trackbars", 0, 255, nothing)
cv2.createTrackbar("L-V", "Trackbars", 0, 255, nothing)
cv2.createTrackbar("U-H", "Trackbars", 180, 180, nothing)
cv2.createTrackbar("U-S", "Trackbars", 255, 255, nothing)
cv2.createTrackbar("U-V", "Trackbars", 255, 255, nothing)
cv2.createTrackbar("size", "Trackbars", 50, 60, nothing)
cv2.createTrackbar("MaxCount", "Trackbars", 1, 20, nothing)
cv2.createTrackbar("MaxSize", "Trackbars", 20, 20, nothing)

# move windows after start so both are visible
cv2.moveWindow("Frame", 0, 0)
cv2.moveWindow("Trackbars", 1000, 0)

# start loop
while True:
        # frameMat = cap.read()
        # Frame = cv2.UMat(frameMat)
        ret, frame_raw = cap.read()
        frame = imutils.rotate(frame_raw, angle)

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # read control elements
        l_h = cv2.getTrackbarPos("L-H", "Trackbars")
        l_s = cv2.getTrackbarPos("L-S", "Trackbars")
        l_v = cv2.getTrackbarPos("L-V", "Trackbars")
        u_h = cv2.getTrackbarPos("U-H", "Trackbars")
        u_s = cv2.getTrackbarPos("U-S", "Trackbars")
        u_v = cv2.getTrackbarPos("U-V", "Trackbars")
        size = cv2.getTrackbarPos("size", "Trackbars")
        maxCount = cv2.getTrackbarPos("MaxCount", "Trackbars")
        maxSize = cv2.getTrackbarPos("MaxSize", "Trackbars")

        # reset count value
        count = 0

        # create numpy arrays from HSV color values
        lower_red = np.array([l_h, l_s, l_v])
        upper_red = np.array([u_h, u_s, u_v])

        # video feed used for image processing
        mask = cv2.inRange(hsv, lower_red, upper_red)
        kernel = np.ones((5, 5), np.uint8)
        mask = cv2.erode(mask, kernel)

        # Thumbnail version of mask video along with trackbars
        r = 240.0 / mask.shape[1]
        dim = (320, int(mask.shape[0] * r))
        maskMini = cv2.resize(mask, dim, interpolation=cv2.INTER_AREA)
        cv2.imshow("Trackbars", maskMini)

        # Contours detection
        # contours = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        # for each countour in this list do:
        for cnt in contours:
            area = cv2.contourArea(cnt)
            approx = cv2.approxPolyDP(cnt, 0.02 * cv2.arcLength(cnt, True), True)
            x = approx.ravel()[0]
            y = approx.ravel()[1]
            # if it has 4 corners, area in range, no more that max count, no bigger than max - go next:
            if len(approx) == 4 and (area > int(size * 100) and (maxCount > count)) and (area < (maxSize * 1000)):
                # if diagonals of polygon are same, draw objects
                if calc.diagDiff(approx) < diffTresh:  # corners:

                    # draw outlines
                    cv2.drawContours(frame, [approx], 0, (0, 0, 0), 2)

                    # increment counter for each object
                    count = count + 1

                    # return difference in diagonals
                    diff = calc.diagDiff(approx)

                    # calculate x,y coordinate of center, insert label
                    M = cv2.moments(cnt)
                    cntX = int(M["m10"] / M["m00"])
                    cntY = int(M["m01"] / M["m00"])
                    cv2.putText(frame, str(count) + ".", (int(cntX), int(cntY)), font, 1, (0, 0, 255))

                    # parsing width, lenght data array
                    x1 = x
                    y1 = y
                    x2 = approx.ravel()[2]
                    y2 = approx.ravel()[3]
                    x3 = approx.ravel()[4]
                    y3 = approx.ravel()[5]
                    x4 = approx.ravel()[6]
                    y4 = approx.ravel()[7]

                    # calculate diagonals and compare them, exclude objects
                    dist1 = calc.distance(x1, y1, x2, y2)
                    # print(dist1)

                    # draw diagonal A
                    pts1 = np.array([[x1, y1], [x3, y3]], np.int32)
                    cv2.polylines(frame, [pts1], True, (0, 0, 0))

                    # place text in the middle of the objects
                    xC = ((x + x3) / 2)
                    yC = ((y + y3) / 2)

                    # print letter to each corner of an object
                    cv2.putText(frame, "A", (int(x), int(y)), font, 0.5, (255, 255, 255))
                    cv2.putText(frame, "B", (int(x2), int(y2)), font, 0.5, (255, 255, 255))
                    cv2.putText(frame, "C", (int(x3), int(y3)), font, 0.5, (255, 255, 255))
                    cv2.putText(frame, "D", (int(x4), int(y4)), font, 0.5, (255, 255, 255))
                    # cv2.putText(frame, str(count)+".", (int(xC), int(yC)), font, 1, (0, 0, 255))

                    cv2.putText(frame, "sqareness: " + str(diff), (x - 20, y - 40), font, 0.5, (0, 0, 255))
                    cv2.putText(frame, "area: " + str(area), (x - 20, y - 20), font, 0.5, (255, 0, 0))
                    cv2.circle(frame, (x4, y4), 3, (0, 255, 0), -1)

        # Draw text inform. overlay
        cv2.putText(frame, str(time.strftime("%a, %d %b %Y %H:%M:%S ")), (130, 30), font, 0.5, (255, 255, 255))
        #cv2.putText(frame, "Unit count: " + str(count), (5, 15), font, 0.5, (255, 0, 0))
        cv2.putText(frame, "Max units: " + str(maxCount), (5, 30), font, 0.5, (255, 0, 0))
        #cv2.putText(frame, "Resolution: " + str(cap.get(3)) + " x " + str(cap.get(4)), (130, 15), font, 0.5, (255, 255, 255))

        # Set prewiev window to size
        rat = int(cap.get(3)) / int(cap.get(4))
        winSize = 0.5
        ax = int(trb * winSize * rat)
        by = int(trb * winSize)

        # final = cv2.resize(frame,(ax, by), interpolation = cv2.INTER_AREA)
        cv2.imshow("Frame", frame)
        cv2.imshow("Mask", maskMini)

        key = cv2.waitKey(1)
        if key == 27:
            break

cap.release()
cv2.destroyAllWindows()
