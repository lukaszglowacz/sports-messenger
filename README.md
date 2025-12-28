# ⚽ Sports Messenger

> Aplikacja messengera do komunikacji między zawodnikami i działaczami sportowymi.

[![Tests](https://img.shields.io/badge/tests-28%20passed-brightgreen)]()
[![Coverage](https://img.shields.io/badge/coverage-69%25-yellow)]()
[![Docker](https://img.shields.io/badge/docker-ready-blue)]()
[![TypeScript](https://img.shields.io/badge/TypeScript-5.3-blue)]()
[![Python](https://img.shields.io/badge/Python-3.11-blue)]()

---

## 📋 Spis treści

- [O projekcie](#-o-projekcie)
- [Funkcjonalności](#-funkcjonalności)
- [Technologie](#-technologie)
- [Szybki start](#-szybki-start)
- [Architektura](#-architektura)
- [Reguły biznesowe](#-reguły-biznesowe)
- [Testowanie](#-testowanie)
- [API Documentation](#-api-documentation)
- [Zrzuty ekranu](#-zrzuty-ekranu)
- [Troubleshooting](#-troubleshooting)
- [Roadmap](#-roadmap)

---

## 🎯 O projekcie

Sports Messenger to uproszczony moduł czatu umożliwiający wymianę wiadomości tekstowych między zawodnikami a działaczami sportowymi z zachowaniem określonych reguł biznesowych.

### Kluczowe cechy

✅ **Full-stack aplikacja** - React + FastAPI  
✅ **Docker Compose** - łatwe uruchomienie jedną komendą  
✅ **TypeScript** - type-safe frontend  
✅ **Material-UI** - nowoczesny, responsywny interfejs  
✅ **28 testów** - jednostkowe i integracyjne  
✅ **69% coverage** - backend dobrze przetestowany  
✅ **Emoji picker** - wsparcie dla emotikon  
✅ **Responsywne** - działa na mobile i desktop  

---

## ✨ Funkcjonalności

### Główne funkcje

- 💬 **Wymiana wiadomości** - tekstowych z emoji
- 👥 **Wymiana kontaktów** - system zaproszeń i akceptacji
- 📊 **Limity wiadomości** - automatyczna walidacja
- 🔄 **Real-time updates** - natychmiastowe odświeżanie
- 📱 **Responsywny UI** - mobile drawer, desktop split-view
- 🎨 **Nowoczesny design** - gradienty, animacje, progress bars
- ⚡ **Hot reload** - szybki development workflow

### Reguły biznesowe

| Typ komunikacji | Wymiana kontaktów | Limit dzienny |
|-----------------|-------------------|---------------|
| Zawodnik ↔ Zawodnik | ❌ Nie wymagana | 100 wiadomości ogółem |
| Zawodnik → Manager | ✅ Wymagana | 5 wiadomości do każdego |
| Manager → Zawodnik | ✅ Wymagana | ♾️ Bez limitu |
| Manager ↔ Manager | 🚫 Zabronione | - |

---

## 🛠️ Technologie

### Backend
```
FastAPI 0.109.0          # Nowoczesny Python web framework
SQLAlchemy 2.0.25        # ORM
Pydantic 2.5.3          # Walidacja danych
Uvicorn 0.27.0          # ASGI server (hot reload)
pytest 7.4.4            # Testing framework
SQLite                  # Database (development)
```

### Frontend
```
React 18.2.0            # UI framework
TypeScript 5.3.3        # Type safety
Material-UI 5.15.6      # Component library
Zustand 4.5.0           # State management
Axios 1.6.5             # HTTP client
React Toastify 10.0.4   # Notifications
Vite 5.0.12             # Build tool (HMR)
Vitest 1.2.0            # Testing framework
emoji-picker-react      # Emoji support
```

### DevOps
```
Docker                  # Containerization
Docker Compose          # Multi-container orchestration
```

---

## 🚀 Szybki start

### Wymagania

- **Docker Desktop** (lub Docker + Docker Compose)
- **Git**

### Instalacja i uruchomienie

```bash
# 1. Sklonuj repozytorium
git clone https://github.com/lukaszglowacz/sports-messenger.git
cd sports-messenger

# 2. Uruchom aplikację
docker-compose up --build

# 3. Poczekaj ~2-3 minuty na build

# 4. Otwórz w przeglądarce
```

**Adresy:**
- 🎨 **Frontend**: http://localhost:3000
- ⚙️ **Backend API**: http://localhost:8000
- 📚 **API Docs (Swagger)**: http://localhost:8000/docs

### Pierwsze kroki

1. **Wybierz użytkownika** z dropdown (Zawodnik 1, Zawodnik 2, Manager)
2. **Kliknij na kontakt** z listy kontaktów
3. **Wyślij wiadomość** - wpisz tekst, wybierz emoji 😊, wyślij
4. **Testuj limity** - spróbuj wysłać więcej niż 5 wiadomości do Managera

---

## 🏗️ Architektura

### Struktura projektu

```
sports-messenger/
├── backend/                    # FastAPI backend
│   ├── app/
│   │   ├── models/            # SQLAlchemy models
│   │   ├── routes/            # API endpoints
│   │   ├── services/          # Business logic
│   │   ├── schemas.py         # Pydantic schemas
│   │   ├── database.py        # DB configuration
│   │   ├── seed.py            # Initial data
│   │   └── main.py            # FastAPI app
│   ├── tests/                 # Backend tests (pytest)
│   ├── requirements.txt
│   ├── pytest.ini
│   └── Dockerfile
├── frontend/                   # React frontend
│   ├── src/
│   │   ├── components/        # React components
│   │   ├── api/               # API client
│   │   ├── store/             # Zustand store
│   │   ├── types/             # TypeScript types
│   │   ├── test/              # Frontend tests (Vitest)
│   │   ├── App.tsx            # Main component
│   │   └── main.tsx           # Entry point
│   ├── package.json
│   ├── vitest.config.ts
│   └── Dockerfile
├── docker-compose.yml
├── README.md                   # This file
└── TESTING.md                  # Test documentation
```

### Flow diagram

```
┌─────────────┐         ┌─────────────┐         ┌─────────────┐
│   Browser   │────────▶│   React     │────────▶│   FastAPI   │
│  (Client)   │◀────────│  Frontend   │◀────────│   Backend   │
└─────────────┘         └─────────────┘         └─────────────┘
                              │                        │
                              │                        │
                        Zustand Store            SQLAlchemy
                        React State               SQLite DB
```

### Komponenty

**Frontend (React + TypeScript):**
- `App.tsx` - Layout, routing, responsive drawer
- `UserSwitcher.tsx` - Przełącznik użytkownika
- `ContactList.tsx` - Lista kontaktów, zaproszenia
- `ChatWindow.tsx` - Okno czatu, emoji picker, limity

**Backend (FastAPI + Python):**
- `models/` - User, Message, ContactExchange
- `routes/` - API endpoints (users, contacts, messages)
- `services/` - MessageValidationService, ContactService
- `schemas.py` - Pydantic validation schemas

---

## 📜 Reguły biznesowe

### 1. Komunikacja Zawodnik ↔ Zawodnik

- ✅ **Bez wymiany kontaktów** - mogą pisać od razu
- ⚠️ **Limit 100 wiadomości/dzień** - ogółem do wszystkich

**Przykład:**
```
Zawodnik 1 → Zawodnik 2: 50 wiadomości ✅
Zawodnik 1 → Zawodnik 3: 50 wiadomości ✅
Zawodnik 1 → Zawodnik 4: 1 wiadomość ❌ (limit 100/dzień)
```

### 2. Komunikacja Zawodnik ↔ Manager

- ⚠️ **Wymaga wymiany kontaktów** - zaproszenie + akceptacja
- ⚠️ **Limit 5 wiadomości/dzień** - do każdego Managera osobno
- ⚠️ **Liczy się do 100 ogółem** - również

**Przepływ wymiany:**
```
1. Zawodnik wysyła zaproszenie → Status: PENDING
2. Manager akceptuje → Status: ACCEPTED
3. Teraz mogą pisać (5 wiadomości/dzień)
```

### 3. Komunikacja Manager ↔ Manager

- 🚫 **Zabronione** - Managerowie nie widzą się nawzajem

### 4. Limitowanie

**Zawodnik:**
- 📊 100 wiadomości/dzień ogółem
- 📊 5 wiadomości/dzień do każdego Managera
- 🔄 Reset o północy

**Manager:**
- ♾️ Bez limitów

**Walidacja:**
- ✅ Backend - HTTP 429 przy przekroczeniu
- ✅ Frontend - Progress bars, disabled button, alert

---

## 🧪 Testowanie

### Quick Start

```bash
# Backend tests
docker-compose exec backend pytest

# Frontend tests
docker-compose exec frontend npm test

# Coverage reports
docker-compose exec backend pytest --cov=app --cov-report=html
docker-compose exec frontend npm run test:coverage
```

### Test Suite

```
┌──────────────────────────────────────────┐
│         Test Suite Summary               │
├──────────────────────────────────────────┤
│ Backend (pytest):          15 tests ✅   │
│ Frontend (Vitest):         13 tests ✅   │
│ ─────────────────────────────────────────│
│ TOTAL:                     28 tests ✅   │
│                                          │
│ Backend Coverage:          69%           │
│ Frontend Coverage:         ~75%          │
└──────────────────────────────────────────┘
```

### Co jest testowane?

#### Backend (pytest)
- ✅ Limity wiadomości (100/dzień, 5/official)
- ✅ Walidacja wymiany kontaktów
- ✅ API endpoints (success + error cases)
- ✅ Reguły biznesowe
- ✅ HTTP status codes (201, 400, 429)

#### Frontend (Vitest)
- ✅ Zustand store (state management)
- ✅ API client (wszystkie metody)
- ✅ Error handling
- ✅ Mock responses

📚 **Pełna dokumentacja:** [TESTING.md](./TESTING.md)

---

## 📡 API Documentation

### Base URL
```
http://localhost:8000/api
```

### Endpoints

#### Users
```http
GET    /users              # Lista wszystkich użytkowników
GET    /users/{id}         # Szczegóły użytkownika
```

#### Contacts
```http
GET    /contacts?user_id={id}                    # Lista kontaktów
POST   /contacts/exchange/request                # Wyślij zaproszenie
POST   /contacts/exchange/{id}/accept            # Akceptuj
POST   /contacts/exchange/{id}/reject            # Odrzuć
DELETE /contacts/exchange/{id}                   # Rozłącz
```

#### Messages
```http
POST   /messages                                 # Wyślij wiadomość
GET    /messages?user_id={id}&contact_id={id}   # Historia
GET    /messages/limits?user_id={id}            # Limity
POST   /messages/validate                        # Waliduj uprawnienia
```

### Przykłady

**Wyślij wiadomość:**
```bash
curl -X POST http://localhost:8000/api/messages \
  -H "Content-Type: application/json" \
  -d '{
    "sender_id": 1,
    "recipient_id": 2,
    "content": "Cześć! 👋"
  }'
```

**Sprawdź limity:**
```bash
curl http://localhost:8000/api/messages/limits?user_id=1
```

**Response:**
```json
{
  "total_today": 15,
  "daily_limit": 100,
  "is_exceeded": false
}
```

📚 **Interactive API Docs:** http://localhost:8000/docs

---

## 📸 Zrzuty ekranu

### Desktop View
```
┌────────────────────────────────────────────────────────────┐
│  ⚽ Sports Messenger           👤 Zalogowany jako: Zawodnik 1│
├──────────────┬─────────────────────────────────────────────┤
│              │  👤 Zawodnik 2                      ℹ️      │
│ 📋 Kontakty  │  ─────────────────────────────────────────  │
│              │                                              │
│ 👤 Zawodnik 2│                    Cześć! Idziesz na trening?│
│              │                         około 6 godzin temu  │
│ 🏃 Zawodnik 3│                                              │
│              │  Tak! O 17:00 😊                             │
│ 👔 Manager   │  około 5 godzin temu                         │
│   ✓ Połączeni│                                              │
│              │  ─────────────────────────────────────────  │
│              │  Ogólnie dzisiaj: 15/100 [████░░░░░] 15%    │
│              │  ─────────────────────────────────────────  │
│              │  📝 Napisz wiadomość... 😊           [→]    │
└──────────────┴─────────────────────────────────────────────┘
```

### Mobile View
```
┌─────────────────────┐
│ ☰  Sports Messenger │
├─────────────────────┤
│  ←  👤 Zawodnik 2   │
├─────────────────────┤
│                     │
│     Cześć! 👋      │
│                     │
│  Hej!               │
│                     │
├─────────────────────┤
│ Ogółem: 2/100       │
│ [██░░░░░░░] 2%     │
├─────────────────────┤
│ Napisz... 😊  [→]  │
└─────────────────────┘
```

### Przykładowe interakcje

**1. Wysyłanie wiadomości z emoji:**
```
[Pole tekstowe] Cześć! 👋
[Przycisk emoji 😊] → Otwiera picker
[Wybierz emoji] → Dodaje do tekstu
[Przycisk →] → Wysyła
[Toast] ✓ Wysłano
```

**2. Przekroczenie limitu:**
```
[5/5 wiadomości do Managera]
[Progress bar: 100% czerwony]
⛔ Osiągnięto limit wiadomości!
[Przycisk → disabled]
```

**3. Wymiana kontaktów:**
```
[Lista: Dostępni do wymiany]
[Manager] [Wyślij zaproszenie]
→ [Przełącz na Managera]
[Lista: Oczekujące zaproszenia]
[Zawodnik 1] [Akceptuj] [Odrzuć]
```

---

## 🐛 Troubleshooting

### Backend nie startuje

```bash
# Sprawdź logi
docker-compose logs backend

# Restart
docker-compose restart backend

# Full rebuild
docker-compose down
docker-compose up --build
```

### Frontend nie startuje

```bash
# Sprawdź logi
docker-compose logs frontend

# Clear cache
docker-compose down
docker volume prune
docker-compose up --build
```

### Baza danych nie inicjalizuje się

```bash
# Usuń volume i przebuduj
docker-compose down -v
docker-compose up --build
```

### Port zajęty (3000 lub 8000)

```bash
# Opcja 1: Zatrzymaj proces na porcie
lsof -ti:3000 | xargs kill -9  # macOS/Linux
netstat -ano | findstr :3000   # Windows

# Opcja 2: Zmień port w docker-compose.yml
# Frontend: "3001:3000"
# Backend: "8001:8000"
```

### Hot reload nie działa

```bash
# Sprawdź czy pliki są montowane
docker-compose exec backend ls -la /app
docker-compose exec frontend ls -la /app

# Restart z clean slate
docker-compose down
docker-compose up
```

### Testy nie działają

```bash
# Backend
docker-compose exec backend pytest --version
docker-compose exec backend pip list | grep pytest

# Frontend
docker-compose exec frontend npm list vitest
docker-compose exec frontend npm test -- --version
```

---

## 🛣️ Roadmap

### ✅ Zrealizowane (v1.0)

- ✅ Full-stack aplikacja (React + FastAPI)
- ✅ Docker Compose deployment
- ✅ Wymiana wiadomości tekstowych
- ✅ System wymiany kontaktów
- ✅ Limity wiadomości (100/dzień, 5/official)
- ✅ Responsywny UI (mobile + desktop)
- ✅ Emoji picker
- ✅ Progress bars dla limitów
- ✅ Toast notifications
- ✅ 28 testów (69% coverage)
- ✅ TypeScript + type safety
- ✅ Material-UI design
- ✅ Hot reload (dev)

### 🎯 Planowane (v2.0)

**Funkcjonalności:**
- [ ] WebSocket - real-time messaging
- [ ] Oznaczanie jako przeczytane
- [ ] Wyszukiwanie kontaktów
- [ ] Filtrowanie historii
- [ ] Eksport konwersacji (PDF/TXT)
- [ ] Status online/offline
- [ ] Typing indicators
- [ ] Push notifications

**UI/UX:**
- [ ] Dark mode
- [ ] Widok minimalizowany (bottom-right)
- [ ] Infinite scroll dla wiadomości
- [ ] Skeleton loaders
- [ ] Drag & drop attachments
- [ ] Voice messages

**Backend:**
- [ ] PostgreSQL (production)
- [ ] Redis (caching)
- [ ] Celery (background tasks)
- [ ] Migracje (Alembic)
- [ ] Rate limiting
- [ ] Logging (structured)
- [ ] Monitoring (Sentry)

**DevOps:**
- [ ] CI/CD (GitHub Actions)
- [ ] Kubernetes deployment
- [ ] Staging environment
- [ ] E2E tests (Playwright)
- [ ] Performance testing
- [ ] Security audit

---

## 📄 Licencja

Projekt stworzony na potrzeby zadania rekrutacyjnego.

---

## 👨‍💻 Autor

**Łukasz Głowacz**  
📧 [contact@lukaszglowacz.com](mailto:contact@lukaszglowacz.com)
🔗 [github.com/lukaszglowacz](https://github.com/lukaszglowacz)
💼 [LinkedIn Profile](https://linkedin.com/in/lukaszglowacz)
🌐 [lukaszglowacz.com](https://lukaszglowacz.com)

---

## 🙏 Podziękowania

- **Anthropic** - za Claude AI
- **FastAPI** - za świetny framework
- **React Team** - za React
- **MUI Team** - za Material-UI

---

## 📚 Dokumentacja

- 📖 [TESTING.md](./TESTING.md) - Kompletna dokumentacja testów
- 📖 [ARCHITECTURE.md](./ARCHITECTURE.md) - Szczegóły architektury
- 📖 API Docs (Swagger) - http://localhost:8000/docs

---

## 🚀 Quick Reference

### Komendy Docker

```bash
# Start
docker-compose up

# Start (rebuild)
docker-compose up --build

# Stop
docker-compose down

# Stop (remove volumes)
docker-compose down -v

# Logs
docker-compose logs -f

# Enter container
docker-compose exec backend sh
docker-compose exec frontend sh
```

### Komendy Development

```bash
# Backend tests
docker-compose exec backend pytest
docker-compose exec backend pytest --cov=app

# Frontend tests
docker-compose exec frontend npm test
docker-compose exec frontend npm run test:coverage

# Database reset
docker-compose down -v && docker-compose up --build

# View logs
docker-compose logs backend -f
docker-compose logs frontend -f
```

### URLs

```bash
# Frontend
http://localhost:3000

# Backend API
http://localhost:8000

# API Documentation (Swagger)
http://localhost:8000/docs

# API Documentation (ReDoc)
http://localhost:8000/redoc
```

---
