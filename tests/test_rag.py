import pytest
import os
from io import BytesIO
from pypdf import PdfReader
from src.api_call import call_rag_openrouter
from dotenv import load_dotenv

load_dotenv()

# Définition du chemin du dossier docs par rapport au dossier tests/
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS_DIR = os.path.join(BASE_DIR, "docs/test")  # Dossier de test spécifique pour les tests unitaires

# def load_default_doc_content():
#     """Charge dynamiquement le contenu du premier document disponible dans le dossier docs."""
#     if not os.path.exists(DOCS_DIR):
#         return "not_found.pdf", "Le dossier docs/test est introuvable."
#     print('ici')
#     doc_files = os.listdir(DOCS_DIR)
#     if not doc_files:
#         return "empty.pdf", "Aucun fichier dans le dossier docs/test."
    
#     # On prend le premier fichier du dossier docs
#     default_file = doc_files[0]
#     file_path = os.path.join(DOCS_DIR, default_file)
    
#     file_content = ""
#     try:
#         if default_file.lower().endswith(".pdf"):
#             reader = PdfReader(file_path)
#             text_pages = [page.extract_text() for page in reader.pages if page.extract_text()]
#             file_content = "\n".join(text_pages)
#         else:
#             with open(file_path, "r", encoding="utf-8") as f:
#                 file_content = f.read()
                
#         return default_file, file_content
#     except Exception as e:
#         return default_file, f"Erreur de lecture du fichier : {str(e)}"

def load_all_docs_content():
    """Charge et concatène dynamiquement tous les documents du dossier docs/test."""
    if not os.path.exists(DOCS_DIR):
        return [], "Le dossier docs/test est introuvable."
    
    doc_files = [f for f in os.listdir(DOCS_DIR) if f.lower().endswith((".pdf", ".txt"))]
    if not doc_files:
        return [], "Aucun fichier supporté dans le dossier docs/test."
    
    all_contents = []
    loaded_files = []
    
    for filename in doc_files:
        file_path = os.path.join(DOCS_DIR, filename)
        try:
            if filename.lower().endswith(".pdf"):
                reader = PdfReader(file_path)
                text_pages = [page.extract_text() for page in reader.pages if page.extract_text()]
                file_content = "\n".join(text_pages)
            else:
                with open(file_path, "r", encoding="utf-8") as f:
                    file_content = f.read()
            
            # Formatage avec un séparateur clair pour chaque source
            formatted_doc = (
                f"\n==============================\n"
                f"[source_id: {filename} | Statut: Validé]\n"
                f"==============================\n"
                f"{file_content}"
            )
            all_contents.append(formatted_doc)
            loaded_files.append(filename)
            
        except Exception as e:
            all_contents.append(f"\n[Erreur de lecture sur le fichier {filename} : {str(e)}]")
            
    return loaded_files, "\n".join(all_contents)

# Chargement automatique de la source depuis le dossier docs

source_filename, file_content_text = load_all_docs_content()
# Construction dynamique du contexte injecté pour les tests
RETRIEVED_CONTEXT = (
    f"[source_id: {source_filename} | Statut: Validé]\n"
    f"{file_content_text}"
)

RETRIEVED_CONTEXT_BIG = file_content_text

# Jeu de test s'appuyant sur le contenu réel du dossier docs
# TEST_CASES = [
#     {
#         "query": "Quel est le principe de conservation des données ?",
#         "should_answer": True
#     },
#     {
#         "query": "Quel est le budget marketing de l'entreprise pour 2030 ?",
#         "should_answer": False
#     },
#     {
#         "query": "Que doit-on faire des données après leur utilisation en base active ?",
#         "should_answer": True
#     },
#     {
#         "query": "Quel est le montant exact des amendes prévues en cas de contrôle ?",
#         "should_answer": False
#     },
#     {
#         "query": "À partir de quelle date le règlement européen est-il applicable ?",
#         "should_answer": True
#     },
#     {
#         "query": "Comment configurer un serveur web sous Nginx avec ce document ?",
#         "should_answer": False
#     }
# ]

TEST_CASES_15 = [
    {
        "query": "Quelles sont les différentes étapes présentées dans ce guide de la CNIL ?",
        "should_answer": True
    },
    {
        "query": "Quel est le budget marketing de l'entreprise pour 2030 ?",
        "should_answer": False
    },
    {
        "query": "En quoi consiste l'étape 1 du guide CNIL ?",
        "should_answer": True
    },
    {
        "query": "Comment configurer un serveur web sous Nginx avec ce document ?",
        "should_answer": False
    },
    {
        "query": "Quel est l'objectif de l'étape concernant la durée de conservation des données ?",
        "should_answer": True
    },
    {
        "query": "Quel est le montant exact en euros des amendes maximales prévues par la CNIL ?",
        "should_answer": False
    },
    {
        "query": "Comment doit-on organiser le recensement des fichiers et des traitements ?",
        "should_answer": True
    },
    {
        "query": "Quelle est la recette traditionnelle de la quiche lorraine ?",
        "should_answer": False
    },
    {
        "query": "Que recommande le document en matière de sécurité des données ?",
        "should_answer": True
    },
    {
        "query": "Quel temps fait-il à Paris aujourd'hui ?",
        "should_answer": False
    },
    {
        "query": "Comment informer les personnes concernées par la collecte de leurs données ?",
        "should_answer": True
    },
    {
        "query": "Comment installer la dernière version de la bibliothèque TensorFlow en Python ?",
        "should_answer": False
    },
    {
        "query": "Quelle est la règle à suivre concernant la gestion des demandes de droits des personnes ?",
        "should_answer": True
    },
    {
        "query": "Quel est le cours actuel de l'action de l'entreprise sur les marchés financiers ?",
        "should_answer": False
    },
    {
        "query": "À partir de quelle date le règlement européen (RGPD) est-il officiellement applicable ?",
        "should_answer": True
    },
    {
        "query": "Qui a gagné la Coupe du monde de football en 1998 selon ce document ?",
        "should_answer": False
    }
]

TEST_CASES_BIG = [
    {
        "query": "Quelles sont les différentes étapes présentées dans ce guide de la CNIL ?",
        "should_answer": True
    },
    {
        "query": "Quel est le budget marketing de l'entreprise pour 2030 ?",
        "should_answer": False
    },
    {
        "query": "En quoi consiste l'étape 1 du guide CNIL ?",
        "should_answer": True
    },
    {
        "query": "Comment configurer un serveur web sous Nginx avec ce document ?",
        "should_answer": False
    },
    {
        "query": "Quel est l'objectif de l'étape concernant la durée de conservation des données ?",
        "should_answer": True
    },
    {
        "query": "Quel est le montant exact en euros des amendes maximales prévues par la CNIL ?",
        "should_answer": False
    },
    {
        "query": "Comment doit-on organiser le recensement des fichiers et des traitements ?",
        "should_answer": True
    },
    {
        "query": "Quelle est la recette traditionnelle de la quiche lorraine ?",
        "should_answer": False
    },
    {
        "query": "Que recommande le document en matière de sécurité des données ?",
        "should_answer": True
    },
    {
        "query": "Quel temps fait-il à Paris aujourd'hui ?",
        "should_answer": False
    },
    {
        "query": "Comment informer les personnes concernées par la collecte de leurs données ?",
        "should_answer": True
    },
    {
        "query": "Comment installer la dernière version de la bibliothèque TensorFlow en Python ?",
        "should_answer": False
    },
    {
        "query": "Quelle est la règle à suivre concernant la gestion des demandes de droits des personnes ?",
        "should_answer": True
    },
    {
        "query": "Quel est le cours actuel de l'action de l'entreprise sur les marchés financiers ?",
        "should_answer": False
    },
    {
        "query": "À partir de quelle date le règlement européen (RGPD) est-il officiellement applicable ?",
        "should_answer": True
    },
    {
        "query": "Qui a gagné la Coupe du monde de football en 1998 selon ce document ?",
        "should_answer": False
    },
    {
        "query": "Le système vérifie-t-il l'intégration des principes FAIR dès la phase de préparation ?",
        "should_answer": True
    },
    {
        "query": "Comment réparer un moteur de voiture diesel ?",
        "should_answer": False
    },
    {
        "query": "Un premier contrôle qualité est-il effectué dès la collecte des données pour valider les données entrantes ?",
        "should_answer": True
    },
    {
        "query": "Pour chaque traitement, l'identité du responsable de traitement et de ses services opérationnels est-elle enregistrée ?",
        "should_answer": True
    },
    {
        "query": "Quelle est la recette traditionnelle de la quiche lorraine ?",
        "should_answer": False
    },
    {
        "query": "Le système permet-il d'organiser l'approche qualité autour des six phases clés du cycle de vie des données ?",
        "should_answer": True
    },
    {
        "query": "L'utilisation des identifiants d'objets fait-elle l'objet d'une stratégie de nommage rigoureuse ?",
        "should_answer": True
    },
    {
        "query": "En quelle année a eu lieu le premier vol habité sur Mars ?",
        "should_answer": False
    },
    {
        "query": "Les rôles et responsabilités des acteurs sont-ils clairement attribués et documentés dans l'outil ?",
        "should_answer": True
    },
    {
        "query": "Le système valide-t-il que les données ouvertes sont aptes à l'utilisation prévue pour les opérations et la prise de décision ?",
        "should_answer": True
    },
    {
        "query": "Quels sont les ingrédients nécessaires pour faire un gâteau au chocolat ?",
        "should_answer": False
    },
    {
        "query": "Le système permet-il à un même utilisateur d'assumer plusieurs fonctions de gestion des données dans le cadre de projets modestes ?",
        "should_answer": True
    },
    {
        "query": "L'organisme a-t-il désigné un pilote ou un Délégué à la Protection des Données pour superviser la gouvernance ?",
        "should_answer": True
    },
    {
        "query": "Quelle est la capitale de l'Australie ?",
        "should_answer": False
    },
    {
        "query": "Les protocoles de collecte et de production des données primaires sont-ils documentés dès leur conception ?",
        "should_answer": True
    },
    {
        "query": "Comment configurer un routeur Cisco en ligne de commande ?",
        "should_answer": False
    },
    {
        "query": "Le système permet-il d'appliquer des marqueurs de qualité ou des indicateurs de précision sur les données collectées ?",
        "should_answer": True
    },
    {
        "query": "La désignation d'un DPD est-elle configurée comme obligatoire pour les organismes publics ou les suivis à grande échelle ?",
        "should_answer": True
    },
    {
        "query": "Quels sont les accords de guitare pour jouer du jazz manouche ?",
        "should_answer": False
    },
    {
        "query": "Les mesures de protection pour les données sensibles ou à caractère personnel sont-elles appliquées dès la phase de production ?",
        "should_answer": True
    },
    {
        "query": "Quel est le taux d'intérêt de la Banque Centrale Européenne aujourd'hui ?",
        "should_answer": False
    },
    {
        "query": "L'outil génère-t-il des identifiants uniques pour chaque donnée collectée afin d'assurer la traçabilité ?",
        "should_answer": True
    },
    {
        "query": "Le DPD dispose-t-il des missions d'information, de conseil, de contrôle et de coopération avec l'autorité de contrôle ?",
        "should_answer": True
    },
    {
        "query": "Comment tailler un rosier grimpant en hiver ?",
        "should_answer": False
    },
    {
        "query": "Les processus de vérification de l'intégrité et de la cohérence des données utilisent-ils des outils spécialisés ?",
        "should_answer": True
    },
    {
        "query": "Quelles sont les règles du jeu d'échecs pour effectuer un roque ?",
        "should_answer": False
    },
    {
        "query": "Les modifications et corrections apportées aux données lors de la phase d'analyse sont-elles systématiquement documentées ?",
        "should_answer": True
    },
    {
        "query": "Le pilote désigné dispose-t-il d'une lettre de mission claire et des moyens nécessaires à sa fonction ?",
        "should_answer": True
    },
    {
        "query": "Quel temps fait-il à Paris aujourd'hui ?",
        "should_answer": False
    },
    {
        "query": "Le système propose-t-il ou convertit-il les données dans des formats ouverts et pérennes ?",
        "should_answer": True
    },
    {
        "query": "Comment rédiger un poème en alexandrins sur le printemps ?",
        "should_answer": False
    },
    {
        "query": "Les jeux de données sont-ils enrichis à l'aide d'identifiants persistants, de vocabulaires contrôlés et d'ontologies disciplinaires ?",
        "should_answer": True
    },
    {
        "query": "Un registre des activités de traitement est-il tenu pour recenser l'ensemble des traitements de données personnelles ?",
        "should_answer": True
    },
    {
        "query": "Quelles sont les dimensions officielles d'un terrain de basketball ?",
        "should_answer": False
    },
    {
        "query": "L'outil prend-il en charge la documentation des méthodes selon des standards reconnus et des ontologies de provenance ?",
        "should_answer": True
    },
    {
        "query": "Comment installer le système d'exploitation Linux Ubuntu sur un vieux PC ?",
        "should_answer": False
    },
    {
        "query": "Un système de versioning est-il appliqué à tous les objets numériques manipulés ?",
        "should_answer": True
    },
    {
        "query": "Le registre capture-t-il pour chaque traitement les catégories de données personnelles traitées et les finalités poursuivies ?",
        "should_answer": True
    },
    {
        "query": "Quelle est la distance entre la Terre et la Lune en moyenne ?",
        "should_answer": False
    },
    {
        "query": "La phase de préservation garantit-elle un environnement de stockage sécurisé avec des mécanismes de redondance et de sauvegarde ?",
        "should_answer": True
    },
    {
        "query": "Quels sont les symptômes principaux de la grippe saisonnière ?",
        "should_answer": False
    },
    {
        "query": "Des tests d'accès, de récupération et d'intégrité sont-ils régulièrement exécutés pour les données sensibles stockées ?",
        "should_answer": True
    },
    {
        "query": "L'identification des acteurs internes et des prestataires sous-traitants est-elle formalisée dans le registre ?",
        "should_answer": True
    },
    {
        "query": "Comment calculer la vitesse de la lumière dans le vide ?",
        "should_answer": False
    },
    {
        "query": "La documentation des procédures de stockage est-elle maintenue à jour ?",
        "should_answer": True
    },
    {
        "query": "Quel film a remporté l'Oscar du meilleur film l'année dernière ?",
        "should_answer": False
    },
    {
        "query": "L'attribution d'identifiants pérennes est-elle automatisée ou documentée lors de la diffusion ?",
        "should_answer": True
    },
    {
        "query": "Les flux de données transfrontaliers hors de l'Union européenne sont-ils tracés avec indication de l'origine et de la destination ?",
        "should_answer": True
    },
    {
        "query": "Comment préparer un cocktail Mojito traditionnel sans alcool ?",
        "should_answer": False
    },
    {
        "query": "Les licences d'accès et de réutilisation sont-elles explicitement définies et cohérentes avec la phase de planification ?",
        "should_answer": True
    },
    {
        "query": "Quelles sont les règles fiscales pour l'achat d'un bien immobilier neuf ?",
        "should_answer": False
    },
    {
        "query": "Le système gère-t-il une politique d'authentification et d'autorisation pour les données à accès restreint ?",
        "should_answer": True
    },
    {
        "query": "La durée de conservation ou les règles de purge sont-elles définies pour chaque catégorie de données personnelles ?",
        "should_answer": True
    },
    {
        "query": "Les métadonnées descriptives sont-elles régulièrement enrichies pour s'adapter aux évolutions des standards communautaires ?",
        "should_answer": True
    },
    {
        "query": "Les mesures de sécurité techniques et organisationnelles minimisant les accès non autorisés sont-elles documentées ?",
        "should_answer": True
    },
    {
        "query": "Le dépôt s'appuie-t-il sur des entrepôts certifiés ou des infrastructures disciplinaires de confiance ?",
        "should_answer": True
    },
    {
        "query": "La priorisation des actions de mise en conformité s'appuie-t-elle sur l'analyse des risques pour les droits et libertés ?",
        "should_answer": True
    },
    {
        "query": "Les mécanismes de citation des données intègrent-ils les identifiants pour les auteurs et structures ?",
        "should_answer": True
    },
    {
        "query": "Le principe de minimisation des données est-il appliqué pour s'assurer que seules les données nécessaires sont collectées ?",
        "should_answer": True
    },
    {
        "query": "Un mécanisme d'alerte post-publication est-il prévu pour notifier les utilisateurs en cas de découverte d'anomalies de qualité ?",
        "should_answer": True
    },
    {
        "query": "La base juridique de chaque traitement est-elle formellement identifiée ?",
        "should_answer": True
    },
    {
        "query": "L'archivage à long terme prévoit-il des stratégies de migration de formats face aux évolutions technologiques ?",
        "should_answer": True
    },
    {
        "query": "Les mentions d'information destinées aux personnes concernées ont-elles été révisées pour être conformes au règlement ?",
        "should_answer": True
    },
    {
        "query": "La check-list qualité intègre-t-elle la caractérisation de la structure des données ?",
        "should_answer": True
    },
    {
        "query": "Les contrats passés avec les sous-traitants intègrent-ils des clauses strictes sur la sécurité et la confidentialité ?",
        "should_answer": True
    },
    {
        "query": "Le niveau de risque des données sensibles est-il évalué et tracé dans le système ?",
        "should_answer": True
    },
    {
        "query": "Les modalités d'exercice des droits des personnes sont-elles opérationnelles ?",
        "should_answer": True
    },
    {
        "query": "L'évaluation de la qualité des données couvre-t-elle les sept dimensions de la check-list ?",
        "should_answer": True
    },
    {
        "query": "Le système identifie-t-il spécifiquement les traitements sensibles tels que la santé ou les infractions ?",
        "should_answer": True
    },
    {
        "query": "La dimension de pertinence vérifie-t-elle que chaque phénomène observé dispose d'une ou plusieurs valeurs représentatives ?",
        "should_answer": True
    },
    {
        "query": "Les traitements impliquant une surveillance systématique ou du profilage font-ils l'objet d'une vigilance accrue ?",
        "should_answer": True
    },
    {
        "query": "La dimension de précision évalue-t-elle si le niveau de granularité reflète fidèlement les variations observées ?",
        "should_answer": True
    },
    {
        "query": "Les transferts de données hors UE vers des pays non reconnus comme adéquats sont-ils encadrés par des outils juridiques ?",
        "should_answer": True
    },
    {
        "query": "La dimension d'adéquation s'assure-t-elle que les attributs correspondent réellement à la réalité du phénomène mesuré ?",
        "should_answer": True
    },
    {
        "query": "Une étude d'impact sur la protection des données est-elle déclenchée avant la mise en œuvre de traitements à haut risque ?",
        "should_answer": True
    },
    {
        "query": "La dimension de couverture contrôle-t-elle l'absence de valeurs manquantes sur les attributs attendus ?",
        "should_answer": True
    },
    {
        "query": "L'étude d'impact contient-elle une description détaillée du traitement, de ses finalités et de sa proportionnalité ?",
        "should_answer": True
    },
    {
        "query": "La dimension de cohérence détecte-t-elle les contradictions internes ou l'incompatibilité avec des sources connexes ?",
        "should_answer": True
    },
    {
        "query": "L'évaluation des risques utilise-t-elle les guides et catalogues de bonnes pratiques de la CNIL ?",
        "should_answer": True
    },
    {
        "query": "Le niveau global de conformité aux principes FAIR peut-il être évalué et mesuré via des modèles de maturité ?",
        "should_answer": True
    },
    {
        "query": "Les mesures correctrices issues de l'étude d'impact permettent-elles de ramener les risques à un niveau acceptable ?",
        "should_answer": True
    },
    {
        "query": "Les métadonnées sont-elles reconnues et traitées par le système comme un type spécifique de données ?",
        "should_answer": True
    },
    {
        "query": "Des processus internes garantissent-ils la protection des données dès la conception ?",
        "should_answer": True
    },
    {
        "query": "Le critère de précision vérifie-t-il si les données représentent correctement l'entité ou l'événement du monde réel ?",
        "should_answer": True
    },
    {
        "query": "Un plan de formation et de sensibilisation des collaborateurs à la remontée d'incidents est-il en place ?",
        "should_answer": True
    },
    {
        "query": "Le système applique-t-il un équilibre entre l'exactitude des données et leur coût de production ou de maintenance ?",
        "should_answer": True
    },
    {
        "query": "Le système de gestion des réclamations permet-il de répondre aux demandes d'exercice des droits par voie électronique ?",
        "should_answer": True
    },
    {
        "query": "Le critère de cohérence détecte-t-il la présence de déclarations contradictoires issues de sources agrégées ?",
        "should_answer": True
    },
    {
        "query": "Un processus de gestion des violations de données est-il opérationnel pour notifier l'autorité de contrôle dans les délais ?",
        "should_answer": True
    },
    {
        "query": "Une description de métadonnées contenant une date de modification antérieure à sa date de création est-elle signalée comme erreur ?",
        "should_answer": True
    },
    {
        "query": "Le dossier de documentation de la conformité regroupe-t-il le registre, les rapports et les cadres de transferts ?",
        "should_answer": True
    },
    {
        "query": "Le critère de disponibilité vérifie-t-il la persistance à long terme des liens d'accès aux jeux de données ?",
        "should_answer": True
    },
    {
        "query": "Les preuves de recueil du consentement et les modèles de mentions d'information sont-ils actualisés régulièrement ?",
        "should_answer": True
    },
    {
        "query": "L'exhaustivité des données garantit-elle la présence de tous les points de données nécessaires à l'application cible ?",
        "should_answer": True
    },
    {
        "query": "Le système vérifie-t-il la présence d'éléments obligatoires dans les métadonnées pour éviter les erreurs d'exhaustivité ?",
        "should_answer": True
    },
    {
        "query": "Le critère de conformité s'assure-t-il du respect des normes et standards en vigueur ?",
        "should_answer": True
    },
    {
        "query": "Le système permet-il de définir et publier des vocabulaires locaux en l'absence de norme standard ?",
        "should_answer": True
    },
    {
        "query": "Le critère de crédibilité évalue-t-il si les données proviennent de sources officielles et d'organismes de confiance ?",
        "should_answer": True
    },
    {
        "query": "Le critère de traitabilité mesure-t-il la capacité des données à être comprises et traitées par des procédés automatisés ?",
        "should_answer": True
    },
    {
        "query": "Les dates et heures sont-elles exprimées selon la syntaxe standard plutôt qu'en texte libre pour garantir la traitabilité ?",
        "should_answer": True
    },
    {
        "query": "Le critère de pertinence vérifie-t-il que le jeu de données contient la quantité appropriée d'informations ?",
        "should_answer": True
    },
    {
        "query": "Le critère de ponctualité évalue-t-il si les données reflètent l'état actuel et sont mises à disposition rapidement ?",
        "should_answer": True
    },
    {
        "query": "Les recommandations pour la publication de données ouvertes liées exigent-elles d'identifier clairement les jeux de données ?",
        "should_answer": True
    },
    {
        "query": "Le modèle de données est-il conçu de manière objective et indépendante des applications ?",
        "should_answer": True
    },
    {
        "query": "Les métadonnées de base obligatoires sont-elles systématiquement exigées ?",
        "should_answer": True
    },
    {
        "query": "Le système bloque-t-il la publication accidentelle d'informations personnelles identifiables ?",
        "should_answer": True
    },
    {
        "query": "Le système s'assure-t-il que les objets sont décrits à l'aide de vocabulaires standard modulaires ?",
        "should_answer": True
    },
    {
        "query": "Les données sources sont-elles converties en représentations de données liées structurées ?",
        "should_answer": True
    },
    {
        "query": "Le portail fournit-il des descriptions textuelles lisibles par l'humain en plus des formats pour machine ?",
        "should_answer": True
    },
    {
        "query": "L'accès aux données est-il offert via des interfaces modernes telles que des API ou des points de terminaison dédiés ?",
        "should_answer": True
    },
    {
        "query": "L'indication d'une licence claire et explicite est-elle un prérequis obligatoire pour chaque jeu de données publié ?",
        "should_answer": True
    },
    {
        "query": "La publication des données sur des domaines institutionnels officiels renforce-t-elle la perception de confiance ?",
        "should_answer": True
    },
    {
        "query": "Le système intègre-t-il un mécanisme de feedback permettant aux utilisateurs de signaler des erreurs ?",
        "should_answer": True
    },
    {
        "query": "Le référentiel des bonnes pratiques pour les données ouvertes est-il pris en compte pour les licences ?",
        "should_answer": True
    },
    {
        "query": "Les droits d'usage sont-ils fournis pour une période illimitée par défaut dans les métadonnées de licence ?",
        "should_answer": True
    },
    {
        "query": "Le système vérifie-t-il que chaque jeu de données est accompagné d'un résumé de licence ?",
        "should_answer": True
    },
    {
        "query": "La syntaxe des vocabulaires utilisés à l'intérieur d'un jeu de données est-elle validée automatiquement ?",
        "should_answer": True
    },
    {
        "query": "Chaque fichier téléchargeable indique-t-il explicitement son format et le jeu de caractères utilisé ?",
        "should_answer": True
    },
    {
        "query": "Le format d'au moins un fichier de diffusion est-il garanti sous un format ouvert et non propriétaire ?",
        "should_answer": True
    },
    {
        "query": "La maintenance continue des métadonnées et des liens persistants est-elle assurée pour éviter les erreurs d'accès ?",
        "should_answer": True
    }
]

# Suivi global pour le calcul de la précision
eval_stats = {"success": 0, "total": len(TEST_CASES_BIG)}

@pytest.fixture(scope="session", autouse=True)
def print_accuracy_summary():
    """Affiche le pourcentage global à la fin de l'exécution de pytest."""
    yield
    accuracy = (eval_stats["success"] / eval_stats["total"]) * 100
    print(f"\n\n>>> Précision globale de l'agent : {accuracy:.2f}% <<<\n")

@pytest.mark.parametrize("test", TEST_CASES_BIG)
def test_rag(test):
    """Teste la précision de l'agent en utilisant le contenu réel des fichiers du dossier docs."""
    response = call_rag_openrouter(
        query=test["query"],
        retrieved_context=RETRIEVED_CONTEXT_BIG,
        api_key=os.getenv("OPENROUTER_API_KEY")
    )

    if test["should_answer"]:
        is_correct = "Information non disponible dans les sources conformes" not in response
        if is_correct:
            eval_stats["success"] += 1
        assert is_correct, (
            f"Échec (Faux négatif) sur la question : '{test['query']}'\nRéponse obtenue : {response}"
        )
    else:
        is_correct = "Information non disponible dans les sources conformes" in response
        if is_correct:
            eval_stats["success"] += 1
        assert is_correct,  (
            f"Échec (Hallucination) sur la question : '{test['query']}'\nRéponse obtenue : {response}"
        )
        