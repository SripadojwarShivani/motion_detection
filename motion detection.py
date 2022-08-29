#import libraries
import datetime
import imutils
import time
import cv2

#reading video from webcam
a = cv2.VideoCapture(0)


#variable declaring first frame
firstFrame=None

#looping through each frame from video
while (True):
    success, frame = a.read()
    if success:  # frame read successfully
        text = "Unoccupied"
        frame = imutils.resize(frame, width=500)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)

        # if the first frame is None, initialize it
        if firstFrame is None:
            firstFrame = gray
            continue

    # compute the absolute difference between the current frame and first frame
        frameDelta = cv2.absdiff(firstFrame, gray)
        thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]

        # dilate the thresholded image to fill in holes, then find contours on thresholded image
        thresh = cv2.dilate(thresh, None, iterations=2)

        #finding contours
        cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)

        # loop over the contours
        for c in cnts:

            # if the contour is too small, ignore it
            if cv2.contourArea(c) < 5000:
                continue

            # Finding the bounding box for the contour, draw it on the frame and update the text
            (x, y, w, h) = cv2.boundingRect(c)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            text = "Occupied"

        # Resizing the output window
        cv2.namedWindow("output", cv2.WINDOW_NORMAL)
        frame = cv2.resize(frame, (900, 500))  

        #labeling the image with text, date and time
        cv2.putText(frame, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"),(10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
        cv2.putText(frame, "Room Status: {}".format(text), (10, 20),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

        #displaying output
        cv2.imshow('output', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

#destroying all windows
a.release()
cv2.destroyAllWindows()