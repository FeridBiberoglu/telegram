# Webhook Setup Guide

This guide explains how to set up webhooks for your Telegram bot using the Telegram Bot Framework.

## What are Webhooks?

Webhooks are a way for Telegram to send updates to your bot in real-time. Instead of your bot constantly asking Telegram for updates (polling), Telegram will immediately notify your bot when something happens (a user sends a message, presses a button, etc.).

Benefits of webhooks:
- **Reduced latency**: Updates are processed immediately
- **Lower server load**: No need for continuous polling
- **Better scalability**: Works well with serverless architectures

## Requirements

To use webhooks, you need:

1. **A public HTTPS server**: Telegram only supports webhooks over HTTPS
2. **Valid SSL certificate**: Self-signed certificates are accepted but require additional setup
3. **A domain or public IP**: Your server must be reachable from the internet
4. **Open ports**: Port 443, 80, 88, or 8443 (recommended)

## Basic Webhook Setup

### Step 1: Configure Your Web Server

First, set up a web server (like Nginx) and obtain an SSL certificate (Let's Encrypt is free and works well).

### Step 2: Create a Bot Application with Webhook Support

```python
from telegram_bot_framework import TelegramBot
from aiohttp import web
import ssl

# Initialize the bot with webhook configuration
bot = TelegramBot(
    token="YOUR_BOT_TOKEN",
    use_webhook=True,
    webhook_url="https://yourdomain.com/webhook/YOUR_SECRET_PATH"
)

# Register your handlers
@bot.on_message()
async def echo(message):
    await bot.send_message(
        chat_id=message.chat.id,
        text=f"You said: {message.text}"
    )

# Create a web application
app = web.Application()

# Register the webhook handler
app.router.add_post("/webhook/YOUR_SECRET_PATH", bot.webhook_handler)

# Add a health check endpoint
async def health_check(request):
    return web.Response(text="Bot is running")
app.router.add_get("/health", health_check)

# Run the application
if __name__ == "__main__":
    web.run_app(app, host="0.0.0.0", port=8443)
```

### Step 3: Set the Webhook with Telegram

You need to tell Telegram where to send updates. The framework can do this for you:

```python
# Set the webhook when starting the bot
if __name__ == "__main__":
    bot.set_webhook()  # This will use the webhook_url provided during initialization
    web.run_app(app, host="0.0.0.0", port=8443)
```

Or you can do it manually using the Telegram Bot API:

```
https://api.telegram.org/bot<YOUR_BOT_TOKEN>/setWebhook?url=https://yourdomain.com/webhook/YOUR_SECRET_PATH
```

## Advanced Webhook Configuration

### Using a Self-Signed Certificate

If you're using a self-signed certificate, you need to upload it to Telegram:

```python
bot = TelegramBot(
    token="YOUR_BOT_TOKEN",
    use_webhook=True,
    webhook_url="https://yourdomain.com/webhook/YOUR_SECRET_PATH",
    certificate_path="/path/to/your/certificate.pem"
)

# When setting the webhook, the certificate will be uploaded
bot.set_webhook()
```

### Securing Your Webhook

To enhance security, use a secret token in your webhook URL and validate incoming requests:

```python
import hmac
import hashlib

SECRET_TOKEN = "your_secret_token"

class SecureWebhookMiddleware:
    """Middleware to validate webhook requests."""
    
    async def process_update(self, update, next_handler):
        # Check X-Telegram-Bot-Api-Secret-Token header
        request = update.request
        token = request.headers.get("X-Telegram-Bot-Api-Secret-Token")
        
        if not token or not hmac.compare_digest(token, SECRET_TOKEN):
            print("Invalid webhook token")
            return None
        
        return await next_handler(update)

# Add the middleware
bot.use_middleware(SecureWebhookMiddleware())

# Set the webhook with the secret token
bot.set_webhook(secret_token=SECRET_TOKEN)
```

### IP Restrictions

Restrict webhook access to Telegram's IP ranges:

```python
TELEGRAM_IP_RANGES = [
    "149.154.160.0/20",
    "91.108.4.0/22"
]

class IPFilterMiddleware:
    """Middleware to filter requests by IP address."""
    
    async def process_update(self, update, next_handler):
        import ipaddress
        
        request = update.request
        ip = request.remote
        
        if not any(ipaddress.ip_address(ip) in ipaddress.ip_network(range) 
                   for range in TELEGRAM_IP_RANGES):
            print(f"Request from unauthorized IP: {ip}")
            return None
        
        return await next_handler(update)

# Add the middleware
bot.use_middleware(IPFilterMiddleware())
```

## Deployment Options

### Deploying with Docker

Here's a sample Dockerfile for deploying a webhook-based bot:

```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8443

CMD ["python", "bot.py"]
```

Build and run:

```bash
docker build -t telegram-bot .
docker run -p 8443:8443 telegram-bot
```

### Deploying to Cloud Platforms

#### AWS Lambda with API Gateway

For serverless deployment, see our [AWS Lambda example](https://github.com/yourusername/telegram-bot-framework/tree/main/examples/aws_lambda).

#### Google Cloud Run

Cloud Run is well-suited for webhook-based bots. See our [Cloud Run example](https://github.com/yourusername/telegram-bot-framework/tree/main/examples/cloud_run).

#### Heroku

Heroku's simple deployment works well with the framework:

```
web: python bot.py
```

Remember to set the `PORT` environment variable to match Heroku's assigned port.

## Troubleshooting

### Common Issues

1. **Webhook not working**:
   - Verify your server is accessible from the internet
   - Check that your SSL certificate is valid and trusted
   - Ensure you're using one of the allowed ports (443, 80, 88, 8443)

2. **Updates not being received**:
   - Check Telegram's response when setting the webhook
   - Look for errors in your application logs
   - Verify the webhook URL exactly matches what you registered

3. **Slow response times**:
   - Keep your handlers lightweight
   - Use asynchronous code for I/O operations
   - Consider using a message queue for processing intensive tasks

### Checking Webhook Status

You can check your webhook status with:

```
https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getWebhookInfo
```

This will return details about your current webhook configuration.

## Switching Back to Polling

If you need to disable webhooks and return to polling:

```python
# Remove the webhook
bot.delete_webhook()

# Start polling
bot.start_polling()
```

Or via the API:

```
https://api.telegram.org/bot<YOUR_BOT_TOKEN>/deleteWebhook
``` 