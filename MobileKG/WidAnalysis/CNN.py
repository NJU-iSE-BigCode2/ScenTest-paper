#import keras
from tensorflow.keras.models import Model, load_model
import numpy as np
import cv2


class CNN:
    def __init__(self, is_load=True):
        self.data = None
        self.model = None
        self.image_shape = (64,64,3)
        self.class_number = None
        self.class_map = None
        self.model_path = None
        if is_load:
            self.load()

    def load(self):
        self.model_path = '../WidAnalysis/vgg16.h5'
        self.class_map = ['Button', 'CheckBox', 'CheckedTextView', 'EditText', 'ImageButton', 'ImageView',
                           'NumberPicker','ProgressBar','ProgressBarHorizontal','ProgressBarVertical',
                          'RadioButton', 'RatingBar', 'SeekBar', 'Switch','Spinner','TextView','ToggleButton']
        self.image_shape = (64, 64, 3)
        self.class_number = len(self.class_map)
        self.model = load_model(self.model_path)
        print('Model Loaded From', self.model_path)

    def preprocess_img(self, image):
        image = cv2.resize(image, self.image_shape[:2])
        x = (image / 255).astype('float32')
        x = np.array([x])
        return x

    def predict(self, imgs, load=True):
        if load:
            self.load()
        if self.model is None:
            print("*** No model loaded ***")
            return
        X = self.preprocess_img(imgs)
        Y = self.class_map[np.argmax(self.model.predict(X))]
        return Y
