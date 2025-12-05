# Guide d'installation

## Prérequis

- Python 3.8+
- pip
- virtualenv (recommandé)

## Installation

1. **Cloner le projet**
   ```bash
   cd /home/jc/chatbot
   ```

2. **Créer un environnement virtuel**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # ou
   venv\Scripts\activate  # Windows
   ```

3. **Installer les dépendances**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configurer les variables d'environnement**
   ```bash
   cp .env.example .env
   # Éditer .env avec vos paramètres
   ```

5. **Lancer l'application**
   ```bash
   python src/main.py
   ```

## Développement

Pour contribuer au projet :

```bash
# Installer les dépendances de développement
pip install -r requirements.txt
pip install pytest pytest-cov black flake8

# Lancer les tests
pytest tests/

# Vérifier la qualité du code
flake8 src/
black src/
```
