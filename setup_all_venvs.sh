#!/bin/bash

# Global setup script for all projects
# Creates virtual environments for chatbots, RAG, and agentic projects

set -e

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "🚀 Setting up virtual environments for all projects..."
echo ""

# List of all project directories
PROJECTS=(
    "chatbots/1-customer-support"
    "chatbots/2-multi-intent"
    "chatbots/3-safety-hardened-chatbot"
    "chatbots/4-conversational-memory-chatbot"
    "chatbots/5-multilingual-chatbot"
    "chatbots/6-healthcare-advisor-chatbot"
    "chatbots/7-streaming-realtime-chatbot"
    "RAG/1-faq-retrieval-chatbot"
    "RAG/2-document-qa"
    "RAG/3-code-search"
    "RAG/4-multi-document-reasoning"
    "RAG/5-conversational-kb"
    "RAG/6-medical-literature-search"
    "RAG/7-legal-compliance-rag"
    "RAG/8-technical-documentation-search"
    "RAG/9-product-catalog-search"
    "agentic/1-multi-tool-agent"
    "agentic/2-data-analysis-agent"
    "agentic/3-research-agent"
    "agentic/4-content-generation-agent"
    "agentic/5-customer-onboarding-agent"
    "agentic/6-travel-planning-agent"
    "agentic/7-project-management-agent"
    "agentic/8-code-review-agent"
    "agentic/9-monitoring-alerting-agent"
    "agentic/10-ecommerce-agent"
    "agentic/11-hr-recruitment-agent"
)

SETUP_COUNT=0
SKIP_COUNT=0

for project in "${PROJECTS[@]}"; do
    PROJECT_PATH="$PROJECT_ROOT/$project"
    
    if [ -d "$PROJECT_PATH" ]; then
        echo "📁 Setting up: $project"
        
        # Check if requirements.txt exists
        if [ -f "$PROJECT_PATH/requirements.txt" ]; then
            cd "$PROJECT_PATH"
            
            if [ -d "venv" ]; then
                echo "   ⚠️  Virtual environment exists, skipping"
                ((SKIP_COUNT++))
            else
                echo "   📦 Creating virtual environment..."
                python3 -m venv venv
                source venv/bin/activate
                
                echo "   📥 Installing dependencies..."
                pip install --upgrade pip --quiet
                pip install -r requirements.txt --quiet
                
                echo "   ✓ Setup complete"
                ((SETUP_COUNT++))
            fi
            
            cd "$PROJECT_ROOT"
        else
            echo "   ⚠️  requirements.txt not found, skipping"
            ((SKIP_COUNT++))
        fi
        
        echo ""
    else
        echo "⚠️  Project directory not found: $project"
        echo ""
    fi
done

echo "================================================"
echo "✅ Virtual environment setup complete!"
echo "================================================"
echo "📊 Summary:"
echo "   Created: $SETUP_COUNT"
echo "   Skipped: $SKIP_COUNT"
echo ""
echo "📋 To activate a project environment, run:"
echo "   source <project>/venv/bin/activate"
echo ""
