# Yolo_grpc

A box with some yolo functions for GRPC.

## YOLO functions

All YOLO functions are stored in the "YoloService.py" file. It contains 3 main functions. 

**predict**:
Used to run the model.predict() function from ultralytics. It expects to receive a datafile variable that is a binary .mat file (containing the image to be analyzed) and a model (based on the ultralytics models). It outputs a .mat file containing the class index, the confidence levels, data, ids, 'is_track', image shape, xywh, xyxy and there normalized variants.

**track**:
Used to run the model.track() function from ultralytics. It expects to receive a datafile variable that is a binary .mat file (containing the frame to be analyzed) and a model (based on the ultralytics models). This version doesn't let the user change the type of tracker, so it uses the ByteTrack tracker as default. It outputs a .mat file containing the class index, the confidence levels, data, ids, 'is_track', image shape, xywh, xyxy and there normalized variants

**plot**:
Used to plot the predict and the track function's output. It expects to receive a .mat file containing the class index, the confidence levels, ids, xyxy and another .mat file containing the original image. It outputs a .mat file containing the plotted image.

## Deploy

To deploy this program it needes to compile the GRPC with the folowing command:

```bash
  python -m grpc_tools.protoc --proto_path=./protos --python_out=. --grpc_python_out=. generic_box.proto
```
To create the Docker image with the program use:

```bash
    docker build -t yolo_grpc --build-arg SERVICE_NAME=generic_box -f docker/Dockerfile .
```

To run the container run the command:

```bash
    docker run -p 8061:8061 -it --rm yolo_grpc
```


## .Mat Output File

The output file follows the structure shown:

```
fileName.mat 	 (dictionary)
└──"frame_0000i" (dictionary)
     ├── "cls"	 (array)
     │    └── wrapper
     │  	├── numpy array containing the detected object's class; 		(numpy array)
     │  	└── type of variable that the numpy array contains;			(dtype)
     │
     ├── "conf"	 (array)
     │    └── wrapper
     │  	├── numpy array containing the detected object's confudence level;	(numpy array)
     │  	└── type of variable that the numpy array contains;			(dtype)
     │
     ├── "id"	(array)
     │    └── wrapper
     │  	├── numpy array containing the detected object's ids;			(numpy array)
     │  	└── type of variable that the numpy array contains;			(dtype)
     │
     ├── "id"	(array)
     │    └── wrapper
     │  	├── numpy array containing the detected object's ids;			(numpy array)
     │  	└── type of variable that the numpy array contains;			(dtype)
     │
     ├── "data"(array)
     │    └── wrapper
     │  	├── numpy array containing the raw tensor with detection boxes and associated data;	(numpy array)
     │  	└── type of variable that the numpy array contains;					(dtype)
     ├── "is_track" (array)
     │    └── wrapper
     │  	├── numpy array containing a 1 if tracking is on and 0 if else;				(numpy array)
     │  	└── type of variable that the numpy array contains;					(dtype)
     │
     ├── "orig_shape"	(array)
     │    └── wrapper
     │  	├── numpy array containing an array containing the original image shape;		(numpy array)
     │  	└── type of variable that the numpy array contains;					(dtype)
     │
     ├── "xywh"	(array)
     │    └── wrapper
     │  	├── numpy array containing a vector for each detected object with the center point's coordenates and the width and hight of the respective rectangle;		(numpy array)
     │  	└── type of variable that the numpy array contains;														(dtype)
     │
     ├── "xywhn"	(array)
     │    └── wrapper
     │  	├── numpy array containing a vector for each detected object with the center point's coordenates and the width and hight of the respective rectangle normalized;(numpy array)
     │  	└── type of variable that the numpy array contains;														(dtype)
     │
     ├── "xyxy"	(array)
     │    └── wrapper
     │  	├── numpy array containing a vector for each detected object with the top left corner's coordenate and bottom right corner's coordenate;			(numpy array)
     │  	└── type of variable that the numpy array contains;														(dtype)
     │
     └── "xyxyn" (array)
          └── wrapper
        	├── numpy array containing a vector for each detected object with the top left corner's coordenate and bottom right corner's coordenate normalized;		(numpy array)
        	└── type of variable that the numpy array contains;														(dtype)
'''
