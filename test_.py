from htr_svea.models.openmmlab_models import OpenmmlabModel
from htr_svea.inferencer.mmdet_inferencer import MMDetInferencer
from htr_svea.utils.helper import timing_decorator
import mmcv

from glob import glob
import os

@timing_decorator
def predict_batch(inferencer, images):
    result = inferencer.predict(images, batch_size=8)
    return result

if __name__ == "__main__":
    region_model = OpenmmlabModel.from_pretrained("Riksarkivet/rtmdet_regions", cache_dir="./config")

    print(region_model)

    #try with region_inferencer instead (type=region till mmdetinferencer)

    inferencer = MMDetInferencer(region_model=region_model)

    imgs = glob(os.path.join('/media/erik/Elements/Riksarkivet/data/datasets/htr/Trolldomskommissionen3/Kommissorialrätt_i_Stockholm_ang_trolldomsväsendet,_nr_4_(1676)', '**', 'bin_image', '*'), recursive=True)
    imgs_numpy = list()
    
    for img in imgs[0:8]:
        imgs_numpy.append(mmcv.imread(img))
    
    result = inferencer.predict(imgs_numpy, batch_size=8)

    for res, img in zip(result, imgs_numpy):
        res.segmentation.remove_overlapping_masks()
        res.segmentation.align_masks_with_image(img)
    
    #print(result[-1].img_shape)
    #print(result['predictions'][0].pred_instances.metadata_fields)
    #print(result['predictions'][0]._metainfo_fields)
    #print(result.keys())
    #print(result)    

    from PIL import Image

    # load image from the IAM database
    #image = Image.open("./image_0.png").convert("RGB")

    # Use a pipeline as a high-level helper
    #from transformers import pipeline

    #pipe = pipeline("image-to-text", model="microsoft/trocr-large-handwritten")
    #print(pipe(image, batch_size=8))
