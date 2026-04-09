import pandas as pd
import os

def clean_data():
    input_file = "../data/raw_mails.csv"
    output_file = "../data/final_dataset.csv"

    print("Chargement des données brutes...")

    df = pd.read_csv(input_file)
    print("Voici les colonnes trouvées dans ton fichier :", list(df.columns))

    colonne_texte = 'text_combined' 
    colonne_label = 'label'
    
    df = df[[colonne_texte, colonne_label]]

    df.columns = ['text', 'label']

    mapping = {'Safe Email': 0, 'Phishing Email': 1, 'ham': 0, 'spam': 1}
    df['label'] = df['label'].replace(mapping)

    df = df.dropna()

    df.to_csv(output_file, index=False)
    print(f"✅ SUCCÈS ! {len(df)} mails ont été nettoyés et sauvegardés dans {output_file}.")

if __name__ == "__main__":
    clean_data()