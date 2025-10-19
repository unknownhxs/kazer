# 📝 Changelog

Toutes les modifications notables de ce projet seront documentées dans ce fichier.

Le format est basé sur [Keep a Changelog](https://keepachangelog.com/fr/1.0.0/),
et ce projet adhère au [Versioning Sémantique](https://semver.org/lang/fr/).

## [2.0.0] - 2024-12-19

### ✨ Ajouté
- **Support Markdown professionnel** avec la bibliothèque Rich
- **Rendu coloré** et formatage automatique des fichiers Markdown
- **Syntaxe highlighting** pour les blocs de code
- **Système de traduction global** via fichier JSON séparé
- **8 langues complètes** : Anglais, Français, Espagnol, Allemand, Japonais, Russe, Chinois, Arabe
- **Caractères spéciaux** pour l'affichage console (fallback)
- **Architecture modulaire** avec package Python
- **Script de lancement** simplifié (`run_file_manager.py`)
- **Système de fallback** robuste pour toutes les fonctionnalités

### 🔧 Modifié
- **Refactorisation complète** du système de traduction
- **Optimisation du code** : suppression de 1,147 lignes inutiles
- **Amélioration de l'interface** avec emojis et formatage
- **Restructuration** des fichiers et dossiers
- **Amélioration** de la gestion d'erreurs

### 🗑️ Supprimé
- **10 fonctions inutilisées** (284 lignes de code)
- **Traductions intégrées** dans le code principal
- **Code dupliqué** et redondant
- **Fonctions obsolètes** de navigation et d'édition

### 🛡️ Sécurité
- **Gestion d'erreurs améliorée** avec fallbacks
- **Validation des entrées** utilisateur
- **Gestion des permissions** de fichiers

## [1.0.0] - 2024-12-18

### ✨ Ajouté
- **Gestionnaire de fichiers console** de base
- **Navigation interactive** avec touches fléchées
- **Opérations de base** : copier, déplacer, supprimer, renommer
- **Éditeur de texte intégré** simple
- **Support multilingue** basique (Anglais, Français)
- **Interface avec emojis** pour une meilleure UX
- **Gestion des fichiers** texte et binaires

### 🔧 Modifié
- **Interface utilisateur** améliorée
- **Gestion des erreurs** de base

### 🐛 Corrigé
- **Bugs de navigation** dans les dossiers
- **Problèmes d'encodage** des fichiers
- **Erreurs de permissions** sur certains systèmes

## [0.9.0] - 2024-12-17

### ✨ Ajouté
- **Version initiale** du gestionnaire de fichiers
- **Navigation de base** dans les dossiers
- **Affichage des fichiers** avec informations de base
- **Interface console** simple

### 🔧 Modifié
- **Structure de base** du projet

---

## 📊 Statistiques des Versions

### Version 2.0.0
- **Lignes de code** : 2,022 (réduction de 38.5%)
- **Fonctions** : 53 (optimisation de 15.9%)
- **Langues** : 8 (augmentation de 300%)
- **Fonctionnalités** : +Support Markdown, +Traductions globales

### Version 1.0.0
- **Lignes de code** : 3,290
- **Fonctions** : 63
- **Langues** : 2
- **Fonctionnalités** : Gestionnaire de base

## 🎯 Prochaines Versions

### [2.1.0] - Planifié
- **Support de plus de langues** (Italien, Portugais, etc.)
- **Thèmes personnalisables** pour l'interface
- **Plugins système** pour étendre les fonctionnalités
- **Mode sombre/clair** automatique

### [2.2.0] - Planifié
- **Support des archives** (ZIP, RAR, TAR)
- **Prévisualisation d'images** en ASCII art
- **Recherche avancée** avec expressions régulières
- **Historique de navigation**

### [3.0.0] - Vision
- **Interface graphique** optionnelle
- **Support réseau** (FTP, SFTP, SMB)
- **Synchronisation** avec services cloud
- **API REST** pour intégration

## 🔄 Types de Changements

- **✨ Ajouté** : Nouvelles fonctionnalités
- **🔧 Modifié** : Changements dans les fonctionnalités existantes
- **🗑️ Supprimé** : Fonctionnalités supprimées
- **🐛 Corrigé** : Corrections de bugs
- **🛡️ Sécurité** : Améliorations de sécurité
- **📚 Documentation** : Mises à jour de la documentation
- **⚡ Performance** : Améliorations de performance

## 📝 Format des Entrées

Chaque entrée suit ce format :
```
### Type
- **Fonctionnalité** : Description détaillée
- **Autre fonctionnalité** : Description
```

## 🏷️ Tags de Version

Les versions suivent le format [SemVer](https://semver.org/) :
- **MAJOR** : Changements incompatibles
- **MINOR** : Nouvelles fonctionnalités compatibles
- **PATCH** : Corrections de bugs compatibles

---

**Dernière mise à jour** : 19 décembre 2024
