#!/usr/bin/env python3
"""
Pixel Pigeon - Email Forwarding Service API

A secure API service for sending formatted emails with HTML templates,
authentication tokens, and logo support.
"""
from dotenv import load_dotenv

load_dotenv()  # take environment variables
import os
import json
import logging
import smtplib
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from pathlib import Path
from typing import Dict, List, Optional

from fastapi import FastAPI, HTTPException, Request, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
import uvicorn

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Pixel Pigeon - Email Forwarding Service",
    description="A secure API for sending formatted HTML emails with authentication",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Security scheme
security = HTTPBearer()

# Request/Response models
class EmailRequest(BaseModel):
    title: str
    message: str

class EmailResponse(BaseModel):
    status: str
    recipients: List[str]

# Configuration
CONFIG_FILE = os.getenv('CONFIG_FILE', '/app/config.json')
SMTP_HOST = os.getenv('SMTP_HOST', 'smtp.gmail.com')
SMTP_PORT = int(os.getenv('SMTP_PORT', 587))
SMTP_USER = os.getenv('SMTP_USER')
SMTP_PASS = os.getenv('SMTP_PASS')
FROM_EMAIL = os.getenv('FROM_EMAIL')
LOGO_PATH = os.getenv('LOGO_PATH', '/app/logo.jpg')
LANGUAGE = os.getenv('LANGUAGE', 'en').lower()  # 'en' or 'tr'

# Language translations
TRANSLATIONS = {
    'en': {
        'email_notification': 'Email Notification',
        'sent_via': 'Sent via Pixel Pigeon',
        'service_name': 'Pixel Pigeon - Email Forwarding Service',
        'service_status': 'active',
        'endpoints': {
            'send': 'POST /send',
            'docs': 'GET /docs', 
            'health': 'GET /health'
        }
    },
    'tr': {
        'email_notification': 'E-posta Bildirimi',
        'sent_via': 'Pixel Pigeon ile gönderildi',
        'service_name': 'Pixel Pigeon - E-posta Yönlendirme Servisi',
        'service_status': 'aktif',
        'endpoints': {
            'send': 'POST /send',
            'docs': 'GET /docs',
            'health': 'GET /health'
        }
    }
}

def get_text(key: str) -> str:
    """Get translated text based on language setting."""
    return TRANSLATIONS.get(LANGUAGE, TRANSLATIONS['en']).get(key, key)

def load_config() -> Dict:
    """Load token configuration from file."""
    try:
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            logger.warning(f"Config file {CONFIG_FILE} not found, using empty config")
            return {"tokens": {}}
    except Exception as e:
        logger.error(f"Error loading config: {e}")
        return {"tokens": {}}

def get_recipients_for_token(token: str) -> Optional[List[str]]:
    """Get allowed recipients for a given token."""
    config = load_config()
    return config.get("tokens", {}).get(token)

def validate_token(credentials: HTTPAuthorizationCredentials = Depends(security)) -> str:
    """Validate the bearer token and return it."""
    token = credentials.credentials
    recipients = get_recipients_for_token(token)
    
    if recipients is None:
        logger.warning(f"Invalid token used: {token[:6]}...")
        raise HTTPException(
            status_code=403,
            detail="Invalid token or unauthorized access"
        )
    
    return token

def create_html_template(title: str, message: str, has_logo: bool = False) -> str:
    """Create a beautiful HTML email template."""
    logo_section = '''
        <div style="text-align: center; margin-bottom: 30px; background-color: #ffffff; padding: 20px; border-radius: 8px;">
            <img src="cid:logo" alt="Logo" style="max-width: 200px; height: auto; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); background-color: #ffffff;">
        </div>
    ''' if has_logo else ''
    
    # Convert newlines to HTML breaks and trim whitespace
    formatted_message = message.strip().replace('\n', '<br>')
    
    html_template = f"""
    <!DOCTYPE html>
    <html lang="{LANGUAGE}">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{title}</title>
    </head>
    <body style="margin: 0; padding: 0; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f5f7fa;">
        <div style="max-width: 600px; margin: 40px auto; background-color: #ffffff; border-radius: 12px; box-shadow: 0 4px 20px rgba(0,0,0,0.08); overflow: hidden;">
            <!-- Header -->
            <div style="background-color: #ffffff; padding: 40px 30px; text-align: center; border-bottom: 1px solid #e2e8f0;">
                {logo_section}
                <h1 style="color: #2d3748; margin: 0; font-size: 28px; font-weight: 600;">
                    {get_text('email_notification')}
                </h1>
            </div>
            
            <!-- Content -->
            <div style="padding: 40px 30px;">
                <div style="background-color: #f8fafc; border-left: 4px solid #667eea; padding: 20px 25px; border-radius: 6px; margin-bottom: 30px;">
                    <h2 style="color: #2d3748; margin: 0 0 15px 0; font-size: 24px; font-weight: 700;">
                        {title}
                    </h2>
                </div>
                
                <div style="background-color: #ffffff; border: 1px solid #e2e8f0; border-radius: 8px; padding: 25px; line-height: 1.6;">
                    <p style="color: #4a5568; margin: 0; font-size: 16px;">
                        {formatted_message}
                    </p>
                </div>
            </div>
            
            <!-- Footer -->
            <div style="background-color: #f7fafc; padding: 20px 30px; text-align: center; border-top: 1px solid #e2e8f0;">
                <p style="color: #718096; margin: 0; font-size: 14px;">
                    {get_text('sent_via')} • {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
                </p>
            </div>
        </div>
    </body>
    </html>
    """
    
    return html_template

def create_plain_text(title: str, message: str) -> str:
    """Create plain text version of the email."""
    return f"""
{title}
{'=' * len(title)}

{message}

---
{get_text('sent_via')}
{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
    """.strip()

def send_email(recipients: List[str], title: str, message: str) -> bool:
    """Send the formatted email to recipients."""
    try:
        # Validate SMTP credentials
        if not SMTP_USER or not SMTP_PASS or not FROM_EMAIL:
            logger.error("SMTP credentials not configured")
            return False
            
        # Create message
        msg = MIMEMultipart('related')
        msg['From'] = FROM_EMAIL
        msg['To'] = ', '.join(recipients)
        msg['Subject'] = title
        
        # Check if logo exists (checked on every request for dynamic loading)
        has_logo = os.path.exists(LOGO_PATH)
        if has_logo:
            logger.debug(f"Logo found at {LOGO_PATH}")
        else:
            logger.debug(f"No logo found at {LOGO_PATH}")
        
        # Create HTML and text versions
        html_content = create_html_template(title, message, has_logo)
        text_content = create_plain_text(title, message)
        
        # Create multipart alternative
        msg_alternative = MIMEMultipart('alternative')
        
        # Add text version
        text_part = MIMEText(text_content, 'plain', 'utf-8')
        msg_alternative.attach(text_part)
        
        # Add HTML version
        html_part = MIMEText(html_content, 'html', 'utf-8')
        msg_alternative.attach(html_part)
        
        msg.attach(msg_alternative)
        
        # Add logo if it exists
        if has_logo:
            try:
                with open(LOGO_PATH, 'rb') as f:
                    logo_data = f.read()
                logo_image = MIMEImage(logo_data)
                logo_image.add_header('Content-ID', '<logo>')
                logo_image.add_header('Content-Disposition', 'inline', filename='logo.jpg')
                msg.attach(logo_image)
            except Exception as e:
                logger.warning(f"Could not attach logo: {e}")
        
        # Send email with secure connection
        if SMTP_PORT == 465:
            # Use SSL for port 465
            with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT) as server:
                server.login(SMTP_USER, SMTP_PASS)
                server.send_message(msg)
        else:
            # Use TLS for other ports (587, 25)
            with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
                server.starttls()
                server.login(SMTP_USER, SMTP_PASS)
                server.send_message(msg)
        
        return True
        
    except Exception as e:
        logger.error(f"Failed to send email: {e}")
        return False

@app.get("/")
async def root():
    """Root endpoint with service information."""
    return {
        "service": get_text("service_name"),
        "version": "1.0.0",
        "status": get_text("service_status"),
        "language": LANGUAGE,
        "endpoints": get_text("endpoints")
    }

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    config = load_config()
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "language": LANGUAGE,
        "smtp_configured": bool(SMTP_HOST and SMTP_USER and SMTP_PASS and FROM_EMAIL),
        "tokens_configured": len(config.get("tokens", {})),
        "logo_available": os.path.exists(LOGO_PATH)
    }

@app.post("/send", response_model=EmailResponse)
async def send_notification(
    email_request: EmailRequest,
    token: str = Depends(validate_token)
):
    """
    Send a formatted email notification.
    
    - **title**: Subject of the email (displayed as heading)
    - **message**: Body content (supports \\n for line breaks)
    
    Requires valid Bearer token in Authorization header.
    """
    try:
        # Validate required fields
        if not email_request.title or not email_request.message:
            raise HTTPException(
                status_code=400,
                detail="Both 'title' and 'message' fields are required"
            )
        
        # Get recipients for this token
        recipients = get_recipients_for_token(token)
        if not recipients:
            raise HTTPException(
                status_code=403,
                detail="No recipients configured for this token"
            )
        
        # Send email
        success = send_email(recipients, email_request.title, email_request.message)
        
        if not success:
            raise HTTPException(
                status_code=500,
                detail="Failed to send email"
            )
        
        # Log successful send
        logger.info(
            f"HTML message '{email_request.title}' sent to {recipients} via token {token[:6]}..."
        )
        
        return EmailResponse(
            status="sent",
            recipients=recipients
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error in send endpoint: {e}")
        raise HTTPException(
            status_code=500,
            detail="Internal server error"
        )

if __name__ == "__main__":
    # Validate required environment variables
    required_vars = [SMTP_HOST, SMTP_USER, SMTP_PASS, FROM_EMAIL]
    if not all(required_vars):
        logger.error("Missing required SMTP environment variables")
        exit(1)
    
    logger.info(f"Starting {get_text('service_name')}...")
    logger.info(f"Language: {LANGUAGE.upper()}")
    logger.info(f"SMTP Host: {SMTP_HOST}:{SMTP_PORT}")
    logger.info(f"From Email: {FROM_EMAIL}")
    logger.info(f"Config File: {CONFIG_FILE}")
    logger.info(f"Logo Path: {LOGO_PATH}")
    
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=8080,
        reload=False,
        log_level="info"
    )