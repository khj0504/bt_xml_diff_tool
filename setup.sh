#!/bin/bash

# Setup script for BehaviorTree XML Diff Tool
# This script checks dependencies and sets up the environment

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "🔧 Setting up BehaviorTree XML Diff Tool..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Check if Python3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 is not installed. Please install Python3 first."
    exit 1
fi

echo "✅ Python3 found: $(python3 --version)"

# Check if Git is installed
if ! command -v git &> /dev/null; then
    echo "❌ Git is not installed. Please install Git first."
    exit 1
fi

echo "✅ Git found: $(git --version)"

# Check if we're in a Git repository
if ! git rev-parse --git-dir > /dev/null 2>&1; then
    echo "⚠️  Warning: Not in a Git repository. Git-based analysis will not work."
    echo "   Make sure to run the tool from within a Git repository."
else
    echo "✅ Git repository detected"
fi

# Check required Python modules
echo ""
echo "🐍 Checking Python dependencies..."

required_modules=("xml.etree.ElementTree" "enum" "json" "subprocess" "pathlib" "typing" "dataclasses")
missing_modules=()

for module in "${required_modules[@]}"; do
    if python3 -c "import $module" 2>/dev/null; then
        echo "✅ $module"
    else
        echo "❌ $module (missing)"
        missing_modules+=("$module")
    fi
done

if [ ${#missing_modules[@]} -ne 0 ]; then
    echo ""
    echo "❌ Missing required Python modules:"
    for module in "${missing_modules[@]}"; do
        echo "   - $module"
    done
    echo "Please install the missing modules and run setup again."
    exit 1
fi

# Make scripts executable
echo ""
echo "🔧 Setting up executable permissions..."
chmod +x "$SCRIPT_DIR/start_server.sh"
chmod +x "$SCRIPT_DIR/run_analysis.sh"
echo "✅ Scripts are now executable"

echo ""
echo "🎉 Setup completed successfully!"
echo ""
echo "📖 Usage:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "🚀 Quick Start (All-in-One):"
echo "   ./run_analysis.sh <source_branch> <target_branch>"
echo "   Example: ./run_analysis.sh develop feature-branch"
echo ""
echo "🔧 Advanced Usage:"
echo "   1. Run analysis: python3 enhanced_branch_analyzer.py <source> <target> -o result.html"
echo "   2. Start server: ./start_server.sh [port]"
echo "   3. Open browser: http://localhost:8080/result.html"
echo ""
echo "📚 For more details, see README.md"