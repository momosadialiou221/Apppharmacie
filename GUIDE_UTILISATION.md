# 📖 Guide d'Utilisation - Assistant Pharmacien Sénégal

## 🚀 Démarrage

### Lancement Rapide
```bash
python run_streamlit.py
```
Ouvre automatiquement http://localhost:8501

### Lancement Manuel
```bash
streamlit run app_streamlit.py
```

## 💬 Utiliser le Chat

### Option 1 : 📸 Analyse de Photo (Nouveau !)

#### Comment utiliser l'analyse par IA ?
1. **Prenez une photo** de votre problème de peau
   - Lumière naturelle (près d'une fenêtre)
   - Distance de 15-20 cm
   - Zone nette et bien visible
   - Pas de flash ni de maquillage

2. **Téléchargez la photo** dans l'interface
   - Formats acceptés : JPG, JPEG, PNG
   - Taille recommandée : < 5 MB

3. **L'IA analyse automatiquement** et détecte :
   - 🔴 Acné et rougeurs
   - 💧 Peau sèche
   - 🟤 Taches pigmentaires
   - ✨ État général

4. **Cliquez sur "Obtenir des recommandations"**
   - Produits adaptés instantanément
   - Conseils personnalisés

#### Conseils pour une bonne photo
- ☀️ **Lumière naturelle** : Évitez les éclairages artificiels
- 📏 **Distance optimale** : 15-20 cm de la zone
- 🎯 **Netteté** : Assurez-vous que la photo n'est pas floue
- 🚫 **Pas de filtres** : Photo brute sans retouche
- 🧼 **Peau propre** : Nettoyez avant de photographier

### Option 2 : 💬 Description Textuelle

#### Décrire Votre Problème
Exemples de messages :
- "J'ai des boutons sur le visage depuis 2 semaines"
- "Ma peau est très sèche et tiraille"
- "Des taches brunes sur les joues"
- "Rides autour des yeux"

### Renseigner Votre Profil
Dans la barre latérale :
- **Âge** : Pour des conseils adaptés à votre tranche d'âge
- **Type de peau** : Normale, Sèche, Grasse, Mixte, Sensible
- **Budget maximum** : Filtrer les produits selon votre budget
- **Localisation** : Pour trouver les pharmacies proches

### Recevoir des Recommandations
Le chatbot vous propose :
- Diagnostic du problème (avec ou sans photo)
- Score de confiance pour l'analyse photo
- 3-5 produits recommandés avec prix
- Conseils d'utilisation personnalisés
- Pharmacies les plus proches

## 🛍️ Explorer le Catalogue

### Filtres Disponibles
- **Type de peau** : Tous, Normale, Sèche, Grasse, Mixte, Sensible
- **Problème** : Acné, Sécheresse, Taches, Rides, Sensibilité
- **Prix** : Gamme de prix en FCFA

### Informations Produit
Chaque produit affiche :
- Nom et marque
- Prix en FCFA
- Type de peau adapté
- Problèmes traités
- Ingrédients clés
- Origine africaine (si applicable)

## 🏥 Trouver une Pharmacie

### Recherche par Localisation
1. Cliquez sur "Activer la géolocalisation"
2. Autorisez l'accès à votre position
3. Les pharmacies s'affichent par ordre de distance

### Filtres
- **Ouvert 24h/24** : Pharmacies de garde
- **Ville** : Dakar, Thiès, Saint-Louis, etc.
- **Quartier** : Plateau, Liberté, Almadies, etc.

### Informations Affichées
- Nom de la pharmacie
- Adresse complète
- Téléphone
- Horaires
- Distance (si géolocalisé)
- Ouverture 24h/24

## 📊 Analytics

### Statistiques Disponibles
- Répartition des produits par type de peau
- Distribution des prix
- Produits africains vs importés
- Pharmacies par ville
- Pharmacies 24h/24

### Graphiques Interactifs
- Survolez pour voir les détails
- Cliquez sur la légende pour filtrer
- Zoomez et déplacez les graphiques

## 💡 Conseils d'Utilisation

### Pour de Meilleurs Résultats
1. **Soyez précis** dans la description de votre problème
2. **Mentionnez la durée** des symptômes (depuis quand)
3. **Renseignez votre profil** pour des conseils personnalisés
4. **Activez la géolocalisation** pour trouver les pharmacies proches

### Exemples de Questions
- "Quelle crème pour peau sèche à moins de 10000 FCFA ?"
- "Produit anti-taches avec ingrédients africains"
- "Pharmacie ouverte maintenant à Liberté 6"
- "Routine complète pour peau grasse et acné"

## 🔧 Résolution de Problèmes

### L'application ne démarre pas
```bash
# Vérifier les dépendances
pip install streamlit pandas plotly

# Réinitialiser la base de données
python data_init.py
```

### Erreur de base de données
```bash
# Supprimer et recréer la base
del pharmacy_assistant.db
python data_init.py
```

### Port déjà utilisé
```bash
# Utiliser un autre port
streamlit run app_streamlit.py --server.port 8502
```

## 📱 Version Mobile

L'application est responsive et fonctionne sur :
- Smartphones
- Tablettes
- Desktop

Utilisez le menu hamburger (☰) pour accéder à la navigation sur mobile.

## 🆘 Support

Pour toute question ou problème :
1. Consultez ce guide
2. Vérifiez les messages d'erreur
3. Redémarrez l'application

---

**Bon usage de votre Assistant Pharmacien ! 🏥**
