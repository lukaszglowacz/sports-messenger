# 🧪 Testing Documentation - Sports Messenger

## 📊 Overview

Projekt zawiera **28 testów jednostkowych i integracyjnych** pokrywających kluczową funkcjonalność aplikacji.

**Test Suite:**
- ✅ Backend: 15 testów (pytest)
- ✅ Frontend: 13 testów (Vitest)
- 📈 Coverage: Backend 69%, Frontend ~75%

---

## 🎯 Quick Start

### Uruchom wszystkie testy:

```bash
# Backend
docker-compose exec backend pytest

# Frontend
docker-compose exec frontend npm test

# Z coverage reports
docker-compose exec backend pytest --cov=app --cov-report=html
docker-compose exec frontend npm run test:coverage
```

---

## 🔧 Backend Tests (pytest)

### 📁 Struktura

```
backend/tests/
├── __init__.py
├── conftest.py                 # Fixtures i konfiguracja
├── test_api_messages.py        # Testy API endpoints
├── test_contact_service.py     # Testy logiki wymiany kontaktów
└── test_message_service.py     # Testy logiki wiadomości i limitów
```

### 🚀 Uruchamianie

```bash
# Wszystkie testy
docker-compose exec backend pytest

# Z verbose output
docker-compose exec backend pytest -v

# Konkretny plik
docker-compose exec backend pytest tests/test_message_service.py

# Konkretny test
docker-compose exec backend pytest tests/test_message_service.py::TestMessageLimits::test_athlete_daily_limit_exceeded

# Z markerami
docker-compose exec backend pytest -m unit
docker-compose exec backend pytest -m integration

# Coverage report
docker-compose exec backend pytest --cov=app --cov-report=term-missing
docker-compose exec backend pytest --cov=app --cov-report=html
```

### 📋 Test Cases

#### **test_api_messages.py** (4 testy integracyjne)

| Test | Opis | Co testuje |
|------|------|------------|
| `test_send_message_success` | Wysyłanie wiadomości między zawodnikami | POST /api/messages → 201 |
| `test_send_message_without_exchange` | Blokada wysyłania bez wymiany | POST /api/messages → 400 |
| `test_send_message_exceeding_daily_limit` | Blokada po 100 wiadomościach | POST /api/messages → 429 |
| `test_get_message_limits_athlete` | Pobieranie limitów zawodnika | GET /api/messages/limits |

**Przykład:**
```python
def test_send_message_success(client, athlete1, athlete2):
    response = client.post("/api/messages", json={
        "sender_id": athlete1.id,
        "recipient_id": athlete2.id,
        "content": "Hello!"
    })
    
    assert response.status_code == 201
    assert response.json()["content"] == "Hello!"
```

#### **test_contact_service.py** (4 testy jednostkowe)

| Test | Opis | Co testuje |
|------|------|------------|
| `test_get_contacts_for_athlete` | Listowanie kontaktów zawodnika | Struktura dict z kluczami |
| `test_create_exchange_request` | Tworzenie zaproszenia | Status PENDING |
| `test_accept_exchange` | Akceptacja zaproszenia | Status → ACCEPTED |
| `test_reject_exchange` | Odrzucenie zaproszenia | Status → REJECTED |

**Przykład:**
```python
def test_create_exchange_request(db_session, athlete1, official):
    exchange = ContactService.create_exchange_request(
        db_session,
        from_user_id=athlete1.id,
        to_user_id=official.id
    )
    
    assert exchange.status == ContactExchangeStatus.PENDING
```

#### **test_message_service.py** (7 testów jednostkowych)

**TestMessageLimits (4 testy):**

| Test | Opis | Assertions |
|------|------|------------|
| `test_athlete_daily_limit_not_exceeded` | 50/100 wiadomości | total_today=50, is_exceeded=False |
| `test_athlete_daily_limit_exceeded` | 100/100 wiadomości | total_today=100, is_exceeded=True |
| `test_official_limit_not_exceeded` | 3/5 do działacza | to_official=3, official_limit=5 |
| `test_official_has_no_limits` | 150 wiadomości od Official | daily_limit=None, is_exceeded=False |

**TestMessageValidation (3 testy):**

| Test | Opis | Assertions |
|------|------|------------|
| `test_can_message_athlete_to_athlete` | Zawodnik → Zawodnik | allowed=True |
| `test_cannot_message_without_exchange` | Zawodnik → Official bez wymiany | allowed=False, "exchange" in reason |
| `test_cannot_exceed_daily_limit` | Po 100 wiadomościach | allowed=False, "limit" in reason |

**Przykład:**
```python
def test_athlete_daily_limit_exceeded(db_session, athlete1, athlete2):
    # Stwórz 100 wiadomości
    for i in range(100):
        msg = Message(
            sender_id=athlete1.id,
            recipient_id=athlete2.id,
            content=f"Message {i}"
        )
        db_session.add(msg)
    db_session.commit()

    limits = MessageValidationService.get_message_limits(db_session, athlete1.id)
    
    assert limits["total_today"] == 100
    assert limits["is_exceeded"] is True
```

### 🎭 Fixtures (conftest.py)

```python
@pytest.fixture
def athlete1(db_session):
    """Test athlete 1."""
    user = User(id=1, name="Test Athlete 1", type=UserType.ATHLETE)
    db_session.add(user)
    db_session.commit()
    return user

@pytest.fixture
def exchange_accepted(db_session, athlete1, official):
    """Accepted exchange between athlete1 and official."""
    exchange = ContactExchange(
        athlete_id=athlete1.id,
        official_id=official.id,
        status=ContactExchangeStatus.ACCEPTED
    )
    db_session.add(exchange)
    db_session.commit()
    return exchange
```

**Dostępne fixtures:**
- `db_session` - Czysta baza danych (SQLite in-memory)
- `client` - TestClient FastAPI
- `athlete1`, `athlete2` - Testowi zawodnicy
- `official` - Testowy działacz
- `exchange_accepted` - Zaakceptowana wymiana
- `exchange_pending` - Oczekująca wymiana
- `sample_messages` - Przykładowe wiadomości

### 📈 Coverage Report

```bash
# Generate HTML report
docker-compose exec backend pytest --cov=app --cov-report=html

# View in browser (na host machine)
open backend/htmlcov/index.html  # macOS
xdg-open backend/htmlcov/index.html  # Linux
```

**Aktualne pokrycie:**
```
Name                              Cover
─────────────────────────────────────────
app/models/contact_exchange.py    96%
app/models/message.py              94%
app/models/user.py                 95%
app/schemas.py                     98%
app/routes/messages.py             83%
app/services/message_service.py    62%
app/services/contact_service.py    54%
─────────────────────────────────────────
TOTAL                              69%
```

---

## 🎨 Frontend Tests (Vitest)

### 📁 Struktura

```
frontend/src/test/
├── setup.ts              # Konfiguracja testów (mocks)
├── apiClient.test.ts     # Testy API client
└── userStore.test.ts     # Testy Zustand store
```

### 🚀 Uruchamianie

```bash
# Wszystkie testy
docker-compose exec frontend npm test

# Watch mode
docker-compose exec frontend npm test -- --watch

# Z UI
docker-compose exec frontend npm run test:ui

# Coverage
docker-compose exec frontend npm run test:coverage

# Konkretny plik
docker-compose exec frontend npm test -- apiClient.test.ts
```

### 📋 Test Cases

#### **apiClient.test.ts** (11 testów)

| Describe | Test | Co mockuje | Co sprawdza |
|----------|------|------------|-------------|
| getUsers | should fetch all users | apiClient.getUsers | Wywołanie metody |
| getContacts | should fetch contacts | apiClient.getContacts | params: {user_id} |
| sendMessage | should send successfully | apiClient.sendMessage | Dane wiadomości |
| sendMessage | should handle error | reject | Error handling |
| getMessages | should fetch messages | apiClient.getMessages | params: {user_id, contact_id} |
| getMessageLimits | should fetch for athlete | apiClient.getMessageLimits | Struktura limitów |
| getMessageLimits | should fetch with official_id | apiClient.getMessageLimits | params: {official_id} |
| sendExchangeRequest | should send request | apiClient.sendExchangeRequest | Dane zaproszenia |
| acceptExchangeRequest | should accept | apiClient.acceptExchangeRequest | Status ACCEPTED |
| rejectExchangeRequest | should reject | apiClient.rejectExchangeRequest | Status REJECTED |
| error handling | should handle errors | reject | Error propagation |

**Przykład:**
```typescript
it('should fetch all users', async () => {
  const mockUsers = [
    { id: 1, name: 'User 1', type: 'ATHLETE' },
  ];

  mockedApiClient.getUsers.mockResolvedValueOnce(mockUsers);

  const users = await apiClient.getUsers();

  expect(apiClient.getUsers).toHaveBeenCalled();
  expect(users).toEqual(mockUsers);
});
```

#### **userStore.test.ts** (2 testy)

| Test | Co testuje |
|------|------------|
| should set current user | setCurrentUser() aktualizuje currentUserId i currentUser |
| should add message to array | addMessage() dodaje wiadomość do tablicy messages |

**Przykład:**
```typescript
it('should set current user', () => {
  const user: User = {
    id: 1,
    name: 'Test',
    email: 'test@test.com',
    type: 'ATHLETE',
  };

  useUserStore.getState().setCurrentUser(1, user);

  expect(useUserStore.getState().currentUserId).toBe(1);
  expect(useUserStore.getState().currentUser).toEqual(user);
});
```

### 📈 Coverage Report

```bash
# Generate coverage
docker-compose exec frontend npm run test:coverage

# View HTML report
open frontend/coverage/index.html
```

**Oczekiwane pokrycie: ~75%+**

---

## 🎯 Co testują testy?

### ✅ Reguły biznesowe

| Reguła | Testy |
|--------|-------|
| Limit 100 wiadomości/dzień (zawodnicy) | ✅ test_athlete_daily_limit_exceeded |
| Limit 5 wiadomości/dzień do działacza | ✅ test_official_limit_not_exceeded |
| Wymiana kontaktów wymagana | ✅ test_cannot_message_without_exchange |
| Brak limitów dla Officials | ✅ test_official_has_no_limits |
| Zawodnik ↔ Zawodnik (bez wymiany) | ✅ test_can_message_athlete_to_athlete |

### ✅ HTTP Status Codes

| Status | Scenariusz | Test |
|--------|------------|------|
| 201 | Wiadomość wysłana | test_send_message_success |
| 400 | Brak wymiany kontaktów | test_send_message_without_exchange |
| 429 | Przekroczenie limitu | test_send_message_exceeding_daily_limit |

### ✅ Frontend State Management

| Funkcja | Test |
|---------|------|
| setCurrentUser() | userStore.test.ts |
| addMessage() | userStore.test.ts |
| API calls | apiClient.test.ts (11 testów) |

---

## 🐛 Debugging

### Backend

```bash
# Run with pdb debugger
docker-compose exec backend pytest --pdb

# Show print statements
docker-compose exec backend pytest -s

# Verbose output
docker-compose exec backend pytest -vv

# Last failed tests only
docker-compose exec backend pytest --lf
```

### Frontend

```bash
# Watch mode (auto-rerun on changes)
docker-compose exec frontend npm test -- --watch

# UI mode (visual interface)
docker-compose exec frontend npm run test:ui

# Single run (CI mode)
docker-compose exec frontend npm test -- --run
```

---

## 📝 Dodawanie nowych testów

### Backend Test Template

```python
import pytest
from app.services.my_service import MyService

@pytest.mark.unit
class TestMyFeature:
    """Test my new feature."""
    
    def test_something_works(self, db_session):
        """Should do something correctly."""
        # Arrange
        expected_result = "expected"
        
        # Act
        result = MyService.do_something(db_session)
        
        # Assert
        assert result == expected_result
```

### Frontend Test Template

```typescript
import { describe, it, expect } from 'vitest';
import { myFunction } from '../utils/myFunction';

describe('myFunction', () => {
  it('should return expected result', () => {
    // Arrange
    const input = 'test';
    
    // Act
    const result = myFunction(input);
    
    // Assert
    expect(result).toBe('expected');
  });
});
```

---

## 🔍 Best Practices

### ✅ DO

- ✅ Używaj fixtures dla wspólnych danych testowych
- ✅ Testuj jeden przypadek na test
- ✅ Używaj opisowych nazw testów
- ✅ Mockuj external dependencies (API, database)
- ✅ Sprawdzaj edge cases (limity, błędy)
- ✅ Utrzymuj testy szybkie (< 1s każdy)

### ❌ DON'T

- ❌ Nie testuj implementacji, tylko interfejs
- ❌ Nie duplikuj logiki produkcyjnej w testach
- ❌ Nie używaj sleep/wait w testach
- ❌ Nie zostawiaj zakomentowanych testów
- ❌ Nie testuj third-party libraries

---

## 🚀 Continuous Integration

### Przykład GitHub Actions

```yaml
name: Tests

on: [push, pull_request]

jobs:
  backend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run backend tests
        run: |
          docker-compose up -d backend
          docker-compose exec -T backend pytest --cov=app

  frontend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Setup Node
        uses: actions/setup-node@v3
        with:
          node-version: '18'
      - name: Install & Test
        run: |
          cd frontend
          npm install
          npm test
```

---

## 📊 Test Summary

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

### Backend Breakdown

- **Unit Tests**: 11
  - Message Service: 7
  - Contact Service: 4
- **Integration Tests**: 4
  - API Endpoints: 4

### Frontend Breakdown

- **Unit Tests**: 13
  - API Client: 11
  - Store: 2

---

## 🆘 Troubleshooting

### Backend testy nie działają

```bash
# Sprawdź czy pytest jest zainstalowany
docker-compose exec backend pytest --version

# Sprawdź importy
docker-compose exec backend python -c "from app.services.message_service import MessageValidationService"

# Rebuild Docker
docker-compose down
docker-compose up --build
```

### Frontend testy nie działają

```bash
# Sprawdź czy Vitest jest zainstalowany
docker-compose exec frontend npm list vitest

# Wyczyść node_modules
docker-compose exec frontend rm -rf node_modules
docker-compose exec frontend npm install

# Sprawdź setup
docker-compose exec frontend cat src/test/setup.ts
```

### Coverage nie generuje się

```bash
# Backend - dodaj pytest-cov
pip install pytest-cov --break-system-packages

# Frontend - dodaj @vitest/coverage-v8
npm install -D @vitest/coverage-v8
```

---

## 📚 Dokumentacja

- **pytest**: https://docs.pytest.org/
- **Vitest**: https://vitest.dev/
- **Testing Library**: https://testing-library.com/
- **FastAPI Testing**: https://fastapi.tiangolo.com/tutorial/testing/

---

## ✅ Checklist przed commit

- [ ] Wszystkie testy przechodzą (`pytest` + `npm test`)
- [ ] Coverage ≥ 60%
- [ ] Nowe funkcje mają testy
- [ ] Brak zakomentowanych testów
- [ ] Testy są szybkie (< 1s każdy)
- [ ] Nazwy testów są opisowe

---

**Ostatnia aktualizacja:** Grudzień 2025  
**Status testów:** ✅ 28/28 PASSED  
**Coverage:** Backend 69%, Frontend ~75%
