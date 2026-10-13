"""L'architecture de ton réseau. Contient uniquement
 la classe PyTorch ou TensorFlow de ton modèle 
(ex. les couches de convolution, le pooling, le dropout)"""

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers


def create_custom_cnn(num_classes):
    model = keras.Sequential([
        keras.Input(shape=(224, 224, 3)),

        # Normalisation des pixels entre 0 et 1
        layers.Rescaling(1.0 / 255),

        # Bloc convolutif 1
        layers.Conv2D(32, (3, 3), padding="same",
                      activation="relu"),
        layers.BatchNormalization(),
        layers.MaxPooling2D((2, 2)),

        # Bloc convolutif 2
        layers.Conv2D(64, (3, 3), padding="same",
                      activation="relu"),
        layers.BatchNormalization(),
        layers.MaxPooling2D((2, 2)),

        # Bloc convolutif 3
        layers.Conv2D(128, (3, 3), padding="same",
                      activation="relu"),
        layers.BatchNormalization(),
        layers.MaxPooling2D((2, 2)),

        # Bloc convolutif 4
        layers.Conv2D(256, (3, 3), padding="same",
                      activation="relu"),
        layers.BatchNormalization(),
        layers.MaxPooling2D((2, 2)),

        # Classification
        layers.GlobalAveragePooling2D(),
        layers.Dense(256, activation="relu"),
        layers.Dropout(0.4),
        layers.Dense(num_classes, activation="softmax")
    ])

    model.compile(
        optimizer=keras.optimizers.Adam(
            learning_rate=0.001
        ),
        loss="sparse_categorical_crossentropy",
        metrics=["accuracy"]
    )

    return model


def creat_resnet50(pretrained=False):...

def creat_mobilenetv2(pretrained=False): ...