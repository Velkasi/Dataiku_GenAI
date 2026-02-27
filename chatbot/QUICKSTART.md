# 🚀 Guide de démarrage rapide

## Étape 1 : Obtenir une clé API Claude

1. Allez sur https://console.anthropic.com/
2. Créez un compte ou connectez-vous
3. Allez dans "API Keys"
4. Créez une nouvelle clé API
5. Copiez la clé (commence par `sk-ant-api03-...`)

## Étape 2 : Configurer le .env

Ouvrez le fichier `chatbot/.env` et ajoutez votre clé API :

```env
# Ajoutez cette ligne (remplacez par votre vraie clé)
ANTHROPIC_API_KEY=sk-ant-api03-votre_cle_ici

# Les autres lignes sont déjà configurées (héritées du projet parent)
DSS_URL=https://dss-ed6dfc0f-8303e211-dku.eu-west-3.app.dataiku.io
DSS_API_KEY=dkuaps-...
DSS_PROJECT_KEY=TEST_WORKFLOW
DSS_SSL_VERIFY=true
```

## Étape 3 : Lancer le chatbot

### Sur Windows (PowerShell) :

```powershell
cd chatbot
.\start.bat
```

### Sur Linux/Mac :

```bash
cd chatbot
chmod +x start.sh
./start.sh
```

### Ou manuellement :

```bash
cd chatbot
../.venv/Scripts/activate  # Windows
source ../.venv/bin/activate  # Linux/Mac
streamlit run app.py
```

## Étape 4 : Utiliser le chatbot

Le navigateur s'ouvre automatiquement sur **http://localhost:8501**

### Premier test :

1. Dans le chat, tapez :
   ```
   Montre-moi les datasets disponibles
   ```

2. Claude va lister :
   - Expanded_data_with_more_features
   - Original_data_with_more_rows
   - healthcare_dataset

3. Ensuite, essayez :
   ```
   Crée un workflow qui copie healthcare_dataset vers un nouveau dataset healthcare_clean
   ```

4. Claude va :
   - Analyser le dataset
   - Proposer une recette Python
   - Demander confirmation
   - Créer le workflow dans DSS

## 🎯 Exemples de requêtes

### Requête simple
```
Copie healthcare_dataset vers un nouveau dataset
```

### Agrégation
```
Agrège healthcare_dataset par patient_id avec la somme des montants
```

### Jointure
```
Joins Original_data et Expanded_data sur la colonne patient_id
```

### Nettoyage
```
Nettoie healthcare_dataset en supprimant les lignes avec des valeurs nulles
```

## 🔧 En cas de problème

### Le navigateur ne s'ouvre pas
→ Ouvrez manuellement : http://localhost:8501

### Erreur "ANTHROPIC_API_KEY non définie"
→ Vérifiez que vous avez bien ajouté la clé dans `.env`

### Erreur de connexion Dataiku
→ Vérifiez que vous êtes dans l'environnement virtuel activé
→ Testez : `python ../scripts/demo.py`

### Le chatbot affiche "Réfléchit..." sans fin
→ Vérifiez votre connexion internet
→ Vérifiez que la clé API Claude est valide

## 📱 Partager avec votre équipe

Pour que vos collègues accèdent au chatbot :

```bash
streamlit run app.py --server.address 0.0.0.0 --server.port 8501
```

Trouvez votre IP locale :
- Windows : `ipconfig`
- Linux/Mac : `ifconfig`

Partagez l'URL : **http://votre-ip:8501**

## 💰 Coûts estimés

Avec Claude 3.5 Sonnet :
- **Input** : $3 / million tokens
- **Output** : $15 / million tokens

Coût typique par workflow :
- Analyse dataset : ~500 tokens input = $0.0015
- Proposition workflow : ~1000 tokens output = $0.015
- **Total** : ~$0.02 par workflow

Pour 100 workflows/mois = **~$2**

## ✅ Checklist de vérification

- [ ] Clé API Claude ajoutée dans `.env`
- [ ] Environnement virtuel activé
- [ ] Streamlit installé (`pip list | grep streamlit`)
- [ ] Connexion Dataiku OK (`python ../scripts/demo.py`)
- [ ] Chatbot lancé et accessible
- [ ] Premier test réussi

## 🎉 C'est prêt !

Vous pouvez maintenant créer des workflows Dataiku en discutant avec Claude !

---

**Besoin d'aide ?** Lisez le `README.md` complet ou demandez à Claude dans le chat.
