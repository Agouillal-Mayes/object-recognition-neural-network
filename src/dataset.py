import os
import kagglehub
from tensorflow import keras
import tensorflow as tf
from keras import layers




IMG_SIZE = (224, 224)
BATCH_SIZE = 32
SEED = 42


def load_dataset():
    """
    Télécharge Caltech-256 et charge les images
    pour l'entraînement et la validation.
    """
    dataset_path = kagglehub.dataset_download(
        "jessicali9530/caltech256"
    )

    data_dir = os.path.join(
        dataset_path, "256_ObjectCategories"
    )

    if not os.path.isdir(data_dir):
        raise FileNotFoundError(
            f"Dossier introuvable : {data_dir}"
        )

    train_ds = keras.utils.image_dataset_from_directory(
        data_dir,
        validation_split=0.2,
        subset="training",
        seed=SEED,
        image_size=IMG_SIZE,
        batch_size=BATCH_SIZE,
        label_mode="int",
    )

    val_ds = keras.utils.image_dataset_from_directory(
        data_dir,
        validation_split=0.2,
        subset="validation",
        seed=SEED,
        image_size=IMG_SIZE,
        batch_size=BATCH_SIZE,
        label_mode="int",
    )

    class_names = train_ds.class_names

    train_ds = train_ds.prefetch(
        buffer_size=tf.data.AUTOTUNE
    )
    val_ds = val_ds.prefetch(
        buffer_size=tf.data.AUTOTUNE
    )

    return train_ds, val_ds, class_names


def get_data_augmentation():
    """Définit la pipeline d'augmentation pour le dataset d'entraînement."""
    return keras.Sequential([
    keras.layers.RandomRotation(0.08),
    keras.layers.RandomZoom(0.1),
    keras.layers.RandomTranslation(0.1, 0.1),
    ], name="data_augmentation")


def clean_class_name(class_name):
    """Retire le préfixe numérique du nom de la classe."""
    return (
        class_name.split(".", 1)[1]
        if "." in class_name
        else class_name
    )
