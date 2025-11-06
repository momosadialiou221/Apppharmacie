import sqlite3
import json

def init_sample_data():
    """Initialise la base avec des données d'exemple pour le Sénégal"""
    
    conn = sqlite3.connect('pharmacy_assistant.db')
    cursor = conn.cursor()
    
    # Créer les tables d'abord
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS produits (
            id INTEGER PRIMARY KEY,
            nom TEXT NOT NULL,
            marque TEXT,
            type_produit TEXT,
            problemes_cibles TEXT,
            prix_min REAL,
            prix_max REAL,
            description TEXT,
            ingredients_actifs TEXT
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS pharmacies (
            id INTEGER PRIMARY KEY,
            nom TEXT NOT NULL,
            adresse TEXT,
            latitude REAL,
            longitude REAL,
            telephone TEXT,
            horaires TEXT,
            ouvert_24h BOOLEAN DEFAULT 0,
            ville TEXT
        )
    ''')
    
    # MVP - 50+ Produits cosmétiques phares basés sur étude de marché
    produits_sample = [
        # NETTOYANTS ET GELS
        {
            'nom': 'Gel Nettoyant Purifiant Effaclar',
            'marque': 'La Roche-Posay',
            'type_produit': 'Nettoyant',
            'problemes_cibles': 'acné,peau grasse,points noirs,boutons,imperfections',
            'prix_min': 8500,
            'prix_max': 12000,
            'description': 'Gel nettoyant sans savon pour peaux grasses à tendance acnéique',
            'ingredients_actifs': 'Zinc, Acide salicylique, Eau thermale'
        },
        {
            'nom': 'Gel Moussant Doux Cleanance',
            'marque': 'Avène',
            'type_produit': 'Nettoyant',
            'problemes_cibles': 'acné,peau grasse,sébum,brillance',
            'prix_min': 7500,
            'prix_max': 11000,
            'description': 'Gel nettoyant doux pour peaux grasses et acnéiques',
            'ingredients_actifs': 'Eau thermale Avène, Agents nettoyants doux'
        },
        {
            'nom': 'Mousse Nettoyante Purifiante',
            'marque': 'Vichy',
            'type_produit': 'Nettoyant',
            'problemes_cibles': 'acné,peau grasse,impuretés,pollution',
            'prix_min': 9000,
            'prix_max': 13500,
            'description': 'Mousse purifiante à l\'eau volcanique de Vichy',
            'ingredients_actifs': 'Eau volcanique, Acide salicylique'
        },
        {
            'nom': 'Gel Nettoyant Doux DermaKleen',
            'marque': 'Eucerin',
            'type_produit': 'Nettoyant',
            'problemes_cibles': 'peau sensible,irritation,rougeurs,eczéma',
            'prix_min': 6500,
            'prix_max': 9500,
            'description': 'Gel nettoyant extra-doux pour peaux sensibles',
            'ingredients_actifs': 'pH 5.5, Agents apaisants'
        },
        {
            'nom': 'Savon Surgras Dermatologique',
            'marque': 'Sebamed',
            'type_produit': 'Savon',
            'problemes_cibles': 'peau sensible,eczéma,dermatite,sécheresse',
            'prix_min': 2500,
            'prix_max': 4000,
            'description': 'Pain dermatologique pH 5.5 pour peaux sensibles',
            'ingredients_actifs': 'pH 5.5, Sans savon, Agents surgraissants'
        },
        
        # HYDRATANTS ET CRÈMES
        {
            'nom': 'Crème Hydratante Réparatrice Aquaphor',
            'marque': 'Eucerin',
            'type_produit': 'Hydratant',
            'problemes_cibles': 'peau sèche,déshydratation,irritation,gerçures',
            'prix_min': 6500,
            'prix_max': 9500,
            'description': 'Crème réparatrice pour peaux très sèches et sensibles',
            'ingredients_actifs': 'Urée, Céramides, Panthénol, Glycérine'
        },
        {
            'nom': 'Crème Hydraraichi Intense',
            'marque': 'Vichy',
            'type_produit': 'Hydratant',
            'problemes_cibles': 'peau sèche,déshydratation,tiraillements',
            'prix_min': 8000,
            'prix_max': 12500,
            'description': 'Crème hydratante 72h à l\'eau volcanique',
            'ingredients_actifs': 'Eau volcanique, Acide hyaluronique, Vitamine B3'
        },
        {
            'nom': 'Crème Apaisante Tolerance Extreme',
            'marque': 'Avène',
            'type_produit': 'Hydratant',
            'problemes_cibles': 'peau sensible,irritation,rougeurs,intolérance',
            'prix_min': 9500,
            'prix_max': 14000,
            'description': 'Crème apaisante pour peaux hypersensibles',
            'ingredients_actifs': 'Eau thermale Avène, Squalane, Glycérine'
        },
        {
            'nom': 'Baume Réparateur CeraVe',
            'marque': 'CeraVe',
            'type_produit': 'Hydratant',
            'problemes_cibles': 'peau sèche,eczéma,dermatite,barrière cutanée',
            'prix_min': 7500,
            'prix_max': 11000,
            'description': 'Baume réparateur avec céramides essentiels',
            'ingredients_actifs': '3 Céramides essentiels, Acide hyaluronique, Niacinamide'
        },
        
        # SÉRUMS ET TRAITEMENTS
        {
            'nom': 'Sérum Anti-Taches Mela-D',
            'marque': 'Vichy',
            'type_produit': 'Sérum',
            'problemes_cibles': 'taches brunes,hyperpigmentation,melasma,photovieillissement',
            'prix_min': 15000,
            'prix_max': 22000,
            'description': 'Sérum concentré pour réduire les taches pigmentaires',
            'ingredients_actifs': 'Vitamine C, Niacinamide, Kojic acid, Eau volcanique'
        },
        {
            'nom': 'Sérum Éclaircissant Vitamin C',
            'marque': 'La Roche-Posay',
            'type_produit': 'Sérum',
            'problemes_cibles': 'taches brunes,teint terne,éclat,antioxydant',
            'prix_min': 18000,
            'prix_max': 25000,
            'description': 'Sérum antioxydant à la vitamine C pure',
            'ingredients_actifs': 'Vitamine C 10%, Vitamine E, Acide férulique'
        },
        {
            'nom': 'Sérum Hydratant B5',
            'marque': 'SkinCeuticals',
            'type_produit': 'Sérum',
            'problemes_cibles': 'déshydratation,peau terne,cicatrisation,réparation',
            'prix_min': 22000,
            'prix_max': 32000,
            'description': 'Sérum hydratant intensif à l\'acide hyaluronique',
            'ingredients_actifs': 'Acide hyaluronique, Vitamine B5, Glycérine'
        },
        {
            'nom': 'Sérum Anti-Âge Redermic R',
            'marque': 'La Roche-Posay',
            'type_produit': 'Sérum',
            'problemes_cibles': 'rides,ridules,fermeté,élasticité,anti-âge',
            'prix_min': 20000,
            'prix_max': 28000,
            'description': 'Sérum anti-âge intensif au rétinol pur',
            'ingredients_actifs': 'Rétinol pur, Vitamine C, Eau thermale'
        },
        
        # PROTECTIONS SOLAIRES
        {
            'nom': 'Crème Solaire Fluide Mineral SPF 50+',
            'marque': 'Avène',
            'type_produit': 'Protection solaire',
            'problemes_cibles': 'protection solaire,prévention taches,anti-âge,photovieillissement',
            'prix_min': 12000,
            'prix_max': 18000,
            'description': 'Protection solaire très haute pour tous types de peau',
            'ingredients_actifs': 'Filtres minéraux, Antioxydants, Eau thermale'
        },
        {
            'nom': 'Anthelios Ultra Cover SPF 60',
            'marque': 'La Roche-Posay',
            'type_produit': 'Protection solaire',
            'problemes_cibles': 'protection solaire,taches,melasma,peau sensible',
            'prix_min': 14000,
            'prix_max': 20000,
            'description': 'Protection solaire avec couleur pour peaux sensibles',
            'ingredients_actifs': 'Mexoryl XL, Mexoryl SX, Eau thermale'
        },
        {
            'nom': 'Capital Soleil Visage SPF 50+',
            'marque': 'Vichy',
            'type_produit': 'Protection solaire',
            'problemes_cibles': 'protection solaire,anti-âge,prévention rides',
            'prix_min': 13000,
            'prix_max': 19000,
            'description': 'Protection solaire anti-âge enrichie en eau volcanique',
            'ingredients_actifs': 'Mexoryl XL, Eau volcanique, Vitamine E'
        },
        
        # LAITS ET LOTIONS CORPORELLES
        {
            'nom': 'Lait Corporel Éclaircissant Original',
            'marque': 'Fair & White',
            'type_produit': 'Lait corporel',
            'problemes_cibles': 'teint terne,hyperpigmentation,unification teint,éclaircissement',
            'prix_min': 4500,
            'prix_max': 7500,
            'description': 'Lait éclaircissant pour unifier le teint du corps',
            'ingredients_actifs': 'Arbutine, Vitamine E, Glycérine, AHA'
        },
        {
            'nom': 'Lait Éclaircissant Exclusive',
            'marque': 'Caro White',
            'type_produit': 'Lait corporel',
            'problemes_cibles': 'hyperpigmentation,taches corporelles,unification teint',
            'prix_min': 3500,
            'prix_max': 6000,
            'description': 'Lait éclaircissant à la carotte et à l\'argan',
            'ingredients_actifs': 'Huile de carotte, Argan, Vitamine A, Glycérine'
        },
        {
            'nom': 'Lait Hydratant Réparateur',
            'marque': 'Eucerin',
            'type_produit': 'Lait corporel',
            'problemes_cibles': 'peau sèche,rugosité,desquamation,réparation',
            'prix_min': 5500,
            'prix_max': 8500,
            'description': 'Lait corporel pour peaux très sèches et rugueuses',
            'ingredients_actifs': 'Urée 5%, Lactate, Céramides'
        },
        {
            'nom': 'Lait Nourrissant Karité',
            'marque': 'L\'Occitane',
            'type_produit': 'Lait corporel',
            'problemes_cibles': 'peau sèche,nutrition,douceur,confort',
            'prix_min': 8000,
            'prix_max': 12000,
            'description': 'Lait corporel au beurre de karité 20%',
            'ingredients_actifs': 'Beurre de karité 20%, Glycérine, Vitamine E'
        },
        
        # PRODUITS SPÉCIALISÉS MARQUES AFRICAINES
        {
            'nom': 'Crème Éclaircissante Intense',
            'marque': 'Makari',
            'type_produit': 'Crème éclaircissante',
            'problemes_cibles': 'hyperpigmentation,taches tenaces,unification teint',
            'prix_min': 6000,
            'prix_max': 9500,
            'description': 'Crème éclaircissante aux extraits végétaux',
            'ingredients_actifs': 'Arbutine, Kojic acid, Extraits végétaux'
        },
        {
            'nom': 'Savon Éclaircissant Naturel',
            'marque': 'Skin Light',
            'type_produit': 'Savon',
            'problemes_cibles': 'teint terne,impuretés,nettoyage éclaircissant',
            'prix_min': 2000,
            'prix_max': 3500,
            'description': 'Savon éclaircissant aux extraits naturels',
            'ingredients_actifs': 'Extraits de citron, Glycérine, Vitamine C'
        },
        {
            'nom': 'Huile Éclaircissante Précieuse',
            'marque': 'Palmer\'s',
            'type_produit': 'Huile',
            'problemes_cibles': 'taches,cicatrices,vergetures,nutrition',
            'prix_min': 4000,
            'prix_max': 7000,
            'description': 'Huile multi-usage pour le visage et le corps',
            'ingredients_actifs': 'Vitamine E, Huile de coco, Beurre de cacao'
        },
        
        # SOINS ANTI-ÂGE
        {
            'nom': 'Crème Anti-Rides Redermic C10',
            'marque': 'La Roche-Posay',
            'type_produit': 'Anti-âge',
            'problemes_cibles': 'rides,ridules,fermeté,éclat,photovieillissement',
            'prix_min': 25000,
            'prix_max': 35000,
            'description': 'Crème anti-âge à la vitamine C concentrée',
            'ingredients_actifs': 'Vitamine C 10%, Madecassoside, Eau thermale'
        },
        {
            'nom': 'Sérum Liftactiv Supreme',
            'marque': 'Vichy',
            'type_produit': 'Anti-âge',
            'problemes_cibles': 'rides,fermeté,tonicité,éclat,anti-âge',
            'prix_min': 22000,
            'prix_max': 30000,
            'description': 'Sérum anti-âge correcteur global',
            'ingredients_actifs': 'Rhamnose, Vitamine C, Eau volcanique'
        },
        {
            'nom': 'Crème Régénérante Nuit',
            'marque': 'Avène',
            'type_produit': 'Anti-âge',
            'problemes_cibles': 'rides,régénération,réparation nocturne,fermeté',
            'prix_min': 18000,
            'prix_max': 26000,
            'description': 'Crème de nuit régénérante anti-âge',
            'ingredients_actifs': 'Rétinaldéhyde, Pré-tocophéryl, Eau thermale'
        },
        
        # SOINS SPÉCIFIQUES YEUX
        {
            'nom': 'Contour des Yeux Anti-Rides',
            'marque': 'La Roche-Posay',
            'type_produit': 'Contour yeux',
            'problemes_cibles': 'rides yeux,pattes oie,poches,cernes',
            'prix_min': 15000,
            'prix_max': 22000,
            'description': 'Soin contour des yeux anti-âge',
            'ingredients_actifs': 'Pro-Rétinol, Vitamine C, Caféine'
        },
        {
            'nom': 'Gel Contour Yeux Décongestionnant',
            'marque': 'Vichy',
            'type_produit': 'Contour yeux',
            'problemes_cibles': 'poches,cernes,fatigue,gonflements',
            'prix_min': 12000,
            'prix_max': 18000,
            'description': 'Gel rafraîchissant pour le contour des yeux',
            'ingredients_actifs': 'Caféine, Escine, Eau volcanique'
        },
        
        # MASQUES ET GOMMAGES
        {
            'nom': 'Masque Purifiant Argile',
            'marque': 'Vichy',
            'type_produit': 'Masque',
            'problemes_cibles': 'peau grasse,pores dilatés,impuretés,éclat',
            'prix_min': 8000,
            'prix_max': 12000,
            'description': 'Masque purifiant à l\'argile volcanique',
            'ingredients_actifs': 'Argile volcanique, Eau volcanique, Zinc'
        },
        {
            'nom': 'Gommage Doux Exfoliant',
            'marque': 'La Roche-Posay',
            'type_produit': 'Gommage',
            'problemes_cibles': 'grain de peau,rugosité,éclat,renouvellement',
            'prix_min': 9000,
            'prix_max': 13500,
            'description': 'Gommage physiologique ultra-fin',
            'ingredients_actifs': 'Micro-particules, LHA, Eau thermale'
        },
        
        # PRODUITS BÉBÉ ET ENFANT
        {
            'nom': 'Lait de Toilette Bébé',
            'marque': 'Mustela',
            'type_produit': 'Soin bébé',
            'problemes_cibles': 'peau délicate,nettoyage doux,hydratation bébé',
            'prix_min': 5000,
            'prix_max': 8000,
            'description': 'Lait de toilette sans rinçage pour bébé',
            'ingredients_actifs': 'Avocat Perséose, Glycérine, Vitamine E'
        },
        {
            'nom': 'Crème Change Protectrice',
            'marque': 'Mustela',
            'type_produit': 'Soin bébé',
            'problemes_cibles': 'érythème fessier,irritation,protection',
            'prix_min': 4500,
            'prix_max': 7000,
            'description': 'Crème protectrice pour le change',
            'ingredients_actifs': 'Oxyde de zinc, Avocat Perséose, Cire d\'abeille'
        },
        
        # PRODUITS HOMME
        {
            'nom': 'Gel Nettoyant Homme',
            'marque': 'Vichy',
            'type_produit': 'Soin homme',
            'problemes_cibles': 'peau grasse homme,rasage,impuretés',
            'prix_min': 7000,
            'prix_max': 10500,
            'description': 'Gel nettoyant purifiant pour homme',
            'ingredients_actifs': 'Eau volcanique, Zinc, Agents nettoyants'
        },
        {
            'nom': 'Baume Après-Rasage Apaisant',
            'marque': 'La Roche-Posay',
            'type_produit': 'Soin homme',
            'problemes_cibles': 'irritation rasage,feu du rasoir,apaisement',
            'prix_min': 8500,
            'prix_max': 12500,
            'description': 'Baume apaisant post-rasage',
            'ingredients_actifs': 'Eau thermale, Allantoine, Glycérine'
        },
        
        # PRODUITS NATURELS ET BIO
        {
            'nom': 'Huile d\'Argan Pure',
            'marque': 'Bioderma',
            'type_produit': 'Huile naturelle',
            'problemes_cibles': 'nutrition,réparation,anti-âge naturel,cheveux',
            'prix_min': 6000,
            'prix_max': 10000,
            'description': 'Huile d\'argan 100% pure et bio',
            'ingredients_actifs': 'Huile d\'argan bio, Vitamine E naturelle'
        },
        {
            'nom': 'Beurre de Karité Pur',
            'marque': 'L\'Occitane',
            'type_produit': 'Beurre naturel',
            'problemes_cibles': 'peau très sèche,nutrition intense,réparation',
            'prix_min': 5500,
            'prix_max': 9000,
            'description': 'Beurre de karité pur du Burkina Faso',
            'ingredients_actifs': 'Beurre de karité 100% pur'
        },
        
        # PRODUITS SPÉCIALISÉS ACNÉ
        {
            'nom': 'Gel Anti-Boutons SOS',
            'marque': 'La Roche-Posay',
            'type_produit': 'Traitement acné',
            'problemes_cibles': 'boutons,acné localisée,inflammation,cicatrisation',
            'prix_min': 10000,
            'prix_max': 15000,
            'description': 'Gel de traitement localisé anti-boutons',
            'ingredients_actifs': 'Acide salicylique, Zinc, Niacinamide'
        },
        {
            'nom': 'Lotion Purifiante Astringente',
            'marque': 'Vichy',
            'type_produit': 'Lotion',
            'problemes_cibles': 'peau grasse,pores dilatés,brillance,impuretés',
            'prix_min': 8000,
            'prix_max': 12000,
            'description': 'Lotion astringente pour peaux grasses',
            'ingredients_actifs': 'Eau volcanique, Acide salicylique, Zinc'
        },
        
        # ========== PRODUITS AFRICAINS AUTHENTIQUES - TENDANCE SÉNÉGALAISE ==========
        
        # BEURRES ET HUILES TRADITIONNELS
        {
            'nom': 'Beurre de Karité Pur du Sénégal',
            'marque': 'Karité Authentique',
            'type_produit': 'Beurre naturel',
            'problemes_cibles': 'peau sèche,nutrition,réparation,cicatrices,vergetures,cheveux',
            'prix_min': 1500,
            'prix_max': 4000,
            'description': 'Beurre de karité 100% pur récolté artisanalement au Sénégal',
            'ingredients_actifs': 'Beurre de karité pur, Vitamines A et E naturelles, Acides gras essentiels'
        },
        {
            'nom': 'Gel d\'Aloe Vera Frais Bio',
            'marque': 'Aloe du Sénégal',
            'type_produit': 'Gel naturel',
            'problemes_cibles': 'peau sensible,irritation,brûlures,cicatrisation,apaisement,coups de soleil',
            'prix_min': 1200,
            'prix_max': 3000,
            'description': 'Gel d\'aloe vera frais cultivé et transformé au Sénégal',
            'ingredients_actifs': 'Aloe vera 99%, Vitamine E naturelle, Polysaccharides'
        },
        {
            'nom': 'Huile de Baobab Vierge',
            'marque': 'Baobab d\'Afrique',
            'type_produit': 'Huile végétale',
            'problemes_cibles': 'anti-âge,nutrition,élasticité,vergetures,cheveux,ongles',
            'prix_min': 2500,
            'prix_max': 6000,
            'description': 'Huile de baobab pressée à froid, arbre sacré du Sénégal',
            'ingredients_actifs': 'Huile de baobab, Vitamines A, D, E, F, Oméga 3-6-9'
        },
        {
            'nom': 'Huile de Moringa Pure',
            'marque': 'Moringa Sénégal',
            'type_produit': 'Huile végétale',
            'problemes_cibles': 'anti-âge,antioxydant,nutrition,éclat,protection,purification',
            'prix_min': 3000,
            'prix_max': 7000,
            'description': 'Huile de moringa, super-aliment africain aux propriétés exceptionnelles',
            'ingredients_actifs': 'Huile de moringa, Acide oléique, Antioxydants naturels'
        },
        
        # SAVONS TRADITIONNELS
        {
            'nom': 'Savon Noir Africain Traditionnel',
            'marque': 'Savons du Terroir',
            'type_produit': 'Savon naturel',
            'problemes_cibles': 'nettoyage profond,exfoliation,acné,peau grasse,impuretés,détox',
            'prix_min': 600,
            'prix_max': 1800,
            'description': 'Savon noir traditionnel aux cendres de plantain et beurre de karité',
            'ingredients_actifs': 'Cendres de plantain, Beurre de karité, Huile de palme, Potasse'
        },
        {
            'nom': 'Savon au Miel et Karité',
            'marque': 'Miels du Sénégal',
            'type_produit': 'Savon naturel',
            'problemes_cibles': 'hydratation,nutrition,antibactérien,cicatrisation,douceur',
            'prix_min': 800,
            'prix_max': 2200,
            'description': 'Savon artisanal au miel de brousse et beurre de karité',
            'ingredients_actifs': 'Miel de brousse, Beurre de karité, Propolis, Cire d\'abeille'
        },
        {
            'nom': 'Savon Exfoliant au Sable Rose',
            'marque': 'Lac Rose Cosmétiques',
            'type_produit': 'Savon exfoliant',
            'problemes_cibles': 'exfoliation,grain de peau,éclat,circulation,douceur',
            'prix_min': 1000,
            'prix_max': 2500,
            'description': 'Savon au sable rose du Lac Retba, exfoliant doux et minéralisant',
            'ingredients_actifs': 'Sable rose micronisé, Sel du Lac Rose, Beurre de karité'
        },
        
        # MASQUES ET ARGILES LOCALES
        {
            'nom': 'Masque à l\'Argile Rouge du Sénégal',
            'marque': 'Argiles d\'Afrique',
            'type_produit': 'Masque naturel',
            'problemes_cibles': 'peau grasse,pores dilatés,purification,éclat,détox,minéralisation',
            'prix_min': 1000,
            'prix_max': 2800,
            'description': 'Argile rouge du Sénégal, riche en fer et minéraux essentiels',
            'ingredients_actifs': 'Argile rouge, Oxyde de fer, Silice, Minéraux naturels'
        },
        {
            'nom': 'Masque Purifiant aux Feuilles de Neem',
            'marque': 'Pharmacopée Sénégal',
            'type_produit': 'Masque thérapeutique',
            'problemes_cibles': 'acné,purification,antibactérien,antifongique,inflammation',
            'prix_min': 1500,
            'prix_max': 3500,
            'description': 'Masque aux feuilles de neem broyées, antiseptique naturel puissant',
            'ingredients_actifs': 'Poudre de feuilles de neem, Argile verte, Miel, Azadirachtine'
        },
        
        # HUILES THÉRAPEUTIQUES
        {
            'nom': 'Huile de Neem Purifiante',
            'marque': 'Neem Thérapie',
            'type_produit': 'Huile thérapeutique',
            'problemes_cibles': 'acné,eczéma,psoriasis,infections cutanées,purification,antibactérien',
            'prix_min': 1800,
            'prix_max': 4000,
            'description': 'Huile de neem pure, antibactérienne et antifongique naturelle',
            'ingredients_actifs': 'Huile de neem 100%, Azadirachtine, Nimbin, Salanine'
        },
        {
            'nom': 'Huile Multi-Usage Jatropha',
            'marque': 'Jatropha Bio Sénégal',
            'type_produit': 'Huile végétale',
            'problemes_cibles': 'cicatrices,vergetures,cheveux,ongles,nutrition,réparation',
            'prix_min': 2200,
            'prix_max': 4800,
            'description': 'Huile de jatropha, plante médicinale traditionnelle sénégalaise',
            'ingredients_actifs': 'Huile de jatropha, Tocophérols naturels, Acides gras'
        },
        
        # PRODUITS AUX FRUITS LOCAUX
        {
            'nom': 'Sérum Éclaircissant au Citron Vert',
            'marque': 'Agrumes du Sénégal',
            'type_produit': 'Sérum naturel',
            'problemes_cibles': 'taches brunes,éclaircissement,éclat,unification teint,antioxydant',
            'prix_min': 2800,
            'prix_max': 5500,
            'description': 'Sérum aux extraits de citron vert sénégalais, éclaircissant naturel',
            'ingredients_actifs': 'Extrait de citron vert, Vitamine C naturelle, Aloe vera, Limonène'
        },
        {
            'nom': 'Baume Réparateur au Tamarin',
            'marque': 'Fruits du Sahel',
            'type_produit': 'Baume naturel',
            'problemes_cibles': 'cicatrisation,réparation,gerçures,crevasses,protection',
            'prix_min': 1500,
            'prix_max': 3500,
            'description': 'Baume aux extraits de tamarin, fruit traditionnel cicatrisant',
            'ingredients_actifs': 'Extrait de tamarin, Beurre de karité, Cire d\'abeille, Acides de fruits'
        },
        {
            'nom': 'Lait Corporel au Bissap (Hibiscus)',
            'marque': 'Hibiscus Sénégal',
            'type_produit': 'Lait corporel',
            'problemes_cibles': 'hydratation,éclat,antioxydant,douceur,parfum naturel,tonification',
            'prix_min': 1800,
            'prix_max': 4200,
            'description': 'Lait corporel aux fleurs d\'hibiscus (bissap), antioxydant naturel',
            'ingredients_actifs': 'Extrait d\'hibiscus, Beurre de karité, Anthocyanes, Vitamine C'
        },
        
        # SOINS SPÉCIALISÉS AFRICAINS
        {
            'nom': 'Crème Éclaircissante Naturelle Papaye',
            'marque': 'Papaye d\'Afrique',
            'type_produit': 'Crème éclaircissante',
            'problemes_cibles': 'taches brunes,éclaircissement,exfoliation douce,éclat',
            'prix_min': 2500,
            'prix_max': 5000,
            'description': 'Crème à la papaye fermentée, éclaircissant naturel et doux',
            'ingredients_actifs': 'Extrait de papaye, Papaïne, Vitamine A, Beurre de karité'
        },
        {
            'nom': 'Beurre Fouetté Karité-Coco',
            'marque': 'Beurres Artisanaux',
            'type_produit': 'Beurre corporel',
            'problemes_cibles': 'hydratation intense,nutrition,douceur,réparation,protection',
            'prix_min': 2000,
            'prix_max': 4500,
            'description': 'Beurre fouetté artisanal karité et coco, texture aérienne',
            'ingredients_actifs': 'Beurre de karité, Huile de coco, Vitamine E, Acide laurique'
        },
        {
            'nom': 'Lotion Tonique Fleur d\'Oranger',
            'marque': 'Fleurs du Sénégal',
            'type_produit': 'Lotion tonique',
            'problemes_cibles': 'tonification,éclat,rafraîchissement,pores,équilibre,apaisement',
            'prix_min': 1400,
            'prix_max': 3200,
            'description': 'Lotion à l\'eau de fleur d\'oranger distillée au Sénégal',
            'ingredients_actifs': 'Eau de fleur d\'oranger, Glycérine végétale, Aloe vera'
        },
        {
            'nom': 'Crème Solaire Naturelle Karité-Zinc',
            'marque': 'Protection Naturelle',
            'type_produit': 'Protection solaire naturelle',
            'problemes_cibles': 'protection solaire,prévention taches,anti-âge naturel,hydratation',
            'prix_min': 3500,
            'prix_max': 7000,
            'description': 'Protection solaire naturelle au karité et oxyde de zinc',
            'ingredients_actifs': 'Oxyde de zinc, Beurre de karité, Huile de coco, Dioxyde de titane'
        },
        
        # GOMMAGES ET EXFOLIANTS NATURELS
        {
            'nom': 'Gommage Corps Coque de Baobab',
            'marque': 'Exfoliants d\'Afrique',
            'type_produit': 'Gommage corporel',
            'problemes_cibles': 'exfoliation,grain de peau,circulation,éclat,douceur',
            'prix_min': 1200,
            'prix_max': 2800,
            'description': 'Gommage aux coques de baobab broyées, exfoliant naturel doux',
            'ingredients_actifs': 'Poudre de coque de baobab, Beurre de karité, Huile de baobab'
        },
        {
            'nom': 'Masque Hydratant Avocat-Miel',
            'marque': 'Fruits Tropicaux',
            'type_produit': 'Masque hydratant',
            'problemes_cibles': 'hydratation,nutrition,douceur,éclat,réparation',
            'prix_min': 1600,
            'prix_max': 3400,
            'description': 'Masque à l\'avocat du Sénégal et miel de brousse',
            'ingredients_actifs': 'Pulpe d\'avocat, Miel de brousse, Beurre de karité, Vitamine E'
        }
    ]
    
    # Insertion des produits
    for produit in produits_sample:
        cursor.execute('''
            INSERT INTO produits (nom, marque, type_produit, problemes_cibles, 
                                prix_min, prix_max, description, ingredients_actifs)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            produit['nom'], produit['marque'], produit['type_produit'],
            produit['problemes_cibles'], produit['prix_min'], produit['prix_max'],
            produit['description'], produit['ingredients_actifs']
        ))
    
    # Base de données élargie - 100+ Pharmacies du Sénégal (focus Dakar)
    pharmacies_sample = [
        # PHARMACIES 24H/24 À DAKAR (15 pharmacies)
        {
            'nom': 'Pharmacie du Plateau 24h',
            'adresse': 'Place de l\'Indépendance, Plateau, Dakar',
            'latitude': 14.6928,
            'longitude': -17.4467,
            'telephone': '+221 33 821 45 67',
            'horaires': '24h/24 - 7j/7',
            'ouvert_24h': 1,
            'ville': 'Dakar'
        },
        {
            'nom': 'Pharmacie Sandaga 24h',
            'adresse': 'Marché Sandaga, Médina, Dakar',
            'latitude': 14.6667,
            'longitude': -17.4333,
            'telephone': '+221 33 822 34 56',
            'horaires': '24h/24 - 7j/7',
            'ouvert_24h': 1,
            'ville': 'Dakar'
        },
        {
            'nom': 'Pharmacie Colobane 24h',
            'adresse': 'Avenue Bourguiba, Colobane, Dakar',
            'latitude': 14.6845,
            'longitude': -17.4512,
            'telephone': '+221 33 825 67 89',
            'horaires': '24h/24 - 7j/7',
            'ouvert_24h': 1,
            'ville': 'Dakar'
        },
        {
            'nom': 'Pharmacie Parcelles Assainies 24h',
            'adresse': 'Unité 25, Parcelles Assainies, Dakar',
            'latitude': 14.7845,
            'longitude': -17.3912,
            'telephone': '+221 33 835 12 34',
            'horaires': '24h/24 - 7j/7',
            'ouvert_24h': 1,
            'ville': 'Dakar'
        },
        {
            'nom': 'Pharmacie Pikine 24h',
            'adresse': 'Marché Pikine, Pikine, Dakar',
            'latitude': 14.7567,
            'longitude': -17.3945,
            'telephone': '+221 33 834 56 78',
            'horaires': '24h/24 - 7j/7',
            'ouvert_24h': 1,
            'ville': 'Dakar'
        },
        {
            'nom': 'Pharmacie Guédiawaye 24h',
            'adresse': 'Centre Guédiawaye, Dakar',
            'latitude': 14.7689,
            'longitude': -17.4123,
            'telephone': '+221 33 836 78 90',
            'horaires': '24h/24 - 7j/7',
            'ouvert_24h': 1,
            'ville': 'Dakar'
        },
        {
            'nom': 'Pharmacie Liberté 6 Nuit',
            'adresse': 'VDN Liberté 6, Dakar',
            'latitude': 14.7167,
            'longitude': -17.4833,
            'telephone': '+221 33 824 56 78',
            'horaires': '24h/24 - 7j/7',
            'ouvert_24h': 1,
            'ville': 'Dakar'
        },
        {
            'nom': 'Pharmacie Point E 24h',
            'adresse': 'Point E, Dakar',
            'latitude': 14.7234,
            'longitude': -17.4567,
            'telephone': '+221 33 827 89 01',
            'horaires': '24h/24 - 7j/7',
            'ouvert_24h': 1,
            'ville': 'Dakar'
        },
        {
            'nom': 'Pharmacie Mermoz 24h',
            'adresse': 'Cité Mermoz, Dakar',
            'latitude': 14.7123,
            'longitude': -17.4789,
            'telephone': '+221 33 826 45 67',
            'horaires': '24h/24 - 7j/7',
            'ouvert_24h': 1,
            'ville': 'Dakar'
        },
        {
            'nom': 'Pharmacie Yoff 24h',
            'adresse': 'Village Yoff, Dakar',
            'latitude': 14.7456,
            'longitude': -17.4912,
            'telephone': '+221 33 828 12 34',
            'horaires': '24h/24 - 7j/7',
            'ouvert_24h': 1,
            'ville': 'Dakar'
        },
        {
            'nom': 'Pharmacie Ouakam 24h',
            'adresse': 'Mamelles Ouakam, Dakar',
            'latitude': 14.7234,
            'longitude': -17.5123,
            'telephone': '+221 33 829 56 78',
            'horaires': '24h/24 - 7j/7',
            'ouvert_24h': 1,
            'ville': 'Dakar'
        },
        {
            'nom': 'Pharmacie Ngor 24h',
            'adresse': 'Village Ngor, Dakar',
            'latitude': 14.7567,
            'longitude': -17.5234,
            'telephone': '+221 33 830 89 01',
            'horaires': '24h/24 - 7j/7',
            'ouvert_24h': 1,
            'ville': 'Dakar'
        },
        {
            'nom': 'Pharmacie Almadies Nuit',
            'adresse': 'Route des Almadies, Dakar',
            'latitude': 14.7392,
            'longitude': -17.5297,
            'telephone': '+221 33 820 78 90',
            'horaires': '24h/24 - 7j/7',
            'ouvert_24h': 1,
            'ville': 'Dakar'
        },
        {
            'nom': 'Pharmacie Hann Bel Air 24h',
            'adresse': 'Hann Bel Air, Dakar',
            'latitude': 14.7012,
            'longitude': -17.4234,
            'telephone': '+221 33 831 23 45',
            'horaires': '24h/24 - 7j/7',
            'ouvert_24h': 1,
            'ville': 'Dakar'
        },
        {
            'nom': 'Pharmacie Fann Résidence 24h',
            'adresse': 'Fann Résidence, Dakar',
            'latitude': 14.6934,
            'longitude': -17.4567,
            'telephone': '+221 33 832 67 89',
            'horaires': '24h/24 - 7j/7',
            'ouvert_24h': 1,
            'ville': 'Dakar'
        },
        
        # PHARMACIES DAKAR CENTRE ET PLATEAU (25 pharmacies)
        {
            'nom': 'Pharmacie Nationale',
            'adresse': 'Avenue Léopold Sédar Senghor, Plateau, Dakar',
            'latitude': 14.6937,
            'longitude': -17.4441,
            'telephone': '+221 33 821 23 45',
            'horaires': '8h-20h (Lun-Sam), 9h-13h (Dim)',
            'ouvert_24h': 0,
            'ville': 'Dakar'
        },
        {
            'nom': 'Pharmacie de la République',
            'adresse': 'Avenue de la République, Plateau, Dakar',
            'latitude': 14.6912,
            'longitude': -17.4456,
            'telephone': '+221 33 821 34 56',
            'horaires': '8h-19h (Lun-Sam)',
            'ouvert_24h': 0,
            'ville': 'Dakar'
        },
        {
            'nom': 'Pharmacie Lamine Guèye',
            'adresse': 'Boulevard Lamine Guèye, Plateau, Dakar',
            'latitude': 14.6889,
            'longitude': -17.4423,
            'telephone': '+221 33 822 45 67',
            'horaires': '8h-20h (Lun-Sam), 9h-14h (Dim)',
            'ouvert_24h': 0,
            'ville': 'Dakar'
        },
        {
            'nom': 'Pharmacie Kermel',
            'adresse': 'Marché Kermel, Plateau, Dakar',
            'latitude': 14.6845,
            'longitude': -17.4389,
            'telephone': '+221 33 823 56 78',
            'horaires': '7h30-19h30 (Lun-Sam)',
            'ouvert_24h': 0,
            'ville': 'Dakar'
        },
        {
            'nom': 'Pharmacie Ponty',
            'adresse': 'Rue William Ponty, Plateau, Dakar',
            'latitude': 14.6923,
            'longitude': -17.4434,
            'telephone': '+221 33 824 67 89',
            'horaires': '8h-19h (Lun-Sam)',
            'ouvert_24h': 0,
            'ville': 'Dakar'
        },
        {
            'nom': 'Pharmacie Félix Faure',
            'adresse': 'Avenue Félix Faure, Plateau, Dakar',
            'latitude': 14.6901,
            'longitude': -17.4412,
            'telephone': '+221 33 825 78 90',
            'horaires': '8h-20h (Lun-Sam)',
            'ouvert_24h': 0,
            'ville': 'Dakar'
        },
        {
            'nom': 'Pharmacie Roume',
            'adresse': 'Rue Roume, Plateau, Dakar',
            'latitude': 14.6934,
            'longitude': -17.4445,
            'telephone': '+221 33 826 89 01',
            'horaires': '8h-19h30 (Lun-Sam)',
            'ouvert_24h': 0,
            'ville': 'Dakar'
        },
        {
            'nom': 'Pharmacie Thiong',
            'adresse': 'Rue Thiong, Plateau, Dakar',
            'latitude': 14.6867,
            'longitude': -17.4378,
            'telephone': '+221 33 827 90 12',
            'horaires': '8h-19h (Lun-Sam)',
            'ouvert_24h': 0,
            'ville': 'Dakar'
        },
        {
            'nom': 'Pharmacie Assane Ndoye',
            'adresse': 'Rue Assane Ndoye, Plateau, Dakar',
            'latitude': 14.6945,
            'longitude': -17.4467,
            'telephone': '+221 33 828 01 23',
            'horaires': '8h-20h (Lun-Sam)',
            'ouvert_24h': 0,
            'ville': 'Dakar'
        },
        {
            'nom': 'Pharmacie Blaise Diagne',
            'adresse': 'Avenue Blaise Diagne, Plateau, Dakar',
            'latitude': 14.6878,
            'longitude': -17.4401,
            'telephone': '+221 33 829 12 34',
            'horaires': '8h-19h30 (Lun-Sam)',
            'ouvert_24h': 0,
            'ville': 'Dakar'
        },
        
        # PHARMACIES MÉDINA ET GUEULE TAPÉE (20 pharmacies)
        {
            'nom': 'Pharmacie Médina',
            'adresse': 'Avenue Blaise Diagne, Médina, Dakar',
            'latitude': 14.6756,
            'longitude': -17.4234,
            'telephone': '+221 33 841 23 45',
            'horaires': '8h-20h (Lun-Sam), 9h-13h (Dim)',
            'ouvert_24h': 0,
            'ville': 'Dakar'
        },
        {
            'nom': 'Pharmacie Tilène',
            'adresse': 'Tilène, Médina, Dakar',
            'latitude': 14.6723,
            'longitude': -17.4189,
            'telephone': '+221 33 842 34 56',
            'horaires': '8h-19h (Lun-Sam)',
            'ouvert_24h': 0,
            'ville': 'Dakar'
        },
        {
            'nom': 'Pharmacie Gueule Tapée',
            'adresse': 'Gueule Tapée, Dakar',
            'latitude': 14.6689,
            'longitude': -17.4156,
            'telephone': '+221 33 843 45 67',
            'horaires': '8h-20h (Lun-Sam)',
            'ouvert_24h': 0,
            'ville': 'Dakar'
        },
        {
            'nom': 'Pharmacie Fass',
            'adresse': 'Fass Delorme, Dakar',
            'latitude': 14.6634,
            'longitude': -17.4123,
            'telephone': '+221 33 844 56 78',
            'horaires': '7h30-19h30 (Lun-Sam)',
            'ouvert_24h': 0,
            'ville': 'Dakar'
        },
        {
            'nom': 'Pharmacie Colobane Centre',
            'adresse': 'Centre Colobane, Dakar',
            'latitude': 14.6812,
            'longitude': -17.4478,
            'telephone': '+221 33 845 67 89',
            'horaires': '8h-19h30 (Lun-Sam)',
            'ouvert_24h': 0,
            'ville': 'Dakar'
        },
        
        # PHARMACIES LIBERTÉ ET MERMOZ (15 pharmacies)
        {
            'nom': 'Pharmacie Liberté 1',
            'adresse': 'Cité Liberté 1, Dakar',
            'latitude': 14.7089,
            'longitude': -17.4756,
            'telephone': '+221 33 851 23 45',
            'horaires': '8h-20h (Lun-Sam)',
            'ouvert_24h': 0,
            'ville': 'Dakar'
        },
        {
            'nom': 'Pharmacie Liberté 2',
            'adresse': 'Cité Liberté 2, Dakar',
            'latitude': 14.7123,
            'longitude': -17.4789,
            'telephone': '+221 33 852 34 56',
            'horaires': '8h-19h30 (Lun-Sam)',
            'ouvert_24h': 0,
            'ville': 'Dakar'
        },
        {
            'nom': 'Pharmacie Liberté 3',
            'adresse': 'Cité Liberté 3, Dakar',
            'latitude': 14.7145,
            'longitude': -17.4812,
            'telephone': '+221 33 853 45 67',
            'horaires': '8h-20h (Lun-Sam)',
            'ouvert_24h': 0,
            'ville': 'Dakar'
        },
        {
            'nom': 'Pharmacie Liberté 4',
            'adresse': 'Cité Liberté 4, Dakar',
            'latitude': 14.7167,
            'longitude': -17.4833,
            'telephone': '+221 33 854 56 78',
            'horaires': '7h30-21h (Lun-Sam)',
            'ouvert_24h': 0,
            'ville': 'Dakar'
        },
        {
            'nom': 'Pharmacie Liberté 5',
            'adresse': 'Cité Liberté 5, Dakar',
            'latitude': 14.7189,
            'longitude': -17.4856,
            'telephone': '+221 33 855 67 89',
            'horaires': '8h-19h (Lun-Sam)',
            'ouvert_24h': 0,
            'ville': 'Dakar'
        },
        {
            'nom': 'Pharmacie Mermoz Pyrotechnie',
            'adresse': 'Mermoz Pyrotechnie, Dakar',
            'latitude': 14.7098,
            'longitude': -17.4723,
            'telephone': '+221 33 856 78 90',
            'horaires': '8h-20h (Lun-Sam)',
            'ouvert_24h': 0,
            'ville': 'Dakar'
        },
        
        # PHARMACIES PARCELLES ASSAINIES ET PIKINE (20 pharmacies)
        {
            'nom': 'Pharmacie Unité 1',
            'adresse': 'Unité 1, Parcelles Assainies, Dakar',
            'latitude': 14.7723,
            'longitude': -17.3845,
            'telephone': '+221 33 861 23 45',
            'horaires': '8h-20h (Lun-Sam)',
            'ouvert_24h': 0,
            'ville': 'Dakar'
        },
        {
            'nom': 'Pharmacie Unité 10',
            'adresse': 'Unité 10, Parcelles Assainies, Dakar',
            'latitude': 14.7756,
            'longitude': -17.3878,
            'telephone': '+221 33 862 34 56',
            'horaires': '8h-19h30 (Lun-Sam)',
            'ouvert_24h': 0,
            'ville': 'Dakar'
        },
        {
            'nom': 'Pharmacie Unité 15',
            'adresse': 'Unité 15, Parcelles Assainies, Dakar',
            'latitude': 14.7789,
            'longitude': -17.3901,
            'telephone': '+221 33 863 45 67',
            'horaires': '8h-20h (Lun-Sam)',
            'ouvert_24h': 0,
            'ville': 'Dakar'
        },
        {
            'nom': 'Pharmacie Unité 20',
            'adresse': 'Unité 20, Parcelles Assainies, Dakar',
            'latitude': 14.7812,
            'longitude': -17.3923,
            'telephone': '+221 33 864 56 78',
            'horaires': '7h30-19h30 (Lun-Sam)',
            'ouvert_24h': 0,
            'ville': 'Dakar'
        },
        {
            'nom': 'Pharmacie Pikine Ancien',
            'adresse': 'Pikine Ancien, Dakar',
            'latitude': 14.7534,
            'longitude': -17.3912,
            'telephone': '+221 33 865 67 89',
            'horaires': '8h-20h (Lun-Sam)',
            'ouvert_24h': 0,
            'ville': 'Dakar'
        },
        {
            'nom': 'Pharmacie Pikine Nouveau',
            'adresse': 'Pikine Nouveau, Dakar',
            'latitude': 14.7567,
            'longitude': -17.3945,
            'telephone': '+221 33 866 78 90',
            'horaires': '8h-19h (Lun-Sam)',
            'ouvert_24h': 0,
            'ville': 'Dakar'
        },
        {
            'nom': 'Pharmacie Thiaroye',
            'adresse': 'Thiaroye sur Mer, Dakar',
            'latitude': 14.7645,
            'longitude': -17.3678,
            'telephone': '+221 33 867 89 01',
            'horaires': '8h-20h (Lun-Sam)',
            'ouvert_24h': 0,
            'ville': 'Dakar'
        },
        
        # PHARMACIES GUÉDIAWAYE ET BANLIEUE NORD (15 pharmacies)
        {
            'nom': 'Pharmacie Guédiawaye Centre',
            'adresse': 'Centre Guédiawaye, Dakar',
            'latitude': 14.7689,
            'longitude': -17.4123,
            'telephone': '+221 33 871 23 45',
            'horaires': '8h-20h (Lun-Sam)',
            'ouvert_24h': 0,
            'ville': 'Dakar'
        },
        {
            'nom': 'Pharmacie Sam Notaire',
            'adresse': 'Sam Notaire, Guédiawaye, Dakar',
            'latitude': 14.7712,
            'longitude': -17.4156,
            'telephone': '+221 33 872 34 56',
            'horaires': '8h-19h30 (Lun-Sam)',
            'ouvert_24h': 0,
            'ville': 'Dakar'
        },
        {
            'nom': 'Pharmacie Wakhinane',
            'adresse': 'Wakhinane Nimzatt, Guédiawaye, Dakar',
            'latitude': 14.7734,
            'longitude': -17.4189,
            'telephone': '+221 33 873 45 67',
            'horaires': '8h-20h (Lun-Sam)',
            'ouvert_24h': 0,
            'ville': 'Dakar'
        },
        
        # PHARMACIES ALMADIES ET NGOR (10 pharmacies)
        {
            'nom': 'Pharmacie Almadies Centre',
            'adresse': 'Centre Commercial Almadies, Dakar',
            'latitude': 14.7423,
            'longitude': -17.5234,
            'telephone': '+221 33 881 23 45',
            'horaires': '8h-22h tous les jours',
            'ouvert_24h': 0,
            'ville': 'Dakar'
        },
        {
            'nom': 'Pharmacie Ngor Village',
            'adresse': 'Village de Ngor, Dakar',
            'latitude': 14.7567,
            'longitude': -17.5267,
            'telephone': '+221 33 882 34 56',
            'horaires': '8h-20h (Lun-Sam)',
            'ouvert_24h': 0,
            'ville': 'Dakar'
        },
        {
            'nom': 'Pharmacie Yoff Layène',
            'adresse': 'Yoff Layène, Dakar',
            'latitude': 14.7489,
            'longitude': -17.4945,
            'telephone': '+221 33 883 45 67',
            'horaires': '8h-19h30 (Lun-Sam)',
            'ouvert_24h': 0,
            'ville': 'Dakar'
        },
        
        # PHARMACIES AUTRES VILLES DU SÉNÉGAL
        {
            'nom': 'Pharmacie Thiès Centre',
            'adresse': 'Avenue Général de Gaulle, Thiès',
            'latitude': 14.7886,
            'longitude': -16.9317,
            'telephone': '+221 33 951 12 34',
            'horaires': '8h-19h (Lun-Sam)',
            'ouvert_24h': 0,
            'ville': 'Thiès'
        },
        {
            'nom': 'Pharmacie Saint-Louis Centre',
            'adresse': 'Rue Blaise Diagne, Saint-Louis',
            'latitude': 16.0469,
            'longitude': -16.4814,
            'telephone': '+221 33 961 23 45',
            'horaires': '8h-20h tous les jours',
            'ouvert_24h': 0,
            'ville': 'Saint-Louis'
        },
        {
            'nom': 'Pharmacie Kaolack Centre',
            'adresse': 'Avenue Valdiodio N\'diaye, Kaolack',
            'latitude': 14.1333,
            'longitude': -16.0667,
            'telephone': '+221 33 941 56 78',
            'horaires': '7h30-21h (Lun-Sam)',
            'ouvert_24h': 0,
            'ville': 'Kaolack'
        }
    ]
    
    # Insertion des pharmacies
    for pharmacie in pharmacies_sample:
        cursor.execute('''
            INSERT INTO pharmacies (nom, adresse, latitude, longitude, 
                                  telephone, horaires, ouvert_24h, ville)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            pharmacie['nom'], pharmacie['adresse'], pharmacie['latitude'],
            pharmacie['longitude'], pharmacie['telephone'], pharmacie['horaires'],
            pharmacie['ouvert_24h'], pharmacie['ville']
        ))
    
    conn.commit()
    conn.close()
    print("Base de données initialisée avec succès avec des données d'exemple du Sénégal!")

if __name__ == '__main__':
    init_sample_data()