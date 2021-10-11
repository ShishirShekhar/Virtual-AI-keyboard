# Import necessary modules
import cv2
import cvzone
from cvzone.HandTrackingModule import HandDetector
from pynput.keyboard import Controller
from time import sleep

# Capture the video
cap = cv2.VideoCapture(0)
# Set height and width
cap.set(3, 1280)
cap.set(4, 720)

# Create an object for hand detection
detector = HandDetector(detectionCon=0.8)

# Create an object for keyboard control
keyboard = Controller()

# Create a two diminsonal list for keys
keys = [["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"],
        ["A", "S", "D", "F", "G", "H", "J", "K", "L", ";"],
        ["Z", "X", "C", "V", "B", "N", "M", ",", ".", "/"]]
specialKey = ["Esc", " ", "Backspace"]
# Create a variable to store output
finalText = ""

# Create a class for buttons
class Button():
    def __init__(self, pos, text, size=(85, 85)):
        self.pos = pos
        self.size = size
        self.text = text

# Create a loop to create objects for each key and append it to a list
buttonList = []     # list for keys object
for i in range(len(keys)):
    for j, key in enumerate(keys[i]):
        pos = (100 * j + 125, 100 * i + 50)
        keyObject = Button(pos=pos, text=key)
        buttonList.append(keyObject)

# Create a loop to create objects for each special key and append it to a list
specialKeyList = []
for i in range(len(specialKey)):
    pos = (100 * 4 * i + 50, 350)
    specialKeyObject = Button(pos=pos, text=specialKey[i], size=(375, 100))
    specialKeyList.append(specialKeyObject)

# Create a function to draw all the buttons
def drawAll(img, buttonList):
    for button in buttonList:
        x, y = button.pos   # get position of button
        w, h = button.size  # get size of button

        # Create a rectangle for the button
        cv2.rectangle(img, pt1=button.pos, pt2=(x + w, y + h),
                    color=(255, 0, 255), thickness=cv2.FILLED)
        # Add corners to the rectangle 
        corner_bbox = (x, y, w, h)
        cvzone.cornerRect(img=img, bbox=corner_bbox, l=20, rt=0)
        # Put text on rectangle
        cv2.putText(img=img, text=button.text, org=(x + 20, y + 65),
                    fontFace=cv2.FONT_HERSHEY_PLAIN, fontScale=4,
                    color=(255, 255, 255), thickness=4)
    
    for specialButton in specialKeyList:
        x, y = specialButton.pos   # get position of button
        w, h = specialButton.size  # get size of button

        # Create a rectangle for the button
        cv2.rectangle(img, pt1=specialButton.pos, pt2=(x + w, y + h),
                    color=(255, 0, 255), thickness=cv2.FILLED)
        # Add corners to the rectangle 
        corner_bbox = (x, y, w, h)
        cvzone.cornerRect(img=img, bbox=corner_bbox, l=20, rt=0)
        # Put text on rectangle
        cv2.putText(img=img, text=specialButton.text, org=(x + 20, y + 65),
                    fontFace=cv2.FONT_HERSHEY_PLAIN, fontScale=4,
                    color=(255, 255, 255), thickness=4)

    return img

# Create flag to run the loop
flag = 1

# While true loop to run the programme
while flag:
    # get image
    success, img = cap.read()
    # Fliping the image as said in question
    img = cv2.flip(img, 1)
    # detect hand
    hands, img = detector.findHands(img)
    
    # Draw the buttons
    img = drawAll(img=img, buttonList=buttonList)

    # Set inital values of landMark and fingers
    lmList1 = 0
    lmList2 = 0
    fin_dis1 = 0
    fin_dis2 = 0

    # Check if hand present
    if hands:
        # Get the values for Hand 1
        hand1 = hands[0]
        lmList1 = hand1["lmList"]       # List of 21 Landmark points
        bbox1 = hand1["bbox"]           # Bounding box info x,y,w,h
        centerPoint1 = hand1['center']  # center of the hand cx,cy
        handType1 = hand1["type"]       # Handtype Left or Right

        # Get fingers
        fingers1 = detector.fingersUp(hand1)
        # Get info of distance of fingers
        fin_dis1, info1, img = detector.findDistance(p1=lmList1[8], p2=lmList1[12], img=img)

        # Check if both the hands are present
        if len(hands) == 2:
            # Get the values for Hand 2
            hand2 = hands[1]
            lmList2 = hand2["lmList"]       # List of 21 Landmark points
            bbox2 = hand2["bbox"]           # Bounding box info x,y,w,h
            centerPoint2 = hand2['center']  # center of the hand cx,cy
            handType2 = hand2["type"]       # Hand Type "Left" or "Right"

            # Get fingers
            fingers2 = detector.fingersUp(hand2)
            # Get info of distance of fingers
            fin_dis2, info2, img = detector.findDistance(p1=lmList2[8], p2=lmList2[12], img=img)

        # Create dynamic functions for the programme
        # Check the values for each button
        for button in buttonList:
            x, y = button.pos   # get position of button
            w, h = button.size  # get size of button
            
            # Check if fingers are on button
            # Create condition
            if (lmList2):
                con = ((x < lmList1[8][0] < x + w) and (y < lmList1[8][1] < y + h)) or ((x < lmList2[8][0] < x + w) and (y < lmList2[8][1] < y + h))
            else:
                con = (x < lmList1[8][0] < x + w) and (y < lmList1[8][1] < y + h)

            # Create if statement
            if (con):
                # Create rectangle of different color on hover
                cv2.rectangle(img=img, pt1=button.pos, pt2=(x + w, y + h),
                            color=(231, 84, 128), thickness=cv2.FILLED)
                # Create text for new rectangle
                cv2.putText(img=img, text=button.text, org=(x + 20, y + 65),
                            fontFace=cv2.FONT_HERSHEY_PLAIN, fontScale=4,
                            color=(255, 255, 255), thickness=4)
                
                # Create condition for click
                if (fin_dis2):
                    click_con = (fin_dis1 < 30) or (fin_dis2 < 30)
                else:
                    click_con = (fin_dis1 < 30)

                # When click
                if (click_con):
                    # Create rectangle of different color on Click
                    cv2.rectangle(img=img, pt1=button.pos, pt2=(x + w, y + h), 
                                color=(0, 255, 0), thickness=cv2.FILLED)
                    # Create text for new rectangle
                    cv2.putText(img=img, text=button.text, org=(x + 20, y + 65),
                                fontFace=cv2.FONT_HERSHEY_PLAIN, fontScale=4, 
                                color=(255, 255, 255), thickness=4)

                    # Press the select text
                    keyboard.press(button.text)
                    # Add the text to final text
                    finalText += button.text
                    # Give a bit time to remove or replace hand
                    sleep(0.5)


        # Check the values for each button
        for specialButton in specialKeyList:
            x, y = specialButton.pos   # get position of button
            w, h = specialButton.size  # get size of button

            # Check if fingers are on button
            # Create condition
            if (lmList2):
                con = ((x < lmList1[8][0] < x + w) and (y < lmList1[8][1] < y + h)) or ((x < lmList2[8][0] < x + w) and (y < lmList2[8][1] < y + h))
            else:
                con = (x < lmList1[8][0] < x + w) and (y < lmList1[8][1] < y + h)

            # Create if statement
            if (con):
                # Create rectangle of different color on hover
                cv2.rectangle(img=img, pt1=specialButton.pos, pt2=(x + w, y + h),
                            color=(231, 84, 128), thickness=cv2.FILLED)
                # Create text for new rectangle
                cv2.putText(img=img, text=specialButton.text, org=(x + 20, y + 65),
                            fontFace=cv2.FONT_HERSHEY_PLAIN, fontScale=4,
                            color=(255, 255, 255), thickness=4)
                
                # Create condition for click
                if (fin_dis2):
                    click_con = (fin_dis1 < 30) or (fin_dis2 < 30)
                else:
                    click_con = (fin_dis1 < 30)

                # When click
                if (click_con):
                    # Create rectangle of different color on Click
                    cv2.rectangle(img=img, pt1=specialButton.pos, pt2=(x + w, y + h),
                                color=(0, 255, 0), thickness=cv2.FILLED)
                    # Create text for new rectangle
                    cv2.putText(img=img, text=specialButton.text, org=(x + 20, y + 65),
                                fontFace=cv2.FONT_HERSHEY_PLAIN, fontScale=4, 
                                color=(255, 255, 255), thickness=4)
                
                    # If text == Esc then quit
                    if (specialButton.text == "Esc"):
                        flag = 0
                        cv2.destroyAllWindows()
                    elif (specialButton.text == "Backspace"):
                        keyboard.press('\b')
                        finalText = finalText[:-1]
                        sleep(0.5)
                    else:
                        # Press the select text
                        keyboard.press(specialButton.text)
                        # Add the text to final text
                        finalText += specialButton.text
                        # Give a bit time to remove or replace hand
                        sleep(0.5)

                

    # Create a rectangle to show the final output
    cv2.rectangle(img=img, pt1=(50, 550), pt2=(700, 650),
                color=(175, 0, 175), thickness=cv2.FILLED)
    # Create text to show the final output.
    cv2.putText(img=img, text=finalText, org=(60, 630),
                fontFace=cv2.FONT_HERSHEY_PLAIN, fontScale=5,
                color=(255, 255, 255), thickness=5)
                    
    # Show the image
    cv2.imshow("Image", img)
    cv2.waitKey(1)