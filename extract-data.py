import os
from docx import Document

chapitres_folder = './chapitres/'

# Liste pour stocker les chapitres
chapitres = []

# Charger les chapitres depuis les fichiers DOCX
for filename in os.listdir(chapitres_folder):
    if filename.endswith('.docx'):
        doc_path = os.path.join(chapitres_folder, filename)
        doc = Document(doc_path)

        # Extraire le texte de chaque paragraphe dans le document
        chapitre_texte = '\n'.join([paragraph.text for paragraph in doc.paragraphs])
        chapitres.append(chapitre_texte)

# Concaténer tous les chapitres en un seul texte
corpus = '\n'.join(chapitres)

# Écriture du corpus dans un fichier texte unique
with open('./chapitres/training-data.txt', 'w', encoding='utf-8') as file:
    file.write(corpus)
