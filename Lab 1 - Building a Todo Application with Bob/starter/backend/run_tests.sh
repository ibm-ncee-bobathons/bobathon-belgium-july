#!/bin/bash
# Script to run tests with coverage report

echo "Running unit tests with coverage..."
echo "=================================="

# Run tests with coverage
python -m pytest test_app.py -v --cov=app --cov=models --cov=database --cov-report=term-missing --cov-report=html

echo ""
echo "=================================="
echo "Coverage report generated!"
echo "View detailed HTML report: htmlcov/index.html"
echo ""
echo "To view the HTML report, run:"
echo "  open htmlcov/index.html  (macOS)"
echo "  start htmlcov/index.html (Windows)"
echo "  xdg-open htmlcov/index.html (Linux)"

# Made with Bob
