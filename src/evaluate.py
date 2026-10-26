import numpy as np
import tensorflow as tf
from tensorflow import keras
from sklearn.metrics import classification_report, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns


def evaluate_model(model, test_ds):
    """Évalue le modèle sur le jeu de données de test et affiche la loss et l'accuracy."""
    print("\nÉvaluation du modèle sur le jeu de test")
    results = model.evaluate(test_ds)
    print(f"Test Loss: {results[0]:.4f}")
    print(f"Test Accuracy: {results[1] * 100:.2f}%")
    return results


def generate_classification_metrics(model, test_ds, class_names=None):
    """Génère un rapport détaillé (Precision, Recall, F1-Score) et calcule la matrice de confusion."""
    print("\nGénération du rapport de classification...")
    
    y_true = []
    y_pred_probs = []

    # Extraction des labels réels et des prédictions du modèle
    for images, labels in test_ds:
        preds = model.predict(images, verbose=0)
        y_true.extend(labels.numpy())
        y_pred_probs.extend(preds)

    y_true = np.array(y_true)
    y_pred = np.argmax(np.array(y_pred_probs), axis=1)

    # Rapport de classification
    report = classification_report(y_true, y_pred, target_names=class_names, zero_division=0)
    print("\nRapport de classification")
    print(report)

    # Matrice de confusion
    cm = confusion_matrix(y_true, y_pred)
    return cm, y_true, y_pred


def plot_confusion_matrix(cm, top_n_classes=20):
    """Affiche une matrice de confusion simplifiée sur les N premières classes (pour éviter l'encombrement avec 257 classes)."""
    plt.figure(figsize=(10, 8))
    sns.heatmap(cm[:top_n_classes, :top_n_classes], annot=True, fmt='d', cmap='Blues')
    plt.title(f'Matrice de confusion (Extrait des {top_n_classes} premières classes)')
    plt.xlabel('Classe Pédite')
    plt.ylabel('Classe Réelle')
    plt.show()