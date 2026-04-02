#!/usr/bin/env python3
"""
Build the documentation website by combining pack data and MCP data into data.json.
"""

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict

import yaml

# Import our data generators
from generate_pack_data import generate_pack_data
from generate_mcp_data import generate_mcp_data
from generate_collection_pages import main as generate_collection_pages
from generation_notice import write_text_or_check


def load_marketplace_icons() -> Dict[str, str]:
    """
    Load collection icon mappings from catalog/marketplace.yaml.

    Returns:
        Dictionary mapping collection id to icon
    """
    marketplace_file = Path('catalog/marketplace.yaml')
    if not marketplace_file.exists():
        print("⚠️  Warning: catalog/marketplace.yaml not found, icons will not be loaded")
        return {}
    try:
        with open(marketplace_file, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
        return {k: v.get('icon', '') for k, v in (data.get('collections') or {}).items()}
    except Exception as e:
        print(f"⚠️  Warning: Failed to load catalog/marketplace.yaml: {e}")
        return {}


def build_website(check: bool = False) -> int:
    """
    Generate the complete website data file, or verify it is up to date.
    """
    if not check:
        print("🔨 Building documentation website...")
        print()

    # Load collection icons from marketplace
    if not check:
        print("🎨 Loading collection icons...")
    collection_icons = load_marketplace_icons()
    if not check:
        print()

    # Generate pack data
    if not check:
        print("📦 Parsing agentic collections...")
    pack_data = generate_pack_data()

    # Merge collection icons and sort alphabetically by collection name
    for pack in pack_data:
        pack['icon'] = collection_icons.get(pack['name'], '')
    pack_data = sorted(pack_data, key=lambda p: p['name'])

    if not check:
        print()

    # Generate MCP server data (needed for collection pages)
    if not check:
        print("🔌 Parsing MCP servers...")
    mcp_data = generate_mcp_data()

    if not check:
        print()

    # Generate (or verify) collection pages
    if not check:
        print("📄 Generating collection pages...")
    pages_result = generate_collection_pages(pack_data=pack_data, mcp_data=mcp_data, check=check)

    if not check:
        print()

    # Combine into final output (note: generated_at is omitted in check mode
    # because the timestamp would differ every run)
    output = {
        'repository': {
            'name': 'agentic-collections',
            'owner': 'Red Hat Ecosystem Engineering',
            'description': 'Agentic collections for Red Hat platforms and products',
            'url': 'https://github.com/RHEcosystemAppEng/agentic-collections'
        },
        'packs': pack_data,
        'mcp_servers': mcp_data,
        'generated_at': datetime.now(timezone.utc).isoformat()
    }

    docs_dir = Path('docs')
    docs_dir.mkdir(exist_ok=True)
    output_file = docs_dir / 'data.json'

    if check:
        # For data.json, compare everything except generated_at (it changes every run)
        if output_file.exists():
            try:
                existing = json.loads(output_file.read_text(encoding='utf-8'))
                existing.pop('generated_at', None)
                candidate = dict(output)
                candidate.pop('generated_at', None)
                if existing != candidate:
                    print(f"  OUT OF SYNC: {output_file}")
                    data_json_ok = False
                else:
                    data_json_ok = True
            except Exception:
                print(f"  MISSING or UNREADABLE: {output_file}")
                data_json_ok = False
        else:
            print(f"  MISSING: {output_file}")
            data_json_ok = False

        if pages_result != 0 or not data_json_ok:
            print("Website files are out of sync. Run 'make generate'.")
            return 1
        print("✓ Website files (data.json + collection pages) match sources")
        return 0

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    print(f"✅ Generated {output_file}")
    print()
    print("📊 Summary:")
    print(f"   • {len(pack_data)} agentic collections")
    total_skills = sum(len(p['skills']) for p in pack_data)
    total_agents = sum(len(p['agents']) for p in pack_data)
    print(f"   • {total_skills} skills")
    print(f"   • {total_agents} agents")
    print(f"   • {len(mcp_data)} MCP servers")
    print()

    return 0


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Verify files match sources without writing")
    args = parser.parse_args()
    sys.exit(build_website(check=args.check))
