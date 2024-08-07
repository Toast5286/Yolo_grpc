import io
from scipy.io import savemat, loadmat
import cv2  #install opencv-python and opencv-contrib-python
import generic_box_pb2
import numpy as np
import os

from PIL import Image
import matplotlib.pyplot as plt
import matplotlib.patches as patches

YOLO_CONFIG_DIR = ""

#----YOLO_Predict---------------------------------

def predict(datafile,model):
    # Read data from mat file
    dados = loadmat(io.BytesIO(datafile)) 
    img = dados['im']
    frameNum = dados['frame']

    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) 

    #process yolo
    yoloResults = YOLOPredict(img,model)

    DataMat = saveResultsToMat(yoloResults,frameNum)

    return generic_box_pb2.Data(file=DataMat)

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
    frameNum = dados['frame']

    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) 

    #process yolo
    yoloResults = YOLOTrack(img,model)
    
    DataMat = saveResultsToMat(yoloResults,frameNum)

    return generic_box_pb2.Data(file=DataMat)


def YOLOTrack(img,model):

    image = cv2.resize(img,(640,369))
    # Run YOLOv8 tracking on the frame, persisting tracks between frames
    results = model.track(image, persist=True)

    return results

#----YOLO_Plot---------------------------------

def plot(im,data,model):

    # Read data from mat file
    imdata = loadmat(io.BytesIO(im)) 
    img = imdata['im']
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = cv2.resize(img,(640,369))
    PickleData = loadmat(io.BytesIO(data)) 

    dados = PickleData[list(PickleData)[-1]]

    if dados['cls'][0][0][0] == 'no detections':
        # Save the numpy array to a .mat file
        imgMatFile = saveBinaryMat({'im': img})

        return generic_box_pb2.Data(file = imgMatFile)

    # Extract relevant data from the dictionary
    xyxy = dados['xyxy'][0][0]  # Bounding boxes in (x1, y1, x2, y2) format
    conf = dados['conf'][0][0][0]  # Confidence scores
    cls = dados['cls'][0][0][0]     # Class indices (assumed to be integer class indices)
    ids = dados['id'][0][0][0]

    # Define class names (update this list according to your dataset)
    class_names = model.names  # Replace with actual class names if available


    # Display the image
    fig, ax = plt.subplots(1)
    ax.imshow(img)


    for i, box in enumerate(xyxy):

        x1, y1, x2, y2 = box
        width = x2 - x1
        height = y2 - y1
        rect = patches.Rectangle((x1, y1), width, height, linewidth=1, edgecolor='r', facecolor='none')
        ax.add_patch(rect)
        
        # Label with class and confidence
        label = f"{class_names[int(cls[i])]}: {conf[i]:.2f}"
        if not ids=='None':
           label+=f", ID: {int(ids[i])}"
        plt.text(x1, y1 - 10, label, color='white', fontsize=8, bbox=dict(facecolor='red', alpha=0.5))

    plt.axis('off')

    # Save the plot to a BytesIO object
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight', pad_inches=0)
    buf.seek(0)

    # Convert the plot to a numpy array
    buf_image = Image.open(buf)
    buf_array = np.array(buf_image)

    # Save the numpy array to a .mat file
    imgMatFile = saveBinaryMat({'im': buf_array})

    # Close the plot
    plt.close(fig)


    return generic_box_pb2.Data(file = imgMatFile)


#----Save Results To Mat---------------------------------

def saveResultsToMat(results,franeNum):

    dataDic={}
    for result in results:
        
        #Make sure there was something detected
        if len(result.boxes.cls.cpu().numpy())<1:
            dataDic['cls'] = np.array([[['no detections']]])
            break

        dataDic['cls'] = np.array(result.boxes.cls.cpu().numpy())
        dataDic['conf'] = np.array(result.boxes.conf.cpu().numpy())
        dataDic['data'] = np.array(result.boxes.data.cpu().numpy())

        #In the case of Predict, the id is None
        if result.boxes.id != None:
            dataDic['id'] = result.boxes.id.numpy()
        else:
            dataDic['id'] = ['None']

        dataDic['is_track'] = result.boxes.is_track
        dataDic['orig_shape'] = result.boxes.orig_shape
        dataDic['xywh'] = np.array(result.boxes.xywh.cpu().numpy())
        dataDic['xywhn'] = np.array(result.boxes.xywhn.cpu().numpy())
        dataDic['xyxy'] = np.array(result.boxes.xyxy.cpu().numpy())
        dataDic['xyxyn'] = np.array(result.boxes.xyxyn.cpu().numpy())

    print(dataDic)

    MatDic={'frame_'+ f'{int(franeNum):05d}':dataDic}
    return saveBinaryMat(MatDic)


def saveBinaryMat(dic):
    #save mat file and open it as binary
    savemat(str(list(dic)[-1])+"data.mat",dic,long_field_names=True)
    with open(str(list(dic)[-1])+"data.mat", 'rb') as fp:
        bytesData = fp.read()
    os.remove(str(list(dic)[-1])+"data.mat")

    return bytesData
