# Problèmes connus

## Versions des dépendances

### Scikit-learn
Les modèles ont été entraînés avec scikit-learn version 1.0.2, mais l'API utilise actuellement la version 1.7.2. 
Cela peut causer des avertissements lors du chargement des modèles.

Solutions possibles :
1. Réentraîner les modèles avec la version actuelle de scikit-learn
2. Revenir à scikit-learn 1.0.2 dans l'environnement de production

### LightGBM
Nécessite l'installation de libomp via Homebrew sur macOS :
```bash
brew install libomp
export LDFLAGS="-L/opt/homebrew/opt/libomp/lib"
export CPPFLAGS="-I/opt/homebrew/opt/libomp/include"
```