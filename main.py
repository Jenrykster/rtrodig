import cv2
import numpy as np
import time
WINDOW_NAME = 'WebCam'

class DialogueBox:
  currText = ""
  textToRender = ""
  lastUpdate = time.time() 
  def __init__(self, height = 75, padding = 10, border_thickness = 2, textSpeed = 0.2):
    self.textSpeed = textSpeed
    self.height = height
    self.padding = padding
    self.border_thickness = border_thickness
    
    wx, wy, wWdith, wHeight = cv2.getWindowImageRect(WINDOW_NAME)
    self.startX = padding
    self.startY = wHeight - height - padding

    self.endX =  wWdith - padding
    self.endY =  wHeight - padding

  def drawBackground(self, img):
    bg_start_point = (self.startX, self.startY + self.border_thickness)
    bg_end_point = (self.endX - self.border_thickness, self.endY - self.border_thickness)
    bg_color = (0, 0, 0)
    bg_thickness = -1
  
    return cv2.rectangle(img, bg_start_point, bg_end_point, bg_color, bg_thickness)

  def drawBorders(self, backgroundImg):
    border_color = (255, 255, 255)

    border_start_point = (self.startX, self.startY)
    border_end_point = (self.endX, self.endY)

    box = cv2.rectangle(backgroundImg, border_start_point, border_end_point, border_color, self.border_thickness)

    return box
  
  def updateText(self):
    now = time.time()
    if(now - self.lastUpdate < self.textSpeed):
      return

    currCharRender = len(self.currText)
    if(currCharRender < len(self.textToRender)):
      self.currText += self.textToRender[currCharRender]
    self.lastUpdate = now

  def drawText(self, img): 
    org = (self.startX + self.padding * 2, self.startY + self.padding * 2)
    font = cv2.FONT_HERSHEY_SIMPLEX
    color = (255, 255, 255)
    return cv2.putText(img, self.currText, org, font, 0.5, color, 2, cv2.LINE_AA ) 

  def setText(self, text: str):
    self.currText = ""
    self.textToRender = text

  def render(self, img):
    self.updateText()
    boxBg = self.drawBackground(img)
    res = self.drawBorders(boxBg)

    if(len(self.textToRender) > 0):
      res = self.drawText(img)

    return res

cap = cv2.VideoCapture(0)
cv2.namedWindow(WINDOW_NAME)
dialogueBox = DialogueBox()
dialogueBox.setText("Hello World")
while True:
  ret, frame = cap.read()

  frame = dialogueBox.render(frame)

  cv2.imshow(WINDOW_NAME, frame)

  if cv2.waitKey(1) == ord('q'):
    break


cap.release()
cv2.destroyAllWindows()

