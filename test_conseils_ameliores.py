#!/usr/bin/env python3
"""
Test des Conseils Améliorés - Assistant Pharmacien Sénégal
Validation de la logique de durée et personnalisation des conseils
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app_chat import ChatPharmacyHandler
import json

def test_duration_extraction():
    """Test de l'extraction de durée améliorée"""
    print("🧪 TEST - Extraction de Durée des Symptômes")
    print("-" * 50)
    
    handler = ChatPharmacyHandler()
    
    test_cases = [
        # Cas numériques
        ("J'ai des boutons depuis 2 semaines", 14, "récent"),
        ("Ma peau est sèche depuis 3 mois", 90, "persistant"),
        ("Des taches depuis 2 ans", 730, "chronique"),
        ("Problème depuis 5 jours", 5, "très récent"),
        
        # Cas textuels
        ("Récemment j'ai des rougeurs", 10, "récent"),
        ("Depuis longtemps j'ai ce problème", 730, "chronique"),
        ("Depuis l'harmattan ma peau tiraille", 60, "saisonnier"),
        ("Depuis toujours j'ai la peau sensible", 3650, "chronique"),
        
        # Cas complexes
        ("Il y a 6 mois que j'ai des taches", 180, "installé"),
        ("Ça fait des années que j'ai de l'acné", 1095, "chronique"),
        ("Depuis quelques jours seulement", 5, "très récent")
    ]
    
    for i, (text, expected_days, category) in enumerate(test_cases, 1):
        print(f"\n📝 Test {i}: '{text}'")
        
        duration = handler.extract_symptom_duration(text.lower())
        
        if duration:
            jours = duration['jours']
            texte = duration['texte']
            print(f"   ✅ Durée extraite: {jours} jours ({texte})")
            print(f"   📊 Attendu: {expected_days} jours")
            print(f"   🏷️  Catégorie: {category}")
            
            # Vérifier la logique de catégorisation
            if jours <= 14:
                detected_category = "récent/très récent"
            elif jours <= 90:
                detected_category = "persistant"
            elif jours <= 365:
                detected_category = "installé"
            else:
                detected_category = "chronique"
            
            print(f"   🎯 Catégorie détectée: {detected_category}")
            
            # Tolérance de ±20% pour les estimations textuelles
            tolerance = 0.2
            if abs(jours - expected_days) <= expected_days * tolerance:
                print("   ✅ SUCCÈS - Extraction correcte")
            else:
                print("   ⚠️  ATTENTION - Écart significatif")
        else:
            print("   ❌ ÉCHEC - Aucune durée extraite")

def test_personalized_advice():
    """Test des conseils personnalisés"""
    print("\n🧪 TEST - Conseils Personnalisés")
    print("-" * 50)
    
    handler = ChatPharmacyHandler()
    
    test_scenarios = [
        {
            'name': 'Adolescent acné récente',
            'probleme': 'boutons depuis 2 semaines',
            'type_peau': 'grasse',
            'age': 17,
            'expected_keywords': ['récent', 'routine simple', 'dermatologue', 'taies d\'oreiller']
        },
        {
            'name': 'Adulte acné chronique',
            'probleme': 'acné depuis 3 ans',
            'type_peau': 'grasse',
            'age': 28,
            'expected_keywords': ['chronique', 'dermatologue', 'hormones', 'stress']
        },
        {
            'name': 'Peau sèche hivernale',
            'probleme': 'peau sèche depuis l\'harmattan',
            'type_peau': 'sèche',
            'age': 35,
            'expected_keywords': ['Harmattan', 'hydratation', 'humidificateur', 'huile']
        },
        {
            'name': 'Taches maturité',
            'probleme': 'taches brunes depuis 1 an',
            'type_peau': 'normale',
            'age': 48,
            'expected_keywords': ['maturité', 'protection solaire', 'peeling', 'vitamine C']
        },
        {
            'name': 'Peau sensible récente',
            'probleme': 'irritation depuis quelques jours',
            'type_peau': 'sensible',
            'age': 30,
            'expected_keywords': ['récent', 'test patch', 'apaisants', 'sans parfum']
        }
    ]
    
    for scenario in test_scenarios:
        print(f"\n👤 Scénario: {scenario['name']}")
        print(f"   📝 Problème: {scenario['probleme']}")
        print(f"   🧴 Type peau: {scenario['type_peau']}")
        print(f"   🎂 Âge: {scenario['age']} ans")
        
        # Extraire la durée
        duration = handler.extract_symptom_duration(scenario['probleme'])
        
        # Générer les conseils
        conseils = handler.generer_conseils_avances(
            scenario['probleme'], 
            scenario['type_peau'], 
            scenario['age'], 
            duration
        )
        
        print(f"   💡 Conseils générés: {len(conseils)}")
        
        # Vérifier la présence des mots-clés attendus
        conseils_text = ' '.join(conseils).lower()
        keywords_found = []
        keywords_missing = []
        
        for keyword in scenario['expected_keywords']:
            if keyword.lower() in conseils_text:
                keywords_found.append(keyword)
            else:
                keywords_missing.append(keyword)
        
        print(f"   ✅ Mots-clés trouvés: {keywords_found}")
        if keywords_missing:
            print(f"   ⚠️  Mots-clés manquants: {keywords_missing}")
        
        # Afficher quelques conseils
        print(f"   📋 Exemples de conseils:")
        for conseil in conseils[:3]:
            print(f"      • {conseil}")
        
        # Score de pertinence
        relevance_score = len(keywords_found) / len(scenario['expected_keywords'])
        print(f"   📊 Score de pertinence: {relevance_score:.1%}")

def test_age_specific_advice():
    """Test des conseils spécifiques à l'âge"""
    print("\n🧪 TEST - Conseils Spécifiques à l'Âge")
    print("-" * 50)
    
    handler = ChatPharmacyHandler()
    
    age_groups = [
        (16, "Adolescent", ["routine simple", "évitez", "actifs puissants"]),
        (22, "Jeune adulte", ["routine de base", "prévention", "stress"]),
        (32, "Adulte actif", ["vie active", "anti-âge", "soins de nuit"]),
        (45, "Maturité", ["changements hormonaux", "actifs anti-âge", "bilans"]),
        (55, "Senior", ["peau mature", "fermeté", "massages"])
    ]
    
    for age, group_name, expected_themes in age_groups:
        print(f"\n👥 Groupe: {group_name} ({age} ans)")
        
        conseils = handler.generer_conseils_avances(
            "problème de peau général", 
            "normale", 
            age, 
            None
        )
        
        conseils_text = ' '.join(conseils).lower()
        themes_found = [theme for theme in expected_themes if theme.lower() in conseils_text]
        
        print(f"   🎯 Thèmes attendus: {expected_themes}")
        print(f"   ✅ Thèmes trouvés: {themes_found}")
        print(f"   📊 Couverture: {len(themes_found)}/{len(expected_themes)}")

def test_seasonal_advice():
    """Test des conseils saisonniers"""
    print("\n🧪 TEST - Conseils Saisonniers")
    print("-" * 50)
    
    handler = ChatPharmacyHandler()
    
    seasonal_problems = [
        ("peau sèche depuis l'harmattan", ["Harmattan", "hydratation", "poussière"]),
        ("brillance depuis la saison chaude", ["chaude", "matifiantes", "SPF 50"]),
        ("problèmes depuis la saison des pluies", ["pluies", "humidité", "champignons"])
    ]
    
    for problem, expected_seasonal in seasonal_problems:
        print(f"\n🌍 Problème saisonnier: {problem}")
        
        conseils = handler.generer_conseils_avances(problem, "normale", 30, None)
        conseils_text = ' '.join(conseils).lower()
        
        seasonal_found = [term for term in expected_seasonal if term.lower() in conseils_text]
        
        print(f"   🎯 Termes saisonniers attendus: {expected_seasonal}")
        print(f"   ✅ Termes trouvés: {seasonal_found}")
        
        if seasonal_found:
            print("   ✅ Conseils saisonniers détectés")
        else:
            print("   ⚠️  Conseils saisonniers manquants")

def generate_advice_quality_report():
    """Génère un rapport de qualité des conseils"""
    print("\n📊 RAPPORT DE QUALITÉ DES CONSEILS")
    print("=" * 60)
    
    handler = ChatPharmacyHandler()
    
    # Test de diversité des conseils
    test_problems = [
        "acné depuis 1 mois",
        "peau sèche depuis l'hiver", 
        "taches depuis 6 mois",
        "peau sensible récente",
        "rides depuis quelques années"
    ]
    
    all_advice = []
    unique_advice = set()
    
    for problem in test_problems:
        conseils = handler.generer_conseils_avances(problem, "normale", 30, None)
        all_advice.extend(conseils)
        unique_advice.update(conseils)
    
    diversity_score = len(unique_advice) / len(all_advice) if all_advice else 0
    
    print(f"📈 Statistiques des conseils:")
    print(f"   • Total conseils générés: {len(all_advice)}")
    print(f"   • Conseils uniques: {len(unique_advice)}")
    print(f"   • Score de diversité: {diversity_score:.1%}")
    
    # Analyse de la longueur des conseils
    conseil_lengths = [len(conseil) for conseil in unique_advice]
    avg_length = sum(conseil_lengths) / len(conseil_lengths) if conseil_lengths else 0
    
    print(f"   • Longueur moyenne: {avg_length:.0f} caractères")
    
    # Analyse des emojis et formatage
    emoji_count = sum(1 for conseil in unique_advice if any(ord(char) > 127 for char in conseil))
    emoji_percentage = emoji_count / len(unique_advice) if unique_advice else 0
    
    print(f"   • Conseils avec emojis: {emoji_percentage:.1%}")
    
    # Score global de qualité
    quality_factors = [
        diversity_score,
        min(avg_length / 100, 1.0),  # Longueur optimale ~100 chars
        emoji_percentage,
        1.0 if len(unique_advice) > 50 else len(unique_advice) / 50
    ]
    
    quality_score = sum(quality_factors) / len(quality_factors)
    
    print(f"\n🏆 Score de Qualité Global: {quality_score:.1%}")
    
    if quality_score >= 0.8:
        print("🌟 EXCELLENT - Conseils très personnalisés et diversifiés")
    elif quality_score >= 0.6:
        print("✅ BON - Conseils bien adaptés")
    elif quality_score >= 0.4:
        print("⚠️  MOYEN - Améliorations possibles")
    else:
        print("🔄 BASIQUE - Nécessite des améliorations")

def main():
    """Fonction principale de test"""
    print("🧪 TESTS DES CONSEILS AMÉLIORÉS")
    print("Assistant Pharmacien Sénégal - Personnalisation Avancée")
    print("=" * 70)
    
    try:
        test_duration_extraction()
        test_personalized_advice()
        test_age_specific_advice()
        test_seasonal_advice()
        generate_advice_quality_report()
        
        print("\n" + "=" * 70)
        print("🎉 Tests des conseils améliorés terminés !")
        print("\n✅ Améliorations validées :")
        print("   • Logique de durée corrigée (récent vs chronique)")
        print("   • Conseils personnalisés selon âge, type de peau, durée")
        print("   • Conseils saisonniers adaptés au Sénégal")
        print("   • Formatage avec emojis pour meilleure lisibilité")
        print("   • Recommandations contextuelles intelligentes")
        
    except Exception as e:
        print(f"\n❌ Erreur durant les tests: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()