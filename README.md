# Yolo_grpc

A box with some yolo functions for GRPC.

## YOLO functions

All YOLO functions are stored in the "YoloService.py" file. It contains 3 main functions. 

**predict**:
Used to run the model.predict() function from ultralytics. It expects to receive a datafile variable that is a binary .mat file (containing the image to be analyzed) and a model (based on the ultralytics models). It outputs a pickle file containing a list of ultralytics' BaseTensor.

**track**:
Used to run the model.track() function from ultralytics. It expects to receive a datafile variable that is a binary .mat file (containing the frame to be analyzed) and a model (based on the ultralytics models). This version doesn't let the user change the type of tracker, so it uses the ByteTrack tracker as default. It outputs a pickle file containing a list of ultralytics' BaseTensor.

**plot**:
Used to plot the predict and the track function's output. It expects to receive a datafile variable that is a pickle file (containing a list of ultralytics' BaseTensor). It outputs a .mat file containing the plotted image.

**matFile**:
Not developed yet. Transcribes the list of ultralytics' BaseTensor in to a readable .mat file.

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
