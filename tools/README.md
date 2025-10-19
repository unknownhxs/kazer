# 📁 KASER File Manager - Tools

Ce dossier contient les outils et le code source du gestionnaire de fichiers KASER.

## 🏗️ Structure du Projet

```
tools/
├── file manager/           # Package principal du gestionnaire
│   ├── __init__.py        # Initialisation du package
│   ├── file_manager.py    # Classe principale du gestionnaire
│   ├── editor.py          # Éditeur de texte intégré
│   ├── translations.json  # Traductions globales (8 langues)
│   ├── data.json          # Fichier de configuration
│   └── generate_translations.py  # Générateur de traductions (utilitaire)
├── run_file_manager.py    # Script de lancement facile
└── README.md              # Ce fichier
```

## 🚀 Démarrage Rapide

### Méthode 1: Utiliser le lanceur (Recommandé)
```bash
cd tools
python run_file_manager.py
```

### Méthode 2: Import direct
```bash
cd tools
python -c "import sys; sys.path.append('file manager'); from file_manager import FileManager; FileManager().run()"
```

## 🌍 Support Multilingue

Le gestionnaire supporte **8 langues** avec traduction complète de l'interface :

- 🇺🇸 **English (en)** - Langue par défaut
- 🇫🇷 **Français (fr)** - Français
- 🇪🇸 **Español (es)** - Espagnol  
- 🇩🇪 **Deutsch (de)** - Allemand
- 🇯🇵 **日本語 (ja)** - Japonais
- 🇷🇺 **Русский (ru)** - Russe
- 🇨🇳 **中文 (zh)** - Chinois
- 🇸🇦 **العربية (ar)** - Arabe

## ⚙️ Configuration

La configuration est stockée dans `file manager/data.json` :

```json
{
    "language": "fr",
    "theme": "default", 
    "show_hidden": false,
    "sort_by": "name"
}
```

### Changer de Langue

1. **Via l'application** : Paramètres → Changer la langue
2. **Via le fichier de configuration** : Modifier `file manager/data.json` et changer la valeur `"language"`

Codes de langue supportés :
- `en` - English
- `fr` - Français  
- `es` - Español
- `de` - Deutsch
- `ja` - 日本語
- `ru` - Русский
- `zh` - 中文
- `ar` - العربية

## ✨ Fonctionnalités

- **📂 Navigation** : Parcourir les répertoires avec indicateurs emoji
- **🔄 Opérations sur fichiers** : Copier, déplacer, supprimer, renommer
- **👁️ Visualisation de contenu** : Voir le contenu des fichiers texte directement
- **📄 Gestion de fichiers** : Créer de nouveaux fichiers et répertoires
- **🎯 Interface conviviale** : Interface à menus avec options numérotées et emojis
- **🌍 Multi-plateforme** : Fonctionne sur Windows, Linux et macOS
- **🛡️ Opérations sécurisées** : Invites de confirmation pour les opérations destructives
- **🎨 Interface élégante** : Interface riche en emojis pour une meilleure expérience visuelle
- **📊 Icônes intelligentes** : Différents emojis pour différents types de fichiers
- **🌐 Multi-langue** : Traduction complète de l'interface en 8 langues
- **📖 Support Markdown** : Rendu professionnel avec la bibliothèque Rich

## ⌨️ Raccourcis Clavier

### Mode de Navigation Interactive (Recommandé)
- `↑↓` - Naviguer dans les fichiers et dossiers
- `Enter` - Sélectionner un dossier ou afficher les options de fichier
- `ESC` - Retour au menu principal
- `H` - Aller au répertoire home
- `V` - Voir le contenu du fichier sélectionné
- `D` - Supprimer l'élément sélectionné
- `C` - Copier l'élément sélectionné
- `M` - Déplacer l'élément sélectionné
- `R` - Renommer l'élément sélectionné
- `N` - Créer un nouveau fichier
- `F` - Créer un nouveau dossier

## 📄 Types de Fichiers Supportés

Le gestionnaire peut afficher le contenu des types de fichiers texte courants :
- 📝 `.txt` - Fichiers texte
- 🐍 `.py` - Fichiers Python
- 📖 `.md` - Fichiers Markdown (avec rendu Rich)
- 📋 `.json` - Fichiers JSON
- 📄 `.xml` - Fichiers XML
- 🌐 `.html` - Fichiers HTML
- 🎨 `.css` - Fichiers CSS
- 🟨 `.js` - Fichiers JavaScript

## 🚫 Gestion des Erreurs

L'application gère les erreurs courantes avec des indicateurs emoji :
- 🚫 Erreurs de permission refusée
- ❌ Erreurs de fichier non trouvé
- ❌ Erreurs d'entrée invalide
- ⚠️ Erreurs de décodage Unicode pour les fichiers binaires

## 📝 Changelog

Consultez l'historique complet des versions dans le [CHANGELOG.md](../CHANGELOG.md) à la racine du projet.

## 📄 Licence

Ce projet est open source et disponible sous licence MIT.