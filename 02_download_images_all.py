import pandas as pd
import numpy as np
import requests
from PIL import Image
import io
import time
from concurrent.futures import ProcessPoolExecutor
from concurrent.futures import ThreadPoolExecutor
import concurrent.futures
import json
import argparse


def si_iiif_url(ids_id, region='full', size='500,', rotation='0', 
                     quality='default', format='jpg'):
    SI_ENDPOINT = 'https://ids.si.edu/ids/iiif'
    si_url = f"{SI_ENDPOINT}/{ids_id}/{region}/{size}/{rotation}/{quality}.{format}"
    return si_url

def requests_PIL_download(id_tuple):
    edan_id, ids_id = id_tuple
    width, height = np.nan, np.nan
    image_url = si_iiif_url(ids_id)
    filename = '../data/images/{}.jpg'.format(edan_id)

    try:
        r = requests.get(image_url, timeout=20)
        if r.headers['Content-Type'] == 'image/jpeg':
            try:
                with Image.open(io.BytesIO(r.content)) as im:
                    width, height = im.size
                    im.save(filename)
            except:
                print('Weird error with ' + edan_id)
    except:
        print('Timeout error with ' + edan_id)
    return {'width': width, 'height': height, 'edan_id': edan_id, 'ids_id': ids_id}


ap = argparse.ArgumentParser()
ap.add_argument('-j', "--edan_json", required=True,
                help="file path containing EDAN metadata JSON")
ap.add_argument("-p", "--processes",
                help="number of processes")
ap.add_argument("-d", "--dim-file",
                help="file path for dimension tsv output")
args = ap.parse_args()

record_ids = []
with open(args.edan_json, 'r') as record_file:
    edan_json = json.load(record_file)
    for record in edan_json:
        if 'online_media' in record['content']['descriptiveNonRepeating']:
            edan_id = record['content']['descriptiveNonRepeating']['record_ID']
            ids_id = record['content']['descriptiveNonRepeating']['online_media']['media'][0]['idsId']
        record_ids.append((edan_id, ids_id))

start_time = time.perf_counter()

dimension_list = []

with ProcessPoolExecutor(max_workers=int(args.processes)) as executor:
    dimension_list = list(executor.map(requests_PIL_download, record_ids))

end_time = time.perf_counter()
elapsed_time = end_time - start_time
print(f"Downloaded {len(record_ids)} images in {elapsed_time} s")

dimension_df = pd.DataFrame(dimension_list)
dimension_df.to_csv(args.dim_file, index=False, sep='\t')

