#!/bin/bash

# Setup script to create docs folder structure for all projects
# This creates a consistent documentation structure across all projects

set -e

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TEMPLATE_INDEX="$PROJECT_ROOT/PROJECT_TEMPLATE_DOCS_INDEX.md"

echo "🚀 Setting up docs/ structure for all projects..."
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

CREATED=0
SKIPPED=0
ERROR=0

for project in "${PROJECTS[@]}"; do
    PROJECT_PATH="$PROJECT_ROOT/$project"
    DOCS_PATH="$PROJECT_PATH/docs"
    
    if [ -d "$PROJECT_PATH" ]; then
        PROJECT_NAME=$(basename "$PROJECT_PATH")
        
        # Check if docs folder already exists
        if [ -d "$DOCS_PATH" ]; then
            # Check if INDEX.md exists
            if [ ! -f "$DOCS_PATH/INDEX.md" ]; then
                echo "📝 Adding INDEX.md to: $project"
                cp "$TEMPLATE_INDEX" "$DOCS_PATH/INDEX.md"
                ((CREATED++))
            else
                echo "⏭️  Skipping: $project (docs/ already has INDEX.md)"
                ((SKIPPED++))
            fi
        else
            echo "📁 Creating docs/ folder for: $project"
            mkdir -p "$DOCS_PATH"
            cp "$TEMPLATE_INDEX" "$DOCS_PATH/INDEX.md"
            ((CREATED++))
        fi
    else
        echo "❌ Project not found: $project"
        ((ERROR++))
    fi
done

echo ""
echo "================================================"
echo "✅ Documentation structure setup complete!"
echo "================================================"
echo "📊 Summary:"
echo "   Created/Updated: $CREATED"
echo "   Skipped: $SKIPPED"
if [ $ERROR -gt 0 ]; then
    echo "   Errors: $ERROR"
fi
echo ""
echo "📋 Next steps:"
echo "   1. Review docs/INDEX.md in each project"
echo "   2. Add project-specific docs as needed:"
echo "      - docs/SETUP.md (detailed setup)"
echo "      - docs/TESTING.md (testing guide)"
echo "      - docs/ARCHITECTURE.md (design docs)"
echo "   3. Update README.md in projects for quick start"
echo ""
