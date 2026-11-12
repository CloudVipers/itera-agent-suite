# ITera Agent Suite

> **38 agentes especializados para todo el ciclo de desarrollo: requerimientos, arquitectura, construcción, calidad, seguridad, DevOps y operación en la nube — coordinados por un agente orquestador.**
> Compatibles con Kiro IDE y Claude (web/API/Projects).

**Creado por**: Stiven Avila | **Organización**: ITera
**Versión**: 2.0.0 | **Fecha**: 2026-11-12

---

## Catálogo de Agentes

### Orquestación & Requerimientos

| # | Agente | Descripción | Kiro Path |
|---|--------|-------------|-----------|
| 0 | **Agent Orchestrator** | Entiende la solicitud, la divide en tareas, enruta a los agentes correctos y consolida resultados | `.kiro/agents/agent-orchestrator/` |
| 0.1 | **Requirements Analyst** | Entiende y traduce requerimientos (negocio ↔ técnico, ES ↔ EN): historias, Gherkin, NFRs, preguntas abiertas | `.kiro/agents/requirements-analyst/` |

### Seguridad

| # | Agente | Descripción | Kiro Path |
|---|--------|-------------|-----------|
| 1 | **Cloud Security** | Seguridad en AWS/Azure/GCP: IAM, red, datos, compliance | `.kiro/agents/cloud-security/` |
| 2 | **SAST (Seguridad Estática)** | Análisis estático de código: data flow, taint tracking, CWE | `.kiro/agents/sast-security/` |
| 3 | **DAST (Seguridad Dinámica)** | Testing dinámico: headers, sesiones, input fuzzing, APIs | `.kiro/agents/dast-security/` |
| 4 | **Penetration Testing** | Red team: cadenas de ataque, MITRE ATT&CK, CVSS, PoC | `.kiro/agents/pentest-security/` |
| 5 | **Auditoría de Seguridad** | Auditoría contra frameworks: ISO 27001, SOC 2, PCI DSS, NIST | `.kiro/agents/security-audit/` |
| 5.1 | **Security Tester (legacy)** | Testing de seguridad general todo-en-uno; preferir SAST/DAST/Pentest | `.kiro/agents/security-tester/` |

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

### Arquitectura & Diseño

| # | Agente | Descripción | Kiro Path |
|---|--------|-------------|-----------|
| 21 | **Software Architecture** | Estilos de arquitectura, DDD, trade-offs, ADRs, diagramas C4 | `.kiro/agents/software-architect/` |
| 22 | **API Design** | REST, GraphQL, gRPC, eventos: OpenAPI/AsyncAPI, versionado, seguridad de APIs | `.kiro/agents/api-design/` |
| 23 | **Database Engineering** | Modelado SQL/NoSQL, índices, planes de ejecución, migraciones sin downtime | `.kiro/agents/database-engineering/` |
| 24 | **Data Engineering** | Pipelines, lakehouse, streaming, dbt/Airflow/Glue, calidad de datos | `.kiro/agents/data-engineering/` |

### Construcción

| # | Agente | Descripción | Kiro Path |
|---|--------|-------------|-----------|
| 25 | **Frontend Engineering** | React/Next/Vue/Angular, estado, Core Web Vitals, seguridad frontend | `.kiro/agents/frontend-engineering/` |
| 26 | **Mobile Engineering** | iOS, Android, React Native, Flutter, offline-first, OWASP MASVS | `.kiro/agents/mobile-engineering/` |
| 27 | **Refactoring & Modernization** | Código legacy, deuda técnica, upgrades, migración a la nube (7 Rs) | `.kiro/agents/refactoring-modernization/` |

### Calidad

| # | Agente | Descripción | Kiro Path |
|---|--------|-------------|-----------|
| 28 | **Test Automation & QA** | Estrategia de pruebas, unit/integration/contract/E2E, tests inestables | `.kiro/agents/test-automation/` |
| 29 | **Performance Engineering** | Profiling, pruebas de carga, percentiles, caching | `.kiro/agents/performance-engineering/` |
| 30 | **Debugging & Troubleshooting** | Causa raíz de errores, stack traces, "funciona aquí pero no allá" | `.kiro/agents/debugging-troubleshooting/` |
| 31 | **Accessibility (a11y)** | Auditoría y corrección WCAG 2.2 AA, web y móvil | `.kiro/agents/accessibility/` |

### Operación, Entrega & Cumplimiento

| # | Agente | Descripción | Kiro Path |
|---|--------|-------------|-----------|
| 32 | **Observability & SRE** | Logs, métricas, trazas (OpenTelemetry), SLOs, alertas, incidentes | `.kiro/agents/observability-sre/` |
| 33 | **Release Management & Git** | Branching, commits, PRs, SemVer, changelogs, releases, recuperación en Git | `.kiro/agents/release-management/` |
| 34 | **FinOps & Cost Optimization** | Visibilidad de costos, right-sizing, Savings Plans, diseño consciente del costo | `.kiro/agents/finops-cost-optimization/` |
| 35 | **Privacy by Design** | Protección de datos: Ley 1581 (Habeas Data), GDPR, LGPD; consentimiento, derechos, retención | `.kiro/agents/privacy-compliance/` |

### ¿Por dónde empezar?

- **No sabes qué agente usar** → `agent-orchestrator`: arma el plan y coordina a los demás.
- **Tienes un correo, RFP, transcripción o idea suelta** → `requirements-analyst`: lo convierte en requerimientos listos para desarrollo.

---

## Uso en Kiro IDE

### Activación

Cada agente tiene dos archivos en `.kiro/agents/`:

- **`<agente>.json`**: configuración de Kiro (esquema v3): nombre, descripción, herramientas, recursos, permisos y mensaje de bienvenida.
- **`<agente>/agent.md`**: el system prompt, referenciado desde el JSON con `"prompt": "file://./<agente>/agent.md"`.

Kiro detecta los agentes del workspace al abrir este repositorio. Para tenerlos disponibles en cualquier proyecto, cópialos a la carpeta global conservando la estructura (el `prompt` es relativo al JSON):

```bash
mkdir -p ~/.kiro/agents && cp -r .kiro/agents/* ~/.kiro/agents/
```

### Permisos (modo seguro)

Cada agente solo tiene las herramientas y permisos que su función necesita:

| Regla | Comportamiento |
|-------|----------------|
| `fs_write` → `allow` | Escritura libre solo en las carpetas de su área (por ejemplo, `infra/**` para IaC, `tests/**` para QA, `reports/**` para auditorías) |
| `fs_read` → `deny` | Ningún agente lee secretos: `.env`, `~/.aws`, `~/.ssh`, llaves (`*.pem`, `*.key`), `*.tfstate` — salvo `.env.example` |
| `shell` → `allow` | Comandos de solo lectura y análisis de su dominio (`git diff`, `terraform plan`, `kubectl get`, linters, tests, escáneres) |
| `shell` → `ask` | Lo que cambia algo pide confirmación: commits, push, instalar dependencias, `kubectl apply`, pruebas de carga, escaneos activos |
| `shell` → `deny` | Bloqueado siempre: `terraform apply/destroy`, `kubectl delete`, leer Secrets de K8s, `git push --force`, `git reset --hard`, `rm -rf`, `sudo`, borrar recursos de AWS, publicar imágenes o paquetes |
| `subagent` → `allow` | Solo el **Agent Orchestrator**: puede invocar a los otros 37 agentes |

En Kiro un `deny` siempre gana sobre un `allow`. Lo que no coincide con ninguna regla pide aprobación en tiempo de ejecución.

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

**Orquestador:**
```
Necesito llevar a producción esta nueva funcionalidad de pagos. Arma el plan con los agentes necesarios y consolida los hallazgos: #Folder src/payments/
```

**Requerimientos:**
```
Convierte este correo del cliente en historias de usuario con criterios de aceptación en inglés: #File docs/cliente/correo-requerimiento.txt
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
│   └── agents/                          # 38 agentes: <agente>.json (config Kiro) + <agente>/agent.md (prompt)
│       ├── accessibility/agent.md
│       ├── agent-orchestrator/agent.md
│       ├── api-design/agent.md
│       ├── aws-best-practices/agent.md
│       ├── cloud-security/agent.md
│       ├── code-reviewer/agent.md
│       ├── container-best-practices/agent.md
│       ├── container-reviewer/agent.md
│       ├── dast-security/agent.md
│       ├── data-engineering/agent.md
│       ├── database-engineering/agent.md
│       ├── debugging-troubleshooting/agent.md
│       ├── dev-best-practices/agent.md
│       ├── dev-documentation/agent.md
│       ├── devops-reviewer/agent.md
│       ├── devsecops-reviewer/agent.md
│       ├── finops-cost-optimization/agent.md
│       ├── frontend-engineering/agent.md
│       ├── genai-aws-practices/agent.md
│       ├── iac-reviewer/agent.md
│       ├── kubernetes-best-practices/agent.md
│       ├── kubernetes-security/agent.md
│       ├── least-privilege/agent.md
│       ├── mobile-engineering/agent.md
│       ├── observability-sre/agent.md
│       ├── pentest-security/agent.md
│       ├── performance-engineering/agent.md
│       ├── privacy-compliance/agent.md
│       ├── refactoring-modernization/agent.md
│       ├── release-management/agent.md
│       ├── requirements-analyst/agent.md
│       ├── sast-security/agent.md
│       ├── secure-development/agent.md
│       ├── security-audit/agent.md
│       ├── security-tester/agent.md
│       ├── software-architect/agent.md
│       ├── test-automation/agent.md
│       └── yaml-best-practices/agent.md
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
| **Funcionalidad nueva de punta a punta** | Requirements Analyst → Software Architecture → API Design ‖ Database → Frontend ‖ Mobile → Test Automation → Code Review → Release Management |
| **De RFP a plan técnico** | Requirements Analyst → Software Architecture → FinOps → Development Documentation |
| **Listo para producción** | Code Review ‖ SAST ‖ Test Automation → Performance → Observability & SRE → Release Management |
| **Modernización de legacy** | Refactoring & Modernization → Software Architecture → Test Automation → AWS Best Practices → FinOps |
| **Incidente en producción** | Debugging ‖ Observability & SRE → Release Management → Development Documentation |
| **Cumplimiento de datos personales** | Privacy by Design ‖ Security Audit → Cloud Security → Least Privilege |

> `‖` = en paralelo. El **Agent Orchestrator** conoce estas combinaciones y elige la adecuada según la solicitud.

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
- **WCAG 2.2** Web Content Accessibility Guidelines
- **OWASP API Security Top 10** y **OWASP MASVS** (móvil)
- **ISO/IEC 25010** calidad de software (requerimientos no funcionales)
- **FinOps Framework** (FinOps Foundation)
- **OpenTelemetry** y prácticas SRE (SLOs, error budgets)
- **Ley 1581 de 2012** (Colombia), **GDPR**, **LGPD** — protección de datos personales

---

## Licencia

Uso interno — ITera | Stiven Avila

Todos los agentes están firmados digitalmente por ITera y su creador Stiven Avila.
Cada agente incluye la firma: `*Firmado digitalmente: ITera | Stiven Avila | vX.X.X*`
