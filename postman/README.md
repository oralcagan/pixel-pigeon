# Postman Collection for Email Forwarding Service

This directory contains comprehensive Postman collections and environments for testing the Email Forwarding Service API.

## 📁 Files

- `Email-Forwarding-Service.postman_collection.json` - Main API collection
- `Email-Forwarding-Service-Local.postman_environment.json` - Local development environment
- `Email-Forwarding-Service-Production.postman_environment.json` - Production environment

## 🚀 Quick Setup

### 1. Import Collection
1. Open Postman
2. Click **Import** 
3. Select `Email-Forwarding-Service.postman_collection.json`
4. Click **Import**

### 2. Import Environment
1. Click **Import** again
2. Select the environment file for your setup:
   - `Email-Forwarding-Service-Local.postman_environment.json` for local testing
   - `Email-Forwarding-Service-Production.postman_environment.json` for production
3. Click **Import**

### 3. Select Environment
1. In the top-right corner of Postman, select the environment you imported
2. Click the eye icon (👁️) to view/edit environment variables

### 4. Update Token
1. In the environment, update the `auth_token` variable with your actual token
2. Save the environment

## 📋 Collection Overview

### Folders:

#### 🔍 Health & Monitoring
- **Health Check** - Check service status and configuration
- **Service Info** - Get basic service information

#### 📧 Email Operations  
- **Send Basic Email** - Simple email with title and message
- **Send Alert Email** - System alert with rich formatting
- **Send Welcome Email** - Friendly welcome message with emojis

#### ❌ Error Testing
- **Invalid Token** - Test 403 Forbidden response
- **Missing Authorization** - Test 401 Unauthorized response  
- **Missing Required Fields** - Test 400 Bad Request response
- **Empty Fields** - Test validation with empty values

#### 📚 Documentation
- **OpenAPI Schema** - Access Swagger UI documentation
- **ReDoc Documentation** - Access ReDoc documentation

## 🔧 Environment Variables

### Local Environment:
```json
{
  "base_url": "http://localhost:8080",
  "auth_token": "demo_token_abc123"
}
```

### Production Environment:
```json
{
  "base_url": "https://your-production-domain.com",
  "auth_token": "your-production-token-here"
}
```

## 🧪 Running Tests

Each request includes automated tests that verify:
- ✅ Correct HTTP status codes
- ✅ Response structure and required fields
- ✅ Response times
- ✅ Authentication behavior
- ✅ Error handling

### Run All Tests:
1. Select the collection in Postman
2. Click **Run Collection**
3. Choose environment and settings
4. Click **Run Email Forwarding Service**

### View Test Results:
- ✅ Green checkmarks indicate passing tests
- ❌ Red X marks indicate failing tests
- Detailed results show response times and assertions

## 📝 Example Usage

### 1. Health Check
```http
GET http://localhost:8080/health
```

### 2. Send Email
```http
POST http://localhost:8080/send
Authorization: Bearer demo_token_abc123
Content-Type: application/json

{
  "title": "Test Alert",
  "message": "This is a test message.\nMultiple lines supported."
}
```

### 3. Expected Response
```json
{
  "status": "sent",
  "recipients": ["support@example.com"]
}
```

## 🔐 Security Notes

- **Never commit production tokens** to version control
- **Use separate tokens** for different environments
- **Rotate tokens regularly** for security
- **Limit token scope** to necessary recipients only

## 🚨 Common Issues

### "Unauthorized" Error (401/403)
- Check that `auth_token` is set correctly in environment
- Verify token exists in `config.json` on server
- Ensure `Authorization: Bearer <token>` header is included

### "Bad Request" Error (400)
- Verify `title` and `message` fields are included
- Check that fields are not empty strings
- Ensure `Content-Type: application/json` header is set

### Connection Refused
- Verify service is running (`docker-compose up`)
- Check `base_url` in environment matches your setup
- Ensure port 8080 is accessible

## 🔄 CI/CD Integration

You can run these tests in CI/CD pipelines using Newman:

```bash
# Install Newman
npm install -g newman

# Run collection with environment
newman run Email-Forwarding-Service.postman_collection.json \
  -e Email-Forwarding-Service-Local.postman_environment.json \
  --reporters cli,json \
  --reporter-json-export results.json
```

## 📊 Test Coverage

The collection tests:
- ✅ Authentication (valid/invalid tokens)
- ✅ Input validation (required fields, empty values)
- ✅ Email sending functionality
- ✅ Error responses and status codes
- ✅ Service health and monitoring
- ✅ API documentation accessibility

## 🤝 Contributing

When adding new endpoints:
1. Add requests to appropriate folder
2. Include test scripts for validation
3. Add example responses
4. Update this README if needed
5. Test with both local and production environments

---

**Happy Testing! 📧✨**