# Intégration EDT UVSQ à Google Agenda

Ce projet permet aux utilisateurs de l'Université de Versailles Saint-Quentin-en-Yvelines (UVSQ) de récupérer leur emploi du temps (EDT) et de l'intégrer automatiquement dans leur Google Agenda, le tout à travers une interface graphique intuitive construite avec Gradio.

## Fonctionnalités Principales

- **Récupération de l'EDT UVSQ :** Permet aux utilisateurs de récupérer leur emploi du temps directement depuis le système UVSQ.
- **Intégration à Google Agenda :** Automatise l'ajout d'événements de l'EDT UVSQ dans le Google Agenda de l'utilisateur.
- **Interface Graphique Gradio :** Fournit une interface utilisateur simple et conviviale pour faciliter la récupération et l'intégration de l'EDT.

## Cas d'Usage

Ce projet est idéal pour les étudiants et les professeurs de l'UVSQ qui cherchent à simplifier la gestion de leur emploi du temps en intégrant directement leur EDT dans leur Google Agenda personnel.

## Configuration Initiale

### Étape 1 : Configurer le projet Google Cloud

Pour utiliser l'API Google Calendar, vous devez configurer un projet dans la Google Cloud Console et activer l'API Google Calendar.

1. Accédez à la [Google Cloud Console](https://console.cloud.google.com/).
2. Créez un nouveau projet ou sélectionnez un projet existant.
3. Accédez à **API et services** > **Bibliothèque** et activez l'API Google Calendar.
4. Configurez l'écran de consentement OAuth dans **Identifiants** > **Configurer l'écran d'autorisation**.
   * Selectionnez **Externe** et cliquez sur **Créer
   * Remplissez les champs requis (Nom de l'application, adresse e-mail d'assistance utilisateur et adresse e-mail) et cliquez sur **Enregistrer et continuer**.
   * Cliquez sur **Ajouter ou supprimer des domaines autorisés** et ajoutez `calendar.app.created` à la liste des domaines autorisés. (Vous pouvez rechercher `calendar.app.created` dans la barre de recherche pour le trouver plus rapidement). Puis cliquez sur **Enregistrer et continuer**.
   * Cliquez sur **ADD USERS** et ajoutez votre adresse e-mail Google. Puis cliquez sur **Enregistrer et continuer**.
   * Vérifiez les informations et cliquez sur **Revenir au tableau de bord**.
5. Créez des identifiants OAuth 2.0 en cliquant sur **Identifiants** > **Créer des identifiants** > **ID client OAuth**.
6. Choisissez **Application de bureau** comme type d'application et suivez les instructions pour créer l'ID client.
7. Téléchargez le fichier json et renommez le `credentials.json` puis placez-le à la racine de votre projet.

### Étape 2 : Installation des Dépendances

Vérifiez d'abord que Python est bien installé sur votre machine. Ensuite, utilisez la commande ci-dessous pour installer toutes les librairies nécessaires en une seule fois :

```bash
pip install gradio==4.19.2 requests==2.31.0 gradio_calendar==0.0.4 google-api-python-client==2.120.0 google-auth-httplib2==0.2.0 google-auth-oauthlib==1.2.0 google-api-core==2.17.1 googleapis-common-protos==1.62.0 google-auth==2.28.1
```

Alternativement, vous pouvez aussi installer chaque librairie individuellement en utilisant les commandes suivantes :

```bash
pip install gradio==4.19.2
pip install requests==2.31.0
pip install gradio_calendar==0.0.4
pip install google-api-python-client==2.120.0
pip install google-auth-httplib2==0.2.0
pip install google-auth-oauthlib==1.2.0
pip install google-api-core==2.17.1
pip install googleapis-common-protos==1.62.0
pip install google-auth==2.28.1
```

## Utilisation

Après avoir configuré votre projet Google Cloud et installé les dépendances, lancez l'application en exécutant le fichier principal du projet (main.py). Suivez les instructions à l'écran pour récupérer votre EDT UVSQ et l'intégrer dans votre Google Agenda.

