.PHONY: help install validate validate-skill-design validate-skill-design-changed generate generate-catalog generate-marketplace generate-plugins generate-readme verify-generated serve clean test test-full check-uv

help:
	@echo "agentic-collections Documentation Generator"
	@echo ""
	@echo "Available targets:"
	@echo "  install                       - Install Python dependencies (requires uv)"
	@echo "  validate                      - Validate pack structure (plugin.json, .mcp.json, frontmatter)"
	@echo "  validate-skill-design         - Validate all skills (use PACK=rh-sre for a specific pack)"
	@echo "  validate-skill-design-changed - Validate only changed skills (staged + unstaged, for local dev)"
	@echo "  generate-catalog              - Generate marketplace, plugins, README from collection.yaml"
	@echo "  generate-marketplace          - Generate .claude-plugin and .cursor-plugin marketplace.json"
	@echo "  generate-plugins              - Generate plugin.json for each pack"
	@echo "  generate-readme               - Generate README.md for each pack"
	@echo "  generate                      - Generate catalog + docs/data.json"
	@echo "  verify-generated              - Verify committed files match generated (for CI)"
	@echo "  serve       - Start local server on http://localhost:8000"
	@echo "  test        - Quick test (validate + generate + verify)"
	@echo "  test-full   - Full test suite (test + serve with browser open)"
	@echo "  clean       - Remove generated files"
	@echo "  update      - Full update (validate + generate)"
	@echo ""
	@echo "Requirements:"
	@echo "  uv - Install with: curl -LsSf https://astral.sh/uv/install.sh | sh"

check-uv:
	@command -v uv >/dev/null 2>&1 || { \
		echo "Error: uv is not installed"; \
		echo ""; \
		echo "Install uv with:"; \
		echo "  curl -LsSf https://astral.sh/uv/install.sh | sh"; \
		echo ""; \
		echo "Or visit: https://github.com/astral-sh/uv"; \
		exit 1; \
	}

install: check-uv
	@echo "Installing Python dependencies with uv..."
	@uv sync
	@echo "Dependencies installed in isolated environment!"

validate: check-uv
	@echo "Validating agentic collection structure..."
	@uv run python scripts/validate_structure.py
	@echo "✓ Validation passed!"

validate-skill-design: check-uv
	@uv run python scripts/validate_skill_design.py $(if $(PACK),$(PACK))

validate-skill-design-changed: check-uv
	@VALIDATE_INCLUDE_UNCOMMITTED=1 ./scripts/ci-validate-changed-skills.sh

generate-catalog: check-uv
	@echo "Generating catalog (marketplace, plugins, README, collection.json)..."
	@uv run python scripts/generate_marketplace.py
	@uv run python scripts/generate_plugins.py
	@uv run python scripts/generate_collection_json.py
	@uv run python scripts/generate_readme.py
	@echo "✓ Catalog generated!"

generate-marketplace: check-uv
	@uv run python scripts/generate_marketplace.py

generate-plugins: check-uv
	@uv run python scripts/generate_plugins.py

generate-readme: check-uv
	@uv run python scripts/generate_readme.py

generate: check-uv generate-catalog
	@echo "Generating documentation..."
	@uv run python scripts/build_website.py
	@echo "✓ Documentation generated in docs/"

verify-generated: check-uv
	@echo "Verifying generated files match committed..."
	@make generate
	@git diff --exit-code .claude-plugin/ .cursor-plugin/ docs/collections/ docs/data.json \
	  rh-sre/.claude-plugin/plugin.json rh-sre/.cursor-plugin/plugin.json rh-sre/README.md rh-sre/collection.json \
	  rh-developer/.claude-plugin/plugin.json rh-developer/.cursor-plugin/plugin.json rh-developer/README.md rh-developer/collection.json \
	  ocp-admin/.claude-plugin/plugin.json ocp-admin/.cursor-plugin/plugin.json ocp-admin/README.md ocp-admin/collection.json \
	  rh-virt/.claude-plugin/plugin.json rh-virt/.cursor-plugin/plugin.json rh-virt/README.md rh-virt/collection.json \
	  rh-ai-engineer/.claude-plugin/plugin.json rh-ai-engineer/.cursor-plugin/plugin.json rh-ai-engineer/README.md rh-ai-engineer/collection.json \
	  rh-automation/.claude-plugin/plugin.json rh-automation/.cursor-plugin/plugin.json rh-automation/README.md rh-automation/collection.json \
	  rh-support-engineer/.claude-plugin/plugin.json rh-support-engineer/.cursor-plugin/plugin.json rh-support-engineer/README.md rh-support-engineer/collection.json \
	  && echo "✓ Generated files match committed" \
	  || (echo "Error: Generated files differ. Run 'make generate' and commit."; exit 1)

serve: check-uv
	@echo "Starting local server on http://localhost:8000"
	@echo "Press Ctrl+C to stop the server"
	@cd docs && uv run python -m http.server 8000

clean:
	@echo "Cleaning generated files..."
	@rm -f docs/data.json
	@echo "✓ Cleaned!"

test: validate generate
	@echo ""
	@echo "Running verification checks..."
	@./scripts/test_local.sh
	@echo ""
	@echo "✓ All tests passed!"
	@echo ""
	@echo "To view the site locally, run: make serve"

test-full: test
	@echo ""
	@echo "Opening browser and starting server..."
	@(sleep 2 && open http://localhost:8000) &
	@make serve

update: validate generate
	@echo "✓ Documentation updated successfully!"
