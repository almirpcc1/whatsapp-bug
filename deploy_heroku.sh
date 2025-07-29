#!/bin/bash

# WhatsApp Bulk Messaging System - Heroku Deploy Script
# Otimizado para Performance-L Dynos com máxima velocidade

echo "🚀 DEPLOYING WHATSAPP BULK SYSTEM TO HEROKU - MAXIMUM VELOCITY MODE"
echo "=================================================="

# Check if heroku CLI is installed
if ! command -v heroku &> /dev/null; then
    echo "❌ Heroku CLI not found. Please install it first."
    echo "   Visit: https://devcenter.heroku.com/articles/heroku-cli"
    exit 1
fi

# Login check
echo "🔐 Checking Heroku login..."
heroku auth:whoami || {
    echo "❌ Please login to Heroku first: heroku login"
    exit 1
}

# App name (you can change this)
APP_NAME="${1:-whatsapp-bulk-system}"

echo "📱 Creating Heroku app: $APP_NAME"

# Create app with Performance-L dyno
heroku create $APP_NAME --region us

# Add PostgreSQL addon
echo "🗄️ Adding PostgreSQL database..."
heroku addons:create heroku-postgresql:standard-0 --app $APP_NAME

# Set config vars for maximum performance
echo "⚡ Setting performance configuration..."
heroku config:set \
  FLASK_ENV=production \
  MAX_WORKERS=10000 \
  BATCH_SIZE=2000 \
  THREAD_MULTIPLIER=500 \
  CONNECTION_POOL_SIZE=3000 \
  RATE_LIMIT_DELAY=0.00001 \
  API_CALLS_PER_SECOND=2000 \
  --app $APP_NAME

# Scale to Performance-L dyno
echo "🔥 Scaling to Performance-L dyno for maximum velocity..."
heroku ps:scale web=1:performance-l --app $APP_NAME

# Deploy
echo "🚀 Deploying to Heroku..."
git add .
git commit -m "Deploy WhatsApp Bulk System - Maximum Velocity Mode"
git push heroku main

# Open app
echo "✅ Deployment complete! Opening app..."
heroku open --app $APP_NAME

echo ""
echo "🎉 DEPLOYMENT SUCCESSFUL!"
echo "=================================================="
echo "App URL: https://$APP_NAME.herokuapp.com"
echo "Performance: Performance-L Dyno (14GB RAM, 8 CPU cores)"
echo "Velocity: Up to 2000 calls/second to WhatsApp API"
echo "Workers: Up to 10,000 concurrent workers"
echo ""
echo "📋 Next steps:"
echo "1. Set your WHATSAPP_ACCESS_TOKEN in Heroku dashboard"
echo "2. Test the system with a small list first"
echo "3. Scale up for massive campaigns!"
echo ""
echo "🔧 Useful commands:"
echo "heroku logs --tail --app $APP_NAME    # View logs"
echo "heroku config --app $APP_NAME         # View config"
echo "heroku ps --app $APP_NAME             # View dynos"