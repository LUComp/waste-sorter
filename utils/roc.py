from detection.process_image import process_image

def random_object_crop(img, model):

    (x, y), width, height = process_image(img, model)

    