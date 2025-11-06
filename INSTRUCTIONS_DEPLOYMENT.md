# 🚀 Instructions de Déploiement - Streamlit Cloud

## 📋 **Étapes Détaillées**

### **1. Préparer votre Repository GitHub**

Assurez-vous que ces fichiers sont dans votre repository :
```
https://github.com/momosadialiou221/Apppharmacie.git
├── app_streamlit.py          # ✅ Application principale
├── requirements.txt          # ✅ Dépendances Streamlit
├── pharmacy_assistant.db     # ✅ Base de données
├── data_init.py             # ✅ Initialisation données
├── .streamlit/
│   └── config.toml          # ✅ Configuration
└── README.md                # ✅ Documentation
```

### **2. Déploiement sur Streamlit Cloud**

#### **A. Accéder à Streamlit Cloud**
1. Allez sur : https://streamlit.io/cloud
2. Cliquez sur **"Sign up"** ou **"Sign in"**
3. Connectez-vous avec votre compte GitHub

#### **B. Créer une nouvelle app**
1. Cliquez sur **"New app"**
2. Sélectionnez votre repository : `momosadialiou221/Apppharmacie`
3. **Branch :** `main` (ou `master`)
4. **Main file path :** `app_streamlit.py`
5. Cliquez sur **"Deploy!"**

#### **C. Configuration automatique**
Streamlit Cloud va automatiquement :
- ✅ Installer les dépendances depuis `requirements.txt`
- ✅ Lancer l'application `app_streamlit.py`
- ✅ Générer une URL publique
- ✅ Configurer HTTPS automatiquement

### **3. URL de votre Application**

Après déploiement, votre app sera disponible à :
```
https://apppharmacie-[hash].streamlit.app
```

### **4. Commandes Git pour Pousser les Fichiers**

```bash
# Ajouter tous les nouveaux fichiers
git add .

# Commit avec message descriptif
git commit -m "🚀 Déploiement Streamlit - Assistant Pharmacien IA"

# Pousser vers GitHub
git push origin main
```

### **5. Mise à Jour de l'Application**

Pour mettre à jour votre app déployée :
1. Modifiez vos fichiers localement
2. Committez et poussez vers GitHub
3. Streamlit Cloud redéploie automatiquement

## 🎯 **Alternative : Déploiement Local**

Si vous voulez tester localement d'abord :

```bash
# Installer Streamlit
pip install streamlit pandas plotly

# Lancer l'application
streamlit run app_streamlit.py

# Ou utiliser le script automatique
python deploy_streamlit.py
```

## 🔧 **Résolution de Problèmes**

### **Erreur de dépendances**
- Vérifiez que `requirements.txt` contient toutes les dépendances
- Utilisez des versions compatibles

### **Erreur de base de données**
- Assurez-vous que `pharmacy_assistant.db` est dans le repository
- Lancez `python data_init.py` pour recréer la base

### **Erreur de configuration**
- Vérifiez que `.streamlit/config.toml` existe
- Utilisez la configuration fournie

## 📊 **Monitoring**

Une fois déployé, vous pouvez :
- ✅ Voir les logs en temps réel
- ✅ Monitorer l'utilisation
- ✅ Redéployer automatiquement
- ✅ Configurer des domaines personnalisés

## 🌟 **Avantages Streamlit Cloud**

- 🆓 **Gratuit** pour les projets publics
- 🚀 **Déploiement instantané** depuis GitHub
- 🔄 **Mise à jour automatique** à chaque push
- 📊 **Analytics intégrés**
- 🔒 **HTTPS automatique**
- 🌍 **CDN global** pour performance

---

**🎉 Votre Assistant Pharmacien Sénégal sera accessible dans le monde entier !**