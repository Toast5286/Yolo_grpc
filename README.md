# Yolo_grpc

A grpc-pipeline element designed to run some yolo functions. This element was designed to be part of a pipeline, therefore does not have any UI. Can be tested using the "test_generic_box.ipynb" file.

## YOLO functions

All YOLO functions are stored in the "YoloService.py" file. It contains 3 main functions. 

The resulting output file from predict and track have the same atributes as results class from ultralytic. More details here: https://docs.ultralytics.com/reference/engine/results/#ultralytics.engine.results.Results

**predict**:
Used to run the model.predict() function from ultralytics. It expects to receive a datafile variable that is a binary .mat file (containing the image to be analyzed) and a model (based on the ultralytics models). It outputs a .mat file containing the class index, the confidence levels, data, ids, 'is_track', image shape, xywh, xyxy and there normalized variants.
It's input file must have the following structure:

```
input.mat (dictionary)
  ├── ”im” - numpy array containing the saved image/frame;
  └── ”frame” – number of the frame of uploaded image image (0 in case of a single image). If this information is not defined, default will be 0;
```

It's output file has the following structure:

```
fileName.mat 	 (dictionary)
   ├── "cls"	 (array)
   │    └── wrapper
   │  	      ├── numpy array containing the detected object's class; (numpy array)
   │           │   (if none where detected, shows -1)
   │  	      └── type of variable that the numpy array contains; (dtype)
   │
   ├── "conf"	 (array)
   │    └── wrapper
   │  	      ├── numpy array containing the detected object's confudence level; (numpy array)
   │  	      └── type of variable that the numpy array contains; (dtype)
   │
   ├── "id"	(array)
   │    └── wrapper
   │  	      ├── numpy array containing the detected object's ids; (numpy array)
   │  	      └── type of variable that the numpy array contains; (dtype)
   │
   ├── "data"(array)
   │    └── wrapper
   │  	      ├── numpy array containing the raw tensor with detection boxes and associated data; (numpy array)
   │  	      └── type of variable that the numpy array contains; (dtype)
   ├── "is_track" (array)
   │    └── wrapper
   │  	      ├── numpy array containing 0; (numpy array)
   │  	      └── type of variable that the numpy array contains; (dtype)
   │
   ├── "orig_shape"	(array)
   │    └── wrapper
   │  	      ├── numpy array containing an array containing the original image shape; (numpy array)
   │  	      └── type of variable that the numpy array contains; (dtype)
   │
   ├── "xywh"	(array)
   │    └── wrapper
   │  	      ├── numpy array containing a vector for each detected object with the center point's coordenates and the width and hight of the respective rectangle; (numpy array)
   │  	      └── type of variable that the numpy array contains; (dtype)
   │
   ├── "xywhn"	(array)
   │    └── wrapper
   │  	      ├── numpy array containing a vector for each detected object with the center point's coordenates and the width and hight of the respective rectangle normalized; (numpy array)
   │  	      └── type of variable that the numpy array contains; (dtype)
   │
   ├── "xyxy"	(array)
   │    └── wrapper
   │  	      ├── numpy array containing a vector for each detected object with the top left corner's coordenate and bottom right corner's coordenate; (numpy array)
   │  	      └── type of variable that the numpy array contains; (dtype)
   │
   └── "xyxyn" (array)
        └── wrapper
              ├── numpy array containing a vector for each detected object with the top left corner's coordenate and bottom right corner's coordenate normalized; (numpy array)
              └── type of variable that the numpy array contains; (dtype)
```

**track**:
Used to run the model.track() function from ultralytics. It expects to receive a datafile variable that is a binary .mat file (containing the frame to be analyzed) and a model (based on the ultralytics models). This version doesn't let the user change the type of tracker, so it uses the ByteTrack tracker as default. It outputs a .mat file containing the class index, the confidence levels, data, ids, 'is_track', image shape, xywh, xyxy and there normalized variants.
It's input file must have the following structure:

```
input.mat (dictionary)
  ├── ”im” - numpy array containing the saved image/frame;
  └── ”frame” – number of the frame of uploaded image image (0 in case of a single image). If this information is not defined, default will be 0;
```

It's output file has the following structure:

```
fileName.mat 	 (dictionary)
   ├── "cls"	 (array)
   │    └── wrapper
   │  	      ├── numpy array containing the detected object's class; (numpy array)
   │          │   (if none where detected, shows -1)
   │  	      └── type of variable that the numpy array contains; (dtype)
   │
   ├── "conf"	 (array)
   │    └── wrapper
   │  	      ├── numpy array containing the detected object's confudence level; (numpy array)
   │  	      └── type of variable that the numpy array contains; (dtype)
   │
   ├── "id"	(array)
   │    └── wrapper
   │  	      ├── numpy array containing the detected object's ids; (numpy array)
   │  	      └── type of variable that the numpy array contains; (dtype)
   │
   ├── "data"(array)
   │    └── wrapper
   │  	      ├── numpy array containing the raw tensor with detection boxes and associated data;	(numpy array)
   │  	      └── type of variable that the numpy array contains; (dtype)
   ├── "is_track" (array)
   │    └── wrapper
   │  	      ├── numpy array containing a 1 if tracking is on and 0 if else; (numpy array)
   │  	      └── type of variable that the numpy array contains; (dtype)
   │
   ├── "orig_shape"	(array)
   │    └── wrapper
   │  	      ├── numpy array containing an array containing the original image shape; (numpy array)
   │  	      └── type of variable that the numpy array contains; (dtype)
   │
   ├── "xywh"	(array)
   │    └── wrapper
   │  	      ├── numpy array containing a vector for each detected object with the center point's coordenates and the width and hight of the respective rectangle; (numpy array)
   │  	      └── type of variable that the numpy array contains; (dtype)
   │
   ├── "xywhn"	(array)
   │    └── wrapper
   │  	      ├── numpy array containing a vector for each detected object with the center point's coordenates and the width and hight of the respective rectangle normalized; (numpy array)
   │  	      └── type of variable that the numpy array contains; (dtype)
   │
   ├── "xyxy"	(array)
   │    └── wrapper
   │  	      ├── numpy array containing a vector for each detected object with the top left corner's coordenate and bottom right corner's coordenate; (numpy array)
   │  	      └── type of variable that the numpy array contains; (dtype)
   │
   └── "xyxyn" (array)
        └── wrapper
              ├── numpy array containing a vector for each detected object with the top left corner's coordenate and bottom right corner's coordenate normalized; (numpy array)
              └── type of variable that the numpy array contains; (dtype)
```

**plot**:
Used to plot the predict and the track function's output. It expects to receive a .mat file containing the class index, the confidence levels, ids, xyxy (same structure as in track/predict) and another .mat file containing the original image (mandetory) and it's user's session hash (optional). It outputs a .mat file containing the plotted image. If any of these informations are missing, will return the original image.
This function requires 2 input files, one of the outputs from the predict or track method and one with the original image.
The file with the original image must have the following structure:

```
Img_input.mat (dictionary)
  ├── ”im” - numpy array containing the saved image/frame;
  └── "session_hash"
         └── The session hash of the user that requested the image. If none was given, this will be 0.
```

The output file has the following structure:

```
imgMatFile.mat 	 (dictionary)
   ├── "im" (numpy array)
   │    └── The ploted image.
   │
   └── "session_hash"
         └── The session hash of the user that requested the image. If none was given, this will be 0.
```

## Deploy

To deploy this program it needes to compile the GRPC with the folowing command.

To create the Docker image with the program use:

```bash
    docker build -t yolo_grpc --build-arg SERVICE_NAME=generic_box -f docker/Dockerfile .
```

After this, just run the pipeline (Instructions are on the pipeline's repository).

In case you want to test this pipeline element, follow the next instructions.

To run the container run the command:

```bash
    docker run -p 8061:8061 -it --rm yolo_grpc
```

To test this pipeline element, it needs the grpc message types. All the grpc functions are stored in the "generic_box_pb2.py" and "generic_box_pb2_grpc.py". To get these files we run:

```bash
  python -m grpc_tools.protoc --proto_path=./protos --python_out=. --grpc_python_out=. generic_box.proto
```

Afterwards, you can run "test_generic_box.ipynb". The output Yolo data will be stored in a "imback.mat".

