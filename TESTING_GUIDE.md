# 🧪 Guide de Test - Analyse de Photos par IA

## 🎯 Objectif des Tests

Vérifier que la fonctionnalité d'analyse de photos fonctionne correctement dans tous les scénarios d'utilisation.

## ✅ Checklist de Tests

### Tests Fonctionnels

#### ✓ Test 1 : Upload d'Image JPG
**Objectif** : Vérifier que les images JPG sont acceptées

**Étapes** :
1. Ouvrir http://localhost:8501
2. Aller dans l'onglet "💬 Chat Assistant"
3. Cliquer sur "Browse files"
4. Sélectionner une image JPG
5. Vérifier que l'image s'affiche

**Résultat attendu** :
- ✅ Image affichée dans la colonne gauche
- ✅ Analyse démarre automatiquement
- ✅ Pas d'erreur affichée

---

#### ✓ Test 2 : Upload d'Image PNG
**Objectif** : Vérifier que les images PNG sont acceptées

**Étapes** :
1. Sélectionner une image PNG
2. Vérifier l'affichage et l'analyse

**Résultat attendu** :
- ✅ Image PNG acceptée et affichée
- ✅ Analyse fonctionne correctement

---

#### ✓ Test 3 : Détection d'Acné
**Objectif** : Vérifier la détection de rougeurs/acné

**Étapes** :
1. Télécharger une photo avec zones rouges
2. Attendre l'analyse
3. Vérifier les résultats

**Résultat attendu** :
- ✅ "Acné détectée" affiché
- ✅ Score de confiance entre 60-95%
- ✅ Bouton "Obtenir recommandations" visible

**Comment créer une image de test** :
```python
# Script Python pour créer une image test acné
from PIL import Image
import numpy as np

# Créer une image avec dominante rouge
img = np.zeros((300, 300, 3), dtype=np.uint8)
img[:, :, 0] = 180  # Rouge élevé
img[:, :, 1] = 140  # Vert moyen
img[:, :, 2] = 130  # Bleu moyen

Image.fromarray(img).save('test_acne.jpg')
```

---

#### ✓ Test 4 : Détection de Peau Sèche
**Objectif** : Vérifier la détection de texture irrégulière

**Étapes** :
1. Télécharger une photo avec texture rugueuse
2. Vérifier la détection

**Résultat attendu** :
- ✅ "Sèche détectée" affiché
- ✅ Score de confiance entre 50-90%

**Image de test** :
```python
# Image avec haute variance (texture)
img = np.random.randint(100, 200, (300, 300, 3), dtype=np.uint8)
Image.fromarray(img).save('test_seche.jpg')
```

---

#### ✓ Test 5 : Détection de Taches
**Objectif** : Vérifier la détection de variations de luminosité

**Étapes** :
1. Télécharger une photo avec zones sombres
2. Vérifier la détection

**Résultat attendu** :
- ✅ "Taches détectées" affiché
- ✅ Score de confiance entre 55-85%

**Image de test** :
```python
# Image avec variations de luminosité
img = np.zeros((300, 300, 3), dtype=np.uint8)
img[:150, :, :] = 100  # Zone sombre
img[150:, :, :] = 180  # Zone claire
# Ajouter du bruit
img += np.random.randint(-30, 30, img.shape, dtype=np.int16)
img = np.clip(img, 0, 255).astype(np.uint8)
Image.fromarray(img).save('test_taches.jpg')
```

---

#### ✓ Test 6 : Peau Normale
**Objectif** : Vérifier le cas où aucun problème n'est détecté

**Étapes** :
1. Télécharger une photo de peau saine
2. Vérifier le message

**Résultat attendu** :
- ✅ "Normale détectée" affiché
- ✅ Message : "Votre peau semble en bonne santé"
- ✅ Pas de bouton de recommandation (ou message différent)

**Image de test** :
```python
# Image uniforme (peau normale)
img = np.full((300, 300, 3), [150, 145, 140], dtype=np.uint8)
Image.fromarray(img).save('test_normale.jpg')
```

---

#### ✓ Test 7 : Génération de Recommandations
**Objectif** : Vérifier le flux complet jusqu'aux recommandations

**Étapes** :
1. Télécharger une photo (ex: acné)
2. Cliquer sur "Obtenir des recommandations"
3. Vérifier le message dans le chat
4. Vérifier les produits recommandés

**Résultat attendu** :
- ✅ Message utilisateur ajouté : "📸 Photo analysée : ..."
- ✅ Réponse assistant avec produits
- ✅ Top 3 produits affichés
- ✅ Conseils personnalisés affichés
- ✅ Prix en FCFA affichés

---

#### ✓ Test 8 : Guide d'Utilisation
**Objectif** : Vérifier l'expander avec conseils

**Étapes** :
1. Cliquer sur "ℹ️ Comment prendre une bonne photo ?"
2. Vérifier le contenu

**Résultat attendu** :
- ✅ Expander s'ouvre/ferme correctement
- ✅ Conseils affichés (lumière, distance, etc.)
- ✅ Liste des détections possibles affichée

---

#### ✓ Test 9 : Nouvelle Conversation
**Objectif** : Vérifier la réinitialisation

**Étapes** :
1. Faire une analyse complète
2. Cliquer sur "🔄 Nouvelle conversation"
3. Vérifier la réinitialisation

**Résultat attendu** :
- ✅ Chat réinitialisé
- ✅ Message de bienvenue affiché
- ✅ Historique précédent effacé
- ✅ Possibilité de télécharger une nouvelle photo

---

### Tests de Performance

#### ✓ Test 10 : Temps d'Analyse
**Objectif** : Vérifier que l'analyse est rapide

**Étapes** :
1. Télécharger une image
2. Chronométrer le temps d'analyse

**Résultat attendu** :
- ✅ Analyse complète en < 2 secondes
- ✅ Pas de freeze de l'interface

---

#### ✓ Test 11 : Grandes Images
**Objectif** : Vérifier le traitement de grandes images

**Étapes** :
1. Télécharger une image de 5 MB
2. Vérifier le traitement

**Résultat attendu** :
- ✅ Image acceptée
- ✅ Redimensionnement automatique
- ✅ Analyse fonctionne normalement

---

### Tests d'Erreurs

#### ✓ Test 12 : Format Non Supporté
**Objectif** : Vérifier le rejet de formats invalides

**Étapes** :
1. Essayer de télécharger un fichier GIF
2. Essayer un fichier PDF
3. Vérifier les messages d'erreur

**Résultat attendu** :
- ✅ Fichier rejeté
- ✅ Message d'erreur clair
- ✅ Formats acceptés rappelés

---

#### ✓ Test 13 : Image Corrompue
**Objectif** : Vérifier la gestion d'erreurs

**Étapes** :
1. Télécharger un fichier JPG corrompu
2. Vérifier la gestion d'erreur

**Résultat attendu** :
- ✅ Erreur capturée
- ✅ Message d'erreur affiché
- ✅ Application ne crash pas

---

### Tests d'Intégration

#### ✓ Test 14 : Intégration avec Profil
**Objectif** : Vérifier que le profil utilisateur est pris en compte

**Étapes** :
1. Renseigner profil (âge: 20, type: grasse, budget: 10000)
2. Télécharger photo avec acné
3. Obtenir recommandations
4. Vérifier les produits

**Résultat attendu** :
- ✅ Produits adaptés à peau grasse
- ✅ Prix ≤ 10000 FCFA
- ✅ Conseils adaptés à l'âge

---

#### ✓ Test 15 : Historique CSV
**Objectif** : Vérifier la sauvegarde dans l'historique

**Étapes** :
1. Faire une analyse complète
2. Ouvrir conversations_historique.csv
3. Vérifier la dernière ligne

**Résultat attendu** :
- ✅ Nouvelle ligne ajoutée
- ✅ Problème détecté enregistré
- ✅ Produits recommandés listés
- ✅ Timestamp correct

---

### Tests Mobile

#### ✓ Test 16 : Responsive Design
**Objectif** : Vérifier l'affichage mobile

**Étapes** :
1. Ouvrir l'app sur smartphone
2. Tester l'upload de photo
3. Vérifier l'affichage des résultats

**Résultat attendu** :
- ✅ Interface adaptée à l'écran
- ✅ Boutons tactiles fonctionnels
- ✅ Images redimensionnées correctement

---

#### ✓ Test 17 : Photo depuis Caméra
**Objectif** : Vérifier la prise de photo directe

**Étapes** :
1. Sur mobile, cliquer "Browse files"
2. Choisir "Prendre une photo"
3. Prendre une photo
4. Vérifier l'upload

**Résultat attendu** :
- ✅ Caméra s'ouvre
- ✅ Photo capturée
- ✅ Upload et analyse fonctionnent

---

## 🔧 Scripts de Test Automatisés

### Script Python pour Tests Unitaires

```python
# test_image_analysis.py
import unittest
from PIL import Image
import numpy as np
import sys
sys.path.append('.')
from app_streamlit import StreamlitPharmacyAssistant

class TestImageAnalysis(unittest.TestCase):
    
    def setUp(self):
        self.assistant = StreamlitPharmacyAssistant()
    
    def test_acne_detection(self):
        """Test détection d'acné"""
        # Créer image avec dominante rouge
        img_array = np.zeros((300, 300, 3), dtype=np.uint8)
        img_array[:, :, 0] = 180  # Rouge
        img_array[:, :, 1] = 140  # Vert
        img_array[:, :, 2] = 130  # Bleu
        img = Image.fromarray(img_array)
        
        result = self.assistant.analyze_skin_image(img)
        
        self.assertIn('acné', result['problems'])
        self.assertGreater(result['confidence']['acné'], 60)
        self.assertLess(result['confidence']['acné'], 95)
    
    def test_dry_skin_detection(self):
        """Test détection peau sèche"""
        # Créer image avec haute variance
        img_array = np.random.randint(100, 200, (300, 300, 3), dtype=np.uint8)
        img = Image.fromarray(img_array)
        
        result = self.assistant.analyze_skin_image(img)
        
        self.assertIn('sèche', result['problems'])
        self.assertGreater(result['confidence']['sèche'], 50)
    
    def test_spots_detection(self):
        """Test détection de taches"""
        # Créer image avec variations
        img_array = np.zeros((300, 300, 3), dtype=np.uint8)
        img_array[:150, :, :] = 100
        img_array[150:, :, :] = 180
        img_array += np.random.randint(-30, 30, img_array.shape, dtype=np.int16)
        img_array = np.clip(img_array, 0, 255).astype(np.uint8)
        img = Image.fromarray(img_array)
        
        result = self.assistant.analyze_skin_image(img)
        
        self.assertIn('taches', result['problems'])
    
    def test_normal_skin(self):
        """Test peau normale"""
        # Créer image uniforme
        img_array = np.full((300, 300, 3), [150, 145, 140], dtype=np.uint8)
        img = Image.fromarray(img_array)
        
        result = self.assistant.analyze_skin_image(img)
        
        self.assertIn('normale', result['problems'])
    
    def test_image_conversion(self):
        """Test conversion d'image"""
        # Créer image en mode L (grayscale)
        img = Image.new('L', (300, 300), 128)
        
        result = self.assistant.analyze_skin_image(img)
        
        # Ne devrait pas crasher
        self.assertIsNotNone(result)
        self.assertIn('problems', result)

if __name__ == '__main__':
    unittest.main()
```

### Exécuter les Tests

```bash
# Installer pytest si nécessaire
pip install pytest

# Exécuter les tests
python -m pytest test_image_analysis.py -v

# Ou avec unittest
python test_image_analysis.py
```

---

## 📊 Rapport de Tests

### Template de Rapport

```markdown
# Rapport de Tests - Analyse de Photos

**Date** : [Date]
**Testeur** : [Nom]
**Version** : 2.0

## Résumé
- Tests réussis : X/17
- Tests échoués : Y/17
- Taux de réussite : Z%

## Détails

### Tests Fonctionnels (1-9)
| Test | Status | Commentaire |
|------|--------|-------------|
| 1. Upload JPG | ✅ | OK |
| 2. Upload PNG | ✅ | OK |
| 3. Détection acné | ✅ | Confiance 85% |
| ... | ... | ... |

### Tests Performance (10-11)
| Test | Status | Temps | Commentaire |
|------|--------|-------|-------------|
| 10. Temps analyse | ✅ | 1.2s | < 2s OK |
| ... | ... | ... | ... |

### Tests Erreurs (12-13)
| Test | Status | Commentaire |
|------|--------|-------------|
| 12. Format invalide | ✅ | Erreur gérée |
| ... | ... | ... |

### Tests Intégration (14-15)
| Test | Status | Commentaire |
|------|--------|-------------|
| 14. Profil utilisateur | ✅ | Filtres appliqués |
| ... | ... | ... |

### Tests Mobile (16-17)
| Test | Status | Commentaire |
|------|--------|-------------|
| 16. Responsive | ✅ | Adapté mobile |
| ... | ... | ... |

## Problèmes Identifiés
1. [Aucun] ou [Liste des bugs]

## Recommandations
1. [Améliorations suggérées]
```

---

## 🐛 Debugging

### Problèmes Courants

#### Problème 1 : "Module not found: numpy"
**Solution** :
```bash
pip install numpy
```

#### Problème 2 : "Module not found: PIL"
**Solution** :
```bash
pip install Pillow
```

#### Problème 3 : Analyse ne démarre pas
**Solution** :
1. Vérifier la console pour erreurs
2. Redémarrer l'application
3. Vérifier le format de l'image

#### Problème 4 : Scores de confiance toujours 0
**Solution** :
1. Vérifier que l'image est bien en RGB
2. Vérifier les calculs dans analyze_skin_image()
3. Ajouter des prints pour debug

### Mode Debug

```python
# Ajouter dans analyze_skin_image() pour debug
print(f"DEBUG - avg_red: {avg_red}")
print(f"DEBUG - avg_green: {avg_green}")
print(f"DEBUG - avg_blue: {avg_blue}")
print(f"DEBUG - variance: {variance}")
print(f"DEBUG - brightness: {brightness}")
```

---

## ✅ Validation Finale

### Checklist de Déploiement

Avant de considérer la fonctionnalité comme prête :

- [ ] Tous les tests fonctionnels passent
- [ ] Performance < 2s par analyse
- [ ] Gestion d'erreurs robuste
- [ ] Interface responsive
- [ ] Documentation complète
- [ ] Code sans erreurs de syntaxe
- [ ] Historique CSV fonctionne
- [ ] Intégration avec profil OK
- [ ] Tests sur mobile OK
- [ ] Feedback utilisateur positif

---

**🧪 Tests Complets pour une Fonctionnalité Robuste**
**✅ Qualité Assurée**
**🚀 Prêt pour Production**
