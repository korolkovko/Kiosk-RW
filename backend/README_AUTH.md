# README_AUTH.md
# KIOSK Authentication System Documentation

## Overview

This document describes the authentication system implemented for the KIOSK application, including user management, role-based access control, and API endpoints.

## Architecture

### Core Components

1. **SQLAlchemy Models** (`app/database/models.py`)
   - User, Role, Session, and other domain entities
   - Based on the comprehensive domain model specifications

2. **Pydantic Schemas** (`app/models/`)
   - Type-safe request/response models
   - Separate files for each entity (user.py, role.py, auth.py, session.py)

3. **Authentication Service** (`app/auth/`)
   - JWT token management
   - Password hashing with bcrypt
   - User authentication and authorization

4. **API Endpoints** (`app/api/v1/endpoints/`)
   - Authentication endpoints (login, logout, setup)
   - User management endpoints (create, read, update, delete)

## Database Schema

### Key Tables

- **roles**: User access control roles (superadmin, admin, staff)
- **users**: System users with role-based permissions
- **sessions**: Active user sessions
- **known_customers**: Customer information for kiosk users

### Default Roles

1. **SuperAdmin**: Full system access, can manage all users and settings
2. **Admin**: Limited admin access, can manage inventory and devices
3. **Staff**: Basic access for regular operations

## API Endpoints

### Authentication Endpoints

#### `GET /api/v1/auth/check-setup`
Check if system needs initial setup (no authentication required)

**Response:**
```json
{
  "setup_required": false,
  "has_superadmin": true,
  "message": "System already configured"
}
```

#### `POST /api/v1/auth/setup-superadmin`
Create first SuperAdmin user (only available when no SuperAdmin exists)

**Request:**
```json
{
  "username": "superadmin",
  "password": "SuperSecurePassword123!",
  "email": "super@admin.com",
  "phone": "+1234567890"
}
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 1800,
  "user": {
    "user_id": 1,
    "username": "superadmin",
    "email": "super@admin.com",
    "role_id": 1,
    "is_active": true
  }
}
```

#### `POST /api/v1/auth/login`
Standard login for existing users

**Request:**
```json
{
  "username": "superadmin",
  "password": "SuperSecurePassword123!"
}
```

**Response:** Same as setup-superadmin

#### `POST /api/v1/auth/logout`
Logout current user (requires authentication)

**Response:**
```json
{
  "message": "User superadmin successfully logged out"
}
```

#### `GET /api/v1/auth/me`
Get current user information (requires authentication)

**Response:**
```json
{
  "user_id": 1,
  "username": "superadmin",
  "email": "super@admin.com",
  "phone": "+1234567890",
  "role_id": 1,
  "is_active": true,
  "is_verified": true,
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": null,
  "last_login_at": "2024-01-15T12:00:00Z"
}
```

### User Management Endpoints (SuperAdmin only)

#### `POST /api/v1/users/create-admin-quick`
Quick endpoint to create Admin user

**Parameters:**
- `username`: Admin username
- `password`: Admin password  
- `email`: Optional email
- `phone`: Optional phone

**Response:**
```json
{
  "user_id": 2,
  "username": "admin_user",
  "email": "admin@kiosk.com",
  "role_id": 2,
  "is_active": true,
  "is_verified": true,
  "created_at": "2024-01-15T10:35:00Z"
}
```

#### `POST /api/v1/users/create-admin`
Full user creation with complete UserCreate schema

#### `GET /api/v1/users/`
Get list of all users (with pagination)

#### `GET /api/v1/users/{user_id}`
Get specific user by ID

#### `PUT /api/v1/users/{user_id}`
Update user information

#### `DELETE /api/v1/users/{user_id}`  
Delete user (cannot delete own account)

## Security Features

### JWT Tokens
- HS256 algorithm with configurable secret key
- Configurable expiration time (default: 30 minutes)
- Stateless authentication (no server-side token storage)

### Password Security
- bcrypt hashing with 12 rounds
- Password strength requirements in Pydantic schemas
- Secure password verification

### Role-Based Access Control
- Hierarchical role system (SuperAdmin > Admin > Staff)
- Permission-based authorization
- Route-level access control with FastAPI dependencies

### Database Security
- SQL injection prevention through SQLAlchemy ORM
- Input validation through Pydantic schemas
- Password hashes never exposed in API responses

## Configuration

### Environment Variables

Create a `.env` file based on `.env.example`:

```bash
# Application Settings
SECRET_KEY="your-super-secret-key-here"
JWT_SECRET_KEY="your-jwt-secret-key-here"
DATABASE_URL="postgresql://user:password@localhost/kiosk_db"

# Token Settings
ACCESS_TOKEN_EXPIRE_MINUTES=1800
JWT_ALGORITHM="HS256"

# Other settings...
```

### Database Setup

1. **Install PostgreSQL** and create database:
```sql
CREATE DATABASE kiosk_db;
CREATE USER kiosk_user WITH PASSWORD 'kiosk_password';
GRANT ALL PRIVILEGES ON DATABASE kiosk_db TO kiosk_user;
```

2. **Install dependencies**:
```bash
cd backend
pip install -r requirements.txt
```

3. **Run the application**:
```bash
python -m app.main
```

The application will automatically:
- Create database tables on startup
- Initialize default roles (superadmin, admin, staff)
- Be ready for first-time SuperAdmin setup

## Testing

### Manual Testing

Run the test script to validate all endpoints:

```bash
python test_auth_apis.py
```

This will test:
1. Health check endpoint
2. Setup status check  
3. SuperAdmin creation (if needed) or login
4. Current user information
5. Admin user creation
6. Admin user login
7. Logout functionality

### API Testing with curl

```bash
# Check setup status
curl -X GET http://localhost:8000/api/v1/auth/check-setup

# Create SuperAdmin (first time only)
curl -X POST http://localhost:8000/api/v1/auth/setup-superadmin \
  -H "Content-Type: application/json" \
  -d '{
    "username": "superadmin",
    "password": "SuperSecurePassword123!",
    "email": "super@admin.com"
  }'

# Login
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "superadmin", 
    "password": "SuperSecurePassword123!"
  }'

# Use token for authenticated requests
curl -X GET http://localhost:8000/api/v1/auth/me \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

## Integration with Frontend

### Authentication Flow

1. **Check Setup Status**: Call `/auth/check-setup` to determine if first-time setup is needed
2. **Initial Setup**: If needed, show SuperAdmin creation form calling `/auth/setup-superadmin`
3. **Regular Login**: Use `/auth/login` for subsequent logins
4. **Token Storage**: Store JWT token securely (localStorage, secure cookies, etc.)
5. **Authenticated Requests**: Include `Authorization: Bearer <token>` header
6. **Logout**: Call `/auth/logout` and clear stored token

### Error Handling

- **401 Unauthorized**: Token invalid/expired - redirect to login
- **403 Forbidden**: Insufficient permissions - show access denied
- **409 Conflict**: SuperAdmin already exists - use regular login
- **400 Bad Request**: Validation errors - show field-specific messages

## Next Steps

1. **Session Management**: Implement Redis-based session storage for better control
2. **Refresh Tokens**: Add refresh token mechanism for long-lived sessions  
3. **Password Reset**: Implement password reset functionality
4. **Audit Logging**: Add comprehensive audit logging for security events
5. **Rate Limiting**: Implement rate limiting for auth endpoints
6. **Multi-Factor Authentication**: Add MFA support for enhanced security

## Troubleshooting

### Common Issues

1. **Database Connection Error**: Check DATABASE_URL in .env file
2. **JWT Token Invalid**: Verify JWT_SECRET_KEY matches between requests
3. **SuperAdmin Already Exists**: Use regular login endpoint instead of setup
4. **Permission Denied**: Ensure user has correct role for endpoint access
5. **Token Expired**: Implement token refresh or re-login

### Debug Mode

Set `DEBUG=true` in .env to enable:
- Detailed error messages
- SQL query logging  
- Additional debug information

---

This authentication system provides a solid foundation for the KIOSK application with security best practices, comprehensive API coverage, and clear integration paths for frontend applications.