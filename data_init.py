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
            'nom': 'Effaclar Duo+',
            'marque': 'La Roche-Posay',
            'type_produit': 'Traitement acné',
            'problemes_cibles': 'acné,imperfections,rougeurs,cicatrisation',
            'prix_min': 11500,
            'prix_max': 16500,
            'description': 'Soin correcteur anti-imperfections et marque post-acné',
            'ingredients_actifs': 'Acide salicylique, Niacinamide, Procerad'
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
            'nom': 'TriAcnéal (sérum/gommage léger)',
            'marque': 'Avène',
            'type_produit': 'Traitement acné/peau texturée',
            'problemes_cibles': 'acné,comedons,taches post-acné,grain de peau',
            'prix_min': 14000,
            'prix_max': 20000,
            'description': 'Soin régulateur pour améliorer la texture et réduire les marques',
            'ingredients_actifs': 'Procerad, Rétinaldéhyde, Acide glycolique'
        },
        {
            'nom': 'Mousse Nettoyante Purifiante',
            'marque': 'Vichy',
            'type_produit': 'Nettoyant',
            'problemes_cibles': 'acné,peau grasse,impuretés,pollution',
            'prix_min': 9000,
            'prix_max': 13500,
            'description': "Mousse purifiante à l'eau volcanique de Vichy pour nettoyage quotidien",
            'ingredients_actifs': 'Eau volcanique, Acide salicylique'
        },
        {
            'nom': 'Normaderm Phytosolution',
            'marque': 'Vichy',
            'type_produit': 'Soin anti-imperfections',
            'problemes_cibles': 'acné,pores dilatés,brillance,imperfections',
            'prix_min': 16000,
            'prix_max': 23000,
            'description': 'Soin anti-imperfections concentré, effet peeling doux',
            'ingredients_actifs': 'Acide salicylique, Neohesperidine, Probiotiques'
        },
        {
            'nom': 'Sébium Gel Moussant',
            'marque': 'Bioderma',
            'type_produit': 'Nettoyant',
            'problemes_cibles': 'peau grasse,acné,sébum,impuretés',
            'prix_min': 7500,
            'prix_max': 10000,
            'description': 'Gel moussant régulateur pour peaux mixtes à grasses',
            'ingredients_actifs': 'Complexe SeboRestore, Zinc, Agents moussants doux'
        },
        {
            'nom': 'Sébium Global (traitement)',
            'marque': 'Bioderma',
            'type_produit': 'Traitement acné',
            'problemes_cibles': 'acné inflammatoire,comédons,marques post-acné',
            'prix_min': 15000,
            'prix_max': 21000,
            'description': "Soin quotidien régulateur contre l'acné et les marques",
            'ingredients_actifs': 'Acide salicylique, TLR2 regulator, CVR complex'
        },
        {
            'nom': 'Cica-Baume B5',
            'marque': 'La Roche-Posay',
            'type_produit': 'Baume réparateur',
            'problemes_cibles': 'peau sensible,irritation,gerçures,post-procédure',
            'prix_min': 9500,
            'prix_max': 14000,
            'description': 'Baume apaisant réparateur pour peaux fragilisées',
            'ingredients_actifs': 'Panthénol (B5), Madecassoside, Eau thermale'
        },
        {
            'nom': 'Hydraphase Intense Légère',
            'marque': 'La Roche-Posay',
            'type_produit': 'Hydratant',
            'problemes_cibles': 'déshydratation,peau sensible,teint terne',
            'prix_min': 13000,
            'prix_max': 18500,
            'description': 'Hydratation longue durée pour peaux déshydratées',
            'ingredients_actifs': 'Acide hyaluronique fragmenté, Eau thermale'
        },
        {
            'nom': 'Foaming Cleanser CeraVe',
            'marque': 'CeraVe',
            'type_produit': 'Nettoyant',
            'problemes_cibles': 'peau mixte,peau grasse,nettoyage quotidien',
            'prix_min': 9000,
            'prix_max': 12500,
            'description': 'Nettoyant moussant respectueux de la barrière cutanée',
            'ingredients_actifs': '3 céramides essentiels, Acide hyaluronique'
        },
        {
            'nom': 'Hydrating Cleanser CeraVe',
            'marque': 'CeraVe',
            'type_produit': 'Nettoyant',
            'problemes_cibles': 'peau sèche,peau sensible,nettoyage doux',
            'prix_min': 8500,
            'prix_max': 12000,
            'description': 'Nettoyant crème hydratant pour peaux sèches',
            'ingredients_actifs': 'Céramides, Niacinamide, Acide hyaluronique'
        },
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
            'nom': 'Baume Réparateur CeraVe',
            'marque': 'CeraVe',
            'type_produit': 'Hydratant',
            'problemes_cibles': 'peau sèche,eczéma,dermatite,barrière cutanée',
            'prix_min': 7500,
            'prix_max': 11000,
            'description': 'Baume réparateur avec céramides essentiels',
            'ingredients_actifs': '3 Céramides essentiels, Acide hyaluronique, Niacinamide'
        },
        {
            'nom': 'Crème Hydratante 72h',
            'marque': 'Vichy (Aqualia Thermal)',
            'type_produit': 'Hydratant',
            'problemes_cibles': 'déshydratation,peau terne,confort',
            'prix_min': 12000,
            'prix_max': 17000,
            'description': "Hydratant longue durée à l'eau volcanique",
            'ingredients_actifs': 'Eau volcanique, Glycérine, Acide hyaluronique'
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
            'nom': 'Sérum Éclaircissant Vitamin C',
            'marque': 'La Roche-Posay',
            'type_produit': 'Sérum',
            'problemes_cibles': 'taches brunes,teint terne,éclat,antioxydant',
            'prix_min': 18000,
            'prix_max': 25000,
            'description': 'Sérum antioxydant à la vitamine C pour uniformiser le teint',
            'ingredients_actifs': 'Vitamine C 10%, Vitamine E, Acide férulique'
        },
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
            'nom': 'Eucerin Anti-Pigment',
            'marque': 'Eucerin',
            'type_produit': 'Sérum/Crème anti-taches',
            'problemes_cibles': 'hyperpigmentation,taches brunes,éclat',
            'prix_min': 17000,
            'prix_max': 24000,
            'description': 'Soin anti-taches pour atténuer les hyperpigmentations',
            'ingredients_actifs': 'Thiamidol (actif breveté), Niacinamide'
        },
        {
            'nom': 'Sérum Niacinamide 10%',
            'marque': 'The Ordinary',
            'type_produit': 'Sérum',
            'problemes_cibles': 'pores,imperfections,teint irrégulier,éclat',
            'prix_min': 8000,
            'prix_max': 12000,
            'description': 'Sérum ciblé pour réduire les pores et uniformiser le teint',
            'ingredients_actifs': 'Niacinamide 10%, Zinc PCA'
        },
        {
            'nom': 'Alpha Arbutin 2% Serum',
            'marque': 'The Ordinary (ou équivalent générique)',
            'type_produit': 'Sérum dépigmentant',
            'problemes_cibles': 'taches brunes,hyperpigmentation,éclaircissement',
            'prix_min': 9000,
            'prix_max': 14000,
            'description': 'Sérum concentré anti-taches à base d\'alpha arbutine',
            'ingredients_actifs': 'Alpha arbutin 2%, Acide hyaluronique'
        },
        {
            'nom': 'Kojic Acid Soap (savon kojic)',
            'marque': 'Marque locale / importée',
            'type_produit': 'Savon dépigmentant doux',
            'problemes_cibles': 'taches brunes,éclaircissement,teint irrégulier',
            'prix_min': 1200,
            'prix_max': 3500,
            'description': 'Savon éclaircissant doux à base d\'acide kojique et extraits naturels',
            'ingredients_actifs': 'Kojic acid, Glycérine, Extraits végétaux'
        },
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
            'nom': 'Anthelios Ultra Cover SPF 60 (teinté)',
            'marque': 'La Roche-Posay',
            'type_produit': 'Protection solaire teintée',
            'problemes_cibles': 'protection solaire,taches,melasma,peau sensible',
            'prix_min': 14000,
            'prix_max': 20000,
            'description': 'Protection solaire avec couvrance pour peaux sensibles',
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
            'nom': 'Crème Change Protectrice (pommade)',
            'marque': 'Mustela',
            'type_produit': 'Soin bébé',
            'problemes_cibles': 'érythème fessier,irritation,protection',
            'prix_min': 4500,
            'prix_max': 7000,
            'description': 'Crème protectrice pour le change, barrière contre l\'humidité',
            'ingredients_actifs': 'Oxyde de zinc, Avocat Perséose, Cire d\'abeille'
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
        {
            'nom': 'Masque Purifiant Argile',
            'marque': 'Vichy',
            'type_produit': 'Masque',
            'problemes_cibles': 'peau grasse,pores dilatés,impuretés,éclat',
            'prix_min': 8000,
            'prix_max': 12000,
            'description': "Masque purifiant à l'argile volcanique pour éliminer l'excès de sébum",
            'ingredients_actifs': 'Argile volcanique, Eau volcanique, Zinc'
        },
        {
            'nom': 'Gommage Doux Exfoliant',
            'marque': 'La Roche-Posay',
            'type_produit': 'Gommage',
            'problemes_cibles': 'grain de peau,rugosité,éclat,renouvellement',
            'prix_min': 9000,
            'prix_max': 13500,
            'description': 'Gommage physiologique ultra-fin pour un renouvellement doux',
            'ingredients_actifs': 'Micro-particules, LHA, Eau thermale'
        },
        {
            'nom': 'Serum Hydratant B5',
            'marque': 'SkinCeuticals (ou équivalent)',
            'type_produit': 'Sérum hydratant',
            'problemes_cibles': 'déshydratation,peau terne,cicatrisation,réparation',
            'prix_min': 22000,
            'prix_max': 32000,
            'description': "Sérum intensif à l'acide hyaluronique pour repulper la peau",
            'ingredients_actifs': 'Acide hyaluronique, Vitamine B5, Glycérine'
        },
        {
            'nom': 'Sérum Anti-Âge Redermic R',
            'marque': 'La Roche-Posay',
            'type_produit': 'Sérum anti-âge',
            'problemes_cibles': 'rides,ridules,fermeté,élasticité,anti-âge',
            'prix_min': 20000,
            'prix_max': 28000,
            'description': 'Sérum anti-âge intensif au rétinol pur adapté aux peaux sensibles',
            'ingredients_actifs': 'Rétinol pur, Vitamine C, Eau thermale'
        },
        {
            'nom': 'Lotion Purifiante Astringente',
            'marque': 'Vichy',
            'type_produit': 'Lotion',
            'problemes_cibles': 'peau grasse,pores dilatés,brillance,impuretés',
            'prix_min': 8000,
            'prix_max': 12000,
            'description': 'Lotion astringente pour réguler le sébum et resserrer les pores',
            'ingredients_actifs': 'Eau volcanique, Acide salicylique, Zinc'
        },
        {
            'nom': 'Gel Anti-Boutons SOS',
            'marque': 'La Roche-Posay',
            'type_produit': 'Traitement local',
            'problemes_cibles': 'boutons,acné localisée,inflammation,cicatrisation',
            'prix_min': 10000,
            'prix_max': 15000,
            'description': 'Gel de traitement localisé pour assécher et apaiser les boutons',
            'ingredients_actifs': 'Acide salicylique, Zinc, Niacinamide'
        },
        {
            'nom': 'Huile d\'Argan Pure (100% vierge)',
            'marque': 'Bioderma / marque locale',
            'type_produit': 'Huile naturelle',
            'problemes_cibles': 'nutrition,réparation,anti-âge,cheveux',
            'prix_min': 6000,
            'prix_max': 10000,
            'description': "Huile d'argan pure pour visage, corps et cheveux (usage polyvalent)",
            'ingredients_actifs': 'Huile d\'argan 100%, Vitamine E naturelle'
        },
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
            'problemes_cibles': 'peau sensible,irritation,brûlures,cicatrisation,apaisement',
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
            'description': 'Huile de baobab pressée à froid, riche en acides gras essentiels',
            'ingredients_actifs': 'Huile de baobab, Vitamines A, D, E, Oméga 3-6-9'
        },
        {
            'nom': 'Huile de Moringa Pure',
            'marque': 'Moringa Sénégal',
            'type_produit': 'Huile végétale',
            'problemes_cibles': 'anti-âge,antioxydant,nutrition,éclat,protection,purification',
            'prix_min': 3000,
            'prix_max': 7000,
            'description': 'Huile de moringa, super-aliment africain aux propriétés nourrissantes',
            'ingredients_actifs': 'Huile de moringa, Acide oléique, Antioxydants naturels'
        },
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
            'ingredients_actifs': 'Poudre de feuilles de neem, Argile verte, Miel'
        },
        {
            'nom': 'Gel Nettoyant Visage Anti-Acné',
            'marque': 'Neutrogena',
            'type_produit': 'Nettoyant',
            'problemes_cibles': 'acné,points noirs,excès de sébum',
            'prix_min': 6500,
            'prix_max': 9000,
            'description': 'Gel nettoyant à l’acide salicylique pour réduire les imperfections.',
            'ingredients_actifs': 'Acide salicylique, glycérine'
        },
        {
            'nom': 'Crème Hydratante Légère',
            'marque': 'CeraVe',
            'type_produit': 'Hydratant',
            'problemes_cibles': 'peau sèche,barrière cutanée fragilisée',
            'prix_min': 8000,
            'prix_max': 13000,
            'description': 'Hydratant léger avec céramides pour peaux normales à sèches.',
            'ingredients_actifs': 'Céramides, acide hyaluronique'
        },
        {
            'nom': 'Crème Anti-Taches Even Tone',
            'marque': 'Urban Skin RX',
            'type_produit': 'Anti-taches',
            'problemes_cibles': 'taches noires,hyperpigmentation,teint irrégulier',
            'prix_min': 12000,
            'prix_max': 17000,
            'description': 'Traitement ciblé pour réduire l’hyperpigmentation chez les peaux noires.',
            'ingredients_actifs': 'Acide kojique, niacinamide, rétinol'
        },
        {
            'nom': 'Sérum Vitamine C 15%',
            'marque': 'The Ordinary',
            'type_produit': 'Sérum',
            'problemes_cibles': 'taches,teint terne,ridules',
            'prix_min': 9000,
            'prix_max': 15000,
            'description': 'Sérum antioxydant pour éclaircir le teint et réduire les taches.',
            'ingredients_actifs': 'Vitamine C, acide hyaluronique'
        },
        {
            'nom': 'Lait Corporel Nourrissant',
            'marque': 'Vaseline',
            'type_produit': 'Hydratant',
            'problemes_cibles': 'peau sèche,desquamation',
            'prix_min': 4500,
            'prix_max': 7000,
            'description': 'Lait hydratant avec ingrédients réparateurs.',
            'ingredients_actifs': 'Glycérine, gelée de pétrole'
        },
        {
            'nom': 'Crème Éclaircissante Naturelle',
            'marque': 'Fair & White Gold',
            'type_produit': 'Dépigmentant',
            'problemes_cibles': 'taches rebelles,hyperpigmentation',
            'prix_min': 9000,
            'prix_max': 14000,
            'description': 'Crème éclaircissante pour uniformiser le teint.',
            'ingredients_actifs': 'Acide kojique, vitamine C'
        },
        {
            'nom': 'Gel Nettoyant Exfoliant',
            'marque': 'Garnier',
            'type_produit': 'Nettoyant',
            'problemes_cibles': 'acné,points noirs,excès de sébum',
            'prix_min': 4500,
            'prix_max': 6500,
            'description': 'Gel exfoliant quotidien pour peaux jeunes et grasses.',
            'ingredients_actifs': 'Acide salicylique, charbon'
        },
        {
            'nom': 'Sérum Anti-Taches Rapid',
            'marque': 'Makari',
            'type_produit': 'Dépigmentant',
            'problemes_cibles': 'taches noires,mélasma,cicatrices acné',
            'prix_min': 15000,
            'prix_max': 25000,
            'description': 'Sérum puissant pour unifier le teint.',
            'ingredients_actifs': 'Glutathion, acide kojique'
        },
        {
            'nom': 'Crème Hydratante Ultra-Nourrissante',
            'marque': 'Nivea',
            'type_produit': 'Hydratant',
            'problemes_cibles': 'sécheresse sévère,gerçures',
            'prix_min': 3500,
            'prix_max': 5500,
            'description': 'Crème visage et corps pour peau très sèche.',
            'ingredients_actifs': 'Panthénol, glycérine'
        },
        {
            'nom': 'Lotion Purifiante',
            'marque': 'Bioderma Sébium',
            'type_produit': 'Tonique',
            'problemes_cibles': 'pores dilatés,acné,excès de sébum',
            'prix_min': 7500,
            'prix_max': 11000,
            'description': 'Tonique purifiant pour peaux grasses.',
            'ingredients_actifs': 'Acide salicylique, gluconate de zinc'
        },
        {
            'nom': 'Crème Éclaircissante Multi-Action',
            'marque': 'Carotone',
            'type_produit': 'Dépigmentant',
            'problemes_cibles': 'taches,teint foncé',
            'prix_min': 2000,
            'prix_max': 3500,
            'description': 'Crème éclaircissante à base de carotte.',
            'ingredients_actifs': 'Carotte, vitamine C'
        },
        {
            'nom': 'Sérum Niacinamide 10%',
            'marque': 'The Ordinary',
            'type_produit': 'Sérum',
            'problemes_cibles': 'taches,pores dilatés,excès de sébum',
            'prix_min': 6000,
            'prix_max': 10000,
            'description': 'Sérum régulateur de sébum et anti-imperfections.',
            'ingredients_actifs': 'Niacinamide, zinc'
        },
        {
            'nom': 'Crème Visage Unifiante',
            'marque': 'Nuhanciam',
            'type_produit': 'Anti-taches',
            'problemes_cibles': 'taches noires,teint irrégulier',
            'prix_min': 13000,
            'prix_max': 18000,
            'description': 'Crème spécialement formulée pour peaux mates et noires.',
            'ingredients_actifs': 'Vitamine C, acide azélaïque'
        },
        {
            'nom': 'Gel Nettoyant Clairisonic',
            'marque': 'Avene Cleanance',
            'type_produit': 'Nettoyant',
            'problemes_cibles': 'acné,sébum,points noirs',
            'prix_min': 7500,
            'prix_max': 11000,
            'description': 'Nettoyant doux pour peaux sensibles et grasses.',
            'ingredients_actifs': 'Eau thermale, acide salicylique'
        },
        {
            'nom': 'Lotion Corps Éclaircissante',
            'marque': 'Pr Francoise Bedon',
            'type_produit': 'Dépigmentant',
            'problemes_cibles': 'taches sur le corps,teint irrégulier',
            'prix_min': 15000,
            'prix_max': 23000,
            'description': 'Lotion éclaircissante haut de gamme.',
            'ingredients_actifs': 'Acide kojique, collagène'
        },
        {
            'nom': 'Crème Cicatrice Acné',
            'marque': 'Mederma',
            'type_produit': 'Traitement',
            'problemes_cibles': 'cicatrices,marques acné',
            'prix_min': 9000,
            'prix_max': 13000,
            'description': 'Crème pour réduire l’apparence des cicatrices.',
            'ingredients_actifs': 'Allantoïne'
        },
        {
            'nom': 'Sérum Rétinol 1%',
            'marque': 'The Ordinary',
            'type_produit': 'Sérum',
            'problemes_cibles': 'taches,ridules,texture irrégulière',
            'prix_min': 9000,
            'prix_max': 14000,
            'description': 'Sérum anti-âge puissant au rétinol.',
            'ingredients_actifs': 'Rétinol, squalane'
        },
        {
            'nom': 'Crème Solaire Peau Noire SPF 50',
            'marque': 'Black Girl Sunscreen',
            'type_produit': 'Solaire',
            'problemes_cibles': 'taches,protection uv',
            'prix_min': 12000,
            'prix_max': 18000,
            'description': 'Crème solaire invisible pour peaux foncées.',
            'ingredients_actifs': 'Avobenzone, oxybenzone'
        },
        {
            'nom': 'Crème Anti-Taches Glycolic',
            'marque': 'Labo Derm',
            'type_produit': 'Anti-taches',
            'problemes_cibles': 'taches,mélasma',
            'prix_min': 7000,
            'prix_max': 11000,
            'description': 'Crème acide glycolique pour exfoliation et éclat.',
            'ingredients_actifs': 'Acide glycolique, AHA'
        },
        {
            'nom': 'Déodorant Peau Sensible',
            'marque': 'Vichy',
            'type_produit': 'Déodorant',
            'problemes_cibles': 'transpiration,irritation aisselles',
            'prix_min': 5500,
            'prix_max': 8000,
            'description': 'Déodorant apaisant 48h.',
            'ingredients_actifs': 'Eau thermale, sels minéraux'
        },
        {
            'nom': 'Sérum Anti-Acné Rapid',
            'marque': 'Neutrogena',
            'type_produit': 'Sérum',
            'problemes_cibles': 'acné,rougeurs',
            'prix_min': 7000,
            'prix_max': 9500,
            'description': 'Sérum anti-acné rapide.',
            'ingredients_actifs': 'Acide salicylique'
        },
        {
            'nom': 'Lait Corporel Unifiant Clairissime',
            'marque': 'Clairissime',
            'type_produit': 'Dépigmentant',
            'problemes_cibles': 'taches,teint uniforme',
            'prix_min': 9000,
            'prix_max': 13000,
            'description': 'Lait unifiant pour peau noire.',
            'ingredients_actifs': 'Vitamine C, plante unifiante'
        },
        {
            'nom': 'Crème Hydratante Hyaluronique',
            'marque': 'Eucerin',
            'type_produit': 'Hydratant',
            'problemes_cibles': 'déshydratation,rides fines',
            'prix_min': 11000,
            'prix_max': 15000,
            'description': 'Crème intensive acide hyaluronique.',
            'ingredients_actifs': 'Acide hyaluronique'
        },
        {
            'nom': 'Lait Peau Sèche Shea Butter',
            'marque': 'Palmer’s',
            'type_produit': 'Hydratant',
            'problemes_cibles': 'peau sèche,desquamation',
            'prix_min': 4500,
            'prix_max': 7000,
            'description': 'Lait au beurre de karité pour peaux sèches.',
            'ingredients_actifs': 'Beurre de karité'
        },
        {
            'nom': 'Crème Éclaircissante Body Tone',
            'marque': 'Fair & White',
            'type_produit': 'Dépigmentant',
            'problemes_cibles': 'taches corps,teint irrégulier',
            'prix_min': 8500,
            'prix_max': 12000,
            'description': 'Crème éclaircissante corps.',
            'ingredients_actifs': 'Kojic acid, vitamine C'
        },
        {
            'nom': 'Masque Purifiant Charbon',
            'marque': 'Garnier',
            'type_produit': 'Masque',
            'problemes_cibles': 'pores dilatés,sébum',
            'prix_min': 1000,
            'prix_max': 2000,
            'description': 'Masque visage tissu purifiant.',
            'ingredients_actifs': 'Charbon actif'
        },
        {
            'nom': 'Lotion Anti-Taches',
            'marque': 'Nuhanciam',
            'type_produit': 'Anti-taches',
            'problemes_cibles': 'hyperpigmentation',
            'prix_min': 9000,
            'prix_max': 15000,
            'description': 'Lotion exfoliante anti-taches.',
            'ingredients_actifs': 'AHA, vitamine C'
        },
        {
            'nom': 'Huile Éclaircissante Naturelle',
            'marque': 'QEI+',
            'type_produit': 'Dépigmentant',
            'problemes_cibles': 'taches sur le corps',
            'prix_min': 12000,
            'prix_max': 18000,
            'description': 'Huile éclaircissante pour peau foncée.',
            'ingredients_actifs': 'Acide kojique, huiles naturelles'
        },
        {
            'nom': 'Gel Spot Acné',
            'marque': 'La Roche-Posay Effaclar Duo+',
            'type_produit': 'Traitement',
            'problemes_cibles': 'acné,taches post-inflammatoires',
            'prix_min': 10000,
            'prix_max': 15000,
            'description': 'Traitement anti-imperfections.',
            'ingredients_actifs': 'Niacinamide, piroctone olamine'
        },
        {
            'nom': 'Crème Vitamine E',
            'marque': 'The Body Shop',
            'type_produit': 'Hydratant',
            'problemes_cibles': 'peau sèche,teint terne',
            'prix_min': 9000,
            'prix_max': 13000,
            'description': 'Hydratant antioxydant vitaminé.',
            'ingredients_actifs': 'Vitamine E'
        },
        {
            'nom': 'Lotion AHA 8%',
            'marque': 'CeraVe',
            'type_produit': 'Exfoliant',
            'problemes_cibles': 'texture irrégulière,taches',
            'prix_min': 9000,
            'prix_max': 14000,
            'description': 'Exfoliation douce au AHA.',
            'ingredients_actifs': 'Acide glycolique, lactique'
        },
        {
            'nom': 'Shampoing Antipelliculaire',
            'marque': 'Head & Shoulders',
            'type_produit': 'Shampoing',
            'problemes_cibles': 'pellicules,démangeaisons',
            'prix_min': 3500,
            'prix_max': 5500,
            'description': 'Shampoing anti-pelliculaire.',
            'ingredients_actifs': 'Pyrithione zinc'
        },
        {
            'nom': 'Lait Carotte Éclaircissant',
            'marque': 'Carotone',
            'type_produit': 'Dépigmentant',
            'problemes_cibles': 'teint foncé,taches',
            'prix_min': 2500,
            'prix_max': 4000,
            'description': 'Lait éclaircissant à la carotte.',
            'ingredients_actifs': 'Carotte, vitamine C'
        },
        {
            'nom': 'Crème Peau Séborrhéique',
            'marque': 'Bioderma',
            'type_produit': 'Traitement',
            'problemes_cibles': 'acné,sébum',
            'prix_min': 9000,
            'prix_max': 13000,
            'description': 'Crème régulatrice pour peau grasse.',
            'ingredients_actifs': 'Zinc, salicylique'
        },
        {
            'nom': 'Sérum Glutathion Éclaircissant',
            'marque': 'Fair & White',
            'type_produit': 'Dépigmentant',
            'problemes_cibles': 'taches tenaces,éclaircissement',
            'prix_min': 12000,
            'prix_max': 18000,
            'description': 'Sérum éclaircissant haute puissance.',
            'ingredients_actifs': 'Glutathion, vitamine C'
        },
        {
            'nom': 'Huile de Coco Pure',
            'marque': 'Cocowell',
            'type_produit': 'Hydratant',
            'problemes_cibles': 'peau sèche,cheveux secs',
            'prix_min': 3500,
            'prix_max': 5000,
            'description': 'Huile multi-usages corps et cheveux.',
            'ingredients_actifs': 'Huile de coco'
        },
        {
            'nom': 'Sérum AHA 30% BHA 2%',
            'marque': 'The Ordinary',
            'type_produit': 'Exfoliant',
            'problemes_cibles': 'taches,texture,pores',
            'prix_min': 7000,
            'prix_max': 11000,
            'description': 'Peeling chimique puissant.',
            'ingredients_actifs': 'AHA, BHA'
        },
        {
            'nom': 'Crème Anti-Taches Acide Kojique',
            'marque': 'QEI+',
            'type_produit': 'Dépigmentant',
            'problemes_cibles': 'hyperpigmentation sévère',
            'prix_min': 14000,
            'prix_max': 20000,
            'description': 'Crème éclaircissante premium.',
            'ingredients_actifs': 'Acide kojique, vitamine C'
        },
        {
            'nom': 'Crème Hydratante Gel',
            'marque': 'Clinique',
            'type_produit': 'Hydratant',
            'problemes_cibles': 'peau mixte,déshydratation',
            'prix_min': 15000,
            'prix_max': 22000,
            'description': 'Hydratant gel non gras.',
            'ingredients_actifs': 'Acide hyaluronique'
        },
        {
            'nom': 'Nettoyant Peau Sensible',
            'marque': 'Cetaphil',
            'type_produit': 'Nettoyant',
            'problemes_cibles': 'sensibilité,irritation',
            'prix_min': 6500,
            'prix_max': 9500,
            'description': 'Nettoyant doux sans parfum.',
            'ingredients_actifs': 'Agents doux, glycérine'
        },
        {
            'nom': 'Sérum Acide Azélaïque',
            'marque': 'The Ordinary',
            'type_produit': 'Anti-imperfections',
            'problemes_cibles': 'taches,rougeurs',
            'prix_min': 7500,
            'prix_max': 12000,
            'description': 'Gel crème anti-taches.',
            'ingredients_actifs': 'Acide azélaïque'
        },
        {
            'nom': 'Crème Visage Carotte',
            'marque': 'L’Abidjanaise',
            'type_produit': 'Dépigmentant',
            'problemes_cibles': 'taches,teint terne',
            'prix_min': 5500,
            'prix_max': 9000,
            'description': 'Crème carotte éclaircissante.',
            'ingredients_actifs': 'Carotte, vitamine C'
        },
        {
            'nom': 'Lait Corps Ultra Hydratant',
            'marque': 'Dove',
            'type_produit': 'Hydratant',
            'problemes_cibles': 'peau sèche',
            'prix_min': 3500,
            'prix_max': 5500,
            'description': 'Lait corporel nourrissant.',
            'ingredients_actifs': 'Glycérine'
        },
        {
            'nom': 'Crème Gommante Visage',
            'marque': 'Avene',
            'type_produit': 'Gommage',
            'problemes_cibles': 'teint terne,cellules mortes',
            'prix_min': 7000,
            'prix_max': 10000,
            'description': 'Gommage doux.',
            'ingredients_actifs': 'Microbilles, eau thermale'
        },
        {
            'nom': 'Sérum Anti-Âge Liftactiv',
            'marque': 'Vichy',
            'type_produit': 'Sérum',
            'problemes_cibles': 'rides,relâchement,taches',
            'prix_min': 18000,
            'prix_max': 25000,
            'description': 'Sérum anti-âge puissant.',
            'ingredients_actifs': 'Vitamine C, peptides'
        },
        {
            'nom': 'Lotion Tonique Peau Grasse',
            'marque': 'Neutrogena',
            'type_produit': 'Tonique',
            'problemes_cibles': 'sébum,acné',
            'prix_min': 5500,
            'prix_max': 8000,
            'description': 'Tonique purifiant.',
            'ingredients_actifs': 'Acide salicylique'
        },
        {
            'nom': 'Gel Éclaircissant Intense',
            'marque': 'Makari',
            'type_produit': 'Dépigmentant',
            'problemes_cibles': 'taches rebelles',
            'prix_min': 14000,
            'prix_max': 23000,
            'description': 'Gel éclaircissant premium.',
            'ingredients_actifs': 'Glutathion, kojic acid'
        },
        {
            'nom': 'Crème Nuit Réparatrice',
            'marque': 'Nivea',
            'type_produit': 'Hydratant',
            'problemes_cibles': 'déshydratation,teint fatigue',
            'prix_min': 4000,
            'prix_max': 6500,
            'description': 'Crème nuit hydratante.',
            'ingredients_actifs': 'Vitamine E'
        },
        {
            'nom': 'Sérum Collagène',
            'marque': 'Advanced Clinicals',
            'type_produit': 'Sérum',
            'problemes_cibles': 'rides,relâchement',
            'prix_min': 8000,
            'prix_max': 11000,
            'description': 'Sérum collagène anti-âge.',
            'ingredients_actifs': 'Collagène, aloe vera'
        },
        {
            'nom': 'Crème Purifiante Peau Grasse',
            'marque': 'Ducray Keracnyl',
            'type_produit': 'Traitement',
            'problemes_cibles': 'acné sévère',
            'prix_min': 8000,
            'prix_max': 12000,
            'description': 'Crème active anti-acné.',
            'ingredients_actifs': 'Myrtacine'
        },
        {
            'nom': 'Masque Nourrissant Karité',
            'marque': 'Shea Moisture',
            'type_produit': 'Masque cheveux',
            'problemes_cibles': 'cheveux secs,cheveux crépus',
            'prix_min': 9500,
            'prix_max': 15000,
            'description': 'Masque nourrissant intense.',
            'ingredients_actifs': 'Beurre de karité, huiles naturelles'
        },
        {
            'nom': 'Sérum Hydratant Pur Hyaluronique',
            'marque': 'The Ordinary',
            'type_produit': 'Sérum',
            'problemes_cibles': 'déshydratation,peau terne',
            'prix_min': 8500,
            'prix_max': 13000,
            'description': 'Sérum hydratant à l’acide hyaluronique pour repulper la peau.',
            'ingredients_actifs': 'Acide hyaluronique'
        },
        {
            'nom': 'Lotion Après-Rasage Apaisante',
            'marque': 'La Roche-Posay',
            'type_produit': 'Soin homme',
            'problemes_cibles': 'irritation,feu du rasoir,rougeurs',
            'prix_min': 8500,
            'prix_max': 12500,
            'description': 'Baume après-rasage pour calmer et réparer la peau.',
            'ingredients_actifs': 'Allantoïne, Eau thermale'
        },
        {
            'nom': 'Crème de Nuit Rétinol Soft',
            'marque': 'Vichy',
            'type_produit': 'Anti-âge',
            'problemes_cibles': 'rides,texture irrégulière,teint terne',
            'prix_min': 20000,
            'prix_max': 28000,
            'description': 'Crème de nuit au rétinol doux pour débuter.',
            'ingredients_actifs': 'Rétinol, Niacinamide'
        },
        {
            'nom': 'Gel Nettoyant Doux Bébé',
            'marque': 'Mustela',
            'type_produit': 'Soin bébé',
            'problemes_cibles': 'peau délicate,nettoyage doux',
            'prix_min': 5000,
            'prix_max': 8000,
            'description': 'Gel nettoyant doux sans savon pour la peau de bébé.',
            'ingredients_actifs': 'Avocat Perséose, Glycérine'
        },
        {
            'nom': 'Crème Réparatrice Mains Séchées',
            'marque': 'Neutrogena Norwegian Formula',
            'type_produit': 'Hydratant',
            'problemes_cibles': 'peau sèche,mains gercées',
            'prix_min': 4000,
            'prix_max': 6500,
            'description': 'Crème ultra nourrissante pour les mains très sèches.',
            'ingredients_actifs': 'Glycérine, Panthénol'
        },
        {
            'nom': 'Sérum Anti-Taches Vitamin C + E',
            'marque': 'Garnier',
            'type_produit': 'Sérum',
            'problemes_cibles': 'taches,teint terne,éclat',
            'prix_min': 11000,
            'prix_max': 16000,
            'description': 'Sérum antioxydant pour unifier le teint et estomper les taches.',
            'ingredients_actifs': 'Vitamine C, Vitamine E'
        },
        {
            'nom': 'Lait Corporel Karité-Cacao',
            'marque': 'The Body Shop',
            'type_produit': 'Hydratant corps',
            'problemes_cibles': 'sécheresse,rugosité',
            'prix_min': 7000,
            'prix_max': 11000,
            'description': 'Lait corporel riche en beurre de karité et cacao.',
            'ingredients_actifs': 'Beurre de karité, beurre de cacao'
        },
        {
            'nom': 'Huile de Jojoba Pure',
            'marque': 'Marque locale / importée',
            'type_produit': 'Huile végétale',
            'problemes_cibles': 'sécheresse,cheveux,éclat',
            'prix_min': 4500,
            'prix_max': 9000,
            'description': 'Huile de jojoba 100% pure, multi-usages.',
            'ingredients_actifs': 'Huile de jojoba'
        },
        {
            'nom': 'Spray Fixateur Maquillage',
            'marque': 'NYX',
            'type_produit': 'Make-up',
            'problemes_cibles': 'tenue maquillage,peau brillante',
            'prix_min': 10000,
            'prix_max': 15000,
            'description': 'Spray pour fixer le maquillage toute la journée.',
            'ingredients_actifs': 'Agent fixateur, glycérine'
        },
        {
            'nom': 'Baume Lèvres Réparateur',
            'marque': 'Burt’s Bees',
            'type_produit': 'Soin lèvres',
            'problemes_cibles': 'gerçures,peau sèche des lèvres',
            'prix_min': 2500,
            'prix_max': 4500,
            'description': 'Baume naturel pour lèvres sèches et gercées.',
            'ingredients_actifs': 'Beurre de karité, huile d’amande douce'
        },
        {
            'nom': 'Crème Dépigmentante Douce',
            'marque': 'Makari',
            'type_produit': 'Dépigmentant',
            'problemes_cibles': 'taches brunes,hyperpigmentation',
            'prix_min': 13000,
            'prix_max': 20000,
            'description': 'Crème éclaircissante naturelle.',
            'ingredients_actifs': 'Glutathion, acide kojique'
        },
        {
            'nom': 'Fluide Lissant Peau Noire',
            'marque': 'Orishas',
            'type_produit': 'Soin peau noire',
            'problemes_cibles': 'grain de peau irrégulier,brillance',
            'prix_min': 8000,
            'prix_max': 14000,
            'description': 'Fluide léger pour unifier et matifier le teint.',
            'ingredients_actifs': 'Niacinamide, huile de baobab'
        },
        {
            'nom': 'Sérum Rétinol + Peptide',
            'marque': 'The Inkey List',
            'type_produit': 'Sérum anti-âge',
            'problemes_cibles': 'rides,perte de fermeté,texture',
            'prix_min': 11000,
            'prix_max': 16000,
            'description': 'Sérum anti-âge combinant rétinol et peptides.',
            'ingredients_actifs': 'Rétinol, Peptides'
        },
        {
            'nom': 'Crème Après-Soleil Réparatrice',
            'marque': 'Bioderma Photoderm After Sun',
            'type_produit': 'Soin solaire',
            'problemes_cibles': 'séchage post-soleil,irritation',
            'prix_min': 9500,
            'prix_max': 15000,
            'description': 'Crème apaisante après exposition au soleil.',
            'ingredients_actifs': 'Eau apaisante, glycérine'
        },
        {
            'nom': 'Masque Cheveux Profond Nourrissant',
            'marque': 'Cantu Shea Butter Deep Treatment Mask',
            'type_produit': 'Masque cheveux',
            'problemes_cibles': 'cheveux secs,cheveux abîmés',
            'prix_min': 9000,
            'prix_max': 14000,
            'description': 'Masque nourrissant intensif au karité.',
            'ingredients_actifs': 'Beurre de karité, huile de coco'
        },
        {
            'nom': 'Shampoing Doux Karité',
            'marque': 'African Pride Shea Miracle',
            'type_produit': 'Shampoing',
            'problemes_cibles': 'cheveux secs,cheveux crépus',
            'prix_min': 8000,
            'prix_max': 13000,
            'description': 'Shampoing nourrissant au beurre de karité.',
            'ingredients_actifs': 'Beurre de karité, huiles végétales'
        },
        {
            'nom': 'Peeling Chimique Léger 10% AHA',
            'marque': 'The Ordinary',
            'type_produit': 'Exfoliant',
            'problemes_cibles': 'teint terne,taches superficielles',
            'prix_min': 7500,
            'prix_max': 12000,
            'description': 'Peeling doux à base d’AHA pour l’éclat.',
            'ingredients_actifs': 'Acide glycolique 10%'
        },
        {
            'nom': 'Nettoyant Exfoliant Poudre',
            'marque': 'Dermalogica Daily Microfoliant',
            'type_produit': 'Nettoyant',
            'problemes_cibles': 'grain de peau,pores,teint terne',
            'prix_min': 20000,
            'prix_max': 30000,
            'description': 'Poudre nettoyante qui devient une mousse au contact de l’eau.',
            'ingredients_actifs': 'Acide salicylique, riz, enzymes de papaye'
        },
        {
            'nom': 'Sérum Peau Noire à la Vitamine C',
            'marque': 'Mame Diarra Cosmetics',
            'type_produit': 'Sérum',
            'problemes_cibles': 'taches,éclat,granularité du teint',
            'prix_min': 12000,
            'prix_max': 20000,
            'description': 'Sérum local pour peau noire avec vitamine C stable.',
            'ingredients_actifs': 'Vitamine C, niacinamide, acide citrique'
        },
        {
            'nom': 'Baume Réparateur Après Rasage',
            'marque': 'Proraso',
            'type_produit': 'Soin homme',
            'problemes_cibles': 'irritation,feu du rasoir',
            'prix_min': 8500,
            'prix_max': 13500,
            'description': 'Baume classique pour apaiser après le rasage.',
            'ingredients_actifs': 'Allantoïne, huile d’eucalyptus'
        },
        {
            'nom': 'Crème Lumière Peau Noire',
            'marque': 'Khessal',
            'type_produit': 'Dépigmentant / éclat',
            'problemes_cibles': 'teint terne,taches légères',
            'prix_min': 7000,
            'prix_max': 12000,
            'description': 'Crème locale sénégalaise pour uniformiser le teint.',
            'ingredients_actifs': 'Arbutine, jus de gingembre'
        },
        {
            'nom': 'Gel Nettoyant Dermato-pédiatrique',
            'marque': 'Mustela Stelatopia',
            'type_produit': 'Nettoyant bébé / peau atopique',
            'problemes_cibles': 'eczéma,peau sèche,irritation',
            'prix_min': 9000,
            'prix_max': 14000,
            'description': 'Gel lavant ultra doux pour peaux très sensibles / atopiques.',
            'ingredients_actifs': 'Lipides essentiels, eau de tournesol'
        },
        {
            'nom': 'Lait Corporel Complet Moringa',
            'marque': 'Moringa Sénégal',
            'type_produit': 'Hydratant corps',
            'problemes_cibles': 'sécheresse,éclat,nutrition',
            'prix_min': 4000,
            'prix_max': 8000,
            'description': 'Lait léger à l’huile de moringa.',
            'ingredients_actifs': 'Huile de moringa, vitamine E'
        },
        {
            'nom': 'Spray Hydratant Cheveux Secs',
            'marque': 'ORS Olive Oil',
            'type_produit': 'Soin cheveux',
            'problemes_cibles': 'secheresse cheveux,frizz',
            'prix_min': 7500,
            'prix_max': 12000,
            'description': 'Spray démêlant et hydratant à l’huile d’olive.',
            'ingredients_actifs': 'Huile d’olive, glycérine'
        },
        {
            'nom': 'Crème Contour Yeux Antirides',
            'marque': 'La Roche-Posay',
            'type_produit': 'Contour yeux',
            'problemes_cibles': 'rides,poches,fermeté',
            'prix_min': 15000,
            'prix_max': 22000,
            'description': 'Soin contour des yeux anti-âge.',
            'ingredients_actifs': 'Pro-rétinol, caféine'
        },
        {
            'nom': 'Huile de Baobab Corps & Cheveux',
            'marque': 'Baobab d’Afrique',
            'type_produit': 'Huile naturelle',
            'problemes_cibles': 'nutrition,réparation,vergetures',
            'prix_min': 3000,
            'prix_max': 6500,
            'description': 'Huile multi-usage pressée à froid au baobab.',
            'ingredients_actifs': 'Huile de baobab, antioxydants'
        },
        {
            'nom': 'Sérum Réparateur Cicatrices',
            'marque': 'Bio-Oil',
            'type_produit': 'Traitement cicatrice',
            'problemes_cibles': 'cicatrices,taches post-acné,stries',
            'prix_min': 13000,
            'prix_max': 21000,
            'description': 'Huile sérum pour améliorer l’apparence des cicatrices.',
            'ingredients_actifs': 'Vitamine A, E, extraits botaniques'
        },
        {
            'nom': 'Lotion Tonique Apaisante',
            'marque': 'Avene',
            'type_produit': 'Tonique',
            'problemes_cibles': 'irritation,peau sensible,rougeurs',
            'prix_min': 8500,
            'prix_max': 13000,
            'description': 'Tonique doux à l’eau thermale pour apaiser.',
            'ingredients_actifs': 'Eau thermale Avène'
        },
        {
            'nom': 'Spray Démêlant Bébé',
            'marque': 'Mustela',
            'type_produit': 'Soin cheveux bébé',
            'problemes_cibles': 'nœuds,cheveux fins',
            'prix_min': 6000,
            'prix_max': 10000,
            'description': 'Spray démêlant doux pour cheveux de bébé.',
            'ingredients_actifs': 'Extraits végétaux, glycérine'
        },
        {
            'nom': 'Crème AHA + BHA Sérum',
            'marque': 'Paula’s Choice',
            'type_produit': 'Exfoliant / anti-imperfections',
            'problemes_cibles': 'pores,grain de peau,acné,pores bouchés',
            'prix_min': 25000,
            'prix_max': 35000,
            'description': 'Sérum exfoliant double acide pour peau texturée.',
            'ingredients_actifs': 'Glycolic acid, salicylic acid'
        },
        {
            'nom': 'Masque Eclaircissant au Papaye',
            'marque': 'Papaye d’Afrique',
            'type_produit': 'Masque naturel',
            'problemes_cibles': 'teint irrégulier,taches,exfoliation douce',
            'prix_min': 2500,
            'prix_max': 5000,
            'description': 'Masque à la papaye fermentée pour clarifier.',
            'ingredients_actifs': 'Papaïne, extrait de papaye, vitamines'
        },
        {
            'nom': 'Lait Corporel Hibiscus (Bissap)',
            'marque': 'Hibiscus Sénégal',
            'type_produit': 'Hydratant corps',
            'problemes_cibles': 'éclat,antioxydant,nutrition',
            'prix_min': 1800,
            'prix_max': 4200,
            'description': 'Lait corporel à l’extrait d’hibiscus sénégalais.',
            'ingredients_actifs': 'Anthocyanes, vitamine C, beurre de karité'
        },
        {
            'nom': 'Sérum Anti-Portes Taches Localisées',
            'marque': 'La Roche-Posay Pigmentclar',
            'type_produit': 'Sérum',
            'problemes_cibles': 'taches,grain irrégulier,hyperpigmentation',
            'prix_min': 16000,
            'prix_max': 24000,
            'description': 'Sérum ciblé pour atténuer les taches et unifier le teint.',
            'ingredients_actifs': 'LHA, Niacinamide, PhE-Resorcinol'
        },
        {
            'nom': 'Crème De Nuit Hydratante Volcanique',
            'marque': 'Vichy Aqualia',
            'type_produit': 'Hydratant nuit',
            'problemes_cibles': 'déshydratation,peau terne',
            'prix_min': 14000,
            'prix_max': 20000,
            'description': 'Crème de nuit hydratante à l’eau volcanique.',
            'ingredients_actifs': 'Eau volcanique, Acide hyaluronique'
        },
        {
            'nom': 'Baume Pour Vergetures',
            'marque': 'Mustela Stretch Mark',
            'type_produit': 'Traitement',
            'problemes_cibles': 'vergetures,élasticité de la peau',
            'prix_min': 13000,
            'prix_max': 20000,
            'description': 'Baume riche pour prévenir et atténuer les vergetures.',
            'ingredients_actifs': 'Extrait d’avocat, centella asiatica'
        },
        {
            'nom': 'Gel Dermocalmant Aloe Vera',
            'marque': 'Aloe du Sénégal',
            'type_produit': 'Gel naturel',
            'problemes_cibles': 'brûlure,irritation,apaisement',
            'prix_min': 1200,
            'prix_max': 3000,
            'description': 'Gel d’aloe vera frais pour apaiser la peau.',
            'ingredients_actifs': 'Aloe vera à 99%'
        },
        {
            'nom': 'Spray Cheveux Crochets et Boucles',
            'marque': 'Mielle Organics',
            'type_produit': 'Soin cheveux',
            'problemes_cibles': 'boucles,frizz,hydratation',
            'prix_min': 9000,
            'prix_max': 14000,
            'description': 'Spray hydratant pour cheveux bouclés.',
            'ingredients_actifs': 'Huile de romarin, glycérine'
        },
        {
            'nom': 'Crème Contour Yeux Anti-Fatigue',
            'marque': 'Garnier SkinActive',
            'type_produit': 'Contour yeux',
            'problemes_cibles': 'poches,cernes,fatigue',
            'prix_min': 12000,
            'prix_max': 18000,
            'description': 'Soin frais pour réveiller le regard.',
            'ingredients_actifs': 'Caféine, excipient hydratant'
        },
        {
            'nom': 'Sérum Anti-Taches Glutathion + Arbutine',
            'marque': 'QEI+',
            'type_produit': 'Dépigmentant',
            'problemes_cibles': 'taches tenaces,hyperpigmentation',
            'prix_min': 15000,
            'prix_max': 25000,
            'description': 'Sérum éclaircissant premium pour un teint homogène.',
            'ingredients_actifs': 'Glutathion, Alpha-arbutine'
        },
        {
            'nom': 'Savon Exfoliant Sable Rose du Lac',
            'marque': 'Lac Rose Cosmétiques',
            'type_produit': 'Savon naturel',
            'problemes_cibles': 'grain de peau,éclat,exfoliation douce',
            'prix_min': 1000,
            'prix_max': 2500,
            'description': 'Savon exfoliant au sable rose du lac sénégalais.',
            'ingredients_actifs': 'Sable micronisé, sel, beure de karité'
        },
        {
            'nom': 'Peeling Plaque Niacinamide + AHA',
            'marque': 'Nuhanciam',
            'type_produit': 'Exfoliant',
            'problemes_cibles': 'taches,pores dilatés,imperfections',
            'prix_min': 20000,
            'prix_max': 30000,
            'description': 'Sérum peeling doux pour peau noire.',
            'ingredients_actifs': 'Niacinamide, AHA'
        },
        {
            'nom': 'Crème Multi-Action Éclaircissante',
            'marque': 'Makari Golden',
            'type_produit': 'Dépigmentant',
            'problemes_cibles': 'taches,éclat,éclaircissement progressif',
            'prix_min': 16000,
            'prix_max': 24000,
            'description': 'Crème haut de gamme pour un teint lumineux.',
            'ingredients_actifs': 'Glutathion, acide kojique, vitamine C'
        },
        {
            'nom': 'Crème Visage Kératolytique',
            'marque': 'SVR Clairial',
            'type_produit': 'Traitement anti-taches',
            'problemes_cibles': 'hyperpigmentation,grain irrégulier',
            'prix_min': 14000,
            'prix_max': 21000,
            'description': 'Crème kératolytique à action progressive.',
            'ingredients_actifs': 'LHA, acide glycolique'
        },
        {
            'nom': 'Baume Lèvres à la Vitamine C',
            'marque': 'The Body Shop',
            'type_produit': 'Soin lèvres',
            'problemes_cibles': 'gerçures,teint des lèvres foncé',
            'prix_min': 3000,
            'prix_max': 5500,
            'description': 'Baume réparateur vitaminé pour les lèvres.',
            'ingredients_actifs': 'Vitamine C, beurre de karité'
        },
        {
            'nom': 'Spray Réparateur Après Sport',
            'marque': 'Vichy',
            'type_produit': 'Soin corps',
            'problemes_cibles': 'rougeur,échauffement,irritation',
            'prix_min': 10000,
            'prix_max': 15000,
            'description': 'Spray apaisant pour la peau après l’effort.',
            'ingredients_actifs': 'Eau volcanique, minéraux'
        },
        {
            'nom': 'Shampoing Nutrition Noix de Coco',
            'marque': 'Creme of Nature',
            'type_produit': 'Shampoing',
            'problemes_cibles': 'cheveux secs,fragilité',
            'prix_min': 8500,
            'prix_max': 14000,
            'description': 'Shampoing nourrissant à la noix de coco.',
            'ingredients_actifs': 'Huile de noix de coco'
        },
        {
            'nom': 'Crème Anti-Taches Léger Nuhanciam',
            'marque': 'Nuhanciam',
            'type_produit': 'Dépigmentant',
            'problemes_cibles': 'taches légères,teint terne',
            'prix_min': 13000,
            'prix_max': 19000,
            'description': 'Crème éclaircissante douce pour peau sensible.',
            'ingredients_actifs': 'Alpha-arbutine, acide citrique'
        },
        {
            'nom': 'Gel Purifiant Sérum',
            'marque': 'Ducray Keracnyl Sébo- Régulateur',
            'type_produit': 'Traitement acné',
            'problemes_cibles': 'imperfections,pores bouchés',
            'prix_min': 8500,
            'prix_max': 13000,
            'description': 'Sérum gelissant pour lisser et purifier.',
            'ingredients_actifs': 'Acide salicylique, gluconate de zinc'
        },
        {
            'nom': 'Crème de Jour Hydratante SPF 30',
            'marque': 'CeraVe',
            'type_produit': 'Hydratant / solaire',
            'problemes_cibles': 'hydratation,protection UV',
            'prix_min': 14000,
            'prix_max': 21000,
            'description': 'Crème de jour qui hydrate et protège du soleil.',
            'ingredients_actifs': 'Céramides, filtres UV, acide hyaluronique'
        },
        {
            'nom': 'Lotion Tonique Clarifiante',
            'marque': 'Khessal',
            'type_produit': 'Tonique peau noire',
            'problemes_cibles': 'taches,teint irrégulier',
            'prix_min': 7000,
            'prix_max': 12000,
            'description': 'Tonique naturel pour uniformiser le teint des peaux noires.',
            'ingredients_actifs': 'Extrait de carotte, jus de gingembre'
        },
        {
            'nom': 'Masque Cou & Décolleté Raffermissant',
            'marque': 'Orishas',
            'type_produit': 'Masque corps',
            'problemes_cibles': 'relâchement,cicatrices',
            'prix_min': 9000,
            'prix_max': 15000,
            'description': 'Masque tonifiant pour le cou et le décolleté.',
            'ingredients_actifs': 'Argile, huile de baobab'
        },
        {
            'nom': 'Spray Solaire Réparateur SPF 50',
            'marque': 'La Roche-Posay Anthelios',
            'type_produit': 'Protection solaire',
            'problemes_cibles': 'brûlure solaire,photosensibilité',
            'prix_min': 16000,
            'prix_max': 23000,
            'description': 'Spray solaire haute protection pour tout le corps.',
            'ingredients_actifs': 'Mexoryl XL, Eau thermale'
        },
        {
            'nom': 'Crème de Jour Peau Noire Légère',
            'marque': 'Khessal',
            'type_produit': 'Hydratant',
            'problemes_cibles': 'sécheresse légère,éclat',
            'prix_min': 8000,
            'prix_max': 14000,
            'description': 'Crème légère adaptée aux peaux foncées.',
            'ingredients_actifs': 'Vitamines, huile de karité'
        },
        {
            'nom': 'Sérum Purifiant Peaux Grasses',
            'marque': 'SkinCeuticals Blemish + Age Defense',
            'type_produit': 'Sérum acné/anti-âge',
            'problemes_cibles': 'acné adulte,pores,texture',
            'prix_min': 30000,
            'prix_max': 42000,
            'description': 'Sérum haute performance pour peaux grasses matures.',
            'ingredients_actifs': 'LHA, dioïque, salicylique'
        },
        {
            'nom': 'Crème Anti-Taches Macro Extrait Papaye',
            'marque': 'Papaye d’Afrique',
            'type_produit': 'Dépigmentant naturel',
            'problemes_cibles': 'taches brunes,teint irrégulier',
            'prix_min': 3500,
            'prix_max': 7000,
            'description': 'Crème à base de papaye pour éclaircir naturellement.',
            'ingredients_actifs': 'Papaïne, extraits de papaye'
        },
        {
            'nom': 'Lotion Capillaire Fortifiante Baobab',
            'marque': 'Exfoliants d’Afrique',
            'type_produit': 'Soin cheveux',
            'problemes_cibles': 'cheveux clairsemés,fragilité',
            'prix_min': 2500,
            'prix_max': 6000,
            'description': 'Lotion tonique pour le cuir chevelu et les cheveux.',
            'ingredients_actifs': 'Huile de baobab, phytostérols'
        },
        {
            'nom': 'Spray Rafraîchissant Peau Noire',
            'marque': 'Fleurs du Sénégal (Eau de fleur d\'oranger)',
            'type_produit': 'Tonique / brumisateur',
            'problemes_cibles': 'brillance,irritation,apaisement',
            'prix_min': 1400,
            'prix_max': 3200,
            'description': 'Brume rafraîchissante à l’eau de fleur d’oranger.',
            'ingredients_actifs': 'Eau de fleur d’oranger, glycérine végétale'
        },
        {
            'nom': 'Crème Réparatrice Post-Procédure',
            'marque': 'La Roche-Posay Cicaplast B5',
            'type_produit': 'Soin réparateur',
            'problemes_cibles': 'irritation,plaies superficielles,post-solaire',
            'prix_min': 12000,
            'prix_max': 18000,
            'description': 'Soin apaisant et réparateur pour peau fragilisée.',
            'ingredients_actifs': 'Panthénol (B5), Madecassoside'
        },
        {
            'nom': 'Gel Nettoyant Purifiant Neem',
            'marque': 'Neem Thérapie',
            'type_produit': 'Nettoyant naturel',
            'problemes_cibles': 'acné,impuretés,bactéries',
            'prix_min': 1800,
            'prix_max': 4000,
            'description': 'Gel nettoyant antibactérien naturel au neem.',
            'ingredients_actifs': 'Huile de neem, extraits de neem'
        },
        {
            'nom': 'Sérum Eclat au Citron Vert',
            'marque': 'Agrumes du Sénégal',
            'type_produit': 'Sérum naturel',
            'problemes_cibles': 'taches,éclat,anti-oxydation',
            'prix_min': 2800,
            'prix_max': 5500,
            'description': 'Sérum local au citron vert sénégalais éclaircissant.',
            'ingredients_actifs': 'Extrait de citron vert, Vitamine C naturelle'
        },
        {
            'nom': 'Baume Réparateur Karité-Coco',
            'marque': 'Beurres Artisanaux',
            'type_produit': 'Beurre corporel',
            'problemes_cibles': 'nutrition,hydratation,protection',
            'prix_min': 2000,
            'prix_max': 4500,
            'description': 'Beurre fouetté karité et coco, texture aérienne.',
            'ingredients_actifs': 'Beurre de karité, huile de coco, vitamine E'
        },
        {
            'nom': 'Crème Soleil Naturelle Karité-Zinc SPF 30',
            'marque': 'Protection Naturelle',
            'type_produit': 'Protection solaire naturelle',
            'problemes_cibles': 'protection solaire,prévention taches,hydratation',
            'prix_min': 3500,
            'prix_max': 7000,
            'description': 'Protection solaire minérale au karité et oxyde de zinc.',
            'ingredients_actifs': 'Oxyde de zinc, beurre de karité, huile de coco'
        },
        {
            'nom': 'Sérum Régulateur Sébum & Taches',
            'marque': 'QEI+ Or Innovateur',
            'type_produit': 'Traitement peau noire',
            'problemes_cibles': 'sébum,taches,imperfections',
            'prix_min': 16000,
            'prix_max': 24000,
            'description': 'Sérum haute performance pour peaux noires à imperfections.',
            'ingredients_actifs': 'Niacinamide, arbutine, glutathion'
        },
        {
            'nom': 'Gel Chauffant Décontractant Musculaire',
            'marque': 'Voltaren / équivalent générique local',
            'type_produit': 'Soins corps',
            'problemes_cibles': 'douleurs musculaires,entorses',
            'prix_min': 9000,
            'prix_max': 15000,
            'description': 'Gel anti-inflammatoire à base de diclofénac.',
            'ingredients_actifs': 'Diclofénac'
        },
        {
            'nom': 'Lait Hydratant Cold Cream',
            'marque': 'Mustela',
            'type_produit': 'Hydratant bébé',
            'problemes_cibles': 'sécheresse, irritation, peau sensible',
            'prix_min': 7500,
            'prix_max': 11000,
            'description': 'Lait nutritif pour peau sèche du nourrisson',
            'ingredients_actifs': 'Cire d’abeille, Cold Cream, Glycérine'
        },
        {
            'nom': 'Savon Éclaircissant Carotone BSC',
            'marque': 'Carotone',
            'type_produit': 'Dépigmentant',
            'problemes_cibles': 'taches, teint terne, hyperpigmentation',
            'prix_min': 1500,
            'prix_max': 2500,
            'description': 'Savon éclaircissant à usage quotidien',
            'ingredients_actifs': 'Carotte, Vitamine C, Kojic Acid'
        },
        {
            'nom': 'Crème Solaire Kids SPF 50+',
            'marque': 'Garnier Ambre Solaire',
            'type_produit': 'Solaire',
            'problemes_cibles': 'protection UV, peau sensible enfant',
            'prix_min': 8500,
            'prix_max': 13000,
            'description': 'Haute protection solaire pour enfants',
            'ingredients_actifs': 'Filtres UVA/UVB'
        },
        {
            'nom': 'Gel Aloe Vera 99%',
            'marque': 'Fruit of the Earth',
            'type_produit': 'Hydratant apaisant',
            'problemes_cibles': 'coup de soleil, irritation, sécheresse',
            'prix_min': 5500,
            'prix_max': 8500,
            'description': 'Gel pur apaisant multi-usages',
            'ingredients_actifs': 'Aloe Barbadensis Leaf Juice'
        },
        {
            'nom': 'Huile de Ricin Pure',
            'marque': 'KTC',
            'type_produit': 'Huile végétale',
                'problemes_cibles': 'alopécie, cheveux cassants, cils rares',
            'prix_min': 2500,
            'prix_max': 4500,
            'description': 'Huile nourrissante pour cheveux et peau',
            'ingredients_actifs': 'Ricinus Communis Oil'
        },
        {
            'nom': 'Gel Nettoyant Anti-Imperfections Clean & Clear',
            'marque': 'Clean & Clear',
            'type_produit': 'Nettoyant',
            'problemes_cibles': 'acné, excès de sébum, points noirs',
            'prix_min': 4500,
            'prix_max': 6500,
            'description': 'Nettoyant anti-acné pour usage quotidien',
            'ingredients_actifs': 'Acide salicylique'
        },
        {
            'nom': 'Crème Teint Unifiant HT26',
            'marque': 'HT26',
            'type_produit': 'Unifiant',
            'problemes_cibles': 'taches, décoloration, hyperpigmentation',
            'prix_min': 11000,
            'prix_max': 18000,
            'description': 'Crème éclaircissante professionnelle',
            'ingredients_actifs': 'Acide kojique, Vitamine C'
        },
        {
            'nom': 'Lait Éclaircissant Clairissime',
            'marque': 'Clairissime',
            'type_produit': 'Dépigmentant',
            'problemes_cibles': 'taches, mélasma, teint irrégulier',
            'prix_min': 7000,
            'prix_max': 11000,
            'description': 'Lait clarifiant à action progressive',
            'ingredients_actifs': 'Kojic Acid, AHA'
        },
        {
            'nom': 'Beurre de Karité Brut',
            'marque': 'Shea Butter Ghana',
            'type_produit': 'Nutrition',
            'problemes_cibles': 'sécheresse, vergetures, irritation',
            'prix_min': 2000,
            'prix_max': 3000,
            'description': 'Beurre de karité artisanal 100% naturel',
            'ingredients_actifs': 'Vitamine A, Vitamine E, acides gras'
        },
        {
            'nom': 'Crème Anti-Tache Rapid Clair',
            'marque': 'Rapid Clair',
            'type_produit': 'Dépigmentant',
            'problemes_cibles': 'taches, hyperpigmentation sévère',
            'prix_min': 4500,
            'prix_max': 7000,
            'description': 'Crème puissante anti-taches',
            'ingredients_actifs': 'Hydroquinone 2%, AHA'
        },

        # Produits 61 - 100
        {
            'nom': 'Crème Eclaircissante Fair & White Gold',
            'marque': 'Fair & White',
            'type_produit': 'Dépigmentant',
            'problemes_cibles': 'taches, teint terne',
            'prix_min': 9000,
            'prix_max': 15000,
            'description': 'Crème clarifiante Gold',
            'ingredients_actifs': 'AHA, Vitamine C'
        },
        {
            'nom': 'Lotion Antiseptique Dettol',
            'marque': 'Dettol',
            'type_produit': 'Antiseptique',
            'problemes_cibles': 'désinfection, acné, irritations',
            'prix_min': 3500,
            'prix_max': 5500,
            'description': 'Antiseptique polyvalent pour peau et surfaces',
            'ingredients_actifs': 'Chloroxylenol'
        },
        {
            'nom': 'Crème Cicatrisante Cicalfate+',
            'marque': 'Avène',
            'type_produit': 'Réparateur',
            'problemes_cibles': 'irritation, cicatrices, peau agressée',
            'prix_min': 9000,
            'prix_max': 13000,
            'description': 'Crème réparatrice pour peaux irritées',
            'ingredients_actifs': 'Sucralfate, Cu-Zn'
        },
        {
            'nom': 'Lait Clarifiant Maxi Tone',
            'marque': 'Maxi Tone',
            'type_produit': 'Dépigmentant',
            'problemes_cibles': 'hyperpigmentation, taches',
            'prix_min': 5500,
            'prix_max': 8500,
            'description': 'Lait clarifiant à base d’AHA',
            'ingredients_actifs': 'AHA, Vitamine C'
        },
        {
            'nom': 'Exfoliant Corps Dove Exfoliating Body Polish',
            'marque': 'Dove',
            'type_produit': 'Exfoliant',
            'problemes_cibles': 'peau terne, rugosités',
            'prix_min': 6000,
            'prix_max': 9000,
            'description': 'Gommage doux pour peau lisse',
            'ingredients_actifs': 'Acides lactiques, glycérine'
        },
        {
            'nom': 'Sérum Anti-Acné 2% BHA',
            'marque': 'The Ordinary',
            'type_produit': 'Sérum',
            'problemes_cibles': 'acné, pores dilatés, points noirs',
            'prix_min': 6500,
            'prix_max': 9500,
            'description': 'Sérum acide salicylique pour peau mixte/grasse',
            'ingredients_actifs': 'Acide salicylique 2%'
        },
        {
            'nom': 'Crème Filorga Time-Filler',
            'marque': 'Filorga',
            'type_produit': 'Anti-âge',
            'problemes_cibles': 'rides, perte fermeté',
            'prix_min': 30000,
            'prix_max': 45000,
            'description': 'Crème anti-rides haut de gamme',
            'ingredients_actifs': 'Acide hyaluronique, peptides'
        },
        {
            'nom': 'Gel Lavant Surgras Uriage',
            'marque': 'Uriage',
            'type_produit': 'Nettoyant',
            'problemes_cibles': 'sécheresse, irritations',
            'prix_min': 8500,
            'prix_max': 12000,
            'description': 'Gel lavant protecteur',
            'ingredients_actifs': "Eau Thermale d'Uriage"
        },
        {
            'nom': 'Huile Jojoba Pure',
            'marque': 'Now Solutions',
            'type_produit': 'Huile végétale',
            'problemes_cibles': 'sébum, peau grasse, hydratation',
            'prix_min': 5000,
            'prix_max': 8000,
            'description': 'Huile non comédogène purifiante',
            'ingredients_actifs': 'Simmondsia Chinensis Oil'
        },
        {
            'nom': 'Crème Éclaircissante Caro White',
            'marque': 'Caro White',
            'type_produit': 'Dépigmentant',
            'problemes_cibles': 'taches, éclaircissement',
            'prix_min': 1500,
            'prix_max': 3000,
            'description': 'Crème éclaircissante à base de carotte',
            'ingredients_actifs': 'Carotte, Hydroquinone'
        },

        # Produits 71 - 100
        {
            'nom': 'Lotion Corporelle Vaseline Cocoa Butter',
            'marque': 'Vaseline',
            'type_produit': 'Hydratant',
            'problemes_cibles': 'déshydratation, peau terne',
            'prix_min': 3500,
            'prix_max': 5500,
            'description': 'Lotion nourrissante au beurre de cacao',
            'ingredients_actifs': 'Cocoa Butter, Vaseline Jelly'
        },
        {
            'nom': 'Savon Dudu Osun Noir',
            'marque': 'Dudu Osun',
            'type_produit': 'Nettoyant naturel',
            'problemes_cibles': 'acné, taches, peau grasse',
            'prix_min': 1500,
            'prix_max': 2500,
            'description': 'Savon noir africain 100% naturel',
            'ingredients_actifs': 'Beurre de karité, Aloe Vera, miel'
        },
        {
            'nom': 'Masque Visage au Charbon Garnier',
            'marque': 'Garnier',
            'type_produit': 'Masque',
            'problemes_cibles': 'peau grasse, pores, excès de sébum',
            'prix_min': 1500,
            'prix_max': 2500,
            'description': 'Masque tissu purifiant au charbon',
            'ingredients_actifs': 'Charbon actif, acide salicylique'
        },
        {
            'nom': 'Sérum Anti-Taches Even & Lovely',
            'marque': 'Even & Lovely',
            'type_produit': 'Unifiant',
            'problemes_cibles': 'taches, teint irrégulier',
            'prix_min': 2500,
            'prix_max': 4500,
            'description': 'Sérum unifiant pour peau terne',
            'ingredients_actifs': 'Vitamine B3, Vitamine C'
        },
        {
            'nom': 'Lotion Peau Sensible Biolane',
            'marque': 'Biolane',
            'type_produit': 'Bébé',
            'problemes_cibles': 'peau sèche, rougeurs',
            'prix_min': 6500,
            'prix_max': 9000,
            'description': 'Lotion douce pour bébés',
            'ingredients_actifs': 'Glycérine, actifs protecteurs'
        },
        {
            'nom': 'Sérum Retinol 1%',
            'marque': 'The Ordinary',
            'type_produit': 'Anti-âge',
            'problemes_cibles': 'rides, taches, peau terne',
            'prix_min': 7500,
            'prix_max': 11000,
            'description': 'Sérum puissant au rétinol',
            'ingredients_actifs': 'Rétinol 1%'
        },
        {
            'nom': 'Crème Anti-Vergetures Palmer’s',
            'marque': 'Palmer’s',
            'type_produit': 'Soin corps',
            'problemes_cibles': 'vergetures, sécheresse',
            'prix_min': 6000,
            'prix_max': 9000,
            'description': 'Crème raffermissante au beurre de cacao',
            'ingredients_actifs': 'Cocoa Butter, Collagène'
        },
        {
            'nom': 'Huile Argan Pure',
            'marque': 'Organic Argan',
            'type_produit': 'Huile végétale',
            'problemes_cibles': 'cheveux secs, peau déshydratée',
            'prix_min': 5500,
            'prix_max': 8000,
            'description': 'Huile nourrissante multi-usages',
            'ingredients_actifs': 'Argania Spinosa Oil'
        },
        {
            'nom': 'Crème Anti-Taches Demelan',
            'marque': 'Demelan',
            'type_produit': 'Dépigmentant médical',
            'problemes_cibles': 'taches brunes, melasma',
            'prix_min': 9000,
            'prix_max': 13500,
            'description': 'Traitement dermatologique des taches sévères',
            'ingredients_actifs': 'Kojic Acid, Glycolic Acid, Arbutin'
        },
        {
            'nom': 'Crème Pure Active Charbon',
            'marque': 'Garnier',
            'type_produit': 'Anti-acné',
            'problemes_cibles': 'acné, excès de sébum',
            'prix_min': 4500,
            'prix_max': 6500,
            'description': 'Crème purifiante au charbon',
            'ingredients_actifs': 'Charbon, Acide salicylique'
        },
        {
            'nom': 'Sérum Hydratant à l’Acide Hyaluronique 2%',
            'marque': 'The Ordinary',
            'type_produit': 'Sérum hydratant',
            'problemes_cibles': 'déshydratation, tiraillement',
            'prix_min': 6500,
            'prix_max': 9500,
            'description': 'Sérum à l’acide hyaluronique haute efficacité',
            'ingredients_actifs': 'Acide Hyaluronique, B5'
        },
        {
            'nom': 'Crème Anti-Taches Movate',
            'marque': 'Movate',
            'type_produit': 'Dépigmentant',
            'problemes_cibles': 'taches, hyperpigmentation sévère',
            'prix_min': 2000,
            'prix_max': 3500,
            'description': 'Crème éclaircissante populaire',
            'ingredients_actifs': 'Hydroquinone, Clobetasol'
        },
        {
            'nom': 'Lait Corps Nivea Natural Glow',
            'marque': 'Nivea',
            'type_produit': 'Unifiant',
            'problemes_cibles': 'teint terne, manque d’éclat',
            'prix_min': 3500,
            'prix_max': 5500,
            'description': 'Lait visage et corps pour teint uniforme',
            'ingredients_actifs': 'Vitamine C, UV filters'
        },
        {
            'nom': 'Crème Cicalfate Post-Acte',
            'marque': 'Avène',
            'type_produit': 'Réparateur',
            'problemes_cibles': 'irritations, post-peeling, rougeurs',
            'prix_min': 9000,
            'prix_max': 13000,
            'description': 'Soin apaisant post-intervention',
            'ingredients_actifs': 'Eau thermale, Sucralfate'
        },
        {
            'nom': 'Gel Nettoyant Visage Tea Tree',
            'marque': 'Thursday Plantation',
            'type_produit': 'Nettoyant',
            'problemes_cibles': 'acné, excès de sébum',
            'prix_min': 7000,
            'prix_max': 10000,
            'description': 'Gel purifiant au tea tree',
            'ingredients_actifs': 'Tea Tree Oil'
        },
        {
            'nom': 'Crème Carowhite Visage',
            'marque': 'Caro White',
            'type_produit': 'Dépigmentant',
            'problemes_cibles': 'taches, éclaircissement',
            'prix_min': 1500,
            'prix_max': 2500,
            'description': 'Crème clarifiante très utilisée',
            'ingredients_actifs': 'Carotte, Hydroquinone'
        },
        {
            'nom': 'Sérum Vitamine C 20%',
            'marque': 'MEDIX',
            'type_produit': 'Sérum',
            'problemes_cibles': 'taches, teint terne',
            'prix_min': 9000,
            'prix_max': 13000,
            'description': 'Sérum vitamine C haute concentration',
            'ingredients_actifs': 'Vitamine C, Hyaluronate'
        },
        {
            'nom': 'Crème Eucerin UreaRepair 5%',
            'nom': 'Crème UreaRepair Plus 5%',
            'marque': 'Eucerin',
            'type_produit': 'Hydratant',
            'problemes_cibles': 'peau très sèche, rugosités',
            'prix_min': 8500,
            'prix_max': 12000,
            'description': 'Crème nourrissante avec 5% d’urée',
            'ingredients_actifs': 'Urée, Céramides'
        },
        {
            'nom': 'Gel Alcoolique Mixa Bébé',
            'marque': 'Mixa',
            'type_produit': 'Hygiène bébé',
            'problemes_cibles': 'irritations, rougeurs',
            'prix_min': 4000,
            'prix_max': 6000,
            'description': 'Gel doux pour peau sensible',
            'ingredients_actifs': 'Glycérine, Cold Cream'
        },
        {
            'nom': 'Lait Éclaircissant Neutrotone',
            'marque': 'Neutrotone',
            'type_produit': 'Dépigmentant',
            'problemes_cibles': 'taches, teint irrégulier',
            'prix_min': 4500,
            'prix_max': 7000,
            'description': 'Lait clarifiant très populaire',
            'ingredients_actifs': 'Hydroquinone, Vitamine C'
        },

        # PRODUITS 111 À 150
        {
            'nom': 'Crème Topicrem Ultra-Hydratante',
            'marque': 'Topicrem',
            'type_produit': 'Hydratant',
            'problemes_cibles': 'déshydratation, tiraillement',
            'prix_min': 7500,
            'prix_max': 11000,
            'description': 'Hydratant haute tolérance',
            'ingredients_actifs': 'Glycérine, urée'
        },
        {
            'nom': 'Sérum Niacinamide 10% + Zinc 1%',
            'marque': 'The Ordinary',
            'type_produit': 'Régulateur de sébum',
            'problemes_cibles': 'taches, pores dilatés, sébum',
            'prix_min': 6500,
            'prix_max': 9500,
            'description': 'Sérum anti-imperfections',
            'ingredients_actifs': 'Niacinamide, Zinc'
        },
        {
            'nom': 'Crème HT26 Multi-Éclaircissante',
            'marque': 'HT26',
            'type_produit': 'Dépigmentant',
            'problemes_cibles': 'mélasma, taches sombres',
            'prix_min': 12000,
            'prix_max': 18000,
            'description': 'Crème éclaircissante premium',
            'ingredients_actifs': 'AHA, Vitamine C'
        },
        {
            'nom': 'Glycolic Acid 7% Toner',
            'marque': 'The Ordinary',
            'type_produit': 'Exfoliant chimique',
            'problemes_cibles': 'teint terne, texture irrégulière',
            'prix_min': 7000,
            'prix_max': 10000,
            'description': 'Lotion exfoliante très populaire',
            'ingredients_actifs': 'Acide glycolique 7%'
        },
        {
            'nom': 'Lait Clarifiant Carotis',
            'marque': 'Carotis',
            'type_produit': 'Dépigmentant',
            'problemes_cibles': 'taches, éclaircissement',
            'prix_min': 4000,
            'prix_max': 7000,
            'description': 'Lait éclaircissant à la carotte',
            'ingredients_actifs': 'Carotte, Vitamine C'
        },
        {
            'nom': 'Huile de Neem Pure',
            'marque': 'Aroma Zone',
            'type_produit': 'Huile végétale',
            'problemes_cibles': 'acné, infection, imperfections',
            'prix_min': 3500,
            'prix_max': 5500,
            'description': 'Huile purifiante et antibactérienne',
            'ingredients_actifs': 'Azadirachta indica Oil'
        },
        {
            'nom': 'Crème Hydrante Cerave SA Smoothing',
            'marque': 'CeraVe',
            'type_produit': 'Lissante',
            'problemes_cibles': 'rugosités, kératose pilaire',
            'prix_min': 9000,
            'prix_max': 14000,
            'description': 'Crème exfoliante douce',
            'ingredients_actifs': 'Acide salicylique, céramides'
        },
        {
            'nom': 'Gommage Visage Neutrogena',
            'marque': 'Neutrogena',
            'type_produit': 'Exfoliant',
            'problemes_cibles': 'peau terne, pores bouchés',
            'prix_min': 5000,
            'prix_max': 8000,
            'description': 'Gommage quotidien pour peau mixte',
            'ingredients_actifs': 'Acide salicylique'
        },
        {
            'nom': 'Savon Kojie San',
            'marque': 'Kojie San',
            'type_produit': 'Dépigmentant',
            'problemes_cibles': 'taches, éclaircissement',
            'prix_min': 2500,
            'prix_max': 4000,
            'description': 'Savon éclaircissant au kojic acid',
            'ingredients_actifs': 'Kojic Acid'
        },
        {
            'nom': 'Crème Dermatologique Betnovate',
            'marque': 'GSK',
            'type_produit': 'Corticostéroïde',
            'problemes_cibles': 'eczéma, irritation sévère',
            'prix_min': 2500,
            'prix_max': 4500,
            'description': 'Crème anti-inflammatoire puissante',
            'ingredients_actifs': 'Betaméthasone'
        },

        {
            'nom': 'Crème Fongicure',
            'marque': 'Fongicure',
            'type_produit': 'Antifongique',
            'problemes_cibles': 'mycoses, démangeaisons',
            'prix_min': 2000,
            'prix_max': 3500,
            'description': 'Crème traitante antifongique',
            'ingredients_actifs': 'Clotrimazole'
        },
        {
            'nom': 'Huile de Coco Parachute',
            'marque': 'Parachute',
            'type_produit': 'Huile',
            'problemes_cibles': 'cheveux secs, nutrition',
            'prix_min': 2500,
            'prix_max': 3500,
            'description': 'Huile de coco pure pour cheveux et peau',
            'ingredients_actifs': 'Cocos Nucifera Oil'
        },
        {
            'nom': 'Sérum Anti-Acné Bioré',
            'marque': 'Bioré',
            'type_produit': 'Anti-acné',
            'problemes_cibles': 'acné, sébum, pores',
            'prix_min': 6000,
            'prix_max': 9000,
            'description': 'Sérum purifiant efficace',
            'ingredients_actifs': 'Acide salicylique'
        },
        {
            'nom': 'Crème Éclaircissante Maxi-Light',
            'marque': 'Maxi-Light',
            'type_produit': 'Dépigmentant',
            'problemes_cibles': 'taches, hyperpigmentation',
            'prix_min': 2000,
            'prix_max': 3500,
            'description': 'Crème éclaircissante économique',
            'ingredients_actifs': 'Hydroquinone'
        },
        {
            'nom': 'Crème Visage Nivea Soft',
            'marque': 'Nivea',
            'type_produit': 'Hydratant',
            'problemes_cibles': 'sécheresse, tiraillement',
            'prix_min': 2000,
            'prix_max': 3500,
            'description': 'Crème hydratante légère',
            'ingredients_actifs': 'Glycérine, Jojoba'
        },
        {
            'nom': 'Baume à Lèvres Carmex',
            'marque': 'Carmex',
            'type_produit': 'Soin lèvres',
            'problemes_cibles': 'gerçures, sécheresse',
            'prix_min': 1500,
            'prix_max': 2500,
            'description': 'Baume réparateur très populaire',
            'ingredients_actifs': 'Beurre cacao, camphre'
        },
        {
            'nom': 'Crème Dermovate',
            'marque': 'GSK',
            'type_produit': 'Corticostéroïde',
            'problemes_cibles': 'psoriasis, démangeaisons sévères',
            'prix_min': 2500,
            'prix_max': 4500,
            'description': 'Crème dermatologique puissante',
            'ingredients_actifs': 'Clobétasol'
        },
        {
            'nom': 'Gel Nettoyant CeraVe Foaming',
            'marque': 'CeraVe',
            'type_produit': 'Nettoyant',
            'problemes_cibles': 'peau grasse, acné',
            'prix_min': 8000,
            'prix_max': 12000,
            'description': 'Nettoyant moussant aux céramides',
            'ingredients_actifs': 'Niacinamide, céramides'
        },
        {
            'nom': 'Huile de Carotte Clarifiante',
            'marque': 'Carotte Intense',
            'type_produit': 'Dépigmentant',
            'problemes_cibles': 'taches, éclat, teint irrégulier',
            'prix_min': 2500,
            'prix_max': 3500,
            'description': 'Huile clarifiante à la carotte',
            'ingredients_actifs': 'Carotte, Vitamine E'
        },
        {
            'nom': 'Crème Sebium Hydra',
            'marque': 'Bioderma',
            'type_produit': 'Hydratant',
            'problemes_cibles': 'déshydratation après traitement acné',
            'prix_min': 8500,
            'prix_max': 12000,
            'description': 'Hydratant pour peau fragilisée',
            'ingredients_actifs': 'Glycerine, Enoxolone'
        },
        {
            'nom': 'Gel Nettoyant Sébium',
            'marque': 'Bioderma',
            'type_produit': 'Nettoyant',
            'problemes_cibles': 'acné,excès de sébum,points noirs',
            'prix_min': 9000,
            'prix_max': 12500,
            'description': 'Gel non comédogène pour peaux grasses',
            'ingredients_actifs': 'Zinc, Sulfate de cuivre'
        },
        {
            'nom': 'Crème de Nuit Anti-Taches',
            'marque': 'Topicrem',
            'type_produit': 'Anti-taches',
            'problemes_cibles': 'taches,noircissement,teint terne',
            'prix_min': 8500,
            'prix_max': 12000,
            'description': 'Crème éclaircissante douce pour le soir',
            'ingredients_actifs': 'Acide glycolique, Vitamine C'
        },
        {
            'nom': 'Savon Purifiant Tea Tree',
            'marque': 'Dr Organic',
            'type_produit': 'Savon',
            'problemes_cibles': 'acné,imperfections,excès de sébum',
            'prix_min': 3500,
            'prix_max': 6000,
            'description': 'Savon antibactérien pour peau acnéique',
            'ingredients_actifs': 'Huile de Tea Tree'
        },
        {
            'nom': 'Gel Aloe Vera Pur 99%',
            'marque': 'Fruit of the Earth',
            'type_produit': 'Hydratant',
            'problemes_cibles': 'irritation,coups de soleil,rougeurs',
            'prix_min': 3000,
            'prix_max': 5500,
            'description': 'Gel apaisant multi-usage pour peaux sensibles',
            'ingredients_actifs': 'Aloe Vera'
        },
        {
            'nom': 'Serum Anti-Acné Rapid Clear',
            'marque': 'Neutrogena',
            'type_produit': 'Sérum',
            'problemes_cibles': 'acné,boutons inflammés',
            'prix_min': 7000,
            'prix_max': 11000,
            'description': 'Traitement rapide contre les boutons',
            'ingredients_actifs': 'Acide salicylique'
        },
        {
            'nom': 'Crème Éclaircissante Maxi-Tone',
            'marque': 'Fair & White',
            'type_produit': 'Dépigmentation',
            'problemes_cibles': 'hyperpigmentation,melasma,taches',
            'prix_min': 6500,
            'prix_max': 9500,
            'description': 'Crème éclaircissante populaire au Sénégal',
            'ingredients_actifs': 'Hydroquinone 2%, AHA'
        },
        {
            'nom': 'Savon Carotone',
            'marque': 'Carotone',
            'type_produit': 'Savon',
            'problemes_cibles': 'taches,teint irrégulier',
            'prix_min': 1500,
            'prix_max': 3000,
            'description': 'Savon éclaircissant au carotte oil',
            'ingredients_actifs': 'Carrot Oil, Vitamine C'
        },
        {
            'nom': 'Lotion Corps Shea Butter',
            'marque': 'Vaseline',
            'type_produit': 'Lotion',
            'problemes_cibles': 'peau sèche,deshydratation',
            'prix_min': 4500,
            'prix_max': 7500,
            'description': 'Lotion nourrissante au beurre de karité',
            'ingredients_actifs': 'Beurre de Karité'
        },
        {
            'nom': 'Gommage Corps Berry',
            'marque': 'Himalaya',
            'type_produit': 'Gommage',
            'problemes_cibles': 'cellules mortes,teint terne',
            'prix_min': 4000,
            'prix_max': 7000,
            'description': 'Exfoliant doux pour peau sèche et mixte',
            'ingredients_actifs': 'Micro-grains naturels'
        },
        {
            'nom': 'Crème Blanchissante Lait Éclaircir',
            'marque': 'Idole',
            'type_produit': 'Dépigmentation',
            'problemes_cibles': 'taches,teint terne,hyperpigmentation',
            'prix_min': 3500,
            'prix_max': 5500,
            'description': 'Crème dépigmentante légère',
            'ingredients_actifs': 'Glycérine, Concentre éclaircissant'
        },

        # ----- produits 161–170 -----

        {
            'nom': 'Huile d’Amande Douce Pure',
            'marque': 'Cooper',
            'type_produit': 'Huile',
            'problemes_cibles': 'peau sèche,eczéma,vergetures',
            'prix_min': 4500,
            'prix_max': 7000,
            'description': 'Huile hydratante pour visage et corps',
            'ingredients_actifs': 'Amande douce'
        },
        {
            'nom': 'Gel Nettoyant Pure Active',
            'marque': 'Garnier',
            'type_produit': 'Nettoyant',
            'problemes_cibles': 'acné,pores dilatés',
            'prix_min': 3500,
            'prix_max': 5500,
            'description': 'Gel anti-imperfections économique',
            'ingredients_actifs': 'Acide salicylique'
        },
        {
            'nom': 'Crème Visage Even Tone',
            'marque': 'Nivea',
            'type_produit': 'Éclaircissant',
            'problemes_cibles': 'taches,ternissement',
            'prix_min': 3500,
            'prix_max': 6000,
            'description': 'Crème visage unifiante pour peau mixte',
            'ingredients_actifs': 'Vitamine C, Glycérine'
        },
        {
            'nom': 'Sérum Dépigmentant Exclusive',
            'marque': 'Fair & White',
            'type_produit': 'Dépigmentation',
            'problemes_cibles': 'hyperpigmentation sévère',
            'prix_min': 8500,
            'prix_max': 12000,
            'description': 'Sérum puissant pour taches tenaces',
            'ingredients_actifs': 'Hydroquinone 2%, Vitamine C'
        },
        {
            'nom': 'Crème Hydratante Skin Repair',
            'marque': 'Johnson’s',
            'type_produit': 'Hydratant',
            'problemes_cibles': 'peau sèche,irritation',
            'prix_min': 3000,
            'prix_max': 5000,
            'description': 'Crème nourrissante légère',
            'ingredients_actifs': 'Beurre de karité, Glycérine'
        },
        {
            'nom': 'Savon Kojic Acid Gold',
            'marque': 'Koji White',
            'type_produit': 'Savon',
            'problemes_cibles': 'taches,teint foncé,acné',
            'prix_min': 3500,
            'prix_max': 6000,
            'description': 'Savon éclaircissant au kojic acid',
            'ingredients_actifs': 'Kojic Acid, Vitamine C'
        },
        {
            'nom': 'Lotion Dépigmentante Lemon Glow',
            'marque': 'Lemon Glow',
            'type_produit': 'Dépigmentation',
            'problemes_cibles': 'taches,teint irrégulier',
            'prix_min': 4500,
            'prix_max': 9000,
            'description': 'Lotion éclaircissante à base de citron',
            'ingredients_actifs': 'Acide citrique, Vitamine C'
        },
        {
            'nom': 'Serum Niacinamide 10% + Zinc',
            'marque': 'The Ordinary',
            'type_produit': 'Sérum',
            'problemes_cibles': 'acné,pores dilatés,taches',
            'prix_min': 8000,
            'prix_max': 12000,
            'description': 'Sérum régulateur de sébum ultra populaire',
            'ingredients_actifs': 'Niacinamide 10%, Zinc 1%'
        },
        {
            'nom': 'Huile de Coco Organique',
            'marque': 'Parachute',
            'type_produit': 'Huile',
            'problemes_cibles': 'cheveux secs,peau sèche',
            'prix_min': 2000,
            'prix_max': 3500,
            'description': 'Huile nourrissante multi-usage',
            'ingredients_actifs': 'Coco pur'
        },
        {
            'nom': 'Crème Blanchissante Rapid Clair',
            'marque': 'Rapid Clair',
            'type_produit': 'Dépigmentation',
            'problemes_cibles': 'taches,hyperpigmentation',
            'prix_min': 4000,
            'prix_max': 7000,
            'description': 'Crème éclaircissante très répandue',
            'ingredients_actifs': 'AHA, Vitamine C'
        },

        # ----- produits 171–180 -----

        {
            'nom': 'Savon Multivitaminé Teint Éclat',
            'marque': 'Clair White',
            'type_produit': 'Savon',
            'problemes_cibles': 'teint terne,taches légères',
            'prix_min': 2500,
            'prix_max': 5000,
            'description': 'Savon vitaminé pour un teint lumineux',
            'ingredients_actifs': 'Vitamine C, B3'
        },
        {
            'nom': 'Sérum Anti-Points Noirs',
            'marque': 'La Roche-Posay',
            'type_produit': 'Sérum',
            'problemes_cibles': 'points noirs,pores dilatés',
            'prix_min': 12000,
            'prix_max': 16000,
            'description': 'Sérum purifiant pour peaux grasses',
            'ingredients_actifs': 'Acide salicylique, Niacinamide'
        },
        {
            'nom': 'Crème Corps Nourrissante Cocoa Butter',
            'marque': 'Palmer’s',
            'type_produit': 'Lotion',
            'problemes_cibles': 'secheresse,vergetures',
            'prix_min': 6000,
            'prix_max': 9000,
            'description': 'Lotion hydratante au beurre de cacao',
            'ingredients_actifs': 'Cocoa Butter, Vitamine E'
        },
        {
            'nom': 'Gommage Visage Purifying',
            'marque': 'Clean & Clear',
            'type_produit': 'Gommage',
            'problemes_cibles': 'boutons,points noirs',
            'prix_min': 3000,
            'prix_max': 5500,
            'description': 'Gommage exfoliant quotidien',
            'ingredients_actifs': 'Micro-perles, Acide salicylique'
        },
        {
            'nom': 'Crème Carotte Intense',
            'marque': 'Pure Carrot',
            'type_produit': 'Éclaircissant',
            'problemes_cibles': 'taches,teint terne',
            'prix_min': 5000,
            'prix_max': 8000,
            'description': 'Crème éclaircissante à l’huile de carotte',
            'ingredients_actifs': 'Carrot Oil, Vitamine E'
        },
        {
            'nom': 'Lotion Anti-Acné Matte',
            'marque': 'Clinique',
            'type_produit': 'Lotion',
            'problemes_cibles': 'acné,brillance',
            'prix_min': 15000,
            'prix_max': 22000,
            'description': 'Lotion matifiante de très bonne qualité',
            'ingredients_actifs': 'Acide salicylique'
        },
        {
            'nom': 'Savon Dépigmentant Exclusive',
            'marque': 'Fair & White',
            'type_produit': 'Savon',
            'problemes_cibles': 'hyperpigmentation,taches',
            'prix_min': 3500,
            'prix_max': 6500,
            'description': 'Savon éclaircissant puissant',
            'ingredients_actifs': 'Hydroquinone, AHA'
        },
        {
            'nom': 'Sérum Vitamine C 20%',
            'marque': 'Dr Rashel',
            'type_produit': 'Sérum',
            'problemes_cibles': 'taches,teint terne',
            'prix_min': 3500,
            'prix_max': 6000,
            'description': 'Sérum vitaminé anti-taches',
            'ingredients_actifs': 'Vitamine C, Acide hyaluronique'
        },
        {
            'nom': 'Crème Corps Lait Glutathione',
            'marque': 'Gluta White',
            'type_produit': 'Éclaircissant',
            'problemes_cibles': 'teint foncé,taches',
            'prix_min': 7000,
            'prix_max': 12000,
            'description': 'Crème éclaircissante au glutathione',
            'ingredients_actifs': 'Glutathione, Vitamine C'
        },
        {
            'nom': 'Baume Lèvres Ultra Hydratant',
            'marque': 'EOS',
            'type_produit': 'Baume',
            'problemes_cibles': 'levres sèches,gerçures',
            'prix_min': 2500,
            'prix_max': 4500,
            'description': 'Baume nourrissant naturel',
            'ingredients_actifs': 'Beurre de karité, Huile de jojoba'
        },

        # ----- produits 181–200 -----

        {
            'nom': 'Huile de Ricin Bio',
            'marque': 'Hemani',
            'type_produit': 'Huile',
            'problemes_cibles': 'cheveux clairsemés,pousse lente',
            'prix_min': 3000,
            'prix_max': 5000,
            'description': 'Huile stimulante pour cheveux et cils',
            'ingredients_actifs': 'Ricin'
        },
        {
            'nom': 'Lait Éclaircissant Caro White',
            'marque': 'Carowhite',
            'type_produit': 'Dépigmentation',
            'problemes_cibles': 'teint foncé,taches',
            'prix_min': 2500,
            'prix_max': 4500,
            'description': 'Lait très utilisé au Sénégal',
            'ingredients_actifs': 'Carrot Oil, BHA éclaircissant'
        },
        {
            'nom': 'Crème Hydratante Soft',
            'marque': 'Nivea',
            'type_produit': 'Hydratant',
            'problemes_cibles': 'sécheresse,irritation',
            'prix_min': 2500,
            'prix_max': 4500,
            'description': 'Crème douce visage et corps',
            'ingredients_actifs': 'Jojoba, Vitamine E'
        },
        {
            'nom': 'Savon Curcuma Lightening',
            'marque': 'Himalaya',
            'type_produit': 'Savon',
            'problemes_cibles': 'taches,inflammation',
            'prix_min': 3000,
            'prix_max': 5000,
            'description': 'Savon anti-imperfections au curcuma',
            'ingredients_actifs': 'Curcuma'
        },
        {
            'nom': 'Sérum Anti-Taches Gluta 700',
            'marque': 'Saeed Ghani',
            'type_produit': 'Dépigmentation',
            'problemes_cibles': 'hyperpigmentation,taches tenaces',
            'prix_min': 5000,
            'prix_max': 8500,
            'description': 'Sérum au glutathione pour éclaircir le teint',
            'ingredients_actifs': 'Glutathione, Vitamine C'
        },
        {
            'nom': 'Lotion Vitamine E',
            'marque': 'Palmer’s',
            'type_produit': 'Hydratant',
            'problemes_cibles': 'peau sèche,vergetures',
            'prix_min': 5500,
            'prix_max': 8500,
            'description': 'Lotion nourrissante au tocophérol',
            'ingredients_actifs': 'Vitamine E'
        },
        {
            'nom': 'Crème Éclaircissante Lemon Clear',
            'marque': 'Lemon Clear',
            'type_produit': 'Éclaircissant',
            'problemes_cibles': 'taches,luminosité',
            'prix_min': 3500,
            'prix_max': 6000,
            'description': 'Crème éclaircissante à base de citron',
            'ingredients_actifs': 'Extrait de citron, Vitamine C'
        },
        {
            'nom': 'Gommage Corps Café',
            'marque': 'Organic Shop',
            'type_produit': 'Gommage',
            'problemes_cibles': 'cellules mortes,pores bouchés',
            'prix_min': 4500,
            'prix_max': 7500,
            'description': 'Gommage stimulant au café',
            'ingredients_actifs': 'Café bio'
        },
        {
            'nom': 'Crème Anti-Ride Q10',
            'marque': 'Nivea',
            'type_produit': 'Anti-âge',
            'problemes_cibles': 'rides,fatigue du visage',
            'prix_min': 6000,
            'prix_max': 9000,
            'description': 'Crème Q10 anti-âge économique',
            'ingredients_actifs': 'Coenzyme Q10'
        },
        {
            'nom': 'Sérum Hydra B5',
            'marque': 'Some By Mi',
            'type_produit': 'Sérum',
            'problemes_cibles': 'déshydratation,peau terne',
            'prix_min': 9000,
            'prix_max': 13000,
            'description': 'Sérum coréen hydratant intense',
            'ingredients_actifs': 'Acide hyaluronique, Vitamine B5'
        },
        {
            'nom': 'Crème Dépigmentante Peau Neuve',
            'marque': 'Movate',
            'type_produit': 'Dépigmentation',
            'problemes_cibles': 'taches tenaces,melasma',
            'prix_min': 2500,
            'prix_max': 4500,
            'description': 'Crème dépigmentante forte',
            'ingredients_actifs': 'Hydroquinone'
        },
        {
            'nom': 'Lait Hydratant Karité + Cacao',
            'marque': 'Queen Elisabeth',
            'type_produit': 'Lotion',
            'problemes_cibles': 'sécheresse,irritation',
            'prix_min': 3500,
            'prix_max': 5500,
            'description': 'Lait hydratant très utilisé au Sénégal',
            'ingredients_actifs': 'Beurre de karité, Beurre de cacao'
        },
        {
            'nom': 'Masque Visage Purifiant',
            'marque': 'Garnier',
            'type_produit': 'Masque',
            'problemes_cibles': 'acné,pores bouchés',
            'prix_min': 2500,
            'prix_max': 4000,
            'description': 'Masque charbon nettoyant',
            'ingredients_actifs': 'Charbon actif'
        },
        {
            'nom': 'Savon Anti-Taches Papaya',
            'marque': 'RDL',
            'type_produit': 'Savon',
            'problemes_cibles': 'taches,teint terne',
            'prix_min': 1500,
            'prix_max': 3000,
            'description': 'Savon populaire au papaye',
            'ingredients_actifs': 'Papaya extract'
        },
        {
            'nom': 'Sérum Glow Booster',
            'marque': 'Pixi',
            'type_produit': 'Sérum',
            'problemes_cibles': 'teint terne,fatigue',
            'prix_min': 12000,
            'prix_max': 16000,
            'description': 'Sérum vitaminé coup d’éclat',
            'ingredients_actifs': 'Vitamine C'
        },
        {
            'nom': 'Crème Ultra Éclaircissante Caro Light',
            'marque': 'Caro Light',
            'type_produit': 'Dépigmentation',
            'problemes_cibles': 'teint foncé,taches',
            'prix_min': 2000,
            'prix_max': 3500,
            'description': 'Crème très connue dans les quartiers au Sénégal',
            'ingredients_actifs': 'Carrot Oil, Vitamine C'
        },
        {
            'nom': 'Lotion Corps Anti-Taches Bio Balance',
            'marque': 'Bio Balance',
            'type_produit': 'Lotion',
            'problemes_cibles': 'taches,teint terne',
            'prix_min': 7500,
            'prix_max': 11000,
            'description': 'Lotion corps anti-taches naturelle',
            'ingredients_actifs': 'Niacinamide, Vitamine C'
        },
        {
            'nom': 'Crème Hydratante Water Burst',
            'marque': 'Neutrogena',
            'type_produit': 'Hydratant',
            'problemes_cibles': 'déshydratation,peau terne',
            'prix_min': 8500,
            'prix_max': 13000,
            'description': 'Crème gel hydratante très légère',
            'ingredients_actifs': 'Acide hyaluronique'
        },
        {
            'nom': 'Sérum Dépigmentant Carotis',
            'marque': 'Carotis',
            'type_produit': 'Dépigmentation',
            'problemes_cibles': 'taches,teint irrégulier',
            'prix_min': 4000,
            'prix_max': 6500,
            'description': 'Sérum éclaircissant à la carotte',
            'ingredients_actifs': 'Carrot Oil, Vitamine C'
        },
        {
            'nom': 'Huile Essentielle Tea Tree',
            'marque': 'Thursday Plantation',
            'type_produit': 'Huile',
            'problemes_cibles': 'acné,bactéries',
            'prix_min': 4500,
            'prix_max': 7000,
            'description': 'Huile essentielle anti-acné',
            'ingredients_actifs': 'Tea Tree Oil'
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