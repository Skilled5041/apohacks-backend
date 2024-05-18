import os
import tensorflow as tf
assert tf.__version__.startswith('2')
import os
from mediapipe_model_maker import image_classifier
import matplotlib.pyplot as plt


image_path = os.path.join(os.path.dirname(__file__), "../dataset/")
print(image_path)
assert os.path.exists(image_path)
data = image_classifier.Dataset.from_folder(image_path)
train_data, remaining_data = data.split(0.8)
test_data, validation_data = remaining_data.split(0.5)



spec = image_classifier.SupportedModels.EFFICIENTNET_LITE0
hparams = image_classifier.HParams(export_dir="exported_model")
options = image_classifier.ImageClassifierOptions(supported_model=spec, hparams=hparams)

model = image_classifier.ImageClassifier.create(
    train_data = train_data,
    validation_data = validation_data,
    options=options,
)

loss, acc = model.evaluate(test_data)
print(f'Test loss:{loss}, Test accuracy:{acc}')

model.export_model()

