# 🏗️ Architecture Documentation - Sports Messenger

> Szczegółowa dokumentacja architektury, wzorców projektowych i decyzji technicznych.

---

## 📋 Spis treści

- [Przegląd](#-przegląd)
- [Architektura systemu](#-architektura-systemu)
- [Backend Architecture](#-backend-architecture)
- [Frontend Architecture](#-frontend-architecture)
- [Database Schema](#-database-schema)
- [API Design](#-api-design)
- [State Management](#-state-management)
- [Security](#-security)
- [Performance](#-performance)
- [Deployment](#-deployment)
- [Design Patterns](#-design-patterns)
- [Decisions Log](#-decisions-log)

---

## 🎯 Przegląd

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                         Client Layer                         │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │   Browser    │  │    Mobile    │  │   Desktop    │      │
│  │  (Chrome)    │  │   (Safari)   │  │   (Edge)     │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└─────────────────────────────────────────────────────────────┘
                              │
                              │ HTTP/REST
                              │
┌─────────────────────────────▼─────────────────────────────┐
│                    Presentation Layer                      │
│  ┌─────────────────────────────────────────────────────┐  │
│  │            React 18 + TypeScript                     │  │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐          │  │
│  │  │   MUI    │  │ Zustand  │  │  Axios   │          │  │
│  │  │Components│  │  Store   │  │  Client  │          │  │
│  │  └──────────┘  └──────────┘  └──────────┘          │  │
│  └─────────────────────────────────────────────────────┘  │
│                         Port: 3000                         │
└────────────────────────────────────────────────────────────┘
                              │
                              │ REST API
                              │
┌─────────────────────────────▼─────────────────────────────┐
│                     Application Layer                      │
│  ┌─────────────────────────────────────────────────────┐  │
│  │              FastAPI + Python 3.11                   │  │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐          │  │
│  │  │  Routes  │  │ Services │  │ Schemas  │          │  │
│  │  │ (API)    │  │(Business)│  │(Pydantic)│          │  │
│  │  └──────────┘  └──────────┘  └──────────┘          │  │
│  └─────────────────────────────────────────────────────┘  │
│                         Port: 8000                         │
└────────────────────────────────────────────────────────────┘
                              │
                              │ ORM
                              │
┌─────────────────────────────▼─────────────────────────────┐
│                       Data Layer                           │
│  ┌─────────────────────────────────────────────────────┐  │
│  │         SQLAlchemy ORM + SQLite                      │  │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐          │  │
│  │  │   Users  │  │ Messages │  │ Exchanges│          │  │
│  │  │  Table   │  │  Table   │  │  Table   │          │  │
│  │  └──────────┘  └──────────┘  └──────────┘          │  │
│  └─────────────────────────────────────────────────────┘  │
│                    messenger.db (SQLite)                   │
└────────────────────────────────────────────────────────────┘
```

### Technology Stack Overview

| Layer | Technology | Purpose |
|-------|------------|---------|
| **Frontend** | React 18 + TypeScript | UI Framework |
| **State** | Zustand | Global state management |
| **UI Library** | Material-UI v5 | Component library |
| **HTTP Client** | Axios | API communication |
| **Build Tool** | Vite | Fast dev server + build |
| **Backend** | FastAPI | Python web framework |
| **ORM** | SQLAlchemy 2.0 | Database abstraction |
| **Validation** | Pydantic v2 | Data validation |
| **Database** | SQLite | Relational database |
| **Containerization** | Docker + Compose | Deployment |

---

## 🔧 Backend Architecture

### Layered Architecture Pattern

```
┌─────────────────────────────────────────────────────────┐
│                    Routes Layer                          │
│  (HTTP Request Handling, Input Validation)              │
│                                                          │
│  • /api/users      → users.py                           │
│  • /api/contacts   → contacts.py                        │
│  • /api/messages   → messages.py                        │
└─────────────────────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────┐
│                   Services Layer                         │
│  (Business Logic, Validation Rules)                     │
│                                                          │
│  • MessageValidationService                             │
│  • ContactService                                       │
└─────────────────────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────┐
│                    Models Layer                          │
│  (Database Models, Relationships)                       │
│                                                          │
│  • User (SQLAlchemy model)                              │
│  • Message (SQLAlchemy model)                           │
│  • ContactExchange (SQLAlchemy model)                   │
└─────────────────────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────┐
│                   Database Layer                         │
│  (SQLite Database)                                      │
│                                                          │
│  • messenger.db                                         │
└─────────────────────────────────────────────────────────┘
```

### Directory Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py                    # FastAPI application entry
│   ├── database.py                # DB configuration & session
│   ├── seed.py                    # Initial data seeding
│   │
│   ├── models/                    # SQLAlchemy Models
│   │   ├── __init__.py
│   │   ├── user.py                # User model + UserType enum
│   │   ├── message.py             # Message model
│   │   └── contact_exchange.py    # ContactExchange + Status enum
│   │
│   ├── routes/                    # API Endpoints
│   │   ├── __init__.py
│   │   ├── users.py               # GET /users, GET /users/{id}
│   │   ├── contacts.py            # Contact exchange endpoints
│   │   └── messages.py            # Message CRUD endpoints
│   │
│   ├── services/                  # Business Logic
│   │   ├── __init__.py
│   │   ├── message_service.py     # Message validation & limits
│   │   └── contact_service.py     # Contact exchange logic
│   │
│   └── schemas.py                 # Pydantic Schemas (validation)
│
├── tests/                         # Pytest tests
│   ├── conftest.py                # Test fixtures
│   ├── test_api_messages.py
│   ├── test_contact_service.py
│   └── test_message_service.py
│
├── requirements.txt               # Python dependencies
├── pytest.ini                     # Pytest configuration
└── Dockerfile                     # Docker image definition
```

### Key Components

#### 1. Models (SQLAlchemy)

**User Model:**
```python
class User(Base):
    __tablename__ = "users"
    
    id: int (PK)
    name: str
    email: str (unique)
    type: UserType (ATHLETE | OFFICIAL)
    created_at: datetime
    
    # Relationships
    sent_messages: List[Message]
    received_messages: List[Message]
    initiated_exchanges: List[ContactExchange]
```

**Message Model:**
```python
class Message(Base):
    __tablename__ = "messages"
    
    id: int (PK)
    sender_id: int (FK -> users.id)
    recipient_id: int (FK -> users.id)
    content: str
    created_at: datetime
    
    # Relationships
    sender: User
    recipient: User
```

**ContactExchange Model:**
```python
class ContactExchange(Base):
    __tablename__ = "contact_exchanges"
    
    id: int (PK)
    athlete_id: int (FK -> users.id)
    official_id: int (FK -> users.id)
    status: ContactExchangeStatus (PENDING | ACCEPTED | REJECTED)
    initiated_by: int (FK -> users.id)
    created_at: datetime
    responded_at: datetime (nullable)
    
    # Relationships
    athlete: User
    official: User
    initiator: User
```

#### 2. Services (Business Logic)

**MessageValidationService:**
```python
class MessageValidationService:
    @staticmethod
    def can_send_message(db, sender_id, recipient_id) -> Dict:
        """
        Validates if sender can message recipient.
        
        Checks:
        1. User types (Athlete/Official)
        2. Contact exchange status
        3. Daily limits (100 for athletes)
        4. Official limits (5 per official)
        
        Returns:
            {
                "allowed": bool,
                "reason": str | None
            }
        """
    
    @staticmethod
    def get_message_limits(db, user_id, official_id=None) -> Dict:
        """
        Returns current message limits for user.
        
        Returns:
            {
                "total_today": int,
                "daily_limit": int | None,
                "to_official": int | None,
                "official_limit": int | None,
                "is_exceeded": bool
            }
        """
```

**ContactService:**
```python
class ContactService:
    @staticmethod
    def get_contacts_for_user(db, user_id) -> Dict:
        """Returns contacts, pending requests, potential contacts."""
    
    @staticmethod
    def create_exchange_request(db, from_user_id, to_user_id):
        """Creates PENDING exchange request."""
    
    @staticmethod
    def accept_exchange(db, exchange_id, user_id):
        """Accepts exchange → status = ACCEPTED."""
    
    @staticmethod
    def reject_exchange(db, exchange_id, user_id):
        """Rejects exchange → status = REJECTED."""
```

#### 3. Routes (API Endpoints)

**Pattern:**
```python
@router.post("/messages", status_code=201)
async def send_message(
    message: MessageCreateRequest,
    db: Session = Depends(get_db)
):
    # 1. Validate using service
    validation = MessageValidationService.can_send_message(
        db, message.sender_id, message.recipient_id
    )
    
    # 2. Return error if not allowed
    if not validation["allowed"]:
        raise HTTPException(status_code=400, detail=validation["reason"])
    
    # 3. Create message
    new_message = Message(**message.dict())
    db.add(new_message)
    db.commit()
    
    # 4. Return response
    return MessageResponse.from_orm(new_message)
```

---

## 🎨 Frontend Architecture

### Component Architecture

```
┌─────────────────────────────────────────────────────────┐
│                      App.tsx                             │
│  (Root Component, Layout, Theme Provider)               │
│                                                          │
│  ┌──────────────────┐  ┌──────────────────┐           │
│  │   UserSwitcher   │  │  Responsive      │           │
│  │   (Dropdown)     │  │  Layout          │           │
│  └──────────────────┘  └──────────────────┘           │
└─────────────────────────────────────────────────────────┘
              │                           │
              ▼                           ▼
┌─────────────────────┐    ┌─────────────────────────────┐
│   ContactList.tsx   │    │      ChatWindow.tsx         │
│                     │    │                             │
│  • Contacts         │    │  • Message History          │
│  • Pending Requests │    │  • Input Field              │
│  • Send Invites     │    │  • Emoji Picker             │
│  • Accept/Reject    │    │  • Limit Progress Bars      │
└─────────────────────┘    └─────────────────────────────┘
              │                           │
              └───────────┬───────────────┘
                          ▼
              ┌─────────────────────┐
              │   Zustand Store     │
              │   (Global State)    │
              │                     │
              │  • currentUser      │
              │  • selectedContact  │
              │  • messages[]       │
              │  • refreshTrigger   │
              └─────────────────────┘
                          │
                          ▼
              ┌─────────────────────┐
              │    API Client       │
              │    (Axios)          │
              │                     │
              │  • getUsers()       │
              │  • getContacts()    │
              │  • sendMessage()    │
              │  • getMessages()    │
              └─────────────────────┘
```

### Directory Structure

```
frontend/
├── src/
│   ├── main.tsx                   # App entry point
│   ├── App.tsx                    # Root component
│   │
│   ├── components/                # React components
│   │   ├── UserSwitcher.tsx       # User selection dropdown
│   │   ├── ContactList.tsx        # Contacts sidebar
│   │   └── ChatWindow.tsx         # Chat interface
│   │
│   ├── api/                       # API layer
│   │   └── client.ts              # Axios client + methods
│   │
│   ├── store/                     # State management
│   │   └── userStore.ts           # Zustand store
│   │
│   ├── types/                     # TypeScript types
│   │   └── index.ts               # Shared types
│   │
│   └── test/                      # Tests
│       ├── setup.ts               # Test configuration
│       ├── apiClient.test.ts      # API client tests
│       └── userStore.test.ts      # Store tests
│
├── public/                        # Static assets
├── index.html                     # HTML template
├── package.json                   # Dependencies
├── tsconfig.json                  # TypeScript config
├── vite.config.ts                 # Vite config
├── vitest.config.ts               # Test config
└── Dockerfile                     # Docker image
```

### Key Components

#### 1. State Management (Zustand)

```typescript
interface UserStore {
  // State
  currentUserId: number | null;
  currentUser: User | null;
  selectedContact: ContactInfo | null;
  messages: Message[];
  refreshTrigger: number;
  
  // Actions
  setCurrentUser: (id: number, user: User) => void;
  setSelectedContact: (contact: ContactInfo | null) => void;
  setMessages: (messages: Message[]) => void;
  addMessage: (message: Message) => void;
  triggerRefresh: () => void;
}
```

**Why Zustand?**
- ✅ Lightweight (< 1KB)
- ✅ No boilerplate
- ✅ TypeScript support
- ✅ DevTools integration
- ✅ No Provider needed

#### 2. API Client (Axios)

```typescript
const api = axios.create({
  baseURL: 'http://localhost:8000/api',
  headers: { 'Content-Type': 'application/json' }
});

export const apiClient = {
  // Users
  getUsers: () => api.get<User[]>('/users'),
  
  // Messages
  sendMessage: (data) => api.post<Message>('/messages', data),
  getMessages: (userId, contactId) => 
    api.get<Message[]>('/messages', { params: { user_id, contact_id } }),
  
  // Contacts
  getContacts: (userId) => 
    api.get<ContactResponse>('/contacts', { params: { user_id } }),
  
  // Exchange
  sendExchangeRequest: (data) => 
    api.post('/contacts/exchange/request', data),
  acceptExchangeRequest: (id, userId) => 
    api.post(`/contacts/exchange/${id}/accept`, { user_id }),
};
```

#### 3. Component Patterns

**Smart Component (Container):**
```typescript
// App.tsx
export const App = () => {
  const { currentUserId, selectedContact } = useUserStore();
  const [users, setUsers] = useState<User[]>([]);
  
  useEffect(() => {
    // Fetch data
    apiClient.getUsers().then(setUsers);
  }, []);
  
  return (
    <ThemeProvider theme={theme}>
      <Layout>
        <UserSwitcher users={users} />
        <ContactList />
        {selectedContact && <ChatWindow />}
      </Layout>
    </ThemeProvider>
  );
};
```

**Presentational Component:**
```typescript
// ChatWindow.tsx
export const ChatWindow = () => {
  const { selectedContact, messages } = useUserStore();
  
  return (
    <Box>
      <Header contact={selectedContact} />
      <MessageList messages={messages} />
      <MessageInput onSend={handleSend} />
    </Box>
  );
};
```

---

## 🗄️ Database Schema

### ERD (Entity Relationship Diagram)

```
┌─────────────────────┐
│       Users         │
├─────────────────────┤
│ PK  id              │
│     name            │
│     email (unique)  │
│     type            │◄───┐
│     created_at      │    │
└─────────────────────┘    │
         △                 │
         │                 │
         │ 1:N             │ N:1
         │                 │
┌────────┴────────┐   ┌────┴─────────────────┐
│    Messages     │   │  ContactExchanges    │
├─────────────────┤   ├──────────────────────┤
│ PK  id          │   │ PK  id               │
│ FK  sender_id   │   │ FK  athlete_id       │
│ FK  recipient_id│   │ FK  official_id      │
│     content     │   │     status           │
│     created_at  │   │ FK  initiated_by     │
└─────────────────┘   │     created_at       │
                      │     responded_at     │
                      └──────────────────────┘
```

### Table Definitions

#### Users Table
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    type VARCHAR(20) NOT NULL,  -- 'ATHLETE' | 'OFFICIAL'
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_users_type ON users(type);
CREATE INDEX idx_users_email ON users(email);
```

#### Messages Table
```sql
CREATE TABLE messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sender_id INTEGER NOT NULL,
    recipient_id INTEGER NOT NULL,
    content TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (sender_id) REFERENCES users(id),
    FOREIGN KEY (recipient_id) REFERENCES users(id)
);

CREATE INDEX idx_messages_sender ON messages(sender_id);
CREATE INDEX idx_messages_recipient ON messages(recipient_id);
CREATE INDEX idx_messages_created_at ON messages(created_at);
CREATE INDEX idx_messages_conversation ON messages(sender_id, recipient_id);
```

#### ContactExchanges Table
```sql
CREATE TABLE contact_exchanges (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    athlete_id INTEGER NOT NULL,
    official_id INTEGER NOT NULL,
    status VARCHAR(20) NOT NULL,  -- 'PENDING' | 'ACCEPTED' | 'REJECTED'
    initiated_by INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    responded_at TIMESTAMP,
    
    FOREIGN KEY (athlete_id) REFERENCES users(id),
    FOREIGN KEY (official_id) REFERENCES users(id),
    FOREIGN KEY (initiated_by) REFERENCES users(id),
    
    UNIQUE(athlete_id, official_id)
);

CREATE INDEX idx_exchanges_status ON contact_exchanges(status);
CREATE INDEX idx_exchanges_athlete ON contact_exchanges(athlete_id);
CREATE INDEX idx_exchanges_official ON contact_exchanges(official_id);
```

### Sample Data (Seed)

```python
# Users
users = [
    User(id=1, name="Zawodnik 1", email="zawodnik1@test.com", type=UserType.ATHLETE),
    User(id=2, name="Zawodnik 2", email="zawodnik2@test.com", type=UserType.ATHLETE),
    User(id=3, name="Manager", email="manager@test.com", type=UserType.OFFICIAL),
]

# Contact Exchange (Zawodnik 2 ↔ Manager)
exchange = ContactExchange(
    athlete_id=2,
    official_id=3,
    status=ContactExchangeStatus.ACCEPTED,
    initiated_by=2
)

# Sample Messages
messages = [
    Message(sender_id=1, recipient_id=2, content="Cześć! Idziesz na trening?"),
    Message(sender_id=2, recipient_id=1, content="Tak! O 17:00 😊"),
]
```

---

## 📡 API Design

### RESTful Principles

| Resource | GET | POST | PUT/PATCH | DELETE |
|----------|-----|------|-----------|--------|
| `/users` | List all | - | - | - |
| `/users/{id}` | Get one | - | - | - |
| `/contacts` | List contacts | - | - | - |
| `/contacts/exchange/request` | - | Create | - | - |
| `/contacts/exchange/{id}/accept` | - | Accept | - | - |
| `/contacts/exchange/{id}` | - | - | - | Delete |
| `/messages` | List | Create | - | - |
| `/messages/limits` | Get limits | - | - | - |

### Request/Response Examples

#### Send Message
```http
POST /api/messages
Content-Type: application/json

{
  "sender_id": 1,
  "recipient_id": 2,
  "content": "Hello! 👋"
}
```

**Response (201 Created):**
```json
{
  "id": 1,
  "sender_id": 1,
  "recipient_id": 2,
  "content": "Hello! 👋",
  "created_at": "2024-12-28T10:00:00Z"
}
```

**Error (429 Too Many Requests):**
```json
{
  "detail": "Osiągnięto dzienny limit wiadomości (100)"
}
```

#### Get Message Limits
```http
GET /api/messages/limits?user_id=1&official_id=3
```

**Response (200 OK):**
```json
{
  "total_today": 15,
  "daily_limit": 100,
  "to_official": 3,
  "official_limit": 5,
  "is_exceeded": false
}
```

### Error Handling Strategy

| Status Code | Meaning | When Used |
|-------------|---------|-----------|
| 200 | OK | Successful GET |
| 201 | Created | Successful POST (message, exchange) |
| 400 | Bad Request | Validation error, no exchange |
| 404 | Not Found | Resource doesn't exist |
| 429 | Too Many Requests | Limit exceeded |
| 500 | Internal Server Error | Server error |

---

## 💾 State Management

### Zustand Store Flow

```
┌─────────────────────────────────────────────────────┐
│                  User Actions                        │
│                                                      │
│  • Select contact                                   │
│  • Send message                                     │
│  • Switch user                                      │
└──────────────────┬──────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────┐
│              Zustand Store Actions                   │
│                                                      │
│  setCurrentUser()                                   │
│  setSelectedContact()                               │
│  addMessage()                                       │
│  triggerRefresh()                                   │
└──────────────────┬──────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────┐
│                 State Update                         │
│                                                      │
│  Store state updated → React re-renders             │
└──────────────────┬──────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────┐
│              UI Components Update                    │
│                                                      │
│  • ContactList shows new selection                  │
│  • ChatWindow displays new messages                 │
│  • Progress bars update                             │
└─────────────────────────────────────────────────────┘
```

---

## 🔐 Security

### Current Implementation

1. **Input Validation**
   - Pydantic schemas validate all inputs
   - SQL injection prevention via ORM
   - XSS prevention via React escaping

2. **CORS Configuration**
   ```python
   app.add_middleware(
       CORSMiddleware,
       allow_origins=["http://localhost:3000"],
       allow_credentials=True,
       allow_methods=["*"],
       allow_headers=["*"],
   )
   ```

3. **Data Sanitization**
   - Message content: plain text only
   - No file uploads
   - Emoji support via Unicode

### Future Enhancements

- [ ] Authentication (JWT tokens)
- [ ] Authorization (role-based)
- [ ] Rate limiting (per IP/user)
- [ ] HTTPS in production
- [ ] Session management
- [ ] CSRF protection

---

## ⚡ Performance

### Backend Optimizations

1. **Database Indexing**
   ```sql
   CREATE INDEX idx_messages_conversation 
   ON messages(sender_id, recipient_id);
   ```

2. **Query Optimization**
   - Lazy loading relationships
   - Select only needed columns
   - Limit results (pagination ready)

3. **Caching Strategy**
   - SQLAlchemy query cache
   - Future: Redis for session/limits

### Frontend Optimizations

1. **Code Splitting**
   - Vite automatically splits by route
   - Lazy loading for heavy components

2. **Memoization**
   ```typescript
   const memoizedValue = useMemo(() => 
     computeExpensiveValue(a, b), 
     [a, b]
   );
   ```

3. **Virtual Scrolling**
   - Ready for implementation
   - For message lists > 100 items

---

## 🚀 Deployment

### Docker Architecture

```
┌─────────────────────────────────────────────────────┐
│              docker-compose.yml                      │
├─────────────────────────────────────────────────────┤
│                                                      │
│  ┌──────────────────┐      ┌──────────────────┐   │
│  │   Frontend       │      │    Backend       │   │
│  │   Container      │      │    Container     │   │
│  │                  │      │                  │   │
│  │  Node 18         │      │  Python 3.11     │   │
│  │  Vite Dev Server │      │  Uvicorn         │   │
│  │  Port: 3000      │      │  Port: 8000      │   │
│  └──────────────────┘      └──────────────────┘   │
│           │                         │              │
│           └─────────┬───────────────┘              │
│                     │                              │
│              ┌──────▼──────┐                       │
│              │   Volume    │                       │
│              │  (Database) │                       │
│              └─────────────┘                       │
└─────────────────────────────────────────────────────┘
```

### Environment Variables

```bash
# Backend (.env)
DATABASE_URL=sqlite:///./messenger.db
CORS_ORIGINS=http://localhost:3000

# Frontend (.env)
VITE_API_URL=http://localhost:8000/api
```

---

## 🎨 Design Patterns

### Backend Patterns

1. **Repository Pattern**
   ```python
   # Services act as repositories
   ContactService.get_contacts_for_user(db, user_id)
   ```

2. **Dependency Injection**
   ```python
   def endpoint(db: Session = Depends(get_db)):
       # db injected automatically
   ```

3. **Factory Pattern**
   ```python
   # Model creation via Pydantic
   Message(**message_create.dict())
   ```

### Frontend Patterns

1. **Container/Presentational**
   - App.tsx (container)
   - ChatWindow.tsx (presentational)

2. **Custom Hooks**
   ```typescript
   const useMessages = (userId, contactId) => {
     const [messages, setMessages] = useState([]);
     // ... fetch logic
     return messages;
   };
   ```

---

## 📝 Decisions Log

### Why FastAPI?

✅ **Pros:**
- Modern async support
- Automatic OpenAPI docs
- Pydantic validation
- Fast performance
- Easy to learn

❌ **Alternatives considered:**
- Django: Too heavy for this use case
- Flask: Less modern, no async

### Why SQLite?

✅ **Pros:**
- Zero configuration
- Perfect for development
- File-based (easy Docker volumes)
- Good for < 100k messages

❌ **Production plan:**
- Migrate to PostgreSQL
- Keep SQLAlchemy (easy migration)

### Why Zustand?

✅ **Pros:**
- Minimal boilerplate
- TypeScript support
- Small bundle size
- No Provider needed

❌ **Alternatives considered:**
- Redux: Too much boilerplate
- Context API: Re-render issues
- Recoil: More complex

### Why Material-UI?

✅ **Pros:**
- Professional components
- Great documentation
- Accessibility built-in
- Theme system
- Large community

❌ **Alternatives considered:**
- Chakra UI: Less mature
- Ant Design: Chinese-focused
- Custom CSS: Too much work

---

## 🔄 Future Architecture

### Planned Improvements

1. **WebSocket Integration**
   ```
   Frontend ←→ WebSocket Server ←→ Backend
            (real-time updates)
   ```

2. **Microservices Split**
   ```
   ┌─────────────┐  ┌─────────────┐  ┌─────────────┐
   │   Auth      │  │  Messaging  │  │   Contacts  │
   │   Service   │  │   Service   │  │   Service   │
   └─────────────┘  └─────────────┘  └─────────────┘
   ```

3. **Event-Driven Architecture**
   ```
   Message Sent → Event Bus → [Analytics, Notifications, Logging]
   ```

---

## 📚 References

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [React Documentation](https://react.dev/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Material-UI Documentation](https://mui.com/)
- [Docker Documentation](https://docs.docker.com/)

---

**Last Updated:** December 2025  
**Version:** 1.0  
**Maintainer:** Development Team
