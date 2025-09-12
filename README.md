# 📬 Email Forwarding Service

A secure, containerized API service for sending beautifully formatted HTML emails with authentication tokens and logo support.

![Email Service](https://img.shields.io/badge/Email-Service-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104.1-green)
![Docker](https://img.shields.io/badge/Docker-Ready-blue)
![Python](https://img.shields.io/badge/Python-3.11-blue)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## ✨ Features

- **🔐 Token-based Authentication**: Secure Bearer token system
- **🎨 Beautiful HTML Emails**: Responsive templates with modern design
- **🖼️ Logo Support**: Inline image embedding with fallback
- **📱 Multi-format**: HTML with plain text fallback
- **🐳 Docker Ready**: Complete containerization with Docker Compose
- **📊 Health Monitoring**: Built-in health checks and logging
- **🔄 Live Configuration**: Hot-reload configuration without restart
- **📚 API Documentation**: Auto-generated OpenAPI/Swagger docs

## 🚀 Quick Start

### 1. Clone and Setup

```bash
git clone &lt;your-repo&gt;
cd email-notif-service
cp .env.example .env
```

### 2. Configure SMTP Settings

Edit `.env` file with your SMTP credentials:

```env
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASS=your-app-password
FROM_EMAIL=your-email@gmail.com
```

### 3. Configure Tokens

Edit `config.json` to set up authentication tokens:

```json
{
  "tokens": {
    "your-secure-token-1": ["recipient1@example.com"],
    "your-secure-token-2": ["recipient2@example.com", "recipient3@example.com"]
  }
}
```

### 4. Add Logo (Optional)

Place your logo as `logo.jpg` in the project directory.

### 5. Start the Service

```bash
docker-compose up -d
```

The service will be available at `http://localhost:8080`

## 📖 API Documentation

### Base URL
```
http://localhost:8080
```

### Authentication
All requests require a Bearer token in the Authorization header:
```
Authorization: Bearer &lt;your-token&gt;
```

### Endpoints

#### `POST /send`
Send a formatted email notification.

**Request Body:**
```json
{
  "title": "Server Alert",
  "message": "CPU usage &gt; 90%\nPlease check immediately."
}
```

**Response:**
```json
{
  "status": "sent",
  "recipients": ["support@example.com"]
}
```

#### `GET /health`
Health check endpoint.

#### `GET /docs`
Interactive API documentation (Swagger UI).

#### `GET /redoc`
Alternative API documentation (ReDoc).

## 🌐 Example Usage

### cURL

```bash
curl -X POST http://localhost:8080/send \
  -H "Authorization: Bearer your-secure-token-1" \
  -H "Content-Type: application/json" \
  -d '{
        "title": "System Alert",
        "message": "Database connection failed\nImmediate attention required."
      }'
```

### Python

```python
import requests

url = "http://localhost:8080/send"
headers = {
    "Authorization": "Bearer your-secure-token-1",
    "Content-Type": "application/json"
}
data = {
    "title": "System Alert",
    "message": "Database connection failed\nImmediate attention required."
}

response = requests.post(url, headers=headers, json=data)
print(response.json())
```

### JavaScript/Node.js

```javascript
const response = await fetch('http://localhost:8080/send', {
  method: 'POST',
  headers: {
    'Authorization': 'Bearer your-secure-token-1',
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    title: 'System Alert',
    message: 'Database connection failed\nImmediate attention required.'
  })
});

const result = await response.json();
console.log(result);
```

## 🎨 Email Template

The service generates beautiful HTML emails with:

- **Header**: Gradient background with logo (if provided)
- **Title Section**: Highlighted with accent border
- **Message Body**: Clean formatting with line break support
- **Footer**: Timestamp and service branding
- **Responsive Design**: Works on desktop and mobile
- **Plain Text Fallback**: For clients that don't support HTML

### Sample Email Output

```
[Logo Image]

📧 Email Notification

┌─────────────────────────────────────┐
│ System Alert                        │
└─────────────────────────────────────┘

Database connection failed
Immediate attention required.

────────────────────────────────────────
Sent via Email Forwarding Service • 2025-09-12 14:30:25
```

## ⚙️ Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `SMTP_HOST` | SMTP server hostname | `smtp.gmail.com` |
| `SMTP_PORT` | SMTP server port | `587` |
| `SMTP_USER` | SMTP username | Required |
| `SMTP_PASS` | SMTP password | Required |
| `FROM_EMAIL` | Sender email address | Required |
| `CONFIG_FILE` | Path to config.json | `/app/config.json` |
| `LOGO_PATH` | Path to logo image | `/app/logo.jpg` |

### Token Configuration

The `config.json` file maps tokens to allowed recipients:

```json
{
  "tokens": {
    "secure-token-123": ["admin@company.com"],
    "alert-token-456": ["ops@company.com", "support@company.com"],
    "sales-token-789": ["sales@company.com", "manager@company.com"]
  }
}
```

**Security Best Practices:**
- Generate tokens using `secrets.token_hex(32)` in Python
- Use different tokens for different purposes
- Rotate tokens regularly
- Never commit real tokens to version control

## 🐳 Docker Deployment

### Development

```bash
# Build and run
docker-compose up --build

# Run in background
docker-compose up -d

# View logs
docker-compose logs -f email-service

# Stop service
docker-compose down
```

### Using Pre-built Image from GitHub Container Registry

```bash
# Pull the latest image
docker pull ghcr.io/yourusername/email-notif-service:latest

# Run with docker-compose using the pre-built image
docker-compose -f docker-compose.yml up -d
```

### Production

1. **Use environment file:**
   ```bash
   cp .env.example .env
   # Edit .env with production values
   docker-compose --env-file .env up -d
   ```

2. **Use external configuration:**
   ```yaml
   volumes:
     - /path/to/config.json:/app/config.json:ro
     - /path/to/logo.jpg:/app/logo.jpg:ro
   ```

3. **Enable restart policy:**
   ```yaml
   restart: unless-stopped
   ```

## 🔍 Monitoring and Logs

### Health Check

```bash
curl http://localhost:8080/health
```

### Log Monitoring

```bash
# Follow logs
docker-compose logs -f email-service

# Check specific container
docker logs email-forwarding-service

# Filter logs
docker-compose logs email-service | grep ERROR
```

### Sample Log Output

```
2025-09-12 14:30:25 [INFO] Starting Email Forwarding Service...
2025-09-12 14:30:25 [INFO] SMTP Host: smtp.gmail.com:587
2025-09-12 14:30:25 [INFO] From Email: notifications@company.com
2025-09-12 14:30:45 [INFO] HTML message 'System Alert' sent to ['admin@company.com'] via token secure...
```

## 🧪 Testing with Postman

A comprehensive Postman collection is provided for testing all API endpoints:

### Import Collection
1. Open Postman
2. Import `postman/Email-Forwarding-Service.postman_collection.json`
3. Import environment: `postman/Email-Forwarding-Service-Local.postman_environment.json`
4. Update the `auth_token` variable with your actual token

### Collection Features
- ✅ All API endpoints with examples
- ✅ Automated tests for response validation
- ✅ Error condition testing
- ✅ Multiple environment configurations
- ✅ Pre-request scripts for dynamic data

### Run All Tests
```bash
# Using Newman (Postman CLI)
npm install -g newman
newman run postman/Email-Forwarding-Service.postman_collection.json \
  -e postman/Email-Forwarding-Service-Local.postman_environment.json
```

## 🚀 CI/CD with GitHub Actions

The project includes automated CI/CD workflows:

### Build & Push Workflow
- **Triggers**: Push to main/develop, tags, PRs
- **Actions**: 
  - Multi-platform Docker builds (amd64, arm64)
  - Push to GitHub Container Registry
  - Security scanning with Trivy
  - Automatic tagging (latest, semver, branch)

### CI/CD Pipeline
- **Testing**: Python linting, pytest, application startup tests
- **Docker Testing**: Container build and health check validation
- **Documentation**: Auto-deployment to GitHub Pages

### Using the Workflows
1. **Push to main**: Triggers full build, test, and deployment
2. **Create release tag**: `git tag v1.0.0 && git push origin v1.0.0`
3. **Pull requests**: Automatically tested before merge

### Container Registry
Images are automatically published to:
```
ghcr.io/yourusername/email-notif-service:latest
ghcr.io/yourusername/email-notif-service:v1.0.0
ghcr.io/yourusername/email-notif-service:main
```

## 🔧 Development

### Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Set environment variables
export SMTP_HOST=smtp.gmail.com
export SMTP_USER=your-email@gmail.com
# ... other variables

# Run development server
python app.py
```

### Running Tests

```bash
# Install test dependencies
pip install pytest httpx

# Run tests
pytest tests/
```

## 📊 API Responses

### Success Response

```json
{
  "status": "sent",
  "recipients": ["user@example.com"]
}
```

### Error Responses

| Status | Error | Description |
|--------|-------|-------------|
| 400 | Bad Request | Missing title or message |
| 401 | Unauthorized | Missing Authorization header |
| 403 | Forbidden | Invalid token |
| 500 | Internal Server Error | SMTP or server error |

## 🔒 Security Considerations

- **Token Storage**: Store tokens securely, never in plain text
- **SMTP Credentials**: Use app-specific passwords for Gmail
- **Network Security**: Use HTTPS in production
- **Rate Limiting**: Consider implementing rate limiting
- **Input Validation**: All inputs are validated and sanitized
- **Logging**: Sensitive data is not logged (tokens are truncated)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

## 🆘 Troubleshooting

### Common Issues

**SMTP Authentication Failed:**
- Check SMTP credentials
- Enable "Less secure app access" or use app passwords
- Verify SMTP host and port

**Token Unauthorized:**
- Check token in config.json
- Verify Authorization header format
- Check for typos in token

**Email Not Received:**
- Check spam folder
- Verify recipient email addresses
- Check SMTP logs for errors

**Docker Issues:**
- Ensure Docker is running
- Check port 8080 is available
- Verify volume mounts

### Getting Help

- Check logs: `docker-compose logs email-service`
- API docs: `http://localhost:8080/docs`
- Health check: `http://localhost:8080/health`

---

**Made with ❤️ for reliable email notifications**