#!/bin/bash

# BehaviorTree XML Diff Tool - All-in-One Runner
# This script runs the analysis and starts the server automatically

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PORT=8080

# Function to show usage
show_usage() {
    echo "Usage: $0 <source_branch> <target_branch> [options]"
    echo ""
    echo "Arguments:"
    echo "  source_branch    Source branch (e.g., develop)"
    echo "  target_branch    Target branch (e.g., feature-branch)"
    echo ""
    echo "Options:"
    echo "  -p, --port       HTTP server port (default: 8080)"
    echo "  -h, --help       Show this help message"
    echo ""
    echo "Note: Output is always saved as 'bt_diff_result.html' (overwritten each time)"
    echo ""
    echo "Examples:"
    echo "  $0 develop feature-bt-tree-viz"
    echo "  $0 main feature-branch -p 8090"
}

# Parse arguments
SOURCE_BRANCH=""
TARGET_BRANCH=""

while [[ $# -gt 0 ]]; do
    case $1 in
        -p|--port)
            PORT="$2"
            shift 2
            ;;
        -h|--help)
            show_usage
            exit 0
            ;;
        -*)
            echo "Unknown option: $1"
            show_usage
            exit 1
            ;;
        *)
            if [[ -z "$SOURCE_BRANCH" ]]; then
                SOURCE_BRANCH="$1"
            elif [[ -z "$TARGET_BRANCH" ]]; then
                TARGET_BRANCH="$1"
            else
                echo "Too many arguments"
                show_usage
                exit 1
            fi
            shift
            ;;
    esac
done

# Check required arguments
if [[ -z "$SOURCE_BRANCH" || -z "$TARGET_BRANCH" ]]; then
    echo "Error: Both source and target branches are required"
    show_usage
    exit 1
fi

echo "🔍 BehaviorTree XML Diff Tool"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📊 Analyzing changes: $SOURCE_BRANCH → $TARGET_BRANCH"
echo "📄 Output file: bt_diff_result.html (overwritten)"
echo "🌐 Server port: $PORT"
echo ""

# Run the analysis
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Always use the same output filename to overwrite previous results
OUTPUT_FILE="bt_diff_result.html"

echo "🔄 Generating analysis (overwriting previous result)..."

# Use the directory where the script was called from as the git repository
ORIGINAL_DIR="$(pwd)"

# Check if current directory is a git repository
if git rev-parse --git-dir > /dev/null 2>&1; then
    echo "✅ Using Git repository: $ORIGINAL_DIR"
    
    # Change to bt_xml_diff_tool directory before running Python script
    cd "$SCRIPT_DIR"
    python3 enhanced_branch_analyzer.py "$SOURCE_BRANCH" "$TARGET_BRANCH" -o "$OUTPUT_FILE" --repo-path "$ORIGINAL_DIR"
    
else
    echo "❌ Error: Current directory is not a Git repository"
    echo "   Please run this script from within a Git repository"
    exit 1
fi

if [[ $? -eq 0 ]]; then
    echo ""
    echo "✅ Analysis completed successfully!"
    echo "📄 Result saved to: $OUTPUT_FILE"
    echo ""
    echo "🚀 Starting HTTP server on port $PORT..."
    
    # Function to clean up background processes
    cleanup() {
        echo ""
        echo "🛑 Shutting down server..."
        pkill -f "python3 -m http.server $PORT" 2>/dev/null || true
        exit 0
    }
    
    # Set up cleanup on script exit
    trap cleanup SIGINT SIGTERM EXIT
    
    # Start HTTP server in background
    python3 -m http.server "$PORT" > /dev/null 2>&1 &
    SERVER_PID=$!
    
    # Wait for server to be fully ready
    URL="http://localhost:$PORT/$OUTPUT_FILE"
    echo "🔄 Waiting for server to start..."
    
    # Check if server is ready (max 10 seconds)
    for i in {1..20}; do
        if curl -s "http://localhost:$PORT" > /dev/null 2>&1; then
            echo "✅ Server ready!"
            break
        fi
        sleep 0.5
    done
    
    # Try to open browser automatically
    echo "🌐 Opening browser: $URL"
    
    if command -v xdg-open &> /dev/null; then
        xdg-open "$URL" 2>/dev/null || echo "⚠️  Could not auto-open browser. Please manually open: $URL"
    elif command -v open &> /dev/null; then
        open "$URL" 2>/dev/null || echo "⚠️  Could not auto-open browser. Please manually open: $URL"
    else
        echo "⚠️  Browser auto-open not supported. Please manually open: $URL"
    fi
    
    echo ""
    echo "🎉 Server is running! Browser should open automatically."
    echo "📍 If browser didn't open, manually navigate to: $URL"
    echo ""
    echo "Press Ctrl+C to stop the server and exit"
    echo ""
    
    # Wait for server process
    wait $SERVER_PID
else
    echo "❌ Analysis failed!"
    exit 1
fi