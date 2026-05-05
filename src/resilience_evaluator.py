import requests
import pandas as pd
from datasets import load_dataset

API_URL = "http://localhost:8000/predict"

def run_resilience_test(n_samples=50):
    dataset_name = "zionia/phishing-emails" 
    
    print(f"📥 Chargement de {n_samples} exemples depuis {dataset_name}...")
    
    try:
        # On utilise streaming=True pour ne pas tout télécharger
        dataset = load_dataset(dataset_name, split="train", streaming=True)
        samples = list(dataset.take(n_samples))
    except Exception as e:
        print(f"❌ Impossible de charger le dataset : {e}")
        return

    results = []
    for i, item in enumerate(samples):
        # On vérifie si la clé est bien 'text', sinon on s'adapte
        email_content = item.get('text') or item.get('body') or item.get('text_combined')
        
        payload = {
            "subject": "🔍 Test Résilience Externe",
            "body": email_content,
            "sender": "research@huggingface.co"
        }

        try:
            response = requests.post(API_URL, json=payload)
            if response.status_code == 200:
                data = response.json()
                
                results.append({
                    "ID": i,
                    "Verdict": data["verdict"],
                    "Confiance": data["score_confiance"],
                    "IA_Score": data["details"]["score_ia_rapide"], 
                    "SLM_Verdict": data["details"]["analyse_slm"]["verdict"],
                    "Raisons": ", ".join(data["details"]["raisons"][:2])
                })
            else:
                print(f"⚠️ Erreur API sur échantillon {i}: {response.status_code}")
        except Exception as e:
            print(f"🔥 Connexion échouée : {e}")

    if not results:
        print("❌ Aucun résultat généré.")
        return

    # Rapport Final
    df_res = pd.DataFrame(results)
    print("\n=== RAPPORT DE RÉSILIENCE (PHISHING RÉEL) ===")
    print(df_res.to_string(index=False))
    
    detection_rate = (df_res['Verdict'] == 'Phishing').sum() / len(df_res)
    print(f"\n📊 Taux de détection global : {round(detection_rate * 100, 2)}%")

if __name__ == "__main__":
    run_resilience_test()