#!/usr/bin/env python3
"""
Démonstration des Conseils Améliorés
"""

import re

def extract_symptom_duration(text):
    """Version simplifiée pour test"""
    patterns = [
        (r'depuis\s+(\d+)\s+ans?', lambda x: int(x) * 365),
        (r'depuis\s+(\d+)\s+mois', lambda x: int(x) * 30),
        (r'depuis\s+(\d+)\s+semaines?', lambda x: int(x) * 7),
        (r'depuis\s+(\d+)\s+jours?', lambda x: int(x)),
        (r'depuis\s+longtemps', lambda x: 365 * 2),
        (r'récemment', lambda x: 10),
        (r'depuis\s+l\'harmattan', lambda x: 60),
    ]
    
    for pattern, converter in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            if match.groups():
                return {'jours': converter(match.group(1)), 'texte': match.group(0)}
            else:
                return {'jours': converter(None), 'texte': match.group(0)}
    return None

def demo_duration_logic():
    """Démonstration de la logique de durée"""
    print("🧪 DÉMONSTRATION - Logique de Durée Corrigée")
    print("-" * 50)
    
    test_cases = [
        "J'ai des boutons depuis 5 jours",
        "Ma peau est sèche depuis 3 semaines", 
        "Des taches depuis 8 mois",
        "Problème depuis 2 ans",
        "Récemment j'ai des rougeurs",
        "Depuis longtemps j'ai ce souci",
        "Depuis l'harmattan ma peau tiraille"
    ]
    
    for text in test_cases:
        print(f"\n📝 '{text}'")
        duration = extract_symptom_duration(text.lower())
        
        if duration:
            jours = duration['jours']
            texte = duration['texte']
            
            if jours <= 14:
                category = "🕐 RÉCENT"
                advice = "Commencez par des soins doux"
            elif jours <= 90:
                category = "📅 PERSISTANT"
                advice = "Routine ciblée nécessaire"
            elif jours <= 365:
                category = "⏰ INSTALLÉ"
                advice = "Approche méthodique requise"
            else:
                category = "🏥 CHRONIQUE"
                advice = "Consultation dermatologue recommandée"
            
            print(f"   Durée: {jours} jours ({texte})")
            print(f"   Catégorie: {category}")
            print(f"   Conseil: {advice}")
        else:
            print("   ❌ Durée non détectée")

if __name__ == '__main__':
    demo_duration_logic()