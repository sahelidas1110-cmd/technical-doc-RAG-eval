# Security in FastAPI

## 1. Introduction

API security is the process of protecting an API from unauthorized access, misuse, and malicious requests.

When building an API, we need to ensure that:

- Only authenticated users can access protected endpoints.
- Users can access only the resources they are authorized to use.
- Passwords are stored securely.
- Access tokens are validated before granting access.
- Sensitive information is not exposed in API responses.

FastAPI provides several security utilities that integrate with its Dependency Injection system and automatic OpenAPI documentation.

Common security concepts include:

1. Authentication
2. Authorization
3. Password hashing
4. Bearer tokens
5. OAuth2
6. JSON Web Tokens (JWT)
7. OAuth2 scopes

## 2. Authentication vs Authorization

These two concepts are related but have different purposes.

### Authentication

Authentication verifies the identity of a user.

It answers:

**Who are you?**

Example:

A user enters a username and password to log in.

The application verifies the credentials and identifies the user.

### Authorization

Authorization determines what an authenticated user is allowed to do.

It answers:

**What are you allowed to access?**

Example:

- An administrator can create, update, and delete users.
- A normal user can view only their own profile.
- A guest user can access public resources.

### Comparison

| Authentication | Authorization |
|---|---|
| Verifies user identity | Checks user permissions |
| Happens before access is granted | Determines which actions are allowed |
| Uses credentials, tokens, or identity providers | Uses roles, permissions, and scopes |
| Example: Login | Example: Admin-only endpoint |

## 3. Security Utilities in FastAPI

FastAPI provides security utilities through `fastapi.security`.

Some commonly used classes include:

| Utility | Purpose |
|---|---|
| `OAuth2PasswordBearer` | Extracts a bearer token from the Authorization header |
| `OAuth2PasswordRequestForm` | Reads username and password from form data |
| `HTTPBasic` | Supports HTTP Basic authentication |
| `HTTPBearer` | Extracts HTTP bearer credentials |
| `APIKeyHeader` | Reads an API key from a request header |
| `APIKeyQuery` | Reads an API key from a query parameter |
| `APIKeyCookie` | Reads an API key from a cookie |
| `SecurityScopes` | Provides OAuth2 scope information |

These utilities help define security requirements and integrate them with FastAPI's OpenAPI documentation.

## 4. Understanding Bearer Tokens

A bearer token is a credential that allows whoever possesses it to access protected resources, subject to the token's validity and permissions.

After successful authentication, the server can issue an access token.

The client sends that token in the HTTP Authorization header when accessing protected endpoints.

Example:

```text
Authorization: Bearer your_access_token
```

The word `Bearer` identifies the authentication scheme.

A typical authentication flow:

```text
Client
  |
  | 1. Send login credentials
  v
FastAPI Login Endpoint
  |
  | 2. Verify credentials
  v
Authentication System
  |
  | 3. Generate access token
  v
Client receives token
  |
  | 4. Send token in Authorization header
  v
Protected API Endpoint
  |
  | 5. Validate token
  v
Return protected resource
```

A bearer token must be protected carefully because anyone who obtains it may be able to use it until it expires or is revoked.

## 5. OAuth2

OAuth2 is an authorization framework that allows applications to obtain limited access to protected resources.

It is commonly used when applications need to access APIs on behalf of users.

For example:

- A third-party application accesses a user's resources through Google.
- An application accesses GitHub repositories with granted permissions.
- A frontend application obtains an access token to communicate with a backend API.

FastAPI provides utilities that help implement OAuth2-based security flows.

### Common OAuth2 Concepts

| Concept | Meaning |
|---|---|
| Resource Owner | The user who owns the protected resources |
| Client | Application requesting access |
| Authorization Server | Server responsible for issuing tokens |
| Resource Server | API that accepts and validates access tokens |
| Access Token | Credential used to access protected resources |
| Scope | Permission or level of access requested |

### Important OAuth2 Flows

Common OAuth2 authorization flows include:

- Authorization Code
- Authorization Code with PKCE
- Client Credentials
- Device Authorization

The appropriate flow depends on the application architecture.

For modern user-facing applications, Authorization Code with PKCE is commonly recommended.

The password flow taught in many FastAPI examples is useful for understanding the mechanics of authentication, but it is not the preferred choice for new third-party user authentication systems. For production applications, consider an established OpenID Connect identity provider and an appropriate modern authorization flow.

## 6. OAuth2PasswordBearer

FastAPI provides `OAuth2PasswordBearer` to extract bearer tokens from incoming requests.

Example:

```python
from typing import Annotated
from fastapi import Depends, FastAPI
from fastapi.security import OAuth2PasswordBearer

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="token"
)

@app.get("/users/me/")
async def read_users_me(
    token: Annotated[str, Depends(oauth2_scheme)]
):
    return {"token": token}
```

Explanation:

- `OAuth2PasswordBearer` defines an OAuth2 bearer-token security scheme.
- `tokenUrl="token"` identifies the relative URL where the client obtains a token.
- `Depends(oauth2_scheme)` extracts the token from the Authorization header.
- The endpoint receives the token as a string.

Example request:

```text
GET /users/me/
Authorization: Bearer abc123
```

At this stage, the example only extracts the token. It does not verify whether the token is valid.

If the Authorization header is missing or does not contain a bearer token, FastAPI returns an authentication error.

## 7. Password Hashing

Passwords should never be stored as plain text in a database.

Instead, applications should store password hashes.

Password hashing transforms a password into a value that can be stored and verified later.

A secure password-hashing algorithm is designed to make recovering the original password computationally difficult.

### Hashing vs Encryption

| Hashing | Encryption |
|---|---|
| One-way transformation | Reversible using the appropriate key |
| Used for password storage | Used to protect data that must be recovered |
| No decryption operation | Decryption is possible with the key |
| Example: Argon2id | Example: AES |

For password storage, use a dedicated password-hashing algorithm such as Argon2id rather than ordinary general-purpose hashing functions such as SHA-256.

### Installing Password Hashing Dependencies

For the examples in this document, use:

```powershell
uv add "pwdlib[argon2]"
```

### Hashing a Password

```python
from pwdlib import PasswordHash

password_hash = PasswordHash.recommended()

def get_password_hash(password: str) -> str:
    return password_hash.hash(password)

hashed_password = get_password_hash("my_secure_password")

print(hashed_password)
```

The stored value is a password hash, not the original password.

### Verifying a Password

```python
def verify_password(
    plain_password: str,
    hashed_password: str
) -> bool:

    return password_hash.verify(
        plain_password,
        hashed_password
    )
```

Example:

```python
hashed = get_password_hash("my_secure_password")

print(verify_password("my_secure_password", hashed))
print(verify_password("wrong_password", hashed))
```

The first verification returns `True`; the second returns `False`.

Password hashing libraries manage salts and algorithm parameters as part of their hashing process.

## 8. JSON Web Tokens (JWT)

JWT stands for JSON Web Token.

It is a compact format for representing claims that can be transmitted between parties.

A JWT commonly consists of three parts separated by dots:

```text
header.payload.signature
```

### JWT Structure

**1. Header**

Contains metadata such as the token type and signing algorithm.

Example:

```json
{
    "alg": "HS256",
    "typ": "JWT"
}
```

**2. Payload**

Contains claims or information associated with the token.

Example:

```json
{
    "sub": "john",
    "role": "user",
    "exp": 1900000000
}
```

**3. Signature**

The signature is used to verify that the token has not been modified and was signed using the expected signing key.

### Important JWT Claims

| Claim | Meaning |
|---|---|
| `sub` | Subject of the token, often a user identifier |
| `exp` | Expiration time |
| `iat` | Issued-at time |
| `iss` | Issuer |
| `aud` | Intended audience |
| `nbf` | Not valid before |

### Important: JWT Is Not Encrypted by Default

A signed JWT is generally readable by anyone who possesses it.

The signature protects integrity and verifies authenticity. It does not hide the payload.

Therefore:

- Do not place passwords in JWT payloads.
- Do not include API keys or confidential information.
- Use HTTPS to protect tokens in transit.
- Validate the token's signature, expiration, issuer, and audience as appropriate.

If confidentiality is required, use an appropriate encryption mechanism rather than assuming a signed JWT hides its contents.

## 9. Installing JWT Dependencies

FastAPI's current JWT tutorial uses PyJWT and pwdlib.

Install them:

```powershell
uv add pyjwt
uv add "pwdlib[argon2]"
```

For the OAuth2 password-form example later in this document, also install:

```powershell
uv add python-multipart
```

`python-multipart` is required to parse form data used by `OAuth2PasswordRequestForm`.

## 10. Creating a JWT Access Token

PyJWT provides functions to encode and decode JWT tokens.

Example:

```python
import jwt
from datetime import datetime, timedelta, timezone

SECRET_KEY = "replace_with_a_secure_secret"
ALGORITHM = "HS256"

def create_access_token(data: dict):

    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(minutes=30)

    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return encoded_jwt
```

Explanation:

- `data` contains the claims to include in the token.
- `exp` defines when the token expires.
- `jwt.encode()` creates the signed token.
- `SECRET_KEY` is used to sign the token.
- `HS256` is the signing algorithm in this example.

**Never use a hardcoded demonstration secret in production.**

Generate a strong random secret and store it in an environment variable or secret manager.

For example, OpenSSL can generate a random secret:

```powershell
openssl rand -hex 32
```

Do not commit the resulting secret to GitHub.

## 11. Decoding and Validating a JWT

A server must validate an incoming JWT before trusting its claims.

Example:

```python
import jwt
from jwt.exceptions import InvalidTokenError

def verify_access_token(token: str):

    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        return payload

    except InvalidTokenError:
        return None
```

The decoding process verifies the signature and checks registered claims such as expiration when present.

For production use, validation should also enforce the expected issuer and audience when those claims are part of the application's token contract.

The server should never trust a token merely because it can decode its payload.

## 12. Protecting Endpoints Using JWT and Depends()

We can combine:

- `OAuth2PasswordBearer`
- JWT validation
- FastAPI Dependency Injection

This allows us to protect endpoints with reusable authentication logic.

Example:

```python
from typing import Annotated
import jwt

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError

app = FastAPI()

SECRET_KEY = "replace_with_a_secure_secret"
ALGORITHM = "HS256"

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="token"
)

def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)]
):

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )

    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        username = payload.get("sub")

        if username is None:
            raise credentials_exception

    except InvalidTokenError:
        raise credentials_exception

    return {"username": username}

@app.get("/users/me/")
async def read_current_user(
    current_user: Annotated[dict, Depends(get_current_user)]
):
    return current_user
```

Explanation:

1. `OAuth2PasswordBearer` extracts the bearer token.
2. `get_current_user()` receives the token.
3. `jwt.decode()` verifies the token.
4. The `sub` claim identifies the user.
5. Invalid tokens result in HTTP 401.
6. The endpoint receives the authenticated user information.

This is a simplified example. A production application must also look up the user in its database and verify that the account is active and authorized.

## 13. OAuth2 Password Request Form

FastAPI provides `OAuth2PasswordRequestForm` to receive username and password values as form data.

Example:

```python
from typing import Annotated
from fastapi import Depends, FastAPI
from fastapi.security import OAuth2PasswordRequestForm

app = FastAPI()

@app.post("/token")
async def login(
    form_data: Annotated[
        OAuth2PasswordRequestForm,
        Depends()
    ]
):
    return {
        "username": form_data.username,
        "password_received": bool(form_data.password)
    }
```

The client submits form data rather than a JSON request body.

The OAuth2 password form uses the field names:

- `username`
- `password`

This example only demonstrates receiving credentials. A real login endpoint must verify the password against the stored password hash and issue a valid access token.

## 14. Complete Authentication Flow

A simplified authentication flow using OAuth2 password form and JWT works as follows:

**Step 1: User submits credentials**

The client sends a username and password to the login endpoint.

**Step 2: Server verifies credentials**

The application retrieves the user record and verifies the supplied password against the stored password hash.

**Step 3: Server creates an access token**

After successful authentication, the application creates a signed JWT with an expiration time.

**Step 4: Client receives the token**

The server returns the access token.

Example:

```json
{
    "access_token": "generated_jwt_token",
    "token_type": "bearer"
}
```

**Step 5: Client calls a protected endpoint**

The client sends the token:

```text
Authorization: Bearer generated_jwt_token
```

**Step 6: Server validates the token**

The application verifies the signature, expiration, and relevant claims.

**Step 7: Access is granted or rejected**

If the token is valid and the user has the required permissions, the API returns the requested resource.

## 15. Authorization Using OAuth2 Scopes

Authentication establishes the identity of a user.

However, an application may need more granular permission control.

OAuth2 scopes provide a way to define specific permissions associated with an access token.

Example scopes:

- `read:users`
- `write:users`
- `read:documents`
- `write:documents`

FastAPI provides `SecurityScopes` and `Security()` for integrating scope-based security.

Example:

```python
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, Security, status
from fastapi.security import (
    OAuth2PasswordBearer,
    SecurityScopes
)

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="token",
    scopes={
        "read:documents": "Read documents",
        "write:documents": "Create or update documents"
    }
)

def get_current_user(
    security_scopes: SecurityScopes,
    token: Annotated[str, Depends(oauth2_scheme)]
):
    # In a real application:
    # 1. Validate the token.
    # 2. Retrieve the user.
    # 3. Obtain the user's granted permissions.

    user_scopes = {"read:documents"}

    for scope in security_scopes.scopes:
        if scope not in user_scopes:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions"
            )

    return {"username": "john", "scopes": list(user_scopes)}

@app.get("/documents/")
async def read_documents(
    user: Annotated[
        dict,
        Security(get_current_user, scopes=["read:documents"])
    ]
):
    return {
        "message": "Documents retrieved",
        "user": user
    }
```

This example illustrates the scope-checking mechanism. The token validation and permission lookup must be implemented using the application's real authentication system.

### Authentication vs Scope-Based Authorization

| Authentication | Scope-Based Authorization |
|---|---|
| Verifies user identity | Checks granted permissions |
| Determines who is making the request | Determines what the user can do |
| Example: Valid JWT | Example: `read:documents` permission |

## 16. HTTP Status Codes Used in Security

| Status Code | Meaning | Typical Use |
|---|---|---|
| 200 | OK | Successful request |
| 401 | Unauthorized | Missing or invalid authentication credentials |
| 403 | Forbidden | Authenticated user lacks permission |
| 404 | Not Found | Requested resource does not exist |
| 429 | Too Many Requests | Rate limit exceeded |

A useful distinction:

- **401:** The request lacks valid authentication credentials.
- **403:** The user is authenticated but does not have sufficient permission.

## 17. API Key Authentication

Some APIs use API keys instead of user login credentials.

An API key is a secret value supplied by a client to identify or authorize access to an API.

FastAPI provides `APIKeyHeader` for reading an API key from a request header.

Example:

```python
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import APIKeyHeader

app = FastAPI()

api_key_header = APIKeyHeader(
    name="X-API-Key"
)

EXPECTED_API_KEY = "replace_with_secure_key"

def verify_api_key(
    api_key: Annotated[str, Depends(api_key_header)]
):

    if api_key != EXPECTED_API_KEY:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid API key"
        )

    return api_key

@app.get("/protected/")
async def protected_endpoint(
    api_key: Annotated[str, Depends(verify_api_key)]
):
    return {"message": "Access granted"}
```

Example request header:

```text
X-API-Key: your_api_key
```

This is a simplified demonstration. In production, API keys should be securely generated, stored as hashes where appropriate, rotated, revocable, and associated with usage limits and permissions.

Never expose an API key in frontend source code or public repositories.

## 18. Security Best Practices

1. Never store passwords in plain text.
2. Use secure password hashing algorithms such as Argon2id.
3. Store secret keys in environment variables or a secret manager.
4. Never commit secrets or access tokens to GitHub.
5. Use HTTPS to protect credentials and tokens during transmission.
6. Set appropriate access-token expiration times.
7. Validate JWT signatures and relevant claims.
8. Avoid storing sensitive information inside JWT payloads.
9. Implement authorization separately from authentication.
10. Use scopes or roles for fine-grained permissions.
11. Return appropriate HTTP status codes for authentication and authorization failures.
12. Validate user permissions on the server for every protected operation.
13. Consider refresh-token rotation, revocation, and secure client-side token storage where appropriate.
14. Use an established identity provider for complex production authentication requirements.
15. Apply rate limiting to sensitive endpoints such as login and token issuance.

## 19. Relevance to AI and RAG Applications

Security is important when deploying AI and RAG applications because users may access private documents, internal knowledge bases, and sensitive information.

Consider an enterprise RAG application where different users have access to different document collections.

Example:

- HR users can access HR policy documents.
- Finance users can access financial documents.
- Administrators can manage document collections.
- Regular employees can ask questions only about documents they are authorized to access.

A RAG API might use authentication and authorization before retrieving documents.

Conceptual architecture:

```text
Client
  |
  v
FastAPI Authentication
  |
  v
JWT Validation
  |
  v
Authorization / User Permissions
  |
  v
RAG Retrieval Pipeline
  |
  v
Permission-Aware Document Retrieval
  |
  v
LLM Generation
  |
  v
Response
```

A critical design principle is that access permissions must be enforced during retrieval, not only when returning the final answer.

Otherwise, the language model might receive information from documents the user is not authorized to access.

In a production RAG system, document-level access control should be enforced through metadata filters or another trusted authorization mechanism before retrieved content is passed to the LLM.

## 20. Official References

- FastAPI — Security First Steps: https://fastapi.tiangolo.com/tutorial/security/first-steps/
- FastAPI — Get Current User: https://fastapi.tiangolo.com/tutorial/security/get-current-user/
- FastAPI — Simple OAuth2 with Password and Bearer: https://fastapi.tiangolo.com/tutorial/security/simple-oauth2/
- FastAPI — OAuth2 with JWT: https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/
- FastAPI — OAuth2 Scopes: https://fastapi.tiangolo.com/advanced/security/oauth2-scopes/
- FastAPI — Security Utilities: https://fastapi.tiangolo.com/reference/security/
- PyJWT Documentation: https://pyjwt.readthedocs.io/
- Pydantic Password Hashing / pwdlib: https://frankie567.github.io/pwdlib/