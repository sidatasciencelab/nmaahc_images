import time
from concurrent.futures import ProcessPoolExecutor
from concurrent.futures import ThreadPoolExecutor
import argparse
from pathlib import Path

from keras.preprocessing.image import img_to_array
from keras.applications import InceptionV3
from keras.applications.inception_v3 import preprocess_input, decode_predictions
from keras_preprocessing.image import load_img

import numpy as np
import pandas as pd

def load_inception():
    model = InceptionV3(include_top=True, weights='imagenet')

    return model

def classify_image(image_tuple):
    model, image_path = image_tuple
    predictions = {'image_id': image_path.stem}
    image = load_img(image_path)
    im = preprocess_input(img_to_array(image.resize((299,299))))
    preds = model.predict(np.expand_dims(im, 0))
    for idx, pred in enumerate(decode_predictions(preds, top=3)[0]):
        wordnet_id, label, confidence = pred
        predictions['label_'+str(idx+1)] = label
        predictions['confidence_'+str(idx+1)] = confidence
    print(predictions)
    return predictions

ap = argparse.ArgumentParser()
ap.add_argument('-i', "--imagedir", required=True,
                help="path for directory containing images")
ap.add_argument("-p", "--processes",
                help="number of processes")
ap.add_argument("-o", "--outfile",
                help="file path for classification tsv output")
args = ap.parse_args()

start_time = time.perf_counter()

model = load_inception()

end_time = time.perf_counter()
elapsed_time = end_time - start_time

print(f"Model load time: {elapsed_time} s")

image_dir = Path(args.imagedir)
tuple_list = [(model,file) for file in image_dir.glob('*.jpg')]

start_time = time.perf_counter()
with ProcessPoolExecutor(max_workers=int(args.processes)) as executor:
    prediction_list = list(executor.map(classify_image, tuple_list[:50]))

end_time = time.perf_counter()
elapsed_time = end_time - start_time
print(f"Prediction time: {elapsed_time} s")

prediction_df = pd.DataFrame(prediction_list)
prediction_df.to_csv(args.outfile, index=False, sep='\t')
