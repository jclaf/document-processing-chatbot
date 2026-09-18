# Architecture du Chatbot

## Vue d'ensemble

Le chatbot est structuré selon une architecture modulaire et scalable.

## Composants principaux

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

## Tests (`tests/`)

### Unit Tests
- Tests unitaires des fonctions isolées

### Integration Tests
- Tests d'intégration entre composants
