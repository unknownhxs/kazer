# 📁 KASER File Manager

Un gestionnaire de fichiers console élégant et moderne avec interface riche en emojis et support multilingue complet.

## ✨ Fonctionnalités

### 🎯 Navigation et Gestion
- **Navigation interactive** avec les touches fléchées
- **Recherche et filtres avancés** par type de fichier
- **Visualisation de fichiers** avec support Markdown professionnel
- **Éditeur de texte intégré** avec fonctionnalités avancées
- **Opérations complètes** : copier, déplacer, supprimer, renommer, créer

### 🌍 Support Multilingue
- **8 langues complètes** : Anglais, Français, Espagnol, Allemand, Japonais, Russe, Chinois, Arabe
- **Traductions globales** via fichier JSON séparé
- **Changement de langue** en temps réel
- **Interface entièrement traduite** : menus, contrôles, messages

### 🎨 Interface Moderne
- **Support Markdown** avec rendu professionnel (Rich library)
- **Caractères spéciaux** pour l'affichage console
- **Interface riche en emojis** pour une meilleure UX
- **Couleurs et formatage** automatiques
- **Navigation intuitive** avec contrôles clavier

## 🚀 Installation

### Prérequis
- Python 3.7+
- Bibliothèque Rich (optionnelle, pour le support Markdown avancé)

### Installation
```bash
# Cloner le projet
git clone https://github.com/user/kaser.git
cd kaser

# Installer les dépendances
pip install -r requirements.txt

# Optionnel : Installer Rich pour le support Markdown avancé
pip install rich
```

## 📖 Utilisation

### Lancement Simple
```bash
cd tools
python run_file_manager.py
```

### Lancement Direct
```bash
cd tools
python -c "import sys; sys.path.append('file manager'); from file_manager import FileManager; FileManager().run()"
```

## ⌨️ Raccourcis Clavier

### Navigation Interactive
| Touche | Action |
|--------|--------|
| `↑↓` | Naviguer dans la liste |
| `Enter` | Sélectionner/Entrer dans un dossier |
| `ESC` | Retour au menu principal |
| `H` | Aller au répertoire home |
| `V` | Voir le contenu d'un fichier |
| `C` | Copier un élément |
| `M` | Déplacer un élément |
| `D` | Supprimer un élément |
| `R` | Renommer un élément |
| `N` | Créer un nouveau fichier |
| `G` | Créer un nouveau dossier |
| `F` | Activer/désactiver les filtres |

### Visualisation Markdown
| Touche | Action |
|--------|--------|
| `Q` / `ESC` | Quitter la visualisation |
| `E` | Passer en mode édition |

## 🌍 Langues Supportées

| Code | Langue | Exemple |
|------|--------|---------|
| `en` | English | "Back to main menu" |
| `fr` | Français | "Retour" |
| `es` | Español | "Volver al menú principal" |
| `de` | Deutsch | "Zurück zum Hauptmenü" |
| `ja` | 日本語 | "メインメニューに戻る" |
| `ru` | Русский | "Вернуться в главное меню" |
| `zh` | 中文 | "返回主菜单" |
| `ar` | العربية | "العودة إلى القائمة الرئيسية" |

## 📁 Structure du Projet

```
kaser/
├── tools/
│   ├── file manager/           # Package principal
│   │   ├── file_manager.py    # Code principal
│   │   ├── editor.py          # Éditeur de texte
│   │   ├── translations.json  # Traductions globales
│   │   ├── data.json         # Configuration
│   │   └── __init__.py       # Package Python
│   ├── run_file_manager.py   # Script de lancement
│   └── README.md             # Documentation
├── requirements.txt          # Dépendances
└── CHANGELOG.md             # Historique des versions
```

## ⚙️ Configuration

### Fichier de Configuration (`tools/file manager/data.json`)
```json
{
    "language": "fr",
    "theme": "default",
    "show_hidden": false,
    "sort_by": "name"
}
```

### Changer la Langue
1. **Via l'application** : Paramètres → Changer la langue
2. **Via le fichier** : Modifier `"language"` dans `data.json`

## 📄 Types de Fichiers Supportés

### Visualisation Directe
- 📝 `.txt` - Fichiers texte
- 🐍 `.py` - Fichiers Python
- 📖 `.md` - Fichiers Markdown (avec rendu Rich)
- 📋 `.json` - Fichiers JSON
- 📄 `.xml` - Fichiers XML
- 🌐 `.html` - Fichiers HTML
- 🎨 `.css` - Fichiers CSS
- 🟨 `.js` - Fichiers JavaScript

### Éditeur Intégré
Tous les fichiers texte peuvent être édités avec l'éditeur intégré.

## 🛡️ Gestion d'Erreurs

- **Permissions** : Messages d'erreur clairs pour les accès refusés
- **Fichiers binaires** : Détection automatique et avertissement
- **Encodage** : Support UTF-8 avec fallback
- **Fallbacks** : Système de secours pour toutes les fonctionnalités

## 🔧 Développement

### Structure du Code
- **Architecture modulaire** avec package Python
- **Séparation claire** : code, traductions, configuration
- **Code optimisé** et maintenable
- **Documentation complète** des fonctions

### Ajout de Traductions
1. Modifier `tools/file manager/translations.json`
2. Ajouter les nouvelles clés dans toutes les langues
3. Tester avec `python run_file_manager.py`

## 📊 Statistiques

- **2,022 lignes** de code Python
- **53 fonctions** actives
- **8 langues** complètes
- **80+ clés** de traduction par langue
- **Support Markdown** professionnel avec Rich

## 🎯 Fonctionnalités Avancées

### Support Markdown
- **Rendu professionnel** avec la bibliothèque Rich
- **Couleurs automatiques** et formatage
- **Syntaxe highlighting** pour le code
- **Fallback** vers caractères spéciaux si Rich indisponible

### Système de Traduction
- **Fichier JSON global** pour toutes les traductions
- **Chargement dynamique** des langues
- **Système de fallback** en cas d'erreur
- **Maintenance facile** sans modification du code

## 📝 Changelog

Consultez l'historique complet des versions et améliorations dans le [CHANGELOG.md](CHANGELOG.md).

## 📄 Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.

## 🤝 Contribution

Les contributions sont les bienvenues ! N'hésitez pas à :
- Signaler des bugs
- Proposer de nouvelles fonctionnalités
- Ajouter des traductions
- Améliorer la documentation

## 📞 Support

Pour toute question ou problème :
- Ouvrir une issue sur GitHub
- Consulter la documentation
- Vérifier le changelog pour les dernières mises à jour

---

**Développé avec ❤️ en Python** - Interface moderne, fonctionnalités avancées, et expérience utilisateur optimale.