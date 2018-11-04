'''
Takes a image from Image Net and compares the classification result of the original image
and an adversarial example generated for the ResNet50 and Inception v3 models.
Also shows the original image, the filter used to generate the adversarial example
and the adversarial example itself.

Authors: Hojin Kang and Tomas Nunez
'''

import numpy as np
from keras.applications import resnet50
from keras.preprocessing import image
from keras.applications import inception_v3

from load_single_imagenet import single_img
import matplotlib.pyplot as plt
import ssl

from adv_example_generation import fast_gradient, arraytoimage

# Fix SSL Error
ssl._create_default_https_context = ssl._create_unverified_context


# 2 Models used: ResNet and Inception V3
resnet_model = resnet50.ResNet50(weights='imagenet')
inception_model = inception_v3.InceptionV3(weights='imagenet')
n = 124619

# Input size for ResNet = 224*224
img, tag, identifier = single_img(n, 224, 224)

# Input size for Inception V3 = 299*299
imgInception, tag, identifier = single_img(n, 299, 299)

# Preprocessing
x = image.img_to_array(img)
x = np.expand_dims(x, axis=0)
x = resnet50.preprocess_input(x)
xInc = image.img_to_array(imgInception)
xInc = np.expand_dims(xInc, axis=0)
xInc = inception_v3.preprocess_input(xInc)

# Get predictions from both models
pred = resnet_model.predict(x)
predInc = inception_model.predict(xInc)
clase = tag
print('Predicted ResNet:', resnet50.decode_predictions(pred, top=5)[0])
print('Predicted InceptionV3: ', inception_v3.decode_predictions(predInc, top=5)[0])
print('Real: ', clase, ' ', identifier)

# Show original imageimg = Image.fromarray(data, 'RGB')
implot = plt.imshow(img)
plt.show()

# Adversarial examples
print('===== Adversarial Examples ======')

# Generate an adversarial example for the resnet model
xadv, filter = fast_gradient(resnet_model, x, 3)
pred = resnet_model.predict(xadv)

# Show adversarial example filter
filtplot = plt.imshow(filter[0])
plt.show()

# Show adversarial example
adversarial_image = arraytoimage(xadv, (224, 224, 3))
adversarialplot = plt.imshow(adversarial_image)
plt.show()

print('Predicted ResNet:', resnet50.decode_predictions(pred, top=5)[0])
