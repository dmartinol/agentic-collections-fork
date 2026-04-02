### Multi-cluster authentication

For consolidated **cluster-report** across many contexts, set up kubeconfig and RBAC using the pack guide: [docs/multi-cluster-auth.md](docs/multi-cluster-auth.md).

### Further documentation

- **[Documentation index](docs/INDEX.md)** — navigation for networking, host requirements, troubleshooting, and static networking.
- **Troubleshooting** — see [docs/troubleshooting.md](docs/troubleshooting.md) for Assisted Installer and cluster-specific issues.

### Configuration notes

- Ensure `OFFLINE_TOKEN` is exported before Assisted Installer or OCM MCP calls.
- Point `KUBECONFIG` at a merged kubeconfig when reporting across fleets; verify with `oc config get-contexts`.
