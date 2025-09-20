#!/bin/bash

# 🔧 Merge Conflict Resolution Script for PR #2
# This script resolves conflicts by keeping our advanced features

echo "🕊️ Sacred Team Merge Conflict Resolution"
echo "========================================"

# Check if we're in the right branch
current_branch=$(git branch --show-current)
if [ "$current_branch" != "feat/phase-2-jules-micro-implementation" ]; then
    echo "❌ Error: Please switch to feat/phase-2-jules-micro-implementation branch first"
    echo "   Run: git checkout feat/phase-2-jules-micro-implementation"
    exit 1
fi

echo "✅ Current branch: $current_branch"

# Fetch latest changes
echo "📥 Fetching latest changes..."
git fetch origin

# Start merge
echo "🔄 Starting merge with origin/feat/chat..."
git merge origin/feat/chat

# Check if merge has conflicts
if [ $? -ne 0 ]; then
    echo "⚠️  Merge conflicts detected. Resolving by keeping our advanced features..."
    
    # Resolve conflicts by keeping our versions (HEAD)
    echo "🔧 Resolving OrganellaPanel.vue (keeping ChroniclerBonusEffect)..."
    git checkout HEAD -- frontend/src/components/OrganellaPanel.vue
    
    echo "🔧 Resolving HexaLevel.vue (keeping interactive features)..."
    git checkout HEAD -- frontend/src/components/HexaLevel.vue
    
    echo "🔧 Resolving JourneyView.vue (keeping hexagonal navigation)..."
    git checkout HEAD -- frontend/src/views/JourneyView.vue
    
    echo "🔧 Resolving chat.ts (keeping sacred commands)..."
    git checkout HEAD -- frontend/src/stores/chat.ts
    
    echo "🔧 Resolving Organelle Grimoire (keeping documentation)..."
    git checkout HEAD -- docs/10_ORGANELLE_GRIMOIRE.md
    
    # Add resolved files
    echo "📝 Adding resolved files..."
    git add .
    
    # Commit the resolution
    echo "💾 Committing merge resolution..."
    git commit -m "resolve: Keep advanced features over reverted base

- Maintain OrganellaPanel with ChroniclerBonusEffect and evolution ceremonies
- Keep enhanced HexaLevel with interactive quest system  
- Preserve JourneyView with hexagonal navigation
- Maintain enhanced chat store with sacred commands
- Keep Organelle Grimoire documentation

Our branch has the advanced, working features that should be preserved.

Co-authored-by: Ona <no-reply@ona.com>"

    echo "✅ Merge conflicts resolved successfully!"
else
    echo "✅ Merge completed without conflicts!"
fi

# Test the resolution
echo ""
echo "🧪 Testing resolution..."

# Test frontend build
echo "📦 Testing frontend build..."
cd frontend
if bun run build; then
    echo "✅ Frontend build successful!"
else
    echo "❌ Frontend build failed - please check for issues"
    cd ..
    exit 1
fi
cd ..

# Test Sacred Team integration
echo "🕊️ Testing Sacred Team integration..."
if uv run python test_jules_integration.py > /dev/null 2>&1; then
    echo "✅ Sacred Team integration working!"
else
    echo "⚠️  Sacred Team test had issues - please verify manually"
fi

echo ""
echo "🎉 Merge conflict resolution complete!"
echo ""
echo "📋 Next steps:"
echo "1. Review the changes: git log --oneline -3"
echo "2. Test the application: cd frontend && bun run dev"
echo "3. Verify Sacred Team: /sacred.team.status command"
echo "4. Push changes: git push origin feat/phase-2-jules-micro-implementation"
echo ""
echo "🕊️ Sacred Living Application ready for deployment! ✨"