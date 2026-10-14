"""La logique d'entraînement. Contient la boucle for epoch in range(...) 
avec le calcul de la perte et la mise à jour des poids."""

import os
import json
import tensorflow as tf
from tensorflow import keras

from src.dataset import load_dataset
from src.model import create_custom_cnn


# Reproductibilité
SEED = 42
keras.utils.set_random_seed(SEED)

# Paramètres
EPOCHS = 40
MODEL_DIR = "models"
MODEL_PATH = os.path.join(MODEL_DIR, "custom_cnn.keras")
CLASSES_PATH = os.path.join(MODEL_DIR, "class_names.json")


def train_model(model, train_ds, val_ds, class_names,):
    os.makedirs(MODEL_DIR, exist_ok=True)

    # Chargement des données
    train_ds, val_ds, class_names = load_dataset()
    num_classes = len(class_names)

    # Callbacks , pour arreter l'entraînement si la validation ne s'améliore pas
    callbacks = [
        keras.callbacks.ModelCheckpoint(
            filepath=MODEL_PATH,
            monitor="val_loss",
            save_best_only=True,
            verbose=1
        ),
        keras.callbacks.EarlyStopping(
            monitor="val_loss",
            patience=7,
            restore_best_weights=True,
            verbose=1
        ),
        keras.callbacks.ReduceLROnPlateau(
            monitor="val_loss",
            factor=0.5,
            patience=3,
            min_lr=1e-6,
            verbose=1
        )
    ]

    # Entraînement
    history = model.fit(
        train_ds,
        validation_data=val_ds,
        epochs=EPOCHS,
        callbacks=callbacks
    )

    # Sauvegarde des noms de classes
    with open(CLASSES_PATH, "w", encoding="utf-8") as f:
        json.dump(class_names, f, ensure_ascii=False, indent=2)

    print(f"Meilleur modèle sauvegardé dans : {MODEL_PATH}")
    print(f"Noms des classes sauvegardés dans : {CLASSES_PATH}")

    return history
