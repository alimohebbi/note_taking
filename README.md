# Note-Taking System
[![GitHub stars](https://img.shields.io/github/stars/alimohebbi/note_taking)](https://github.com/alimohebbi/note_taking/stargazers)
[![GitHub issues](https://img.shields.io/github/issues/alimohebbi/note_taking)](https://github.com/alimohebbi/note_taking/issues)
[![GitHub license](https://img.shields.io/github/license/alimohebbi/note_taking)](https://github.com/alimohebbi/note_taking/blob/main/LICENSE)

## Introduction

This repository contains the code for a Note-Taking System, which allows users to manage their notes by providing functionalities to create, update, and delete notes. The system is implemented using the Python programming language and the Django framework. This README provides an overview of the design, implementation, and key features of the system.

## Table of Contents

1. [Design and Implementation](#design-and-implementation)
    1. [Database Schema](#database-schema)
    2. [RESTful APIs](#restful-apis)
    3. [Unit Testing (Bonus)](#unit-testing-bonus)
2. [Design Decisions and Trade-offs](#design-decisions-and-trade-offs)
3. [Version Control and Repository](#version-control-and-repository)
4. [Conclusion](#conclusion)

## Design and Implementation

### Database Schema

The system's database schema is designed to efficiently support note-taking functionalities. It includes two primary tables:
- **User**: To store user information.
  - Fields: id, username, email, password.
- **Note**: To store the notes created by users.
  - Fields: id, user id, title, description.
  - Relationships: A foreign key relationship is established between the Note table and the User table, ensuring that each note is associated with a specific user.
  - Constraints: Various constraints are applied to maintain data integrity.

### RESTful APIs

RESTful APIs are implemented using the Python framework Django and Django REST framework. The following endpoints are provided:

- Create Note
- Read Note
- Update Note
- Delete Note
- Read Notes List
- Register
- Login
- Logout

These APIs are designed for scalability, performance, and adhere to Microsoft API guidelines. Proper validation and informative error messages are provided for data integrity and reliability. Pagination is also implemented for optimized performance.

### Unit Testing (Bonus)

Comprehensive unit tests are implemented using Django's testing framework, achieving 100% code coverage. These tests cover various use cases, input validation, and error handling. They ensure the reliability and maintainability of the system.

## Design Decisions and Trade-offs

- Feature Scope vs. Time to Market
- Flexibility vs. Conformity (Authentication)
- Flexibility vs. Conformity (RESTful implementation)
- Scalability (SQL vs. NoSQL)
- Scalability (Authentication)

## Version Control and Repository

The codebase is version-controlled using Git, and the repository can be accessed on [GitHub](https://github.com/alimohebbi/note_taking).

## Conclusion

The implementation of the Note-Taking System aligns with the specified requirements. The database schema is well-structured, and the RESTful APIs are designed for performance and maintainability. Comprehensive unit tests further ensure the reliability of the system.

If you have any questions or need further information, please don't hesitate to reach out. Thank you for the opportunity to complete this task.

## References

- [Django Rest Framework](https://www.django-rest-framework.org)
- [Microsoft API Guidelines](https://github.com/microsoft/api-guidelines)
- [Postman](https://www.postman.com)


### RESTful APIs

RESTful APIs are implemented using the Python framework Django and Django REST framework. The following endpoints are provided:

- **Create Note**
  - HTTP Method: POST
  - URL: `/api/v1/notes/`

- **Read Note**
  - HTTP Method: GET
  - URL: `/api/v1/notes/{note_id}/`

- **Update Note**
  - HTTP Method: PUT
  - URL: `/api/v1/notes/{note_id}/`

- **Delete Note**
  - HTTP Method: DELETE
  - URL: `/api/v1/notes/{note_id}/`

- **Read Notes List**
  - HTTP Method: GET
  - URL: `/api/v1/notes/?page={page}&page size={limit}`

- **Register**
  - HTTP Method: POST
  - URL: `/api/v1/account/register/`

- **Login**
  - HTTP Method: POST
  - URL: `/api/v1/account/login/`

- **Logout**
  - HTTP Method: POST
  - URL: `/api/v1/account/logout/`

These APIs are designed for scalability, performance, and adhere to Microsoft API guidelines. Proper validation and informative error messages are provided for data integrity and reliability. Pagination is also implemented for optimized performance.

### RESTful APIs

The system provides the following RESTful APIs:

1. **Create Note** (POST /api/v1/notes/)
   - JSON Input Example:
   ```json
   {
     "user_id": 1,
     "title": "Sample Note",
     "description": "This is a sample note."
   }
