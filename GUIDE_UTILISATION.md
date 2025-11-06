# Guide d'Utilisation - Assistant Pharmacien Sénégal

## 🎯 Objectif
Cet assistant aide les pharmaciens sénégalais à conseiller leurs clients sur les produits cosmétiques adaptés à leurs problèmes de peau, tout en localisant les pharmacies proches.

## 🚀 Installation et Lancement

### Prérequis
- Python 3.7 ou plus récent
- Connexion internet pour la géolocalisation

### Installation
```bash
# Cloner ou télécharger le projet
cd assistant-pharmacien-senegal

# Installer les dépendances
pip install -r requirements.txt

# Lancer l'application
python run.py
```

### Accès
- Ouvrir un navigateur web
- Aller à l'adresse : `http://localhost:5000`

## 📱 Utilisation de l'Interface

### 1. Diagnostic Cosmétique
- **Décrire le problème** : Saisir les symptômes (ex: "acné sur le visage", "peau très sèche")
- **Type de peau** : Sélectionner parmi normale, sèche, grasse, mixte, sensible
- **Âge** : Indiquer l'âge du patient (optionnel)
- Cliquer sur "Obtenir des Recommandations"

### 2. Localisation des Pharmacies
- Cliquer sur "Utiliser ma Position" pour activer la géolocalisation
- Cocher "Pharmacies ouvertes 24h/24" si nécessaire
- Les pharmacies s'affichent automatiquement avec leur distance

### 3. Résultats
- **Conseils personnalisés** : Recommandations d'hygiène et de soins
- **Produits recommandés** : Liste avec prix, marques et descriptions
- **Pharmacies proches** : Classées par distance avec coordonnées

## 🏥 Pharmacies Incluses

### Dakar
- Pharmacie du Plateau (24h/24)
- Pharmacie Sandaga (24h/24)
- Pharmacie Nationale
- Pharmacie Almadies
- Pharmacie Liberté 6

### Autres Villes
- Thiès, Saint-Louis, Kaolack avec pharmacies locales

## 💊 Produits Cosmétiques

### Marques Disponibles
- La Roche-Posay, Vichy, Eucerin, Avène
- Fair & White, Caro White, Makari
- Nivea, Palmer's, Sebamed

### Types de Produits
- Nettoyants et gels purifiants
- Crèmes hydratantes
- Sérums anti-taches
- Protections solaires
- Laits corporels éclaircissants

## 🔧 Problèmes Courants

### Géolocalisation ne fonctionne pas
- Vérifier les autorisations du navigateur
- Utiliser HTTPS en production
- Saisir manuellement la ville si nécessaire

### Aucun produit trouvé
- Reformuler la description du problème
- Utiliser des termes simples (acné, sèche, taches)
- Vérifier l'orthographe

### Pharmacies non trouvées
- Augmenter le rayon de recherche
- Vérifier la position GPS
- Essayer sans le filtre 24h/24

## 📊 Administration

### Ajouter des Produits
Modifier le fichier `data_init.py` et relancer :
```python
python data_init.py
```

### Ajouter des Pharmacies
Utiliser les coordonnées GPS exactes pour une meilleure précision.

### Base de Données
- Fichier : `pharmacy_assistant.db`
- Sauvegarde automatique des consultations
- Statistiques d'utilisation disponibles

## 🌍 Adaptation Locale

### Monnaie
- Prix en Francs CFA (FCFA)
- Gammes de prix adaptées au marché sénégalais

### Langues
- Interface en français
- Termes médicaux locaux acceptés

### Géographie
- Coordonnées GPS du Sénégal
- Villes principales intégrées

## 📞 Support

Pour toute question ou amélioration :
- Consulter les logs de l'application
- Vérifier la configuration dans `config.py`
- Adapter les données selon les besoins locaux

## 🔒 Sécurité

- Aucune donnée personnelle stockée
- Géolocalisation temporaire uniquement
- Base de données locale sécurisée