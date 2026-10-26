"""L'architecture de ton réseau. Contient uniquement
 la classe PyTorch ou TensorFlow de ton modèle 
(ex. les couches de convolution, le pooling, le dropout)"""

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras import regularizers
from src.dataset import get_data_augmentation
def create_custom_cnn(num_classes):
    l2_reg = regularizers.l2(1e-4)

    model = keras.Sequential([
        keras.Input(shape=(224, 224, 3)),

        get_data_augmentation(),
        layers.Rescaling(1.0 / 255),

        # Blocs convolutifs sans Dropout interne
        layers.Conv2D(32, (3, 3), padding="same", activation="relu", kernel_regularizer=l2_reg),
        layers.BatchNormalization(),
        layers.MaxPooling2D((2, 2)),

        layers.Conv2D(64, (3, 3), padding="same", activation="relu", kernel_regularizer=l2_reg),
        layers.BatchNormalization(),
        layers.MaxPooling2D((2, 2)),

        layers.Conv2D(128, (3, 3), padding="same", activation="relu", kernel_regularizer=l2_reg),
        layers.BatchNormalization(),
        layers.MaxPooling2D((2, 2)),

        layers.Conv2D(256, (3, 3), padding="same", activation="relu", kernel_regularizer=l2_reg),
        layers.BatchNormalization(),
        layers.MaxPooling2D((2, 2)),

        layers.Conv2D(512, (3, 3), padding="same", activation="relu", kernel_regularizer=l2_reg),
        layers.BatchNormalization(),
        layers.MaxPooling2D((2, 2)),

        # Classification
        layers.GlobalAveragePooling2D(),
        layers.Dense(512, activation="relu", kernel_regularizer=l2_reg),
        layers.Dropout(0.5),
        layers.Dense(num_classes, activation="softmax")
    ])

    model.compile(
        optimizer=keras.optimizers.Adam(learning_rate=0.001),
        loss="sparse_categorical_crossentropy",
        metrics=["accuracy"]
    )

    return model


def creat_resnet50(pretrained=False):...

def creat_mobilenetv2(pretrained=False): ...