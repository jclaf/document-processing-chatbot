# Architecture du Chatbot

## Vue d'ensemble

Le chatbot est structuré selon une architecture modulaire et scalable.

## Composants principaux

### Models (`src/models/`)
- Définition des modèles de données
- Schémas de requêtes/réponses

### Services (`src/services/`)
- Logique métier
- Traitement des requêtes
- Interactions avec les modèles IA

### Routes (`src/routes/`)
- Points d'entrée API
- Gestion des requêtes HTTP

### Middleware (`src/middleware/`)
- Authentification
- Validation
- Logging

### Utils (`src/utils/`)
- Fonctions utilitaires
- Helpers
- Outils de traitement de texte

### Config (`src/config/`)
- Configuration de l'application
- Gestion des variables d'environnement

## Data (`data/`)

### Training
- Datasets d'entraînement
- Données brutes

### Models
- Modèles pré-entraînés
- Poids des réseaux de neurones

## Tests (`tests/`)

### Unit Tests
- Tests unitaires des fonctions isolées

### Integration Tests
- Tests d'intégration entre composants
