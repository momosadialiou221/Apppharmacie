#!/usr/bin/env python3
"""
Script pour supprimer les doublons de produits dans la base de données
"""

import sqlite3

def remove_duplicate_products():
    """Supprime les produits en double en gardant le premier"""
    conn = sqlite3.connect('pharmacy_assistant.db')
    cursor = conn.cursor()
    
    # Trouver les doublons
    duplicates = cursor.execute('''
        SELECT nom, COUNT(*) as count 
        FROM produits 
        GROUP BY nom 
        HAVING count > 1
    ''').fetchall()
    
    print(f"🔍 Doublons trouvés : {len(duplicates)}")
    
    total_deleted = 0
    
    for nom, count in duplicates:
        # Garder le premier, supprimer les autres
        cursor.execute('''
            DELETE FROM produits 
            WHERE id NOT IN (
                SELECT MIN(id) 
                FROM produits 
                WHERE nom = ?
            ) AND nom = ?
        ''', (nom, nom))
        
        deleted = cursor.rowcount
        total_deleted += deleted
        print(f"  ✓ {nom}: supprimé {deleted} doublon(s)")
    
    conn.commit()
    
    # Vérifier le résultat
    total_produits = cursor.execute('SELECT COUNT(*) FROM produits').fetchone()[0]
    remaining_duplicates = cursor.execute('''
        SELECT COUNT(*) 
        FROM (
            SELECT nom, COUNT(*) as count 
            FROM produits 
            GROUP BY nom 
            HAVING count > 1
        )
    ''').fetchone()[0]
    
    conn.close()
    
    print(f"\n✅ Nettoyage terminé !")
    print(f"   - {total_deleted} doublons supprimés")
    print(f"   - {total_produits} produits restants")
    print(f"   - {remaining_duplicates} doublons restants")

if __name__ == '__main__':
    remove_duplicate_products()
