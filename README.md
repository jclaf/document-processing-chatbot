# Agent RAG 

Agent conversationnel RAG permettant de garantir la Data Quality et la conformité d'un document.
## Structure du projet

```
face-recognition-system/
├── src/                    # Code source principal
│   ├── models/            # Modèles 
│   ├── services/          # Services métier
│   ├── routes/            # Routes API
│   ├── middleware/        # Middlewares
│   ├── utils/             # Fonctions utilitaires
│   ├── config/            # Configuration
│   ├── api_call.py         # Fonctions appel api 
│   ├── streamlit_app.py    # Front End
│   └── main.py            # Back End
├── data/
│   ├── training/          # Données d'entraînement
│   └── models/            # Modèles pré-entraînés
├── tests/
│   ├── unit/              # Tests unitaires
│   └── integration/       # Tests d'intégration
├── docs/                  # Documentation
├── logs/                  # Fichiers journaux
└── requirements.txt       # Dépendances Python
```

## Installation

```bash
pip install -r requirements.txt
```

## Utilisation

```bash
python src/main.py
```

## Tests

```bash
pytest tests/
```

## Documentation

Consultez [ARCHITECTURE.md](docs/ARCHITECTURE.md) pour plus de détails sur la structure du projet.
