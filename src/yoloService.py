import io
from scipy.io import savemat, loadmat
import cv2  #install opencv-python and opencv-contrib-python
import generic_box_pb2
import numpy as np
import pickle

YOLO_CONFIG_DIR = ""

#----YOLO_Predict---------------------------------

def predict(datafile,model):
    # Read data from mat file
    dados = loadmat(io.BytesIO(datafile)) 
    img = dados['im']

    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) 

    #process yolo
    yoloResults = YOLOPredict(img,model)
    
    bytesData = pickle.dumps(yoloResults)

    return generic_box_pb2.File(data=bytesData)

def YOLOPredict(img,model):

    image = cv2.resize(img,(640,369))
    # Run YOLOv8 tracking on the frame, persisting tracks between frames
    results = model.predict(image)

    return results

#----YOLO_Track---------------------------------

def track(datafile,model):
    # Read data from mat file
    dados = loadmat(io.BytesIO(datafile)) 
    img = dados['im']

    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) 

    #process yolo
    yoloResults = YOLOTrack(img,model)
    
    bytesData = pickle.dumps(yoloResults)

    return generic_box_pb2.File(data=bytesData)


def YOLOTrack(img,model):

    image = cv2.resize(img,(640,369))
    # Run YOLOv8 tracking on the frame, persisting tracks between frames
    results = model.track(image, persist=True)

    return results

#----YOLO_Plot---------------------------------

def plot(results):
    
    yoloResults = pickle.loads(results)
    yoloImg = YOLOImage(yoloResults)

    i=0
    for img in yoloImg:
        tempDic = {'im'+str(i):img}
        i+=1
    imgMatFile = saveBinaryMat(tempDic)


    return generic_box_pb2.File(data = imgMatFile)

def YOLOImage(results):

    annotated_frame=[]

    # Visualize the results on the frame
    for result in results:
        annotated_frame.append(result.plot())


    # Display the annotated frame
    return annotated_frame

def saveBinaryMat(dic):
    #save mat file and open it as binary
    savemat("data.mat",dic,long_field_names=True)
    with open("data.mat", 'rb') as fp:
        bytesData = fp.read()

    return bytesData