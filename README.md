[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![GitHub issues](https://img.shields.io/github/issues/alimohebbi/note_taking)](https://github.com/alimohebbi/note_taking/issues)
![Coverage](https://img.shields.io/badge/coverage-100%25-brightgreen)
![Last Commit](https://img.shields.io/github/last-commit/alimohebbi/note_taking)
![Code Style](https://img.shields.io/badge/code%20style-PEP8-brightgreen)
![GitHub release (latest by date)](https://img.shields.io/github/v/release/alimohebbi/note_taking)

## Note-Taking System Backend

Welcome to the Note-Taking System repository! This project is an implementation of a note-taking system that allows
users to manage their notes. Whether you want to jot down ideas, record thoughts, or set reminders, this system has got
you covered. It was developed using the Python programming language and the Django framework. In this README, you'll
find all the information you need to understand the design and usage of system.

## Table of Contents

1. [Design and Implementation](#design-and-implementation)
    1. [Database Schema](#database-schema)
    2. [RESTful APIs](#restful-apis)
2. [Key Features](#key-features)
    1. [Database Schema](#1-database-schema)
    2. [RESTful APIs](#2-restful-apis)
3. [API Endpoints](#api-endpoints)
4. [Unit Testing](#unit-testing)
5. [Installation](#installation)
6. [Adding Random Data](#adding-random-data-to-the-system)
7. [References](#references)

## Design and Implementation

### Database Schema

The system's database schema is designed to efficiently support note-taking functionalities. It includes two primary
tables:

- **User**: To store user information.
    - Fields: id, username, email, password.
- **Note**: To store the notes created by users.
    - Fields: id, user_id, title, content, note_type, created_at, updated_at, remind_at.
- **SharedNote** : To facilitate note-sharing between users.
    - Fields: id, recipient_id, note_id, created_at.

### RESTful APIs

RESTful APIs have been implemented using the Python framework Django and Django REST framework. The APIs provide various
functionalities, including note management, sharing, and user authentication.

You can find the complete list of API endpoints in the [API Endpoints](#api-endpoints) section of this README. The APIs
adhere to Microsoft API guidelines and offer validation, error handling, and performance optimizations.

## Key Features

### 1. Database Schema
   - **Efficient Data Management:** The system's database schema is designed to efficiently support note-taking functionalities. It includes tables for User, Note, and SharedNote with appropriate relationships and constraints to ensure data integrity.
   - **Performance Optimization:** Indexing is implemented on frequently queried columns, such as foreign key fields and timestamps, to enhance database performance.
   - **Scalability Support:** UUIDs are adopted for keys to support sharding and reduce reliance on centralized key generation services. This design promotes scalability and maintainability.

### 2. RESTful APIs
   - **User-Friendly Endpoints:** RESTful APIs are implemented using Django REST framework, providing user-friendly endpoints for creating, reading, updating, and deleting notes, as well as user management operations.
   - **Validation and Error Handling:** APIs incorporate validation rules from the database schema and return informative error messages in case of errors. This enhances user experience and makes troubleshooting easier.
   - **Pagination for UI:** API endpoints that support pagination offer additional details to facilitate UI development. These details, including links to previous and next results, simplify the UI development process.
   - **Versioning for Scalability:** API versioning allows for the introduction of new features or changes without affecting older clients, ensuring scalability and backward compatibility.
   - **Privacy Protection:** The system enforces privacy by securely storing user passwords and restricting access to notes that do not belong to the user.


## API Endpoints

The project offers the following API endpoints:

| Functionality                              | HTTP Method | URL                                     |
|--------------------------------------------|-------------|-----------------------------------------|
| Create a note                              | POST        | /api/v1/notes/                          |
| Read a note                                | GET         | /api/v1/notes/<note_id>/                |
| Update a note                              | PUT         | /api/v1/notes/<note_id>/                |
| Delete a note                              | DELETE      | /api/v1/notes/<note_id>/                |
| Retrieve a list of notes                   | GET         | /api/v1/notes/                          |
| Share a note with a user                   | POST        | /api/v1/notes/<note_id>/share-with/     |
| Retrieve shared note recipients            | GET         | /api/v1/notes/<note_id>/share-with/     |
| Stop sharing a note with a user            | DELETE      | /api/v1/notes/<note_id>/share-with      |
| Retrieve shared notes for the current user | GET         | /api/v1/notes/shared-with-me/           |
| Stop sharing a note with the current user  | DELETE      | /api/v1/notes/<note_id>/shared-with-me/ |
| Register a user                            | POST        | /api/v1/account/register/               |
| Log in                                     | POST        | /api/v1/account/login/                  |
| Log out                                    | POST        | /api/v1/account/logout/                 |

For more details, refer to the postman documentation of the end
points ([postman documentation](https://documenter.getpostman.com/view/1712946/2s9YXe6Nxx)).

## Unit Testing

The project includes comprehensive unit tests covering various use cases, input validation, and error handling. These
tests ensure the functionality and behavior of the implemented APIs. The unit tests have achieved 100% coverage and
follow common conventions for API testing, enhancing code maintainability and readability.

## Installation

To run this backend on your local machine, follow these steps:

1. Clone the repository:
   ```bash
   git clone https://github.com/alimohebbi/note_taking.git
   ```

2. Install the required dependencies using pip:
   ```bash
   pip install -r requirements.txt
   ```

3. Create database migrations:
   ```bash
   python manage.py makemigrations
    ```

4. Apply database migrations:
   ```bash
   python manage.py migrate
   ```

5. Run Postgres data base using docker compose:
   ```bash
   docker-compose -f postgresql-compose.yml up    
   ```

6. Start the development server:
   ```bash
   python manage.py runserver
   ```

Your backend will be running at `http://127.0.0.1:8000/`.
To make the instructions in your readme file clearer and more user-friendly, you can rephrase them as follows:

## Adding Random Data to the System

You can populate the system with data by using the following commands:

### 1. Create Multiple Users with Notes

To create multiple users, each of whom has a specified number of notes, use the following command:

```bash
manage.py create_fake_records --users [number of users] --notes [number of notes]
```

**Sample Result:**

```bash
10 users created, each with 15 notes.
```

### 2. Create Objects with Relationships

You can create objects that have specific relationships with others. This includes creating a user with a
certain number of notes, a note shared with a specified number of users (owned by the previous user), and a user that
has received a certain number of notes. Use the following command:

```bash
manage.py create_champion_objects --size [number of relationships]
```

**Sample Result:**

```bash
Pro writer User:
{'email': 'danielledaniels@example.org', 'user_name': 'xFNrtsQgad', 'password': '_8C!#Ctrsk'}

Pro shared note:
{'note_id': 'BBVADsquTCqwW0CyIgrO2A'}

Pro Recipient User:
{'email': 'shirley45@example.org', 'user_name': 'LigwyBftJF', 'password': '9A9DAc)aV)'}
```

These commands will help you quickly and efficiently add data to the system.

## References

- [Django Rest Framework](https://www.django-rest-framework.org)
- [Microsoft API Guidelines](https://github.com/microsoft/api-guidelines)
- [Postman](https://www.postman.com)

