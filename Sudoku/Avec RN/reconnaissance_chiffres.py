import os
import numpy as np
import tensorflow as tf
from tensorflow.keras import layers, models
# from tensorflow.keras.preprocessing import image
from tensorflow.keras.preprocessing.image import img_to_array, load_img, ImageDataGenerator

from capture_ecran import *


# -------------------------------- Constante

NOM_MODELE = "modele_dechiffrage.keras"
DIMENSION_IMAGES = (40,40) # La dimension de l'image représentant la case qui sera traitée par le reseau de neurone (pas necessairement la dimension de l'image d'origine)


# -------------------------------- Entrainement du modèle

def entrainer_modele():
    """
    Crée et entraine le modèle à déchiffrer les chiffres à partir des images d'entrainement créée par creer_images_entrainement()

    ATTENTION : Il faut renommer les images avec le numero qu'elles representent (par exemple 8.png) en ne gardant qu'un seul exemplaire de chaque chiffre
                et 0.png pour une case vide.
    """
    """
    donnees = []
    etiquettes = []
    for nom_fichier in sorted(os.listdir(CHEMIN_IMAGES_ENTRAINEMENT)):
        donnees.append(img_to_array(load_img(CHEMIN_IMAGES_ENTRAINEMENT+nom_fichier, target_size = DIMENSION_IMAGES)))
        etiquettes.append(int(nom_fichier.split(".")[0]))

    dataset = tf.data.Dataset.from_tensor_slices((donnees, etiquettes))
    """

    # Créer un générateur pour les données d'entraînement avec augmentation
    generateur_entrainement = ImageDataGenerator(
        rescale=1./255,         # Réduire l'intensité des pixels à l'échelle [0, 1]
        width_shift_range=0.1,  # Translation horizontale aléatoire de l'image dans la plage [-10%, 10%] de la largeur de l'image
        height_shift_range=0.1, # Translation verticale aléatoire de l'image dans la plage [-10%, 10%] de la hauteur de l'image
        fill_mode='nearest'     # Mode de remplissage utilisé pour combler les pixels nouvellement créés
    )

    donnees_entrainement = generateur_entrainement.flow_from_directory(
        CHEMIN_IMAGES_ENTRAINEMENT,        # Chemin ou se trouvent les dossier avec les images
        target_size = DIMENSION_IMAGES,    # Dimension des images
        shuffle = True                     # On mélange
    )

    # Créer le modèle
    model = models.Sequential()
    model.add(layers.Conv2D(32, (3, 3), activation='relu', input_shape=(*DIMENSION_IMAGES, 3)))
    model.add(layers.MaxPooling2D((2, 2)))
    model.add(layers.Conv2D(64, (3, 3), activation='relu'))
    model.add(layers.MaxPooling2D((2, 2)))
    model.add(layers.Conv2D(128, (3, 3), activation='relu'))
    model.add(layers.MaxPooling2D((2, 2)))
    model.add(layers.Flatten())
    model.add(layers.Dense(128, activation='relu'))
    model.add(layers.Dense(10, activation='softmax'))

    # Compiler le modèle
    model.compile(optimizer='adam',loss='categorical_crossentropy',metrics=['accuracy'])

    # Entraîner le modèle
    model.fit(donnees_entrainement, epochs=100, steps_per_epoch = len(donnees_entrainement))

    model.save(f'{NOM_MODELE}')


# ------------------------------- Reconnaissance des chiffres

def reconnaitre_grille(modele):
    """
    Capture la grille, reconnait le chiffre dans chaque case puis renvoie la grille des chiffres.
    """
    liste_images_cases = capturer_images_cases()

    # Chaque image est redimensionnée pour correspondre à l'entrée du reseau de neurone, transformée en numpy array et normalisée (couleurs entre 0 et 1 au lieu de 255)
    liste_images_array = [img_to_array(image.resize(DIMENSION_IMAGES))/255.0 for image in liste_images_cases]

    # On fait les prédictions
    predictions = modele.predict(np.array(liste_images_array))

    # On récupère pour chaque case, la prédiction la meilleure et on présente le résultat sous forme de grille
    grille = np.argmax(predictions,axis=1).reshape((9,9))
    print(grille)
    return grille

if __name__ =="__main__":
    modele = tf.keras.models.load_model(NOM_MODELE)
    reconnaitre_grille(modele)