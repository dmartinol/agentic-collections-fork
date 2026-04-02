#!/usr/bin/env bash
#
# Install pre-commit hooks
#
# Stage 1: gitleaks — scans staged changes for secrets.
# Stage 2: generated-files — verifies that generated files (README.md,
#   collection.json, plugin.json, marketplace.json, docs) are in sync with
#   their sources (collection.yaml, SKILL.md). Uses 'make verify-generated'
#   which runs in --check mode: no files are written, no git operations.
#
# If Stage 2 fails, run 'make generate' locally, stage the updated files,
# and recommit.
#

set -euo pipefail

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo "========================================="
echo "Gitleaks Pre-Commit Hook Installation"
echo "========================================="
echo ""

# Check if we're in a git repository
if [ ! -d ".git" ]; then
    echo -e "${RED}Error: Not a git repository${NC}"
    echo "Run this script from the repository root"
    exit 1
fi

# Check if gitleaks is installed
if ! command -v gitleaks >/dev/null 2>&1; then
    echo -e "${YELLOW}Gitleaks not found.${NC} Installing..."
    echo ""

    # Detect OS and install
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        if command -v brew >/dev/null 2>&1; then
            echo "Installing via Homebrew..."
            brew install gitleaks
        else
            echo -e "${RED}Error: Homebrew not found${NC}"
            echo "Install gitleaks manually: https://github.com/gitleaks/gitleaks#installation"
            exit 1
        fi
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        # Linux
        echo "Downloading gitleaks binary..."
        GITLEAKS_VERSION="8.18.2"
        ARCH=$(uname -m)

        if [ "$ARCH" = "x86_64" ]; then
            ARCH="x64"
        elif [ "$ARCH" = "aarch64" ]; then
            ARCH="arm64"
        fi

        curl -sSfL "https://github.com/gitleaks/gitleaks/releases/download/v${GITLEAKS_VERSION}/gitleaks_${GITLEAKS_VERSION}_linux_${ARCH}.tar.gz" | \
            tar -xz -C /tmp
        sudo mv /tmp/gitleaks /usr/local/bin/
        sudo chmod +x /usr/local/bin/gitleaks
    else
        echo -e "${RED}Error: Unsupported OS${NC}"
        echo "Install gitleaks manually: https://github.com/gitleaks/gitleaks#installation"
        exit 1
    fi
else
    echo -e "${GREEN}✓${NC} Gitleaks already installed: $(gitleaks version)"
fi

echo ""

# Create pre-commit hook
HOOK_FILE=".git/hooks/pre-commit"

# Backup existing hook if present
if [ -f "$HOOK_FILE" ]; then
    BACKUP="${HOOK_FILE}.backup-$(date +%Y%m%d-%H%M%S)"
    echo -e "${YELLOW}Backing up existing hook to: $BACKUP${NC}"
    mv "$HOOK_FILE" "$BACKUP"
fi

# Write pre-commit hook (two stages: gitleaks + generated files)
cat > "$HOOK_FILE" << 'EOF'
#!/usr/bin/env bash
#
# Pre-commit hook
# Stage 1: gitleaks secrets scan
# Stage 2: verify generated files are in sync with sources
#

set -e

# ── Stage 1: Secrets scan ──────────────────────────────────────────────────
if ! gitleaks protect --staged --redact --verbose; then
    echo ""
    echo "========================================="
    echo "COMMIT BLOCKED - Secrets Detected"
    echo "========================================="
    echo ""
    echo "Gitleaks found potential secrets in your staged changes."
    echo ""
    echo "To fix:"
    echo "  1. Remove hardcoded secrets"
    echo "  2. Use environment variables: \${ENV_VAR}"
    echo "  3. Review .gitleaks.toml for allowed patterns"
    echo ""
    echo "To bypass (DANGEROUS - only for test fixtures):"
    echo "  git commit --no-verify"
    echo ""
    echo "For help: See SECURITY.md"
    echo "========================================="
    exit 1
fi

echo "✓ No secrets detected"

# ── Stage 2: Generated files consistency check ─────────────────────────────
if command -v uv >/dev/null 2>&1; then
    echo ""
    echo "Verifying generated files are in sync with sources..."
    if ! make verify-generated; then
        echo ""
        echo "========================================="
        echo "COMMIT BLOCKED - Generated Files Out of Sync"
        echo "========================================="
        echo ""
        echo "One or more generated files differ from what would be produced"
        echo "by 'make generate'. This means either:"
        echo "  • You edited a source file (collection.yaml / SKILL.md) without"
        echo "    regenerating, or"
        echo "  • You manually edited a generated file (README.md, plugin.json,"
        echo "    collection.json, marketplace.json, docs/...)."
        echo ""
        echo "To fix:"
        echo "  make generate"
        echo "  git add <updated files>"
        echo "  git commit"
        echo ""
        echo "To bypass (use only when you are certain):"
        echo "  git commit --no-verify"
        echo "========================================="
        exit 1
    fi
    echo "✓ Generated files are in sync"
else
    echo ""
    echo "Note: 'uv' not found — skipping generated file check."
    echo "Install uv to enable this check: curl -LsSf https://astral.sh/uv/install.sh | sh"
fi

exit 0
EOF

chmod +x "$HOOK_FILE"

echo -e "${GREEN}✓${NC} Pre-commit hook installed: $HOOK_FILE"
echo ""

# Verify configuration exists
if [ ! -f ".gitleaks.toml" ]; then
    echo -e "${YELLOW}Warning: .gitleaks.toml not found${NC}"
    echo "Gitleaks will use default rules only"
else
    echo -e "${GREEN}✓${NC} Configuration found: .gitleaks.toml"
fi

echo ""
echo "========================================="
echo "Installation Complete"
echo "========================================="
echo ""
echo "The hook runs two stages on every commit:"
echo "  Stage 1 — gitleaks: scans staged changes for secrets"
echo "  Stage 2 — verify-generated: ensures generated files match sources"
echo ""
echo "If Stage 2 blocks your commit:"
echo "  make generate"
echo "  git add <updated files>"
echo "  git commit"
echo ""
echo "Manual checks:"
echo "  gitleaks detect --source . --verbose   # secrets"
echo "  make verify-generated                   # generated files"
echo ""
echo "Update hook:"
echo "  Re-run this script: scripts/install-hooks.sh"
echo ""
