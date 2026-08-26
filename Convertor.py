import tensorflowjs as tfjs
from tensorflow.keras.models import load_model

# 1. Load your .h5 model
model = load_model("lungmodel.h5")

# 2. Convert and save as TensorFlow.js model
tfjs.converters.save_keras_model(model, "model")

print("✅ Conversion complete: model saved to ./model folder")
