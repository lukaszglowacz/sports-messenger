#!/bin/bash
# Run backend tests

echo "🧪 Running backend tests..."
echo ""

pytest tests/ \
    --verbose \
    --cov=app \
    --cov-report=term-missing \
    --cov-report=html

echo ""
echo "✅ Tests complete!"