<p align="center">
  <img src="preview.gif" />
</p>

# Easy Pointer (WIP)

A web-based platform designed to help beginners (IT students) understand and practice **pointers in C** through interactive exercises and in-browser execution.

Students write C code, compile it to WebAssembly using WASM-4, and run it in a controlled sandboxed environment. The platform focuses on making memory concepts concrete and observable.

## Overview

The platform provides:

* An in-browser code editor (Monaco)
* C compilation and execution via WASM-4
* Progressive challenges
* GitHub-based authentication (OAuth2)
* Stateless session management using JWT
* Persistent storage with SQLite

The system is designed to remain simple, secure, and easy to deploy.

## Architecture

**Frontend**

* Node.js
* Vite
* React
* Monaco Editor

**Backend**

* Python
* FastAPI
* SQLite
* Caddy (reverse proxy)

**Execution Layer**

* [WASM-4 toolchain](https://wasm4.org/)
* WebAssembly sandbox
* Isolated user execution

Authentication flow:

1. User authenticates with GitHub (OAuth2)
2. Backend validates the OAuth2 flow
3. Backend issues a signed JWT
4. Frontend stores and attaches JWT to API requests
5. Backend remains stateless

## Project Structure

Come from the following conventions: https://github.com/zhanymkanov/fastapi-best-practices?tab=readme-ov-file

```
.
├── bin/
│   └── w4-linux/w4
├── Caddyfile
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── contexts/
│   │   ├── hooks/
│   │   ├── pages/
│   │   ├── utils/
│   │   └── userWorker.js
│   └── vite.config.js
├── http_request/
│   └── test.http
├── requirements.txt
├── src/
│   ├── auth/
│   ├── challenge/
│   ├── editor/
│   ├── github/
│   ├── user/
│   ├── database.py
│   └── main.py
└── templates/
    └── w4/hello-world/
```

## Backend Modules

* `auth/` – OAuth2 flow, JWT generation, authentication dependencies
* `github/` – GitHub API client and configuration
* `user/` – User models, DAO, business logic
* `challenge/` – Challenge definitions and validation
* `editor/` – Code execution logic and WASM integration
* `database.py` – SQLite configuration and session management
* `main.py` – FastAPI application entry point

## Frontend Structure

* `contexts/` – Authentication context
* `hooks/` – Custom hooks (API client, auth, local storage, iframe keyboard gating)
* `pages/` – Layouts, editor page, OAuth2 flow pages
* `userWorker.js` – Execution worker
* `api.js` – Backend communication layer

## Installation

### Backend

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn src.main:app --reload
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```


### Reverse Proxy

A Caddyfile is provided to be able to test the application behind reverse proxy with managed SSL certificate.

```bash
caddy start
```

```bash
fastapi dev src/main.py --forwarded-allow-ips="*" --root-path /api
```

```bash
cd frontend
npm run dev
```

Go to https://localhost:8443 