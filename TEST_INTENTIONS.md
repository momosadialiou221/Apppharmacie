# 🧪 Tests de Détection d'Intention

## Objectif
Vérifier que le chatbot détecte correctement les intentions et répond de manière appropriée.

## ✅ Tests à Effectuer

### Test 1 : Recherche de Produits
**Messages à tester** :
- "listes des produit pour acnee"
- "donne moi des produits pour l'acné"
- "produits pour peau sèche"
- "crème hydratante"
- "quel produit pour les taches"

**Résultat attendu** :
- ✅ Détection : `find_product`
- ✅ Réponse : Liste directe des produits (Top 5)
- ✅ Pas de questions supplémentaires
- ✅ Affichage : Nom, marque, prix, description

**Exemple de réponse** :
```
💊 Produits trouvés pour votre recherche :

J'ai trouvé 8 produits adaptés.

🛍️ Top 5 recommandations :

1. Effaclar Gel Moussant (La Roche-Posay)
   💰 8000-12000 FCFA
   📝 Nettoyant purifiant pour peau grasse...

2. Cleanance Gel Nettoyant (Avène)
   💰 7000-10000 FCFA
   📝 Élimine les impuretés...
...
```

---

### Test 2 : Recherche de Pharmacies
**Messages à tester** :
- "pharmacies à proximité"
- "où acheter"
- "pharmacie ouverte maintenant"
- "pharmacie 24h"
- "pharmacie de garde"

**Résultat attendu** :
- ✅ Détection : `find_pharmacy`
- ✅ Réponse : Liste des pharmacies proches
- ✅ Affichage : Nom, adresse, téléphone, distance, 24h/24

**Exemple de réponse** :
```
🏥 Pharmacies à proximité de Dakar :

1. Pharmacie Plateau 🟢 24h/24
   📍 Avenue Pompidou
   📞 33 821 XX XX
   📏 Distance: 1.2 km

2. Pharmacie Liberté
   📍 Rue 10
   📞 33 825 XX XX
   📏 Distance: 2.5 km
...
```

---

### Test 3 : Demande de Conseils
**Messages à tester** :
- "comment traiter l'acné"
- "conseils pour peau sèche"
- "routine pour taches"
- "comment utiliser un sérum"
- "aide pour peau grasse"

**Résultat attendu** :
- ✅ Détection : `get_advice`
- ✅ Réponse : Liste de conseils personnalisés
- ✅ Pas de produits (sauf si demandé)

**Exemple de réponse** :
```
💡 Mes conseils pour vous :

1. Routine simple : Nettoyant doux + hydratant léger
2. Évitez de toucher votre visage
3. Changez vos taies d'oreiller régulièrement
4. Produits avec acide salicylique le soir
5. Protection solaire obligatoire
...
```

---

### Test 4 : Salutations
**Messages à tester** :
- "bonjour"
- "salut"
- "hello"
- "merci"
- "ok"

**Résultat attendu** :
- ✅ Détection : `greeting`
- ✅ Réponse : Message d'accueil avec options

**Exemple de réponse** :
```
👋 Bonjour ! Comment puis-je vous aider aujourd'hui ?

Je peux :
• 📸 Analyser une photo de votre peau
• 💊 Recommander des produits
• 🏥 Trouver des pharmacies proches
• 💡 Donner des conseils personnalisés

Que souhaitez-vous faire ?
```

---

### Test 5 : Problème de Peau (Défaut)
**Messages à tester** :
- "j'ai de l'acné"
- "ma peau est sèche"
- "j'ai des taches brunes"
- "boutons sur le visage"

**Résultat attendu** :
- ✅ Détection : `skin_problem`
- ✅ Comportement : Pose des questions si infos manquantes
- ✅ Ou : Donne recommandations directes si infos complètes

---

## 🔍 Comment Tester

### Méthode 1 : Test Manuel
1. Ouvrir http://localhost:8501
2. Aller dans l'onglet "💬 Chat Assistant"
3. Taper chaque message de test
4. Vérifier la réponse

### Méthode 2 : Test Automatisé
```python
# test_intentions.py
from app_streamlit import StreamlitPharmacyAssistant

assistant = StreamlitPharmacyAssistant()

# Test 1
intent = assistant.detect_user_intent("listes des produit pour acnee")
assert intent['type'] == 'find_product'
assert intent['confidence'] > 0.9
print("✅ Test 1 passed")

# Test 2
intent = assistant.detect_user_intent("pharmacies à proximité")
assert intent['type'] == 'find_pharmacy'
print("✅ Test 2 passed")

# Test 3
intent = assistant.detect_user_intent("comment traiter l'acné")
assert intent['type'] == 'get_advice'
print("✅ Test 3 passed")

# Test 4
intent = assistant.detect_user_intent("bonjour")
assert intent['type'] == 'greeting'
print("✅ Test 4 passed")

# Test 5
intent = assistant.detect_user_intent("j'ai de l'acné")
assert intent['type'] == 'skin_problem'
print("✅ Test 5 passed")

print("\n🎉 Tous les tests passés !")
```

---

## 📊 Résultats Attendus

| Message | Intention Détectée | Confiance | Réponse |
|---------|-------------------|-----------|---------|
| "listes des produit pour acnee" | find_product | 95% | Liste produits |
| "pharmacies à proximité" | find_pharmacy | 90% | Liste pharmacies |
| "comment traiter l'acné" | get_advice | 80% | Conseils |
| "bonjour" | greeting | 95% | Accueil |
| "j'ai de l'acné" | skin_problem | 90% | Questions/Reco |

---

## ❌ Problèmes Possibles

### Problème 1 : Détection Incorrecte
**Symptôme** : "listes des produit pour acnee" → Pose des questions au lieu de lister

**Cause** : Méthode `detect_user_intent()` non trouvée

**Solution** : Vérifier que la méthode existe dans la classe

### Problème 2 : Pas de Réponse
**Symptôme** : Message envoyé mais pas de réponse

**Cause** : Erreur dans le traitement de l'intention

**Solution** : Vérifier les logs Streamlit

### Problème 3 : Mauvaise Intention
**Symptôme** : Détecte `skin_problem` au lieu de `find_product`

**Cause** : Mots-clés insuffisants ou ordre de vérification

**Solution** : Ajouter plus de mots-clés ou ajuster la priorité

---

## 🔧 Debugging

### Activer le Mode Debug
Ajouter dans le code :
```python
# Dans detect_user_intent()
print(f"DEBUG - Message: {message}")
print(f"DEBUG - Intent: {intent}")
```

### Vérifier les Logs
```bash
# Dans le terminal Streamlit
# Chercher les messages d'erreur
```

### Tester la Méthode Directement
```python
from app_streamlit import StreamlitPharmacyAssistant

assistant = StreamlitPharmacyAssistant()
intent = assistant.detect_user_intent("listes des produit pour acnee")
print(intent)
# Devrait afficher: {'type': 'find_product', 'confidence': 0.95}
```

---

## ✅ Checklist de Validation

Avant de considérer le test comme réussi :

- [ ] Test 1 : Recherche produits fonctionne
- [ ] Test 2 : Recherche pharmacies fonctionne
- [ ] Test 3 : Demande conseils fonctionne
- [ ] Test 4 : Salutations fonctionnent
- [ ] Test 5 : Problèmes de peau fonctionnent
- [ ] Pas de questions inutiles pour produits/pharmacies
- [ ] Réponses rapides (< 2 secondes)
- [ ] Format de réponse correct
- [ ] Pas d'erreurs dans les logs

---

## 🎯 Critères de Succès

### Excellent (90-100%)
- ✅ Toutes les intentions détectées correctement
- ✅ Réponses instantanées et pertinentes
- ✅ Aucune question inutile
- ✅ Format parfait

### Bon (70-89%)
- ✅ La plupart des intentions détectées
- ⚠️ Quelques questions inutiles
- ✅ Réponses correctes

### À Améliorer (< 70%)
- ❌ Intentions mal détectées
- ❌ Trop de questions
- ❌ Réponses incorrectes

---

**🧪 Tests Essentiels pour Validation de l'Intelligence du Chatbot**
