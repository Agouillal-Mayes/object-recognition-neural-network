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


def create_resnet50(num_classes, pretrained=False):
    """# Charger l'architecture ResNet50
    # weights=None : poids initialisés aléatoirement
    # weights="imagenet" : poids préentraînés sur ImageNet
    weights = "imagenet" if pretrained else None"""

    base_model = keras.applications.ResNet50(
        #weights=weights,
        include_top=False,
        input_shape=(224, 224, 3)
    )

    """ # Pour le transfer learning, geler la base au départ
    base_model.trainable = not pretrained"""

    inputs = keras.Input(shape=(224, 224, 3))
    from src.dataset import get_data_augmentation
    data__augmentation = get_data_augmentation()
    x = data__augmentation(inputs)

    # Prétraitement spécifique à ResNet50
    x = keras.applications.resnet50.preprocess_input(inputs)

    # Extraction des caractéristiques
    x = base_model(x, training=False)

    # Tête de classification adaptée à Caltech-256
    x = layers.GlobalAveragePooling2D()(x)
    x = layers.Dense(256, activation="relu",kernel_regularizer=keras.regularizers.l2(1e-4))(x)
    x = layers.Dropout(0.5)(x)
    outputs = layers.Dense(
        num_classes, activation="softmax"
    )(x)

    model = keras.Model(inputs, outputs)

    model.compile(
        optimizer=keras.optimizers.Adam(learning_rate=1e-4),
        loss="sparse_categorical_crossentropy",
        metrics=["accuracy"]
    )

    return model

def creat_mobilenetv2(pretrained=False): ...