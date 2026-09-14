import tensorflow as tf

# Load trained CNN
base_model = tf.keras.models.load_model("models/closetcoach_cnn.h5")

# Create embedding model by extracting the second-to-last layer output
# This gives us the 128-dim dense layer before the classification softmax
embedding_model = tf.keras.Model(
    inputs=base_model.input,
    outputs=base_model.layers[-2].output
)

# Save embedding model
embedding_model.save("models/embedding_model.h5")

print("✅ Embedding model created and saved successfully")
