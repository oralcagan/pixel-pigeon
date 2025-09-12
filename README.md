# � Pixel Pigeon - Email Forwarding Service

Containerized API service for sending notification emails to preconfigured list of users.

## Quick Start

### 1. Clone and Setup

```bash
git clone pixel-pigeon
cd pixel-pigeon
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

## Configuration

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

### Using Pre-built Image from GitHub Container Registry

```bash
# Pull the latest image
docker pull ghcr.io/oralcagan/pixel-pigeon:latest

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

## Monitoring and Logs

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