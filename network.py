import numpy as np
import time
import cv2
import plot


CONFID = 0.5
THRESH = 0.5


class Yolo3:
    def __init__(self):
        pass

    def initialize(self, model_path):
        # Load Yolov3 weights
        weights_path = model_path + "yolov3.weights"
        config_path = model_path + "yolov3.cfg"
        self.net = cv2.dnn.readNetFromDarknet(config_path, weights_path)
        lnames = self.net.getLayerNames()
        self.layer_names = [lnames[layer[0] - 1] for layer in self.net.getUnconnectedOutLayers()]

    def detect_people(self, image, config):
        #print("Start detecting ...")
        (H, W) = image.shape[:2]
        src = np.float32([[config.bl_x, config.bl_y], [config.br_x, config.br_y],
                          [config.tr_x, config.tr_y], [config.tl_x, config.tl_y]])
        dst = np.float32([[0, H], [W, H], [W, 0], [0, 0]])
        p_transform = cv2.getPerspectiveTransform(src, dst)

        blob = cv2.dnn.blobFromImage(image, 1 / 255.0, (416, 416), swapRB=True, crop=False)
        self.net.setInput(blob)
        start = time.time()
        layer_outputs = self.net.forward(self.layer_names)
        end = time.time()
        boxes = []
        confidences = []
        class_ids = []   
    
        for output in layer_outputs:
            for detection in output:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
                # detecting people in the image
                if class_id == 0:

                    if confidence > CONFID:

                        box = detection[0:4] * np.array([W, H, W, H])
                        (cx, cy, width, height) = box.astype("int")

                        x = int(cx - (width / 2))
                        y = int(cy - (height / 2))

                        boxes.append([x, y, int(width), int(height)])
                        confidences.append(float(confidence))
                        class_ids.append(class_id)
        idxs = cv2.dnn.NMSBoxes(boxes, confidences, CONFID, THRESH)
        font = cv2.FONT_HERSHEY_PLAIN
        boxes1 = []
        for i in range(len(boxes)):
            if i in idxs:
                boxes1.append(boxes[i])
                x,y,w,h = boxes[i]

        #print(len(boxes1))
        if len(boxes1) == 0:
            return image

        bottom_points = []
        for box in boxes1:
            pnts = np.array([[[int(box[0] + (box[2] * 0.5)), int(box[1] + box[3])]]], dtype="float32")
            bd_pnt = cv2.perspectiveTransform(pnts, p_transform)[0][0]
            pnt = [int(bd_pnt[0]), int(bd_pnt[1])]
            bottom_points.append(pnt)

        distances_mat = []
        bxs = []

        for i in range(len(bottom_points)):
            for j in range(len(bottom_points)):
                if i != j:
                    p1 = bottom_points[i]
                    p2 = bottom_points[j]
                    dis_w = float((abs(p2[0]-p1[0]) / W) * config.width)
                    dis_h = float((abs(p2[1]-p1[1]) / H) * config.depth)
                    dist = int(np.sqrt(((dis_h)**2) + ((dis_w)**2)))

                    if dist <= 150:
                        closeness = 0
                        distances_mat.append([bottom_points[i], bottom_points[j], closeness])
                        bxs.append([boxes1[i], boxes1[j], closeness])
                    elif dist > 150 and dist <= 180:
                        closeness = 1
                        distances_mat.append([bottom_points[i], bottom_points[j], closeness])
                        bxs.append([boxes1[i], boxes1[j], closeness])
                    else:
                        closeness = 2
                        distances_mat.append([bottom_points[i], bottom_points[j], closeness])
                        bxs.append([boxes1[i], boxes1[j], closeness])

        r = []
        g = []
        y = []

        for i in range(len(distances_mat)):

            if distances_mat[i][2] == 0:
                if (distances_mat[i][0] not in r) and (distances_mat[i][0] not in g) and (distances_mat[i][0] not in y):
                    r.append(distances_mat[i][0])
                if (distances_mat[i][1] not in r) and (distances_mat[i][1] not in g) and (distances_mat[i][1] not in y):
                    r.append(distances_mat[i][1])

        for i in range(len(distances_mat)):

            if distances_mat[i][2] == 1:
                if (distances_mat[i][0] not in r) and (distances_mat[i][0] not in g) and (distances_mat[i][0] not in y):
                    y.append(distances_mat[i][0])
                if (distances_mat[i][1] not in r) and (distances_mat[i][1] not in g) and (distances_mat[i][1] not in y):
                    y.append(distances_mat[i][1])

        for i in range(len(distances_mat)):

            if distances_mat[i][2] == 2:
                if (distances_mat[i][0] not in r) and (distances_mat[i][0] not in g) and (distances_mat[i][0] not in y):
                    g.append(distances_mat[i][0])
                if (distances_mat[i][1] not in r) and (distances_mat[i][1] not in g) and (distances_mat[i][1] not in y):
                    g.append(distances_mat[i][1])

        risk_count = (len(r),len(y),len(g))

        image_copy = np.copy(image)
        
        image = plot.social_distancing_view(image_copy, bxs, boxes1, risk_count)
        #image = plot.detection_view(image_copy, boxes1)
        
        return image

from camera import Camera

if __name__ == '__main__':
    #cam = Camera('example2.mp4')
    cam = Camera(0)
    cam.initialize()
    print(cam)
    frame = cam.get_frame()
    #print(frame)
    cam.close_camera()
    cv2.imshow("frame", frame)
    cv2.waitKey(0)
    net = Yolo3()
    net.initialize("yolo3/")
    print(net)
    image = net.detect_people(frame)
    #print(image)