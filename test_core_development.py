#!/usr/bin/env python3
"""
Test du Développement Core - Assistant Pharmacien Sénégal
Validation des améliorations et nouvelles fonctionnalités
"""

import sqlite3
import json
from advanced_analysis import AdvancedNeedsAnalyzer
from database_expansion import DatabaseExpansion

def test_database_expansion():
    """Test de l'expansion de la base de données"""
    print("🧪 TEST - Expansion de la Base de Données")
    print("-" * 50)
    
    conn = sqlite3.connect('pharmacy_assistant.db')
    
    # Vérifier les nouvelles tables
    tables = ['product_categories', 'brands_extended', 'active_ingredients', 'produits_extended']
    
    for table in tables:
        try:
            count = conn.execute(f'SELECT COUNT(*) FROM {table}').fetchone()[0]
            print(f"✅ Table {table}: {count} entrées")
        except sqlite3.OperationalError:
            print(f"❌ Table {table}: Non trouvée")
    
    # Statistiques détaillées
    try:
        categories = conn.execute('SELECT name FROM product_categories LIMIT 5').fetchall()
        print(f"📂 Exemples de catégories: {[c[0] for c in categories]}")
        
        brands = conn.execute('SELECT name, brand_positioning FROM brands_extended LIMIT 5').fetchall()
        print(f"🏷️  Exemples de marques: {[(b[0], b[1]) for b in brands]}")
        
        ingredients = conn.execute('SELECT name FROM active_ingredients LIMIT 5').fetchall()
        print(f"🧪 Exemples d'ingrédients: {[i[0] for i in ingredients]}")
        
    except Exception as e:
        print(f"⚠️  Erreur lors de la lecture: {e}")
    
    conn.close()

def test_advanced_analysis():
    """Test du système d'analyse avancée"""
    print("\n🧪 TEST - Analyse Avancée des Besoins")
    print("-" * 50)
    
    try:
        analyzer = AdvancedNeedsAnalyzer()
        
        # Cas de test réalistes
        test_cases = [
            {
                'input': "Bonjour, j'ai des boutons sur le front depuis 3 semaines, je débute dans les soins, budget limité",
                'context': {'age': 19, 'type_peau': 'grasse'},
                'expected': ['acné', 'routine_beginner', 'économique']
            },
            {
                'input': "Ma peau est très sèche depuis l'harmattan, j'ai déjà essayé plusieurs crèmes sans succès",
                'context': {'age': 32, 'type_peau': 'sèche'},
                'expected': ['hydratation', 'routine_advanced', 'harmattan']
            },
            {
                'input': "Je veux des produits haut de gamme pour mes taches brunes, résultats rapides svp",
                'context': {'age': 45, 'type_peau': 'normale'},
                'expected': ['éclaircissement', 'premium_seeker', 'high']
            }
        ]
        
        for i, case in enumerate(test_cases, 1):
            print(f"\n📝 Test {i}: {case['input'][:50]}...")
            
            analysis = analyzer.analyze_user_needs(case['input'], case['context'])
            
            print(f"   🎯 Besoins primaires: {analysis['primary_needs']}")
            print(f"   🔍 Pattern comportemental: {analysis['behavior_pattern']}")
            print(f"   💰 Budget détecté: {analysis['budget_indication']}")
            print(f"   📊 Score de confiance: {analysis['confidence_score']:.2f}")
            print(f"   ⏰ Urgence: {analysis['urgency_level']}")
            
            # Test des recommandations
            recommendations = analyzer.get_advanced_recommendations(analysis, limit=3)
            print(f"   💊 Top 3 recommandations:")
            for j, prod in enumerate(recommendations, 1):
                score = prod.get('recommendation_score', 0)
                print(f"      {j}. {prod['nom']} (Score: {score:.2f})")
            
            # Test des conseils
            advice = analyzer.generate_personalized_advice(analysis)
            print(f"   💡 Conseils générés: {len(advice)}")
            
        print(f"\n✅ Analyse avancée fonctionnelle")
        
    except Exception as e:
        print(f"❌ Erreur analyse avancée: {e}")

def test_integration():
    """Test de l'intégration complète"""
    print("\n🧪 TEST - Intégration Complète")
    print("-" * 50)
    
    # Simuler une requête complète
    test_request = {
        'probleme': "J'ai la peau qui tiraille depuis l'hiver, première fois que j'utilise des soins",
        'type_peau': 'sèche',
        'age': 25,
        'localisation': {'latitude': 14.6937, 'longitude': -17.4441}
    }
    
    try:
        analyzer = AdvancedNeedsAnalyzer()
        
        # Analyse complète
        context = {
            'age': test_request['age'],
            'type_peau': test_request['type_peau'],
            'localisation': test_request['localisation']
        }
        
        analysis = analyzer.analyze_user_needs(test_request['probleme'], context)
        recommendations = analyzer.get_advanced_recommendations(analysis, limit=5)
        advice = analyzer.generate_personalized_advice(analysis)
        
        print(f"✅ Analyse: {len(analysis['primary_needs'])} besoins identifiés")
        print(f"✅ Recommandations: {len(recommendations)} produits")
        print(f"✅ Conseils: {len(advice)} suggestions")
        print(f"✅ Score global: {analysis['confidence_score']:.2f}")
        
        # Vérifier la cohérence
        if analysis['primary_needs'] and recommendations and advice:
            print("✅ Intégration complète réussie")
        else:
            print("⚠️  Intégration partielle")
            
    except Exception as e:
        print(f"❌ Erreur intégration: {e}")

def test_performance():
    """Test de performance du système"""
    print("\n🧪 TEST - Performance du Système")
    print("-" * 50)
    
    import time
    
    try:
        analyzer = AdvancedNeedsAnalyzer()
        
        # Test de charge
        test_inputs = [
            "J'ai des boutons depuis 2 semaines",
            "Ma peau est sèche et tiraille",
            "Des taches brunes sur les joues",
            "Peau sensible qui rougit",
            "Rides autour des yeux"
        ] * 10  # 50 requêtes
        
        start_time = time.time()
        
        for i, input_text in enumerate(test_inputs):
            analysis = analyzer.analyze_user_needs(input_text, {'age': 30})
            recommendations = analyzer.get_advanced_recommendations(analysis, limit=3)
            
            if (i + 1) % 10 == 0:
                elapsed = time.time() - start_time
                print(f"   📊 {i + 1} requêtes traitées en {elapsed:.2f}s")
        
        total_time = time.time() - start_time
        avg_time = total_time / len(test_inputs)
        
        print(f"✅ Performance: {avg_time*1000:.1f}ms par requête en moyenne")
        
        if avg_time < 0.1:  # Moins de 100ms
            print("🚀 Performance excellente")
        elif avg_time < 0.5:  # Moins de 500ms
            print("✅ Performance bonne")
        else:
            print("⚠️  Performance à améliorer")
            
    except Exception as e:
        print(f"❌ Erreur test performance: {e}")

def generate_development_report():
    """Génère un rapport de développement"""
    print("\n📊 RAPPORT DE DÉVELOPPEMENT CORE")
    print("=" * 60)
    
    conn = sqlite3.connect('pharmacy_assistant.db')
    
    # Statistiques de base
    stats = {
        'produits_base': conn.execute('SELECT COUNT(*) FROM produits').fetchone()[0],
        'pharmacies': conn.execute('SELECT COUNT(*) FROM pharmacies').fetchone()[0],
    }
    
    # Statistiques étendues
    try:
        stats.update({
            'categories': conn.execute('SELECT COUNT(*) FROM product_categories').fetchone()[0],
            'marques_etendues': conn.execute('SELECT COUNT(*) FROM brands_extended').fetchone()[0],
            'ingredients': conn.execute('SELECT COUNT(*) FROM active_ingredients').fetchone()[0],
            'produits_etendus': conn.execute('SELECT COUNT(*) FROM produits_extended').fetchone()[0],
            'analyses_avancees': conn.execute('SELECT COUNT(*) FROM advanced_interactions').fetchone()[0]
        })
    except sqlite3.OperationalError:
        stats.update({
            'categories': 0,
            'marques_etendues': 0,
            'ingredients': 0,
            'produits_etendus': 0,
            'analyses_avancees': 0
        })
    
    conn.close()
    
    print(f"📈 Base de Données:")
    print(f"   • Produits de base: {stats['produits_base']}")
    print(f"   • Produits étendus: {stats['produits_etendus']}")
    print(f"   • Pharmacies: {stats['pharmacies']}")
    print(f"   • Catégories: {stats['categories']}")
    print(f"   • Marques étendues: {stats['marques_etendues']}")
    print(f"   • Ingrédients actifs: {stats['ingredients']}")
    
    print(f"\n🤖 Analyse Avancée:")
    print(f"   • Interactions analysées: {stats['analyses_avancees']}")
    
    # Calcul du score de développement
    total_possible = 300  # 200 produits + 100 autres éléments
    total_actuel = (stats['produits_base'] + stats['produits_etendus'] + 
                   stats['categories'] + stats['marques_etendues'] + stats['ingredients'])
    
    completion_score = min((total_actuel / total_possible) * 100, 100)
    
    print(f"\n🎯 Score de Développement Core: {completion_score:.1f}%")
    
    if completion_score >= 80:
        print("🏆 Développement Core: EXCELLENT")
    elif completion_score >= 60:
        print("✅ Développement Core: BON")
    elif completion_score >= 40:
        print("⚠️  Développement Core: EN COURS")
    else:
        print("🔄 Développement Core: INITIAL")

def main():
    """Fonction principale de test"""
    print("🧪 TESTS DU DÉVELOPPEMENT CORE")
    print("Assistant Pharmacien Sénégal - Phase Avancée")
    print("=" * 60)
    
    # Lancer tous les tests
    test_database_expansion()
    test_advanced_analysis()
    test_integration()
    test_performance()
    generate_development_report()
    
    print("\n" + "=" * 60)
    print("🎉 Tests du développement core terminés !")
    print("\n🚀 Prochaines étapes:")
    print("   1. Continuer l'expansion à 200+ produits")
    print("   2. Améliorer l'analyse comportementale")
    print("   3. Ajouter la vérification d'interactions")
    print("   4. Implémenter le mode formation")

if __name__ == '__main__':
    main()