# Oak
Code developed for using OAK-D camera

### Setup

Make sure to have DepthAI API installed, or install it like this

```python
git clone https://github.com/luxonis/depthai.git
cd depthai
python3 install_requirements.py
python3 depthai_demo.py
```

### Documentation

[Luxonis DepthAI Documentation](https://docs.luxonis.com/projects/api/en/latest/)

### Projects

+ [Read camera frames and display them](./read_rgb)
+ [Read depth map](./read_depth)

### Example pipeline

#### Create a pipeline

```python
import depthai as dai
pipeline = dai.Pipeline()
mono = pipeline.createMonoCamera()  # create camera node
mono.setBoardSocket(dai.CameraBoardSocket.LEFT) # select a camera
```

#### Create out node and acquire frames

```python
xout = pipeline.createXLinkOut()
xout.setStreamName("left")
mono.out.link(xout.input)
```

#### Get frame in numpy format

```python
with dai.Device(pipeline) as device:
  queue = device.getOutputQueue(name="left")
  frame = queue.get()
  imOut = frame.getCvFrame()
```