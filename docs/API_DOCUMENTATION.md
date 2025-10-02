### KIOSK API Documentation System

This document explains how KIOSK's **executable documentation** works and how to maintain consistency between code and documentation during development.

Where Swagger Documentation is Generated

  1. Main FastAPI App Configuration

  File: /backend/app/main.py
  app = FastAPI(
      title=settings.PROJECT_NAME,           # → Page title in Swagger
      version="0.1.0",                      # → Version shown
      description="KIOSK Application Backend API",  # → Main description
      openapi_url=f"{settings.API_V1_STR}/openapi.json",  # → OpenAPI spec URL
  )

  2. Route Definitions Generate Endpoints

  Files: /backend/app/api/*.py (users.py, auth.py, etc.)
  @router.post("/create-admin", response_model=UserResponse)  # ← Creates endpoint
  async def create_admin_user(
      user_data: AdminCreate,  # ← Request schema in Swagger
      # ...
  ):
      """
      Create a new Admin user...  # ← Description in Swagger
      """

  3. Pydantic Models Generate Schemas

  Files: /backend/app/models/*.py (user.py, auth.py, etc.)
  class AdminCreate(BaseModel):
      username: str = Field(..., description="Unique username")  # ← Field docs
      # ...
      model_config = ConfigDict(
          json_schema_extra={
              "example": {  # ← Example JSON in Swagger
                  "username": "admin_user",
                  "password": "AdminPass123"
              }
          }
      )

  📍 Key Locations for Swagger Content

  | What You See in Swagger  | Generated From        | File Location              |
  |--------------------------|-----------------------|----------------------------|
  | Page Title & Info        | FastAPI() constructor | /backend/app/main.py:19-24 |
  | Endpoints List           | @router decorators    | /backend/app/api/*.py      |
  | Request/Response Schemas | Pydantic models       | /backend/app/models/*.py   |
  | Endpoint Descriptions    | Function docstrings   | /backend/app/api/*.py      |
  | Examples                 | model_config examples | /backend/app/models/*.py   |
  | Authentication           | Depends() decorators  | /backend/app/api/*.py      |

  🎯 Built-in Swagger URLs

  FastAPI automatically provides these:
  - http://localhost:8000/docs - Swagger UI (interactive)
  - http://localhost:8000/redoc - ReDoc (clean docs)
  - http://localhost:8000/openapi.json - Raw OpenAPI specification

  🔧 No Separate Swagger Files Needed

  Unlike traditional APIs, you don't need:
  - ❌ swagger.yaml files
  - ❌ swagger.json files
  - ❌ Manual documentation writing
  - ❌ Separate documentation maintenance

  Everything is generated automatically from your Python code! This is why it's called "executable documentation" - it's always in sync with
   your actual API.


## 📋 Available Documentation URLs

### Interactive Documentation Interfaces

| Tool | URL | Purpose | Best For |
|------|-----|---------|----------|
| **Swagger UI** | http://localhost:8000/docs | Interactive API testing and exploration | Development, testing, client integration |
| **ReDoc** | http://localhost:8000/redoc | Clean, readable API documentation | Documentation review, client reference |
| **OpenAPI Spec** | http://localhost:8000/openapi.json | Raw JSON specification | API tooling, code generation, validation |

### Additional Endpoints
| Endpoint | URL | Purpose |
|----------|-----|---------|
| Root | http://localhost:8000/ | Basic server info |
| Health Check | http://localhost:8000/health | Service status monitoring |
| Replenish or remove stock | http://localhost:8000/api/v1/replenish-or-remove | Adjust stock quantity by positive or negative amount; Admin only |
| Update LiveItem stop list status     | http://localhost:8000/api/v1/stop-list         | Update stop list status of a LiveItem; Admin only |
| Update LiveItem properties           | http://localhost:8000/api/v1/update-item-properties | Update properties of a LiveItem; Admin only |
| Get all LiveItems                    | http://localhost:8000/api/v1/getallitemlive       | Retrieve list of all LiveItems; any authenticated user |
## 📘 Endpoint: Replenish or Remove Stock

**Path:** POST /api/v1/replenish-or-remove  
**Description:** Adjust stock for a LiveItem by positive or negative quantity; stock never goes below zero. Only accessible by Admin or SuperAdmin.

**Request Schema:** ItemLiveStockReplenishmentRequest  
- item_id (int): ID of the LiveItem  
- quantity (int): Positive (to add) or negative (to remove) quantity  

**Response Schema:** ItemLiveStockReplenishmentResponse  
- item_id (int)  
- unit_name_ru (string)  
- unit_name_eng (string)  
- stock_quantity (int)  
- reserved_quantity (int)  
- operation_id (int)  
- changed_at (datetime string)  

**Authorization:** Bearer token with Admin or SuperAdmin role

## 📘 Endpoint: Update LiveItem Stop List Status

**Path:** PUT /api/v1/stop-list/
**Description:** Update the stop list status of a LiveItem. Only accessible by Admin or SuperAdmin.

**Request Schema:** ItemStopListRequest
- item_id (int): ID of the LiveItem
- is_active (bool): Desired active status

**Response Schema:** ItemStopListResponse
- item_id (int)
- is_active (bool)

**Authorization:** Bearer token with Admin or SuperAdmin role

## 📘 Endpoint: Update LiveItem Properties

**Path:** PUT /api/v1/update-item-properties/
**Description:** Update properties of an existing LiveItem (description, price, VAT, categories, etc.). Only accessible by Admin or SuperAdmin.

**Request Schema:** ItemUpdatePropertiesRequest
- item_id (int): ID of the LiveItem to update
- name_ru (string): New Russian name (optional)
- name_eng (string): New English name (optional)
- description_ru (string): New Russian description (optional)
- description_eng (string): New English description (optional)
- unit_measure_name_eng (string): Unit of measure name (English) (optional)
- food_category_name (string): Food category name (optional)
- day_category_name (string): Day category name (optional)
- price_net (string): New net price (optional)
- vat_rate (string): New VAT rate % (optional)
- vat_amount (string): New VAT amount (optional)
- price_gross (string): New gross price (optional)

**Response Schema:** ItemUpdatePropertiesResponse
- item_id (int)
- name_ru (string)
- name_eng (string)
- description_ru (string)
- description_eng (string)
- unit_measure_name_eng (string)
- food_category_name (string)
- day_category_name (string)
- price_net (string)
- vat_rate (string)
- vat_amount (string)
- price_gross (string)
- is_active (bool)
- created_at (datetime string)
- created_by (int)

**Authorization:** Bearer token with Admin or SuperAdmin role

## 📘 Endpoint: Get All LiveItems

**Path:** GET /api/v1/getallitemlive

**Description:** Retrieve list of all LiveItems. Accessible by any authenticated user.

**Response Schema:** List[ItemLiveResponse]

**Authorization:** Bearer token for any authenticated user

## 🔧 How the Documentation System Works

### 1. **Automatic Generation Process**

```mermaid
graph LR
    A[Python Code] --> B[FastAPI Introspection]
    B --> C[OpenAPI Specification]
    C --> D[Swagger UI]
    C --> E[ReDoc]
    
    F[Pydantic Models] --> B
    G[Type Hints] --> B
    H[Docstrings] --> B
    I[Route Decorators] --> B
```

**FastAPI automatically scans your code and generates documentation by:**
- **Introspecting route decorators** (`@router.post("/create-admin")`)
- **Analyzing Pydantic models** for request/response schemas
- **Reading Python type hints** for parameter types
- **Extracting docstrings** for endpoint descriptions
- **Processing Field descriptions** for parameter documentation

### 2. **Key Components That Generate Documentation**

#### **A. FastAPI App Configuration** (`main.py`)
```python
app = FastAPI(
    title="KIOSK Application Backend API",    # → Page title
    version="0.1.0",                         # → Version display
    description="KIOSK Application Backend API", # → Main description
    openapi_url="/api/v1/openapi.json",     # → OpenAPI spec location
)
```

#### **B. Route Decorators** (`users.py`)
```python
@router.post("/create-admin", response_model=UserResponse)  # ← Endpoint definition
async def create_admin_user(
    user_data: AdminCreate,  # ← Request schema
    current_user: User = Depends(get_current_superadmin),  # ← Auth requirement
    db: Session = Depends(get_db)  # ← Database dependency
):
    """
    Create a new Admin user. Only accessible by SuperAdmin.  # ← Description
    
    Logic:
    1. Verify requester is SuperAdmin (handled by dependency)  # ← Detailed docs
    2. Check if 'admin' role exists in roles table
    3. Assign admin role_id from roles table to new user
    4. Return success/failure message
    """
```

#### **C. Pydantic Models** (`models/user.py`)
```python
class AdminCreate(BaseModel):
    """Schema for creating admin user (role_id automatically assigned from roles table)"""
    username: str = Field(..., min_length=3, max_length=100, description="Unique username")
    password: str = Field(..., min_length=8, max_length=100, description="User password")
    email: Optional[EmailStr] = Field(None, description="User email address")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {  # ← Example in Swagger UI
                "username": "admin_user",
                "password": "AdminPass123",
                "email": "admin@test.com"
            }
        }
    )
```

### 3. **Documentation Generation Flow**

1. **Server Startup**: FastAPI scans all registered routes and models
2. **Schema Generation**: Creates OpenAPI 3.0 specification from code analysis
3. **UI Rendering**: Swagger UI and ReDoc consume the OpenAPI spec
4. **Live Updates**: Documentation updates automatically when code changes (on server restart)

## 🎯 Understanding Each Documentation Tool

### **Swagger UI** (http://localhost:8000/docs)
**Purpose**: Interactive API testing and exploration

**Features**:
- ✅ **Try It Out** buttons for live API testing
- ✅ **Request/Response examples** with actual data
- ✅ **Authentication testing** (Bearer token input)
- ✅ **Real-time validation** of request data
- ✅ **Response inspection** with status codes and headers
- ✅ **Schema exploration** with collapsible sections

**Best for**:
- Development and debugging
- Manual API testing
- Client integration testing
- Understanding request/response formats

**Example Usage**:
1. Navigate to `/docs`
2. Find `POST /api/v1/users/create-admin`
3. Click "Try it out"
4. Fill in authentication token
5. Modify request body
6. Execute and see real response

### **ReDoc** (http://localhost:8000/redoc)
**Purpose**: Clean, professional API documentation

**Features**:
- ✅ **Clean, organized layout** with navigation sidebar
- ✅ **Comprehensive schema documentation** with nested models
- ✅ **Code examples** in multiple languages
- ✅ **Downloadable specification** 
- ✅ **Search functionality** across all endpoints
- ✅ **Mobile-responsive design**

**Best for**:
- Client developer reference
- API documentation review
- Sharing with external teams
- Professional presentation

### **OpenAPI Specification** (http://localhost:8000/openapi.json)
**Purpose**: Machine-readable API specification

**Features**:
- ✅ **JSON format** following OpenAPI 3.0 standard
- ✅ **Complete API definition** with all endpoints, schemas, and examples
- ✅ **Tool integration** for code generation and validation
- ✅ **Version control friendly** for tracking API changes

**Best for**:
- API client code generation
- Integration with API management tools
- Automated testing setup
- API versioning and change tracking

## ⚡ Development Best Practices for Executable Documentation

### 1. **Keep Code and Documentation in Sync**

#### **✅ DO: Use Type Hints Everywhere**
```python
async def create_admin_user(
    user_data: AdminCreate,  # ← Type hint generates schema
    current_user: User = Depends(get_current_superadmin),  # ← Dependency docs
    db: Session = Depends(get_db)
) -> UserResponse:  # ← Return type hint
```

#### **✅ DO: Write Comprehensive Docstrings**
```python
"""
Create a new Admin user. Only accessible by SuperAdmin.

Logic:
1. Verify requester is SuperAdmin (handled by dependency)
2. Check if 'admin' role exists in roles table  
3. Assign admin role_id from roles table to new user
4. Return success/failure message

Args:
    user_data: User creation data (role_id field is ignored - admin role assigned automatically)
    current_user: Current SuperAdmin user (verified)
    db: Database session
    
Returns:
    Created admin user information
    
Raises:
    HTTPException: If admin role not found or user creation fails
"""
```

#### **✅ DO: Use Descriptive Field Documentation**
```python
class AdminCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=100, description="Unique username")
    password: str = Field(..., min_length=8, max_length=100, description="User password")
    email: Optional[EmailStr] = Field(None, description="User email address")
```

### 2. **Provide Realistic Examples**

#### **✅ DO: Include Practical Examples**
```python
model_config = ConfigDict(
    json_schema_extra={
        "example": {
            "username": "admin_user",           # ← Real username format
            "password": "AdminPass123",         # ← Meets validation rules
            "email": "admin@test.com",         # ← Valid email
            "phone": "+1234567890"             # ← Valid phone format
        }
    }
)
```

#### **❌ DON'T: Use Generic Examples**
```python
# Bad - unhelpful examples
"example": {
    "username": "string",
    "password": "string",
    "email": "user@example.com"
}
```

### 3. **Design API-First with Documentation in Mind**

#### **✅ DO: Plan Endpoints for Clarity**
```python
# Clear, RESTful endpoints
POST /api/v1/users/create-admin     # ← Specific purpose
GET  /api/v1/users/                 # ← List users
GET  /api/v1/users/{user_id}        # ← Get specific user
PUT  /api/v1/users/{user_id}        # ← Update user
DELETE /api/v1/users/{user_id}      # ← Delete user
```

#### **✅ DO: Use Consistent Response Models**
```python
# All endpoints return consistent structure
response_model=UserResponse         # ← Same response model
# vs mixing different response formats
```

### 4. **Validate Documentation Regularly**

#### **Testing Workflow**:
1. **After code changes** → Restart server
2. **Check Swagger UI** → Verify examples work
3. **Test with curl** → Ensure docs match reality
4. **Review ReDoc** → Check professional presentation
5. **Validate OpenAPI spec** → Ensure specification correctness

#### **Documentation Checklist**:
- [ ] All endpoints have clear descriptions
- [ ] Request/response examples are realistic
- [ ] Authentication requirements are documented
- [ ] Error responses are documented
- [ ] Field validation rules are clear
- [ ] Examples can be copy-pasted and work

### 5. **Handle Authentication in Documentation**

#### **✅ DO: Document Auth Requirements Clearly**
```python
# FastAPI automatically documents dependencies
current_user: User = Depends(get_current_superadmin)  # ← Shows auth requirement
```

#### **✅ DO: Include Auth Examples in SETUP_GUIDE.md**
```bash
# Always provide working examples with real tokens
curl -X POST http://localhost:8000/api/v1/users/create-admin \
  -H "Authorization: Bearer YOUR_SUPERADMIN_TOKEN_HERE" \
  -d '{"username": "admin_user", "password": "AdminPass123"}'
```

## 🚀 Development Workflow for Consistent Documentation

### **Daily Development Process**:

1. **Code First**: Write endpoint with proper type hints
2. **Document**: Add comprehensive docstring
3. **Model**: Create/update Pydantic models with examples
4. **Test**: Restart server and test in Swagger UI
5. **Validate**: Ensure curl examples work
6. **Update Guides**: Update SETUP_GUIDE.md if needed

### **Before Committing Code**:

1. **Swagger UI Check**: All endpoints show correct examples
2. **ReDoc Review**: Documentation reads professionally
3. **Manual Testing**: curl commands from docs work
4. **Example Validation**: All examples are realistic and functional

### **API Evolution Strategy**:

1. **Version Control**: Track OpenAPI spec changes
2. **Backward Compatibility**: Ensure changes don't break clients
3. **Documentation Updates**: Update guides when APIs change
4. **Client Communication**: Share updated documentation links

## 🎨 Why This is "Executable Documentation"

**Traditional Documentation Problems**:
- ❌ Gets outdated quickly
- ❌ Separate from code
- ❌ Can't test examples
- ❌ Manual maintenance burden

**FastAPI's Executable Documentation Benefits**:
- ✅ **Always Current**: Generated from actual code
- ✅ **Interactive**: Can test immediately
- ✅ **Self-Validating**: Examples must work or code breaks
- ✅ **Zero Maintenance**: Updates automatically with code
- ✅ **Multiple Formats**: Swagger UI, ReDoc, OpenAPI spec
- ✅ **Development Friendly**: Integrated into workflow

**The term "executable documentation" fits because**:
- Documentation **executes** real API calls
- Examples are **executable** and testable
- Documentation **drives** development workflow
- Code changes **automatically execute** documentation updates

This creates a **living, breathing documentation system** that stays synchronized with your codebase and provides immediate feedback during development.

## 🔗 Integration with Development Tools

### **IDE Integration**:
- Use FastAPI plugin for VS Code
- Enable OpenAPI schema validation
- Set up auto-completion from schema

### **Testing Integration**:
- Generate test cases from OpenAPI spec
- Use documentation examples in automated tests
- Validate API responses against documented schemas

### **CI/CD Integration**:
- Include OpenAPI spec validation in pipeline
- Generate client SDKs from specification
- Document API changes in release notes

This system ensures your API documentation is always accurate, testable, and useful for both development and client integration.