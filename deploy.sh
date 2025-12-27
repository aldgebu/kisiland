#!/usr/bin/env bash
set -e

PYTHON=python3.12
BUILD_DIR=build
ZIP_NAME=lambda.zip

echo "🧹 Cleaning old build..."
rm -rf $BUILD_DIR $ZIP_NAME

echo "📦 Creating build directory..."
mkdir -p $BUILD_DIR

echo "🐍 Installing dependencies..."
$PYTHON -m pip install --upgrade pip
$PYTHON -m pip install -r requirements.txt -t $BUILD_DIR

echo "📁 Copying application code..."
cp lambda_handler.py $BUILD_DIR/
cp -r app $BUILD_DIR/

echo "🗜 Creating Lambda ZIP..."
cd $BUILD_DIR
zip -r ../$ZIP_NAME .
cd ..

echo "✅ Build complete: $ZIP_NAME"
aws lambda update-function-code \
  --function-name fastapi-service-dev-api \
  --zip-file fileb://lambda.zip \
  --profile kisiland \
  --region us-east-1

echo "✅ Deployment complete: $ZIP_NAME"


