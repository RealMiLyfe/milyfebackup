# MiLyfe Security Audit Checklist

**Standard:** Defense-in-depth. Default deny. Worst-case-first.  
**Rule:** Special data (health, kids, biometrics) needs a real legal basis.

---

## Application Security

### Authentication
- [ ] WebAuthn/passkeys as primary authentication
- [ ] No password-based login (passkey or recovery friends only)
- [ ] Session tokens are httpOnly, secure, sameSite
- [ ] Session expiry: 7 days private device, 30 min shared device
- [ ] Panic freeze invalidates all sessions immediately
- [ ] Rate limiting on all authentication endpoints
- [ ] No account enumeration (same response for valid/invalid)

### Authorization (MiScope)
- [ ] Every API endpoint checks permissions
- [ ] Child safety rules cannot be weakened by any role
- [ ] Emergency exceptions are logged and time-limited
- [ ] No role has universal access
- [ ] Keeper cannot access private messages, balances, or location
- [ ] Recovery friends cannot access any private data
- [ ] Role expiry enforced automatically

### Data Protection
- [ ] All data encrypted at rest (device) and in transit (TLS 1.3)
- [ ] End-to-end encryption for messages (Matrix protocol)
- [ ] No server-side access to message content
- [ ] Location data: never stored, never transmitted without explicit consent
- [ ] Health/child/legal data: isolated storage, additional encryption layer
- [ ] Export generates complete data package (GDPR-style)
- [ ] Deletion is real deletion (not soft-delete for sensitive data)

### Money (Pocket/Ledger)
- [ ] Double-spend protection via reservation system
- [ ] Offline conflicts flagged for human review (never auto-resolved)
- [ ] Practice/Live boundary enforced at service layer
- [ ] Freeze actually stops all movement
- [ ] No value created by the app (UBI schedule is deterministic)
- [ ] Tax export matches actual transaction history

### Supply Chain
- [ ] All dependencies OSI-licensed (MiCompat gate)
- [ ] SBOM generated for every release
- [ ] No dependency with known critical vulnerabilities ships
- [ ] Dependencies pinned to exact versions
- [ ] Sigstore signing on releases
- [ ] Reproducible builds where possible

---

## Infrastructure Security

### Network
- [ ] All services behind network policies (K3s)
- [ ] No public-facing admin endpoints
- [ ] Rate limiting on all external endpoints
- [ ] DDoS mitigation configured
- [ ] DNS over HTTPS

### Secrets Management
- [ ] OpenBao (not HashiCorp Vault) for all secrets
- [ ] No secrets in environment variables, code, or git
- [ ] Key rotation automated
- [ ] Place-level keys have N-of-M recovery
- [ ] Backup keys stored geographically separated

### Monitoring
- [ ] Security events logged (not private content)
- [ ] Alerting on: failed auth bursts, admin access, key rotation due
- [ ] No analytics that identifies individuals
- [ ] Warrant canary maintained
- [ ] Incident response plan documented and tested

---

## Threat Model

| Threat | Mitigation |
|---|---|
| Stolen phone | Panic freeze + recovery friends + 3-day delay |
| Abusive partner | Leave-now + hidden location + frozen jars + device removal |
| Sybil UBI farming | Personhood verification (3 intros or hello-day) |
| Captured vote | Private ballot + no live tallies + independent audit |
| Helper gone wrong | Rails enforced + labeled always + fireable + audit |
| Supply chain attack | MiCompat gate + SBOM + pinned versions + scanning |
| Lawful process | Hold little data server-side + client-side encryption |
| Place-level failure | Multi-keeper key backup + N-of-M recovery + fork allowed |
| Offline double-spend | Reservation system + human review on conflict |
| Network surveillance | E2E encryption + mesh fallback + DTN |

---

## Penetration Testing Scope

### In Scope
- Web application (all 54 screens)
- API layer (when connected to real backends)
- Authentication and session management
- Authorization boundary testing (child rules, keeper limits)
- Offline conflict resolution logic
- Recovery flow (can someone steal an identity?)
- Shared device isolation
- Export/leave (does deletion actually delete?)

### Out of Scope
- Physical device security (handled by OS/hardware)
- Third-party services (Matrix Synapse, Ollama — test their interfaces only)
- Social engineering (but document risks)
- Network infrastructure (test the app, not the cloud)

---

## Compliance Considerations

| Jurisdiction | Requirement | Status |
|---|---|---|
| US (FL) | No money transmission without MSB license | Practice mode only; live requires counsel |
| US (FL) | COPPA for children under 13 | Youth mode + guardian consent |
| EU | GDPR data subject rights | Export + deletion + consent receipts |
| EU | MiCA for crypto-assets (if live) | Counsel required before live |
| Global | Accessibility (various) | WCAG 2.2 AA minimum |
| US (FL) | Florida Information Protection Act | Encrypted storage + breach notification plan |
