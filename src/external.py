import io
from scipy.io import savemat, loadmat
import cv2  #install opencv-python and opencv-contrib-python
import generic_box_pb2
import numpy as np
import pickle

YOLO_CONFIG_DIR = ""

def calling_function(datafile,model):
    # Read data from mat file
    dados = loadmat(io.BytesIO(datafile)) 
    img = dados['im']

    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) 

    #process yolo
    yoloResults = YOLOProcessing(img,model)
    
    bytesData = pickle.dumps(yoloResults)

    return generic_box_pb2.Data(file=bytesData)


def YOLOProcessing(img,model):

    image = cv2.resize(img,(640,369))
    # Run YOLOv8 tracking on the frame, persisting tracks between frames
    results = model.track(image, persist=True)

    return results