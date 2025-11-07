# 🏥 Assistant Pharmacien Sénégal

Application web intelligente pour conseiller les clients sur les produits cosmétiques et localiser les pharmacies au Sénégal.

## ✨ Fonctionnalités

### 💬 Chat Intelligent
- Diagnostic des problèmes de peau
- Recommandations personnalisées selon l'âge et le type de peau
- Conseils d'utilisation des produits

### 🛍️ Catalogue Produits
- **60+ produits cosmétiques** adaptés au marché sénégalais
- Focus sur les ingrédients africains (karité, baobab, aloe vera)
- Gamme de prix en FCFA (2000 - 35000)
- Filtres par type de peau et problème

### 📍 Géolocalisation
- **100+ pharmacies** au Sénégal
- **17 pharmacies ouvertes 24h/24**
- Calcul de distance en temps réel
- Informations de contact et horaires

### 📊 Analytics
- Statistiques des produits
- Graphiques interactifs
- Analyse des tendances

## 🚀 Démarrage Rapide

### Installation
```bash
pip install streamlit pandas plotly
```

### Lancement
```bash
# Méthode automatique
python run_streamlit.py

# OU méthode manuelle
streamlit run app_streamlit.py
```

L'application sera accessible sur **http://localhost:8501**

### Version Chat Alternative
```bash
python app_chat.py
```
Accessible sur **http://localhost:8000**

## 📦 Structure du Projet

```
Apppharmacie/
├── app_streamlit.py          # Application Streamlit principale
├── app_chat.py               # Version chat conversationnel
├── run_streamlit.py          # Script de lancement
├── start.py                  # Démarrage automatique
├── data_init.py              # Initialisation base de données
├── pharmacy_assistant.db     # Base de données SQLite
├── requirements.txt          # Dépendances Python
├── .streamlit/
│   └── config.toml          # Configuration Streamlit
├── templates/
│   └── index_chat.html      # Template chat
├── static/
│   └── script_chat.js       # JavaScript chat
└── models/
    └── database.py          # Modèles de données
```

## 🌐 Déploiement sur Streamlit Cloud

1. Poussez votre code sur GitHub
2. Allez sur https://streamlit.io/cloud
3. Connectez votre repository
4. Sélectionnez `app_streamlit.py` comme fichier principal
5. Déployez !

L'application se redéploie automatiquement à chaque push.

## 📊 Base de Données

### Produits
- **60+ produits cosmétiques**
- Marques : La Roche-Posay, Vichy, CeraVe, Fair & White, etc.
- Ingrédients africains : Beurre de karité, huile de baobab, aloe vera
- Prix adaptés au marché sénégalais

### Pharmacies
- **100+ pharmacies** géolocalisées
- Couverture complète de Dakar et principales villes
- **17 pharmacies 24h/24** pour les urgences
- Informations de contact et services

## 🛠️ Technologies

- **Frontend** : Streamlit, HTML/CSS/JavaScript
- **Backend** : Python, Flask
- **Base de données** : SQLite
- **Visualisation** : Plotly
- **Géolocalisation** : Geopy

## 📝 Guide d'Utilisation

### Pour les Clients
1. Décrivez votre problème de peau dans le chat
2. Renseignez votre profil (âge, type de peau)
3. Recevez des recommandations personnalisées
4. Localisez les pharmacies les plus proches

### Pour les Pharmaciens
1. Consultez le catalogue complet
2. Filtrez par type de peau ou problème
3. Accédez aux informations détaillées des produits
4. Visualisez les statistiques et tendances

## 🔧 Configuration

### Variables d'Environnement
Aucune configuration requise pour l'utilisation locale.

### Base de Données
Pour réinitialiser la base de données :
```bash
python data_init.py
```

## 📱 Versions Disponibles

### Version Streamlit (Recommandée)
- Interface moderne et responsive
- Analytics et graphiques
- Optimisée pour desktop et mobile

### Version Chat
- Interface conversationnelle
- Bulles de chat fluides
- Focus sur l'interaction

## 🤝 Contribution

Ce projet est développé pour améliorer l'accès aux soins cosmétiques au Sénégal.

## 📄 Licence

MIT License

---

**🇸🇳 Fait avec ❤️ pour le Sénégal**
