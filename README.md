# ITera Agent Suite

> **20 agentes especializados para revisión de código, seguridad, DevOps y buenas prácticas en la nube.**
> Compatibles con Kiro IDE y Claude (web/API/Projects).

**Creado por**: Stiven Avila | **Organización**: ITera
**Versión**: 1.0.0 | **Fecha**: 2026-08-21

---

## Catálogo de Agentes

### Seguridad

| # | Agente | Descripción | Kiro Path |
|---|--------|-------------|-----------|
| 1 | **Cloud Security** | Seguridad en AWS/Azure/GCP: IAM, red, datos, compliance | `.kiro/agents/cloud-security/` |
| 2 | **SAST (Seguridad Estática)** | Análisis estático de código: data flow, taint tracking, CWE | `.kiro/agents/sast-security/` |
| 3 | **DAST (Seguridad Dinámica)** | Testing dinámico: headers, sesiones, input fuzzing, APIs | `.kiro/agents/dast-security/` |
| 4 | **Penetration Testing** | Red team: cadenas de ataque, MITRE ATT&CK, CVSS, PoC | `.kiro/agents/pentest-security/` |
| 5 | **Auditoría de Seguridad** | Auditoría contra frameworks: ISO 27001, SOC 2, PCI DSS, NIST | `.kiro/agents/security-audit/` |

### Buenas Prácticas

| # | Agente | Descripción | Kiro Path |
|---|--------|-------------|-----------|
| 6 | **AWS Best Practices** | Well-Architected Framework: 6 pilares, servicios, patrones | `.kiro/agents/aws-best-practices/` |
| 7 | **Mínimo Privilegio** | IAM least privilege: AWS, K8s RBAC, application-level authz | `.kiro/agents/least-privilege/` |
| 8 | **Desarrollo Seguro** | Secure coding: OWASP, crypto, input validation, CI/CD gates | `.kiro/agents/secure-development/` |
| 9 | **Buenas Prácticas de Desarrollo** | Clean code, SOLID, patrones, testing, arquitectura | `.kiro/agents/dev-best-practices/` |

### Revisión

| # | Agente | Descripción | Kiro Path |
|---|--------|-------------|-----------|
| 10 | **Code Review** | Revisión de código: correctness, security, performance, design | `.kiro/agents/code-reviewer/` |
| 11 | **IaC Review** | Revisión de Terraform, CloudFormation, Helm, Ansible | `.kiro/agents/iac-reviewer/` |
| 12 | **DevOps Review** | CI/CD, DORA metrics, SRE, observabilidad, deployment | `.kiro/agents/devops-reviewer/` |
| 13 | **DevSecOps Review** | Security in SDLC, supply chain, gates, SLSA, compliance-as-code | `.kiro/agents/devsecops-reviewer/` |

### Contenedores & Kubernetes

| # | Agente | Descripción | Kiro Path |
|---|--------|-------------|-----------|
| 14 | **Container Review** | Revisión de Dockerfiles, imágenes, runtime security | `.kiro/agents/container-reviewer/` |
| 15 | **Container Best Practices** | Diseño de contenedores: 12-factor, networking, storage, registries | `.kiro/agents/container-best-practices/` |
| 16 | **Kubernetes Best Practices** | Workloads, resources, networking, storage, observability K8s | `.kiro/agents/kubernetes-best-practices/` |
| 17 | **YAML Best Practices** | YAML correcto: pitfalls, K8s manifests, CI/CD, Helm values | `.kiro/agents/yaml-best-practices/` |
| 18 | **Kubernetes Security Breaches** | Vectores de ataque K8s, kill chains, detección, respuesta | `.kiro/agents/kubernetes-security/` |

### Documentación & GenAI

| # | Agente | Descripción | Kiro Path |
|---|--------|-------------|-----------|
| 19 | **Development Documentation** | Documentación técnica: Diátaxis, ADR, API docs, README, changelog | `.kiro/agents/dev-documentation/` |
| 20 | **GenAI AWS Best Practices** | Bedrock, RAG, agents, guardrails, cost optimization, responsible AI | `.kiro/agents/genai-aws-practices/` |

---

## Uso en Kiro IDE

### Activación

Los agentes se detectan automáticamente al abrir este workspace en Kiro. Selecciónalos desde el chat.

### Ejemplos por categoría

**Seguridad Cloud:**
```
Analiza la seguridad de mi cuenta AWS basándote en estos archivos de Terraform: #Folder infra/
```

**SAST:**
```
Realiza un análisis de seguridad estática del #Folder src/api/ buscando injection y auth issues
```

**Penetration Testing:**
```
Construye cadenas de ataque realistas contra este endpoint: #File src/controllers/auth.ts
```

**Code Review:**
```
Revisa este PR con foco en correctness y performance: #Git Diff
```

**IaC Review:**
```
Revisa la seguridad y buenas prácticas de #Folder terraform/modules/
```

**Kubernetes:**
```
Analiza las brechas de seguridad en estos manifiestos: #Folder k8s/production/
```

**GenAI:**
```
Revisa la arquitectura RAG que estamos implementando con Bedrock: #File docs/architecture/genai.md
```

---

## Uso en Claude

### Opción 1: Claude Projects (recomendado)

1. Crear un Project en [claude.ai](https://claude.ai)
2. Copiar el contenido del `agent.md` correspondiente como **Project Instructions**
3. Subir archivos de código como **Knowledge**
4. Iniciar conversación

### Opción 2: Claude API

```python
import anthropic

# Leer el system prompt del agente
with open(".kiro/agents/cloud-security/agent.md") as f:
    system_prompt = f.read()

client = anthropic.Anthropic()
message = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=8096,
    system=system_prompt,
    messages=[
        {"role": "user", "content": "Analiza esta política IAM:\n\n```json\n{...}\n```"}
    ]
)
print(message.content[0].text)
```

### Opción 3: Script batch para múltiples agentes

```bash
#!/bin/bash
# Ejecutar análisis con múltiples agentes sobre el mismo código
AGENTS=("sast-security" "code-reviewer" "secure-development")
CODE_FILE="src/auth/login.ts"

for agent in "${AGENTS[@]}"; do
    echo "=== Running: $agent ==="
    # Usar tu herramienta CLI preferida para invocar Claude
    # con el system prompt del agente y el archivo como input
done
```

---

## Estructura del Proyecto

```
.
├── .kiro/
│   └── agents/                          # Agentes nativos para Kiro IDE
│       ├── aws-best-practices/agent.md
│       ├── cloud-security/agent.md
│       ├── code-reviewer/agent.md
│       ├── container-best-practices/agent.md
│       ├── container-reviewer/agent.md
│       ├── dast-security/agent.md
│       ├── dev-best-practices/agent.md
│       ├── dev-documentation/agent.md
│       ├── devops-reviewer/agent.md
│       ├── devsecops-reviewer/agent.md
│       ├── genai-aws-practices/agent.md
│       ├── iac-reviewer/agent.md
│       ├── kubernetes-best-practices/agent.md
│       ├── kubernetes-security/agent.md
│       ├── least-privilege/agent.md
│       ├── pentest-security/agent.md
│       ├── sast-security/agent.md
│       ├── secure-development/agent.md
│       ├── security-audit/agent.md
│       └── yaml-best-practices/agent.md
├── claude/                              # System prompts legacy (Claude web/API)
│   ├── code-reviewer.md
│   └── security-tester.md
└── README.md
```

---

## Combinaciones Recomendadas

Para un análisis completo, usa múltiples agentes en secuencia:

| Objetivo | Agentes (en orden) |
|----------|-------------------|
| **Security review completo** | SAST → DAST → Cloud Security → Pentest |
| **Code review riguroso** | Code Review → Secure Development → Dev Best Practices |
| **Audit de compliance** | Security Audit → Cloud Security → Least Privilege |
| **Revisión de infraestructura** | IaC Review → AWS Best Practices → Cloud Security |
| **Review de K8s production** | K8s Best Practices → K8s Security → Container Review → YAML |
| **Pipeline DevSecOps** | DevOps Review → DevSecOps Review → Container Review |
| **Proyecto GenAI** | GenAI AWS → Cloud Security → Secure Development |

---

## Frameworks y Estándares de Referencia

Los agentes están alineados con:

- **OWASP** Top 10, ASVS, Testing Guide, Secure Coding Practices
- **MITRE ATT&CK** para Containers y Enterprise
- **CIS Benchmarks** AWS, Kubernetes, Docker
- **NIST** CSF 2.0, SP 800-218 (SSDF), SP 800-53
- **ISO 27001:2022** Annex A controls
- **PCI DSS v4.0**
- **SOC 2** Trust Service Criteria
- **AWS Well-Architected** Framework (6 pilares)
- **SLSA** Supply-chain Levels for Software Artifacts
- **DORA** Metrics (DevOps Research and Assessment)
- **12-Factor App** Methodology
- **CWE** Common Weakness Enumeration

---

## Licencia

Uso interno — ITera | Stiven Avila

Todos los agentes están firmados digitalmente por ITera y su creador Stiven Avila.
Cada agente incluye la firma: `*Firmado digitalmente: ITera | Stiven Avila | vX.X.X*`
