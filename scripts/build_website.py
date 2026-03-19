#!/usr/bin/env python3
"""
Build the documentation website by combining pack data and MCP data into data.json.
"""

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


def build_website():
    """
    Generate the complete website data file.
    """
    print("🔨 Building documentation website...")
    print()

    # Load collection icons from marketplace
    print("🎨 Loading collection icons...")
    collection_icons = load_marketplace_icons()
    print()

    # Generate pack data
    print("📦 Parsing agentic collections...")
    pack_data = generate_pack_data()
    
    # Merge collection icons and sort alphabetically by collection name
    for pack in pack_data:
        pack['icon'] = collection_icons.get(pack['name'], '')
    pack_data = sorted(pack_data, key=lambda p: p['name'])
    
    print()

    # Generate MCP server data (needed for collection pages)
    print("🔌 Parsing MCP servers...")
    mcp_data = generate_mcp_data()
    
    print()

    # Generate collection pages (with tabbed view)
    print("📄 Generating collection pages...")
    generate_collection_pages(pack_data=pack_data, mcp_data=mcp_data)
    
    print()

    # Combine into final output
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

    # Ensure docs directory exists
    docs_dir = Path('docs')
    docs_dir.mkdir(exist_ok=True)

    # Write data.json
    output_file = docs_dir / 'data.json'
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
    sys.exit(build_website())
