#!/usr/bin/env python3
"""
Generate static HTML collection pages with tabbed view.

Creates docs/collections/{id}.html for each pack with collection.yaml.
Tabs: Overview, Skills, Resources, Agents.
"""

import json
import re
import sys
from pathlib import Path
from typing import Any, Dict, List

import markdown
import yaml
from jinja2 import Environment, FileSystemLoader

REPO_ROOT = Path(__file__).resolve().parent.parent


def load_collection(pack_dir: str) -> Dict[str, Any] | None:
    """Load collection.yaml for a pack."""
    coll_path = REPO_ROOT / pack_dir / "collection.yaml"
    if not coll_path.exists():
        return None
    with open(coll_path, encoding="utf-8") as f:
        return yaml.safe_load(f)


def discover_collections() -> list[tuple[str, Dict[str, Any]]]:
    """Find all packs with collection.yaml."""
    result = []
    for item in sorted(REPO_ROOT.iterdir()):
        if not item.is_dir() or item.name.startswith("."):
            continue
        data = load_collection(item.name)
        if data:
            result.append((item.name, data))
    return result


def parse_docs(pack_dir: str) -> List[Dict[str, Any]]:
    """Parse documentation files from pack docs/."""
    docs = []
    docs_dir = REPO_ROOT / pack_dir / "docs"
    if not docs_dir.exists():
        return docs
    EXCLUDE = {"README.md", "INDEX.md", "SOURCES.md"}
    for doc_file in docs_dir.rglob("*.md"):
        if doc_file.name in EXCLUDE or ".ai-index" in doc_file.parts:
            continue
        try:
            content = doc_file.read_text(encoding="utf-8")
            match = re.match(r"^---\s*\n(.*?)\n---\s*\n", content, re.DOTALL)
            title = doc_file.stem.replace("-", " ").title()
            if match:
                fm = yaml.safe_load(match.group(1)) or {}
                title = fm.get("title", title)
            rel = str(doc_file.relative_to(REPO_ROOT / pack_dir))
            docs.append({"title": title, "file_path": rel})
        except Exception:
            pass
    return sorted(docs, key=lambda d: d["title"])


def parse_mcp_servers(pack_dir: str) -> List[Dict[str, Any]]:
    """Parse MCP servers from pack .mcp.json."""
    mcp_file = REPO_ROOT / pack_dir / ".mcp.json"
    if not mcp_file.exists():
        return []
    try:
        with open(mcp_file, encoding="utf-8") as f:
            config = json.load(f)
        servers = []
        for name, cfg in config.get("mcpServers", {}).items():
            servers.append({
                "name": name,
                "description": cfg.get("description", ""),
                "type": cfg.get("type", "command"),
            })
        return servers
    except Exception:
        return []


def md_to_html(text: str) -> str:
    """Convert markdown to HTML."""
    if not text or not str(text).strip():
        return ""
    md = markdown.Markdown(extensions=["fenced_code", "tables", "nl2br"])
    return md.convert(str(text))


def _split_deploy_into_sections(deploy: str) -> tuple[str, list[tuple[str, str]]]:
    """Split deploy_and_use into pre-install content and install sections.
    Returns (pre_content, [(platform_name, content), ...]).
    """
    install_pattern = re.compile(
        r"### Installation \((Claude Code|Cursor|Open Code)\)\s*\n(.*?)(?=### Installation \(|\Z)",
        re.DOTALL,
    )
    matches = install_pattern.findall(deploy)
    if not matches:
        return deploy.strip(), []
    pre_end = deploy.find("### Installation (")
    pre_content = deploy[:pre_end].strip() if pre_end > 0 else deploy.strip()
    return pre_content, [(platform, content.strip()) for platform, content in matches]


def build_overview_html(data: Dict[str, Any]) -> str:
    """Build Overview tab: Overview, Quick Start, Security Model, License."""
    parts = []
    # Overview
    summary = data.get("summary", "")
    if summary:
        parts.append("<h2>Overview</h2>")
        parts.append(md_to_html(summary))
    # Quick Start
    deploy = data.get("deploy_and_use", "")
    if deploy:
        parts.append("<h2>Quick Start</h2>")
        pre_content, install_sections = _split_deploy_into_sections(deploy)
        if pre_content:
            parts.append(md_to_html(pre_content))
        if install_sections:
            parts.append('<div class="install-accordion">')
            for i, (platform, content) in enumerate(install_sections):
                open_attr = " open" if i == 0 else ""
                content_html = md_to_html(content)
                parts.append(f'<details class="install-accordion-item"{open_attr}>')
                parts.append(f'<summary class="install-accordion-header">Installation ({platform})</summary>')
                parts.append(f'<div class="install-accordion-body">{content_html}</div>')
                parts.append("</details>")
            parts.append("</div>")
    # Security Model
    security = data.get("security_model", "")
    if security:
        parts.append("<h2>Security Model</h2>")
        parts.append(md_to_html(security))
    # License
    legal = data.get("legal_resources", {})
    license_text = data.get("license", "Apache 2.0")
    if legal and legal.get("license_agreement_url"):
        parts.append("<h2>License</h2>")
        parts.append(f'<p><a href="{legal["license_agreement_url"]}">{license_text}</a></p>')
    else:
        parts.append("<h2>License</h2>")
        parts.append(f"<p>{license_text}</p>")
    return "\n".join(parts) if parts else "<p>No overview content.</p>"


def build_skills_html(data: Dict[str, Any]) -> str:
    """Build Skills tab: Skills, Orchestration Skill, Skills Decision Guide."""
    parts = []
    contents = data.get("contents", {})
    # Skills
    desc = contents.get("description", "")
    skills = contents.get("skills", [])
    if desc:
        parts.append("<h2>Skills</h2>")
        parts.append(md_to_html(desc))
    if skills:
        parts.append("<ol class=\"skill-list\">")
        for s in skills:
            name = s.get("name", "")
            desc_s = s.get("description", "")
            summary = md_to_html(s.get("summary_markdown", ""))
            parts.append(f"<li><strong>/{name}</strong> - {desc_s}")
            if summary:
                parts.append(f"<div class=\"skill-summary\">{summary}</div>")
            parts.append("</li>")
        parts.append("</ol>")
    # Orchestration Skills
    orch = contents.get("orchestration_skills", [])
    if orch:
        label = "Orchestration Skill" if len(orch) == 1 else "Orchestration Skills"
        parts.append(f"<h2>{label}</h2>")
        parts.append("<ol class=\"skill-list\">")
        for s in orch:
            name = s.get("name", "")
            desc_s = s.get("description", "")
            summary = md_to_html(s.get("summary_markdown", ""))
            parts.append(f"<li><strong>/{name}</strong> - {desc_s}")
            if summary:
                parts.append(f"<div class=\"skill-summary\">{summary}</div>")
            parts.append("</li>")
        parts.append("</ol>")
    # Skills Decision Guide
    guide = contents.get("skills_decision_guide", [])
    if guide:
        parts.append("<h2>Skills Decision Guide</h2>")
        rows = []
        for d in guide:
            req = d.get("user_request", "")
            skill = d.get("skill_to_use", "")
            skill_display = f"/{skill}" if skill and not skill.startswith("/") else skill
            reason = d.get("reason", "")
            rows.append(f"<tr><td>{req}</td><td><code>{skill_display}</code></td><td>{reason}</td></tr>")
        parts.append(
            '<table><thead><tr><th>User request</th><th>Skill to use</th><th>Reason</th></tr></thead><tbody>'
            + "".join(rows)
            + "</tbody></table>"
        )
    return "\n".join(parts) if parts else "<p>No skills content.</p>"


def build_resources_html(data: Dict[str, Any], docs: List[Dict[str, Any]], pack_dir: str) -> str:
    """Build Resources tab: Documentation, References."""
    parts = []
    base_url = "https://github.com/RHEcosystemAppEng/agentic-collections/blob/main"
    # Documentation
    if docs:
        parts.append("<h2>Documentation</h2>")
        parts.append("<ul>")
        for d in docs:
            url = f"{base_url}/{pack_dir}/{d['file_path']}"
            parts.append(f'<li><a href="{url}" target="_blank" rel="noopener">{d["title"]}</a></li>')
        parts.append("</ul>")
    # References
    resources = data.get("resources", [])
    if resources:
        parts.append("<h2>References</h2>")
        parts.append("<ul>")
        for r in resources:
            title = r.get("title", "")
            url = r.get("url", "#")
            desc = r.get("description", "")
            extra = f" - {desc}" if desc else ""
            parts.append(f'<li><a href="{url}" target="_blank" rel="noopener">{title}</a>{extra}</li>')
        parts.append("</ul>")
    return "\n".join(parts) if parts else "<p>No resources.</p>"


def _escape_html(s: str) -> str:
    """Escape HTML special characters."""
    return (
        str(s)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def build_agents_html(
    data: Dict[str, Any],
    mcp_servers: List[Dict[str, Any]],
    mcp_custom: Dict[str, Any],
    pack_dir: str,
) -> str:
    """Build Agents tab: MCP Server Integrations, Sample Workflows."""
    parts = []
    # MCP Server Integrations - use card layout with link to open popup on main catalog
    if mcp_servers:
        parts.append("<h2>MCP Server Integrations</h2>")
        parts.append('<div class="grid collection-mcp-grid">')
        for srv in mcp_servers:
            name = srv.get("name", "")
            pack = srv.get("pack", pack_dir)
            custom = mcp_custom.get(name, {})
            title = srv.get("title") or custom.get("title", name)
            desc = srv.get("description") or custom.get("description", "")
            icon = srv.get("icon", "") or custom.get("icon", "")
            owner = srv.get("owner", "Red Hat")
            srv_type = srv.get("type", "command")
            env = srv.get("env", [])
            tools = srv.get("tools", [])
            parts.append(f'<div class="card mcp-card collection-mcp-card" data-mcp-pack="{_escape_html(pack)}" data-mcp-name="{_escape_html(name)}" role="button" tabindex="0">')
            icon_span = f'<span class="card-icon">{_escape_html(icon)}</span>' if icon else ""
            http_span = '<span title="HTTP Remote Server" style="font-size:1rem">🌐</span>' if srv_type == "http" else ""
            parts.append(
                f'<h3 style="display:flex;align-items:center;gap:0.5rem;">'
                f"{icon_span}<span>{_escape_html(title)}</span>{http_span}"
                f"</h3>"
            )
            parts.append(f'<p class="mcp-owner" style="color:var(--text-muted);font-size:0.85rem;margin-top:0.25rem;">By {_escape_html(owner)}</p>')
            parts.append(
                f'<p class="container">{_escape_html("Type: HTTP Remote" if srv_type == "http" else "Type: Container")}</p>'
            )
            env_text = f"{len(env)} env var{'s' if len(env) != 1 else ''}" if env else "No env vars"
            parts.append(f'<div class="env-vars">{env_text}</div>')
            if tools:
                parts.append(f'<div class="env-vars">{len(tools)} tool{"s" if len(tools) != 1 else ""}</div>')
            parts.append("</div>")
        parts.append("</div>")
    # Sample Workflows
    workflows = data.get("sample_workflows", [])
    workflows = [w for w in workflows if w.get("name") != "TODO: Add workflow"]
    if not workflows:
        workflows = [{"name": "See collection.yaml", "workflow": "Add workflows in collection.yaml."}]
    if workflows:
        parts.append("<h2>Sample Workflows</h2>")
        for w in workflows:
            parts.append(f"<h3>{w.get('name', '')}</h3>")
            parts.append(md_to_html(w.get("workflow", "")))
    return "\n".join(parts) if parts else "<p>No agents content.</p>"


def load_mcp_custom() -> Dict[str, Any]:
    """Load docs/mcp.json for titles and descriptions."""
    path = REPO_ROOT / "docs" / "mcp.json"
    if not path.exists():
        return {}
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def main(pack_data: List[Dict[str, Any]] | None = None, mcp_data: List[Dict[str, Any]] | None = None) -> int:
    collections = discover_collections()
    if not collections:
        print("No collection.yaml files found.")
        return 1

    pack_by_name = {p["name"]: p for p in (pack_data or [])}
    mcp_by_pack: Dict[str, List[Dict]] = {}
    if mcp_data:
        for srv in mcp_data:
            pack = srv.get("pack", "")
            mcp_by_pack.setdefault(pack, []).append(srv)

    mcp_custom = load_mcp_custom()
    env = Environment(loader=FileSystemLoader(str(REPO_ROOT / "catalog")))
    template = env.get_template("collection_page.html.j2")
    collections_dir = REPO_ROOT / "docs" / "collections"
    collections_dir.mkdir(parents=True, exist_ok=True)

    for pack_dir, data in collections:
        pack_info = pack_by_name.get(pack_dir, {})
        docs = pack_info.get("docs") or parse_docs(pack_dir)
        mcp_servers = mcp_by_pack.get(pack_dir) or [
            {"name": s["name"], "description": s.get("description", "")}
            for s in parse_mcp_servers(pack_dir)
        ]

        overview_html = build_overview_html(data)
        skills_html = build_skills_html(data)
        resources_html = build_resources_html(data, docs, pack_dir)
        agents_html = build_agents_html(data, mcp_servers, mcp_custom, pack_dir)

        collection_id = data.get("id", pack_dir)
        title = data.get("name", pack_dir)
        subtitle = (data.get("description", "") or "")[:120]

        page = template.render(
            title=title,
            subtitle=subtitle,
            overview_html=overview_html,
            skills_html=skills_html,
            resources_html=resources_html,
            agents_html=agents_html,
        )
        out_path = collections_dir / f"{collection_id}.html"
        out_path.write_text(page, encoding="utf-8")
        print(f"Generated docs/collections/{collection_id}.html")

    print(f"Generated {len(collections)} collection pages")
    return 0


if __name__ == "__main__":
    sys.exit(main())
