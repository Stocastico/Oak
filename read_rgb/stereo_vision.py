import cv2
import depthai as dai
import numpy as np


def getFrame(queue):
  """
  Queries the frame from the queue, transfers it to the host and converts the frame to a numpy array
  """
  frame = queue.get()
  return frame.getCvFrame()

def getMonoCamera(pipeline, isLeft, resolution=400):
  """
  Create a camera node for the pipeline. Then, set the camera resolution using 
  the setResolution method. The sensorResolution class has the following 
  attributes to choose from:
    THE_700_P          (1280x720p)
    THE_800_P          (1280x800p)
    THE_400_P          (640x400p)
    THE_480_P          (640x480p)
  If not specified or the format is invalid, the resolution will be set to 640x400p.
  Resolution can be either 400, 480, 700 or 800
  """
  mono = pipeline.createMonoCamera()
  
  if not resolution:
    resolution=dai.MonoCameraProperties.SensorResolution.THE_400_P
  else if resolution == 400:     
    resolution=dai.MonoCameraProperties.SensorResolution.THE_400_P
  else if resolution == 480:
   resolution=dai.MonoCameraProperties.SensorResolution.THE_480_P
  else if resolution == 700:
   resolution=dai.MonoCameraProperties.SensorResolution.THE_700_P
  else if resolution == 800:
    resolution=dai.MonoCameraProperties.SensorResolution.THE_800_P
  else:
    resolution=dai.MonoCameraProperties.SensorResolution.THE_400_P
  mono.setResolution(resolution)

  if isLeft:
    mono.setBoardSocket(dai.CameraBoardSocket.LEFT)
  else :
    mono.setBoardSocket(dai.CameraBoardSocket.RIGHT)
  return mono


if __name__ == '__main__':
  
  pipeline = dai.Pipeline()
  
  monoLeft = getMonoCamera(pipeline, isLeft = True)
  monoRight = getMonoCamera(pipeline, isLeft = False)
  
  xoutLeft = pipeline.createXLinkOut()
  xoutLeft.setStreamName("left")
  
  xoutRight = pipeline.createXLinkOut()
  xoutRight.setStreamName("right")
  
  monoLeft.out.link(xoutLeft.input)
  monoRight.out.link(xoutRight.input)

  with dai.Device(pipeline) as device:
    leftQueue = device.getOutputQueue(name="left", maxSize=1)
    rightQueue = device.getOutputQueue(name="right", maxSize=1)
    cv2.namedWindow("Stereo Pair")
    sideBySide = True

  while True:
    leftFrame = getFrame(leftQueue)
    rightFrame = getFrame(rightQueue)

    if sideBySide:
      imOut = np.hstack((leftFrame, rightFrame))
    else :
      imOut = np.uint8(leftFrame/2 + rightFrame/2)

    cv2.imshow("Stereo Pair", imOut)
    key = cv2.waitKey(1)
    if key == ord('q'):
        break
    elif key == ord('t'):
        sideBySide = not sideBySide
