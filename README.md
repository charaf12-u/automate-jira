# Jira Automate Pro 🚀

Jira Automate Pro est une application de bureau avec interface graphique (GUI) élégante pour automatiser l'importation de tickets depuis un fichier JSON directement vers **Jira Cloud**.

![Jira Automate](https://img.shields.io/badge/Status-Active-success) ![Python](https://img.shields.io/badge/Python-3.x-blue) ![CustomTkinter](https://img.shields.io/badge/GUI-CustomTkinter-yellow)

## ✨ Fonctionnalités
- Interface utilisateur Premium (Dark & Gold) grâce à **CustomTkinter**.
- Importation complète d'une hiérarchie de tâches (Ex: `Epic` ➡️ `Tâche` ➡️ `Sous-tâche`).
- **Nouveau :** Mappage dynamique des types de tickets ! L'application lit les noms exacts de vos `Issue Types` configurés dans Jira via le bloc `jira_mapping` du fichier JSON.
- Multithreading pour éviter le gel (freeze) de l'interface durant les longues importations.
- Reconnexion sécurisée à l'API via API Token (Jira REST API v3).

## 📥 Prérequis et Installation

1. Clonez ce dépôt GitHub :
   ```bash
   git clone https://github.com/charaf12-u/automate-jira.git
   cd automate-jira
   ```
2. Installez les dépendances requises :
   ```bash
   pip install -r requirements.txt
   ```
3. Créez un fichier `.env` à la racine du projet et ajoutez vos identifiants Jira :
   ```env
   JIRA_DOMAIN=votre-domaine.atlassian.net
   JIRA_EMAIL=votre.email@entreprise.com
   JIRA_API_TOKEN=votre_api_token_jira
   ```
   *Astuce : [Générez votre jeton API Jira ici](https://id.atlassian.com/manage-profile/security/api-tokens).*

## 🔌 Comment Utiliser

### 1. Préparer le fichier JSON
L'application s'appuie sur une structure JSON spécifique. Vous devez impérativement configurer le bloc `jira_mapping` selon les noms **exacts** disponibles dans les paramètres *Issue Types* de votre projet Jira.

Exemple de mappage (`exemple.json`) :
```json
{
    "jira_mapping": {
        "epic": "Epic",
        "task": "Tâche",
        "subtask": "Sous-tâche"
    },
    "epics": [
        ...
```
*(Si votre projet Jira n'utilise pas ces noms, vous DEVEZ modifier cette partie pour indiquer à l'application quels types créer).*

### 2. Lancer l'application
Exécutez le script principal via Python :
```bash
python app.py
```
*Si vous avez compilé l'application en exécutable, double-cliquez simplement sur `dist/app.exe`.*

### 3. Démarrer l'importation
- Dans l'application, entrez **la clé du Projet Jira** (ex: `PROJ` ou `NTB`).
- Sélectionnez le fichier `.json` préparé.
- Cliquez sur **Lancer L'importation**.
- L'application créera automatiquement les Epics, y rattachera les Tâches, puis y intégrera les Sous-tâches !

## 🏗️ Structure du JSON supportée

Voici la hiérarchie standard acceptée par l'application :
```json
{
    "jira_mapping": { "epic": "Epic", "task": "Tâche", "subtask": "Sous-tâche" },
    "epics": [
        {
            "epic": "Titre du Grand Objectif",
            "tasks": [
                {
                    "task_name": "Titre de la tâche 1",
                    "subtasks": [ "Sous-tâche 1.1", "Sous-tâche 1.2" ]
                }
            ]
        }
    ]
}
```

## ⚠️ Dépannage (Erreurs courantes)
- **Erreur API (400) : "Le type de ticket sélectionné n'est pas valide."**
  👉 Cela signifie que l'un des types mentionnés dans `jira_mapping` n'est pas activé/disponible sur votre Jira pour ce projet. Rendez-vous dans les "Paramètres du Projet > Types de tickets" dans votre Jira, et ajoutez-les.
- **Plantage à l'ouverture :**
  👉 Assurez-vous d'avoir exécuté `pip install -r requirements.txt`.
