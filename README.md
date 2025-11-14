# 🎓 Bot4Univ - Assistant Universitaire Intelligent

Une interface web moderne et intuitive pour interagir avec un assistant intelligent conçu spécifiquement pour l'écosystème universitaire, développée avec Flask.

![Bot4Univ Logo](stactic/img/logo.jpg)

## 📋 Table des matières

- [🎓 Bot4Univ - Assistant Universitaire Intelligent](#-bot4univ---assistant-universitaire-intelligent)
  - [📋 Table des matières](#-table-des-matières)
  - [🎯 À propos](#-à-propos)
  - [✨ Fonctionnalités](#-fonctionnalités)
    - [🌐 Landing Page](#-landing-page)
    - [💬 Interface de Chat](#-interface-de-chat)
    - [🎨 Design \& UX](#-design--ux)
    - [🔌 Backend \& API](#-backend--api)
  - [🏗️ Architecture](#️-architecture)
  - [📦 Prérequis](#-prérequis)
  - [🚀 Installation](#-installation)
    - [1. Cloner le repository](#1-cloner-le-repository)
    - [2. Créer un environnement virtuel](#2-créer-un-environnement-virtuel)
    - [3. Installer les dépendances](#3-installer-les-dépendances)
  - [⚙️ Configuration](#️-configuration)
    - [Variables d'environnement](#variables-denvironnement)
    - [Configuration Flask](#configuration-flask)
  - [🎮 Utilisation](#-utilisation)
    - [Démarrer l'application](#démarrer-lapplication)
    - [Endpoints disponibles](#endpoints-disponibles)
    - [Accéder à l'application](#accéder-à-lapplication)
  - [📁 Structure du projet](#-structure-du-projet)
  - [📚 Documentation](#-documentation)
    - [Documents principaux](#documents-principaux)
    - [Diagrammes techniques](#diagrammes-techniques)
    - [Design \& Mockups](#design--mockups)
  - [🛠️ Technologies utilisées](#️-technologies-utilisées)
    - [Backend](#backend)
    - [Frontend](#frontend)
    - [Design](#design)
    - [Outils de développement](#outils-de-développement)
  - [🎨 Design System](#-design-system)
    - [Palette de couleurs](#palette-de-couleurs)
    - [Typographie](#typographie)
    - [Espacements](#espacements)
  - [📱 Interface Responsive](#-interface-responsive)
    - [Breakpoints](#breakpoints)
    - [Adaptations mobiles](#adaptations-mobiles)
  - [🤝 Contribution](#-contribution)
    - [Standards de code](#standards-de-code)
  - [✅ Statut du projet](#-statut-du-projet)
    - [Fonctionnalités complétées ✅](#fonctionnalités-complétées-)
    - [En cours de développement 🚧](#en-cours-de-développement-)
  - [📝 Roadmap](#-roadmap)
    - [Phase 1 : MVP ✅ (Complété)](#phase-1--mvp--complété)
    - [Phase 2 : Production 🎯 (En cours)](#phase-2--production--en-cours)
    - [Phase 3 : Améliorations 🚀 (Futur)](#phase-3--améliorations--futur)
  - [🐛 Bugs connus](#-bugs-connus)
    - [Améliorations possibles](#améliorations-possibles)
  - [📄 Licence](#-licence)
  - [� Équipe](#-équipe)
    - [Développement](#développement)
    - [Coordination](#coordination)
    - [Contributeurs principaux](#contributeurs-principaux)
  - [📞 Contact](#-contact)
  - [🎓 Contexte académique](#-contexte-académique)
    - [Objectifs pédagogiques](#objectifs-pédagogiques)
  - [🌟 Remerciements](#-remerciements)

## 🎯 À propos

**Bot4Univ** est un assistant intelligent développé spécifiquement pour accompagner les **préinscriptions à l'Université de Douala**. Notre mission est de simplifier le processus de préinscription en fournissant un assistant IA disponible 24/7 pour répondre aux questions des futurs étudiants.

Conçu avec les dernières technologies d'intelligence artificielle (Google Gemini), Bot4Univ offre des réponses contextuelles, rapides et pertinentes sur les démarches de préinscription, les documents requis, et guide les utilisateurs vers le portail officiel SYSTHAG de l'Université de Douala.

## ✨ Fonctionnalités

### 🌐 Landing Page
- ✅ **Page d'accueil moderne** - Design attrayant avec sections informatives
- ✅ **Navigation fluide** - Menu avec liens vers Accueil, Fonctionnalités, À propos, Université
- ✅ **Menu hamburger responsive** - Actif sur tablettes et mobiles (≤1000px)
- ✅ **Section hero** - Mise en avant de la préinscription UDo avec CTAs clairs
- ✅ **Boutons d'action** - Accès direct au chat et au portail de préinscription SYSTHAG
- ✅ **Statistiques** - 100% Open Source, 24/7 Disponible, ∞ Questions
- ✅ **Footer personnalisé** - Crédits Groupe 19 et Dr Justin Moskolai
- ✅ **Authentification** - Boutons de connexion et inscription dans la barre de navigation

### 💬 Interface de Chat
- ✅ **Chat en temps réel** - Échanges instantanés avec l'assistant IA Gemini
- ✅ **Interface intuitive** - Design moderne inspiré des applications de messagerie
- ✅ **Bannière préinscription** - Accès direct au portail SYSTHAG depuis le chat
- ✅ **États visuels** - Empty state, loading, erreurs avec retry
- ✅ **Avatar du bot** - Identité visuelle cohérente avec logo robot
- ✅ **Historique** - Conservation et affichage des conversations via SQLite
- ✅ **Nouveau chat** - Réinitialisation complète pour démarrer une nouvelle conversation
- ✅ **Zone de saisie optimisée** - Hauteur réduite, meilleure visibilité des éléments
- ✅ **Focus préinscription** - L'IA guide spécifiquement sur les démarches UDo
- ✅ **Déconnexion** - Bouton de déconnexion sécurisé dans l'en-tête

### 🔐 Système d'authentification
- ✅ **Connexion utilisateur** - Authentification sécurisée par email et mot de passe
- ✅ **Inscription** - Création de compte avec validation email universitaire
- ✅ **Gestion de session** - JWT tokens pour maintenir l'état de connexion
- ✅ **Récupération mot de passe** - Système de réinitialisation par email
- ✅ **Vérification email** - Confirmation de l'email universitaire
- ✅ **Protection des routes** - Accès restreint aux utilisateurs connectés
- ✅ **Rôles utilisateur** - Différenciation étudiant/administrateur/invité

### 🎨 Design & UX
- ✅ **Responsive Design** - Compatible desktop, tablette et mobile
- ✅ **Design System** - Palette de couleurs cohérente (bleu universitaire)
- ✅ **Animations** - Transitions fluides et micro-interactions
- ✅ **Logo personnalisé** - Logo SVG Bot4Univ avec robot aux yeux jaunes (#ffc600)
- ✅ **Typographie** - Police Inter pour une lecture optimale
- ✅ **Accessibilité** - Navigation au clavier, labels ARIA
- ✅ **Palette moderne** - Couleur primaire navy (#07294d) et secondaire jaune (#ffc600)

### 🔌 Backend & API
- ✅ **API REST** - Endpoints `/api/chat`, `/api/history`, `/api/ai/health`
- ✅ **Authentification API** - Endpoints `/api/auth/login`, `/api/auth/register`, `/api/auth/logout`
- ✅ **Gestion des sessions** - Maintien du contexte avec SQLite (UUID, timestamps)
- ✅ **Gemini AI** - Génération de réponses via Google Gemini 2.5 Flash (obligatoire)
- ✅ **Retry & Resilience** - Gestion automatique des erreurs transitoires (503)
- ✅ **Gestion d'erreurs** - 502 en cas d'échec IA (conforme au diagramme de séquence)
- ✅ **Architecture modulaire** - Routes, services et DB séparés (MVC)
- ✅ **Préinscription UDo** - Prompts IA optimisés pour guider sur la préinscription
- ✅ **Configuration flexible** - Variables d'environnement via `.env`
- ✅ **Sécurité** - Hashage bcrypt des mots de passe, tokens JWT, validation des emails

## 🏗️ Architecture

Le projet suit une architecture MVC (Model-View-Controller) avec Flask :

```
┌─────────────────────────────────────────────────────────┐
│                    FRONTEND                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐ │
│  │ Landing Page │  │ Chat Interface│  │   Assets     │ │
│  │  (HTML/CSS)  │  │  (HTML/CSS/JS)│  │  (SVG/IMG)   │ │
│  └──────────────┘  └──────────────┘  └──────────────┘ │
└─────────────────────────────────────────────────────────┘
                          ↕ HTTP/REST
┌─────────────────────────────────────────────────────────┐
│                   FLASK BACKEND                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐ │
│  │   Routes     │  │   Services   │  │   Database   │ │
│  │  Blueprints  │  │ Gemini AI    │  │    SQLite    │ │
│  └──────────────┘  └──────────────┘  └──────────────┘ │
└─────────────────────────────────────────────────────────┘
                          ↕ API
┌─────────────────────────────────────────────────────────┐
│                  GOOGLE GEMINI API                       │
│           (gemini-2.5-flash + retry logic)               │
└─────────────────────────────────────────────────────────┘
```

Pour plus de détails, consultez :
- [Diagramme d'architecture](docs/diagram/system_architecture.mmd)
- [Diagramme de séquence](docs/diagram/sequence.mmd)
- [Modèle de données](docs/diagram/entity_relationship.mmd)

## 📦 Prérequis

Avant de commencer, assurez-vous d'avoir installé :

- **Python 3.8+** - [Télécharger Python](https://www.python.org/downloads/)
- **pip** - Gestionnaire de paquets Python (inclus avec Python)
- **Git** - Pour cloner le repository

## 🚀 Installation

### 1. Cloner le repository

```bash
git clone https://github.com/josepha237/BotInterface.git
cd BotInterface
```

### 2. Créer un environnement virtuel

**Windows (PowerShell) :**
```powershell
python -m venv env
.\env\Scripts\Activate.ps1
```

**Linux/Mac :**
```bash
python3 -m venv env
source env/bin/activate
```

### 3. Installer les dépendances

```bash
pip install -r requirements.txt
```

## ⚙️ Configuration

### Variables d'environnement

Créez un fichier `.env` à la racine du projet :

```env
FLASK_APP=app.py
FLASK_ENV=development
FLASK_DEBUG=1
SECRET_KEY=votre_clé_secrète_ici
BOT_API_URL=http://localhost:5001/api
GEMINI_API_KEY=cle_api_gemini_ici
GEMINI_MODEL=gemini-2.5-flash
SQLITE_DB_PATH=database/botinterface.db
GEMINI_MAX_RETRIES=2
GEMINI_RETRY_DELAY_MS=400
PREINSCRIPTION_URL=http://www.systhag-online.cm:8080/SYSTHAG-ONLINE/faces/etudiants/preInscription.xhtml
```

### Configuration Flask

Ajustez les paramètres dans `app.py` selon vos besoins :

```python
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-key')
app.config['BOT_API_URL'] = os.environ.get('BOT_API_URL')
```

## 🎮 Utilisation

### Démarrer l'application

```bash
python app.py
```

L'application sera accessible à l'adresse : `http://localhost:5000`

### Endpoints disponibles

| Méthode | Endpoint | Description |
|---------|----------|-------------|
| `GET` | `/` | Landing page avec présentation du projet |
| `GET` | `/app` | Interface de chat principale |
| `POST` | `/api/chat` | Envoyer un message au bot (body: `{message, session_id?}`) |
| `GET` | `/api/history` | Récupérer l'historique de la session courante |
| `GET` | `/api/ai/health` | Vérifier la disponibilité de Gemini |

### Accéder à l'application

1. **Landing Page** : `http://localhost:5000`
2. **Chat Interface** : `http://localhost:5000/app`
3. **Préinscription UDo (portail officiel)** : Utilisez `PREINSCRIPTION_URL` (boutons visibles sur la landing et dans le chat)

## 📁 Structure du projet

```
BotInterface/
│
├── app.py                      # 🐍 Application Flask principale
├── requirements.txt            # 📦 Dépendances Python (Flask, Gemini, SQLite)
├── README.md                   # 📖 Documentation du projet
├── .env                        # 🔐 Variables d'environnement (non versionné)
├── .gitignore                  # 🚫 Fichiers ignorés par Git
│
├── database/                   # 💾 Base de données SQLite
│   ├── db.py                  # Module de gestion DB (CRUD)
│   └── botinterface.db        # Fichier SQLite (sessions/messages)
│
├── route/                      # 🛣️ Routes Flask (Blueprints)
│   ├── page_routes.py         # Routes pages (/, /app, /login, /register)
│   ├── chat_routes.py         # Routes chat (/api/chat, /api/history)
│   ├── ai_routes.py           # Routes IA (/api/ai/health)
│   └── auth_routes.py         # Routes authentification (/api/auth/*)
│
├── service/                    # ⚙️ Services métier
│   ├── gemini_service.py      # Service Gemini (retry, prompts)
│   └── auth_service.py        # Service authentification (bcrypt, JWT)
│
├── test/                       # 🧪 Tests
│   ├── test_db.py             # Tests DB SQLite
│   ├── test_integration.py    # Tests routes et APIs
│   ├── test_gemini_connectivity.py  # Tests Gemini
│   └── test_ai_error_path.py  # Tests gestion erreurs IA
│
├── docs/                       # �📚 Documentation
│   ├── srs.pdf                # 📋 Cahier des charges (SRS)
│   ├── diagram/               # 📊 Diagrammes Mermaid
│   │   ├── system_architecture.mmd     # Architecture système
│   │   ├── sequence.mmd                # Diagramme de séquence
│   │   ├── entity_relationship.mmd     # Modèle de données
│   │   └── use_case.mmd                # Cas d'utilisation
│   └── ui-mockups/            # 🎨 Maquettes d'interface
│       ├── README.md          # Guide de création des mockups
│       ├── MOCKUPS_INDEX.md   # Index des mockups
│       ├── desktop/           # Mockups desktop (SVG)
│       ├── mobile/            # Mockups mobile (SVG)
│       └── design-system.svg  # Bibliothèque de composants
│
├── stactic/                    # 📦 Ressources statiques
│   ├── css/
│   │   └── styles.css         # 🎨 Styles CSS (1450+ lignes, responsive)
│   ├── js/
│   │   └── index.js           # ⚡ JavaScript frontend (430+ lignes)
│   └── img/                   # 🖼️ Images et assets
│       ├── logo.svg           # Logo Bot4Univ
│       ├── logo.jpg           # Logo alternatif
│       └── landing.svg        # Mockup pour landing
│
└── templates/                  # 📄 Templates HTML
    ├── landing.html           # 🏠 Landing page (hero préinscription, auth buttons)
    ├── index.html             # 💬 Interface chat (bannière SYSTHAG, logout)
    ├── login.html             # 🔐 Page de connexion
    ├── register.html          # 📝 Page d'inscription
    └── forgot-password.html   # 🔑 Récupération mot de passe
```

## 📚 Documentation

### Documents principaux
- **[Cahier des charges (SRS)](docs/srs.pdf)** - Spécifications détaillées du projet

### Diagrammes techniques
- **[Architecture système](docs/diagram/system_architecture.mmd)** - Vue d'ensemble de l'architecture avec auth_routes et AuthService
- **[Diagramme de séquence](docs/diagram/sequence.mmd)** - Flux de communication avec authentification JWT
- **[Modèle entité-relation](docs/diagram/entity_relationship.mmd)** - Structure des données (USER, SESSION, MESSAGE, PASSWORD_RESET, LOGIN_ATTEMPT)
- **[Cas d'utilisation](docs/diagram/use_case.mmd)** - Scénarios d'utilisation avec authentification
- **[Cas d'utilisation](docs/diagram/use_case.mmd)** - Scénarios utilisateur et admin

### Design & Mockups
- **[Guide des mockups](docs/ui-mockups/README.md)** - Processus de création avec GitHub Copilot + SVG + Mermaid
- **[Index des mockups](docs/ui-mockups/MOCKUPS_INDEX.md)** - Catalogue complet avec aperçus
- **[Design System](docs/ui-mockups/design-system.svg)** - Bibliothèque de composants réutilisables

## 🛠️ Technologies utilisées

### Backend
- **[Flask 3.0.3](https://flask.palletsprojects.com/)** - Framework web Python avec Blueprints
- **[SQLite 3](https://www.sqlite.org/)** - Base de données légère avec mode WAL
- **[Google Gemini API](https://ai.google.dev/)** - Modèle IA gemini-2.5-flash
- **[python-dotenv 1.0.1](https://pypi.org/project/python-dotenv/)** - Gestion des variables d'environnement
- **Python 3.8+** - Langage de programmation backend

### Frontend
- **HTML5** - Structure sémantique moderne
- **CSS3** - Stylisation avancée avec variables CSS, flexbox, grid
- **JavaScript (Vanilla ES6+)** - Interactivité sans frameworks
- **SVG** - Graphiques vectoriels pour logo et mockups

### Design
- **[Inter Font](https://fonts.google.com/specimen/Inter)** - Typographie optimisée pour l'UI
- **GitHub Copilot** - Génération de code SVG et assistance au développement
- **Mermaid** - Diagrammes as code pour la documentation

### Outils de développement
- **Git & GitHub** - Contrôle de version et collaboration
- **VS Code** - Éditeur de code avec extensions SVG/Mermaid
- **Python venv** - Environnement virtuel isolé
- **PowerShell** - Terminal pour développement Windows

## 🎨 Design System

Le projet utilise un design system cohérent avec :

### Palette de couleurs
- **Navy principal** : `#07294d` - Confiance, autorité, académique (couleur de base)
- **Navy intermédiaire** : `#092e56` - Hover states, gradients, profondeur visuelle
- **Jaune secondaire** : `#ffc600` - Énergie, innovation, accent (CTA, robot)
- **Navy foncé** : `#051f3a` - États actifs et ombres profondes
- **Jaune clair** : `#fff9e6` - Backgrounds et états secondaires (messages utilisateur)
- **Vert** : `#28a745` - Succès, validation (force mot de passe)
- **Gris** : `#6c757d` - Texte secondaire
- **Blanc** : `#ffffff` - Fond principal

### Typographie
- **Police** : Inter (Google Fonts)
- **Tailles** : 14px (petit), 16px (base), 18-20px (sous-titres), 24-56px (titres)

### Espacements
- Grille de base : **8px**
- Padding sections : **40-60px**
- Gap entre éléments : **16-32px**

## 📱 Interface Responsive

### Breakpoints
- **Desktop** : > 1000px (navigation horizontale, 2 boutons header)
- **Tablette** : 521-1000px (menu hamburger actif, grid adapté)
- **Mobile** : ≤ 520px (menu hamburger, layout vertical, boutons empilés)

### Adaptations mobiles
- Menu hamburger avec overlay
- Boutons full-width
- Textes réduits
- Images optimisées
- Touch-friendly (44px minimum)

## 🤝 Contribution

Les contributions sont les bienvenues ! Voici comment contribuer :

1. **Fork** le projet
2. Créez votre branche de fonctionnalité (`git checkout -b feature/AmazingFeature`)
3. **Committez** vos changements (`git commit -m 'feat: add some AmazingFeature'`)
4. **Push** vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvrez une **Pull Request**

### Standards de code

- **Python** : Suivre PEP 8
- **JavaScript** : ES6+, pas de point-virgule
- **CSS** : BEM naming convention
- **Commits** : [Conventional Commits](https://www.conventionalcommits.org/)
- **Documentation** : Commenter le code complexe
- **Tests** : Tester avant de soumettre

## ✅ Statut du projet

### Fonctionnalités complétées ✅
- [x] Landing page avec focus préinscription Université de Douala
- [x] Interface de chat fonctionnelle avec Gemini AI
- [x] Menu hamburger responsive (tablettes et mobiles)
- [x] Backend Flask modulaire (routes, services, DB)
- [x] Base de données SQLite avec persistance des sessions
- [x] Intégration Gemini 2.5 Flash avec retry automatique
- [x] Gestion d'erreurs conforme au diagramme de séquence
- [x] Bannière et CTAs vers le portail SYSTHAG
- [x] Logo et design system cohérent
- [x] Documentation complète (diagrammes, mockups, tests)
- [x] Responsive design optimisé (desktop/tablette/mobile)
- [x] Zone de saisie optimisée sans compteur de caractères
- [x] Réinitialisation complète des conversations (nouveau chat)

### En cours de développement 🚧
- [ ] Analytics des questions de préinscription fréquentes
- [ ] Support multilingue (français/anglais)
- [ ] Authentification étudiants (optionnel)

## 📝 Roadmap

### Phase 1 : MVP ✅ (Complété)
- [x] Backend Flask complet
- [x] Interface utilisateur moderne
- [x] Design responsive
- [x] Documentation

### Phase 2 : Production 🎯 (En cours)
- [x] Intégration Gemini AI réelle
- [x] Base de données SQLite persistante
- [ ] Tests unitaires et d'intégration complets (pytest)
- [ ] CI/CD avec GitHub Actions
- [ ] Déploiement (Heroku/Railway/VPS)

### Phase 3 : Améliorations 🚀 (Futur)
- [ ] FAQ préinscription avec réponses instantanées
- [ ] Liste dynamique des documents requis
- [ ] Support multilingue (français/anglais)
- [ ] Mode sombre
- [ ] Export de conversations (PDF/TXT)
- [ ] Recherche dans l'historique
- [ ] Notifications de rappel (dates importantes)
- [ ] PWA (Progressive Web App)

## 🐛 Bugs connus

Aucun bug majeur connu pour le moment. Si vous en trouvez, veuillez [ouvrir une issue](https://github.com/josepha237/BotInterface/issues).

### Améliorations possibles
- Ajouter un système de feedback sur les réponses
- Intégrer un calendrier des dates importantes de préinscription
- Créer une FAQ interactive avec les questions les plus fréquentes
- Améliorer les prompts IA avec des données réelles de l'UDo

## 📄 Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.

## � Équipe

### Développement
**Groupe 19** - Équipe de développement

### Coordination
**Dr Justin Moskolai** - Coordinateur du projet

### Contributeurs principaux
- **Joseph A.** ([@josepha237](https://github.com/josepha237)) - Développeur principal
- Membres du Groupe 19 - Développement et tests

## 📞 Contact

Pour toute question ou suggestion, n'hésitez pas à :
- 📧 Ouvrir une [issue sur GitHub](https://github.com/josepha237/BotInterface/issues)
- 💬 Contacter l'équipe de développement
- 🎓 Consulter Dr Justin Moskolai (coordinateur)

---

## 🎓 Contexte académique

Ce projet a été développé dans le cadre d'un projet universitaire sous la coordination de **Dr Justin Moskolai**. Bot4Univ représente une initiative pour **simplifier et moderniser le processus de préinscription à l'Université de Douala** en utilisant l'intelligence artificielle conversationnelle.

### Objectifs pédagogiques
- Application des concepts de génie logiciel et architecture MVC
- Développement d'une application web complète avec IA
- Intégration d'APIs externes (Google Gemini)
- Gestion de base de données et persistance
- Travail en équipe et gestion de projet
- Documentation technique et professionnelle
- Tests et validation de logiciel

---

## 🌟 Remerciements

Merci à tous les contributeurs, testeurs et utilisateurs qui ont participé au développement de Bot4Univ. Un remerciement spécial à **Dr Justin Moskolai** pour sa coordination et ses conseils précieux.

⭐ **N'oubliez pas de mettre une étoile au projet si vous le trouvez utile !**

---

<div align="center">

**Bot4Univ** - Construit avec amour ❤ par le **Groupe 19**

*Dernière mise à jour : Novembre 2025*

</div>
