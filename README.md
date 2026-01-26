![Videoflix](assets/logo_icon.svg)

This repository contains the backend for the Videoflix platform, a video streaming application similar to Netflix. The system is built on Django and the Django Rest Framework (DRF), providing a robust RESTful API. It includes features for user authentication, video management, and adaptive streaming (HLS) via background processing.

## Table of Contents

1.  Technical Overview
2.  Frontend Application
3.  Features
4.  Prerequisites
5.  Installation and Setup
6.  Configuration
7.  API Documentation
8.  Background Processes and Caching
9.  Testing

## 1. Technical Overview

The project adheres to a container-based architecture and Clean Code principles.

*   **Framework:** Django 6.0, Django Rest Framework
*   **Database:** PostgreSQL
*   **Caching & Message Broker:** Redis
*   **Asynchronous Tasks:** Django RQ
*   **Video Processing:** FFmpeg (for HLS transcoding)
*   **Containerization:** Docker & Docker Compose
*   **Server:** Gunicorn with Whitenoise for static files

## 2. Frontend Application

This backend is designed to serve the Videoflix Frontend application. The client-side logic, user interface, and video player implementation are located in a separate repository.

*   **Repository URL:** [https://github.com/Developer-Akademie-Backendkurs/project.Videoflix](https://github.com/Developer-Akademie-Backendkurs/project.Videoflix)

Please refer to the frontend repository for specific installation and startup instructions for the client application. The frontend is configured to communicate with this backend via the REST API (default: `http://localhost:8000`).

## 3. Features

### Authentication & User Management
*   **Registration:** Double-Opt-In process via email activation.
*   **Login:** Implementation of JWT (JSON Web Token) supporting `HttpOnly` Cookies and `Authorization: Bearer` headers (fallback).
*   **Password Management:** Functionality for requesting password resets and changing passwords via email links.

### Video Streaming
*   **Upload:** Video file upload via the Django Admin Panel.
*   **Transcoding:** Automatic conversion into HLS format (HTTP Live Streaming) in 480p, 720p, and 1080p resolutions using FFmpeg.
*   **Streaming:** Delivery of `.m3u8` playlists and `.ts` video segments via protected API endpoints.
*   **Dashboard:** Provision of a sorted video list including metadata and thumbnails.

## 4. Prerequisites

The following tools are required to run the application:

*   **Docker Desktop** (including Docker Compose)
*   **Git**

## 5. Installation and Setup

The project is fully containerized. Follow these steps to start the development environment:

1.  **Clone the Repository**
    ```bash
    git clone <repository-url>
    cd videoflix.backend
    ```

2.  **Configure Environment Variables**
    Create a `.env` file based on the template:
    ```bash
    cp .env.template .env
    ```
    Adjust the values in the `.env` file as needed (particularly email configuration for sending activation links).

3.  **Build and Start Containers**
    ```bash
    docker compose up --build
    ```
    The server will be accessible at `http://localhost:8000`.

4.  **Database Migrations**
    Migrations are automatically executed by the entrypoint script upon startup. If manual migrations are necessary:
    ```bash
    docker compose exec web python manage.py migrate
    ```

5.  **Create Superuser**
    A superuser is automatically created based on the environment variables (Default: admin / adminpassword).

## 6. Configuration

Central configuration is managed via the `.env` file. Key variables include:

*   `SECRET_KEY`: Django Secret Key.
*   `DEBUG`: Should be set to `False` in production.
*   `ALLOWED_HOSTS`: Comma-separated list of allowed hosts.
*   `DB_NAME`, `DB_USER`, `DB_PASSWORD`: PostgreSQL credentials.
*   `REDIS_LOCATION`: URL for the Redis service.
*   `EMAIL_HOST`, `EMAIL_PORT`, `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD`: SMTP server settings.

## 7. API Documentation

The API is divided into two main sections: Authentication and Video Content.

### Authentication Endpoints

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| POST | `/api/register/` | Registers a new user. |
| POST | `/api/login/` | User login. Sets JWT in HttpOnly Cookies. |
| POST | `/api/logout/` | User logout. Blacklists the refresh token. |
| POST | `/api/token/refresh/` | Refreshes the access token. |
| GET | `/api/activate/<uid>/<token>/` | Activates the account after registration. |
| POST | `/api/password_reset/` | Requests an email to reset the password. |
| POST | `/api/password_confirm/<uid>/<token>/` | Sets a new password. |

### Video Endpoints

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| GET | `/api/video/` | Retrieves a list of all videos (newest first). |
| GET | `/api/video/<id>/<res>/index.m3u8` | Retrieves the HLS playlist for a specific resolution. |
| GET | `/api/video/<id>/<res>/<segment>/` | Retrieves a binary video segment (.ts). |

**Note:** All video endpoints require authentication (Cookie or Bearer Token).

## 8. Background Processes and Caching

### Video Conversion
The system uses `django-rq` and Redis to process videos asynchronously.
1.  An admin uploads a video.
2.  A `post_save` signal triggers a task.
3.  The worker (`python manage.py rqworker`) picks up the task.
4.  FFmpeg generates HLS streams in `media/hls/<id>/`.
5.  Database flags (`has_720p`, etc.) are updated upon completion.

### Caching
Redis is used as a caching layer for database queries and session storage to minimize response times.

## 9. Testing

The project uses `pytest` for unit and integration testing. The tests cover authentication workflows, video listings, and model logic.

To run the tests:
```bash
docker compose exec web pytest
```
