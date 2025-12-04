====================================
Newsapp — Project Documentation
====================================

Overview
--------
Newsapp is a Django-based application designed to manage the creation, editing, approval, publishing, and reading of news articles and newsletters. The system uses a role-based access structure with four primary user types:

- **Publisher**
- **Journalist**
- **Editor**
- **Reader**

Each role has specific permissions, and all content follows a workflow from creation → approval → publication → reading.

Features
--------
- **Journalists**
  - Create articles
  - Create newsletters
  - Edit or delete their own posts
- **Editors**
  - Review and approve/reject articles and newsletters
  - Edit content
- **Publishers**
  - Publish approved content to readers
  - Manage journalist/editor teams
- **Readers**
  - Subscribe to journalists or publishers
  - Access published articles and newsletters

Project Structure
-----------------
Newsapp contains the following core model entities:

**Publisher**
Represents a publisher profile linked to a User. Tracks when a publisher account was created. Includes permissions for publishing and viewing own articles.

**Journalist**
Linked to a User and optionally associated with a Publisher. Capable of creating, editing, and deleting content. Contains timestamps and custom permissions.

**Editor**
Linked to a User and a Publisher. Can edit, approve, or publish posts. Has custom permissions for posting and updating content.

**Reader**
Represents a general reader profile. Linked to a User and includes subscription permissions.

**Article**
Represents a news article written by a Journalist and associated with a Publisher. Contains a title, content body, approval flag, and a timestamp.

**Newsletter**
Similar to Article but intended for periodic newsletter content. Created by journalists, approved by editors, and published by publishers.

**Subscription**
Allows a User to subscribe to either a Publisher or a Journalist. Tracks subscription type and date.

**ResetToken**
Manages password-reset tokens linked to User accounts. Stores token strings, expiration dates, and usage status.

The serializers associated with each model enable API responses and data validation.

Documentation Contents
----------------------
The API reference is generated automatically through Sphinx autodoc and can be found in the section below.

.. toctree::
   :maxdepth: 2
   :caption: API Reference:

   modules
