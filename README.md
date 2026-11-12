# ITera Agent Suite

> **175 agentes especializados: requerimientos, arquitectura, desarrollo (web, backend, mobile, 10+ lenguajes), QA, ciberseguridad, IAM multicloud, DevOps/DevSecOps, IaC, observabilidad y SRE, bases de datos, datos e IA, FinOps, multicloud (AWS, Azure, GCP, IBM, OCI), regulación y derecho, RRHH, gestión y liderazgo, videojuegos, audio y 3D, y blockchain — coordinados por un agente orquestador.**
> Compatibles con Kiro IDE y Claude (web/API/Projects).

**Creado por**: Stiven Avila | **Organización**: ITera
**Versión**: 4.0.0 | **Fecha**: 2026-11-12

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

### Ciberseguridad Especializada

| # | Agente | Descripción | Kiro Path |
|---|--------|-------------|-----------|
| 36 | **Threat Modeling** | STRIDE, PASTA, LINDDUN: amenazas y requisitos de seguridad antes de construir | `.kiro/agents/threat-modeling/` |
| 37 | **Incident Response (DFIR)** | Triage, contención, evidencia forense, recuperación y notificaciones | `.kiro/agents/incident-response/` |
| 38 | **Secrets Management** | Secretos expuestos, Secrets Manager/Vault, rotación, identidad de workloads | `.kiro/agents/secrets-management/` |
| 39 | **Supply Chain Security** | Dependencias, SBOM, SLSA, firma de artefactos, hardening de CI/CD | `.kiro/agents/supply-chain-security/` |
| 40 | **Vulnerability Management** | Priorización por KEV, EPSS y exposición; SLAs y métricas | `.kiro/agents/vulnerability-management/` |
| 41 | **WAF & DDoS** | Reglas WAF, rate limiting, bots, Shield, resiliencia ante DDoS | `.kiro/agents/waf-ddos-protection/` |
| 42 | **Detection Engineering & SIEM** | Detecciones como código (Sigma/KQL/SPL) mapeadas a MITRE ATT&CK | `.kiro/agents/detection-engineering/` |
| 43 | **Network Security & Zero Trust** | Segmentación, firewalls, egress, conectividad privada, zero trust | `.kiro/agents/network-security/` |
| 44 | **Criptografía & Cifrado** | Algoritmos, AEAD, hashing de contraseñas, KMS, post-cuántico | `.kiro/agents/cryptography-encryption/` |
| 45 | **PKI & Certificados** | Certificados, CAs, TLS/mTLS, renovación automática | `.kiro/agents/pki-certificates/` |
| 46 | **AI & LLM Security** | Prompt injection, agencia excesiva, fugas en RAG (OWASP LLM Top 10) | `.kiro/agents/ai-llm-security/` |

### Identidad & Accesos (IAM)

| # | Agente | Descripción | Kiro Path |
|---|--------|-------------|-----------|
| 47 | **Federación & SSO** | OAuth 2.0, OIDC, SAML, passkeys, Entra ID, Okta, Cognito | `.kiro/agents/identity-federation-sso/` |
| 48 | **AWS Organizations IAM** | SCPs, RCPs, perímetro de datos, permission sets, Access Analyzer | `.kiro/agents/aws-organizations-iam/` |
| 49 | **Identity Governance** | Altas-cambios-bajas, revisiones de acceso, SoD, accesos privilegiados | `.kiro/agents/identity-governance/` |

### FinOps Especializado

| # | Agente | Descripción | Kiro Path |
|---|--------|-------------|-----------|
| 50 | **Tagging & Cost Allocation** | Etiquetado obligatorio, asignación de costos, showback | `.kiro/agents/tagging-governance/` |
| 51 | **Savings Plans & RIs** | Cobertura, utilización y compras escalonadas de compromisos | `.kiro/agents/commitment-management/` |
| 52 | **Kubernetes FinOps** | Right-sizing de requests, autoscaling, Spot/Graviton, costos por equipo | `.kiro/agents/kubernetes-finops/` |
| 53 | **Forecasting & Budgets** | Pronósticos por drivers, presupuestos, varianzas, anomalías | `.kiro/agents/cloud-cost-forecasting/` |
| 54 | **GenAI FinOps** | Costo por solicitud de LLMs, enrutamiento de modelos, caching, límites | `.kiro/agents/genai-finops/` |

### Cloud (AWS, Azure, GCP, IBM, OCI)

| # | Agente | Descripción | Kiro Path |
|---|--------|-------------|-----------|
| 55 | **Azure Architect** | Well-Architected de Azure, landing zones, Azure Policy, Bicep | `.kiro/agents/azure-architect/` |
| 56 | **Google Cloud Architect** | Jerarquía de recursos, org policies, VPC-SC, Cloud Run, BigQuery | `.kiro/agents/gcp-architect/` |
| 57 | **IBM Cloud Architect** | VPC, OpenShift, Code Engine, Key Protect, Financial Services | `.kiro/agents/ibm-cloud-architect/` |
| 58 | **Oracle Cloud (OCI) Architect** | Compartments, Autonomous DB, Exadata, licenciamiento | `.kiro/agents/oci-architect/` |
| 59 | **Multi-Cloud Strategy** | Cuándo usar varias nubes, ubicación de workloads, equivalencias | `.kiro/agents/multi-cloud-strategy/` |
| 60 | **AWS Landing Zone** | Organizations, Control Tower, Account Factory, baseline de cuentas | `.kiro/agents/aws-landing-zone/` |
| 61 | **AWS Serverless** | Lambda, API Gateway, Step Functions, EventBridge, SQS, DynamoDB | `.kiro/agents/aws-serverless/` |
| 62 | **AWS Networking** | VPC/IPAM, Transit Gateway, Cloud WAN, Direct Connect, Route 53 | `.kiro/agents/aws-networking/` |
| 63 | **AWS Migration (MAP)** | Assess/Mobilize/Migrate, 7 Rs, olas, MGN/DMS, cutover | `.kiro/agents/aws-migration-map/` |
| 64 | **Disaster Recovery** | RTO/RPO, estrategias de DR, backups inmutables, pruebas de recuperación | `.kiro/agents/disaster-recovery/` |

### Arquitectura Especializada

| # | Agente | Descripción | Kiro Path |
|---|--------|-------------|-----------|
| 65 | **Presales Solutions Architect** | De la necesidad o RFP del cliente a una propuesta defendible | `.kiro/agents/presales-solutions-architect/` |
| 66 | **Event-Driven Architecture** | Eventos, outbox, idempotencia, sagas, evolución de esquemas | `.kiro/agents/event-driven-architecture/` |
| 67 | **Microservices Architecture** | Límites de servicios, datos, resiliencia, monolito distribuido | `.kiro/agents/microservices-architecture/` |
| 68 | **Enterprise Architecture** | Mapa de capacidades, portafolio de aplicaciones, roadmaps | `.kiro/agents/enterprise-architecture/` |
| 69 | **Platform Engineering** | Plataformas internas, golden paths, Backstage, autoservicio | `.kiro/agents/platform-engineering/` |

### Desarrollo por Lenguaje & Especialidad

| # | Agente | Descripción | Kiro Path |
|---|--------|-------------|-----------|
| 70 | **Python Developer** | FastAPI, Django, asyncio, Pydantic, pytest, Ruff, mypy | `.kiro/agents/python-developer/` |
| 71 | **TypeScript & Node.js** | Express, Fastify, NestJS, Prisma, Zod, Vitest | `.kiro/agents/typescript-node-developer/` |
| 72 | **Java & Spring Boot** | Java 17/21, JPA, Spring Security, resiliencia, Testcontainers | `.kiro/agents/java-spring-developer/` |
| 73 | **.NET Developer** | C#, ASP.NET Core, EF Core, async, DI | `.kiro/agents/dotnet-developer/` |
| 74 | **Go Developer** | Errores, goroutines, context, servicios HTTP, race detector | `.kiro/agents/go-developer/` |
| 75 | **AI Agent Developer** | Apps con LLMs, RAG, agentes con herramientas, MCP, evaluaciones | `.kiro/agents/ai-agent-developer/` |
| 76 | **UI/UX Design** | Flujos, interfaces, design systems y tokens listos para implementar | `.kiro/agents/ui-ux-design/` |
| 77 | **Shell Scripting** | Bash, sh, PowerShell seguros, idempotentes y con dry-run | `.kiro/agents/shell-scripting-automation/` |
| 78 | **Linux Administration** | Diagnóstico, hardening CIS, systemd, Ansible | `.kiro/agents/linux-administration/` |

### Datos & IA

| # | Agente | Descripción | Kiro Path |
|---|--------|-------------|-----------|
| 79 | **MLOps Engineering** | Pipelines de ML, model registry, despliegue, monitoreo de drift | `.kiro/agents/mlops-engineering/` |
| 80 | **Analytics & BI** | KPIs con definición precisa, modelos semánticos, dashboards | `.kiro/agents/analytics-bi/` |

### Gestión de Proyectos & Liderazgo

| # | Agente | Descripción | Kiro Path |
|---|--------|-------------|-----------|
| 81 | **Project Manager** | Plan, WBS, cronograma, RAID, control de cambios, estado honesto | `.kiro/agents/project-manager/` |
| 82 | **Scrum Master & Agile Coach** | Eventos, métricas de flujo, Monte Carlo, retrospectivas | `.kiro/agents/scrum-master/` |
| 83 | **Product Owner** | Objetivo de producto, roadmap, backlog, priorización, métricas | `.kiro/agents/product-owner/` |
| 84 | **Engineering Manager** | 1:1, feedback, crecimiento, contratación, salud del equipo | `.kiro/agents/engineering-manager/` |
| 85 | **Tech Lead** | RFCs, ADRs, desglose en slices, estándares, revisión de código | `.kiro/agents/tech-lead/` |
| 86 | **Technology Strategy (CTO)** | Build vs buy, apuestas de plataforma, adopción de IA, presupuesto | `.kiro/agents/technology-strategy/` |
| 87 | **Software Estimation** | Estimaciones en rangos, PERT, trabajo oculto, contingencia | `.kiro/agents/software-estimation/` |

### QA Especializado

| # | Agente | Descripción | Kiro Path |
|---|--------|-------------|-----------|
| 88 | **QA Manual & Exploratorio** | Casos de prueba, sesiones exploratorias, reportes de bugs | `.kiro/agents/qa-manual-testing/` |
| 89 | **Web E2E Automation** | Playwright, Cypress, Selenium: suites estables en CI | `.kiro/agents/web-e2e-automation/` |
| 90 | **API Testing** | Funcional, negativo, autorización (BOLA), contratos (Pact), fuzzing | `.kiro/agents/api-testing/` |
| 91 | **Mobile Test Automation** | Espresso, XCUITest, Appium, Maestro, Detox, device farms | `.kiro/agents/mobile-test-automation/` |
| 92 | **QA Lead** | Estrategia de calidad, métricas, criterios y decisión de release | `.kiro/agents/qa-lead/` |

### Blockchain

| # | Agente | Descripción | Kiro Path |
|---|--------|-------------|-----------|
| 93 | **Smart Contract Security** | Auditoría Solidity/EVM: reentrancy, oráculos, flash loans, PoCs | `.kiro/agents/smart-contract-security/` |
| 94 | **Blockchain Architecture** | Si blockchain aplica; plataforma, custodia, tokenización, cumplimiento | `.kiro/agents/blockchain-architecture/` |

### Contenedores & Docker

| # | Agente | Descripción | Kiro Path |
|---|--------|-------------|-----------|
| 95 | **Docker Engineering** | Dockerfiles multi-stage, Compose, BuildKit, imágenes multi-arch | `.kiro/agents/docker-engineering/` |
| 96 | **AWS ECS & Fargate** | Task definitions, servicios, despliegues, autoscaling | `.kiro/agents/aws-ecs-fargate/` |

### Más Lenguajes

| # | Agente | Descripción | Kiro Path |
|---|--------|-------------|-----------|
| 97 | **Rust** | Ownership, errores, Tokio, unsafe justificado | `.kiro/agents/rust-developer/` |
| 98 | **PHP & Laravel** | Eloquent sin N+1, Form Requests, policies, colas | `.kiro/agents/php-laravel-developer/` |
| 99 | **Ruby on Rails** | Active Record, migraciones seguras, Brakeman | `.kiro/agents/ruby-rails-developer/` |
| 100 | **C++** | RAII, undefined behavior, sanitizers, CMake | `.kiro/agents/cpp-developer/` |

### Requerimientos & Especificaciones

| # | Agente | Descripción | Kiro Path |
|---|--------|-------------|-----------|
| 101 | **Business Process Analyst** | BPMN/DMN, procesos as-is/to-be, KPIs | `.kiro/agents/business-process-analyst/` |
| 102 | **Technical Specification Writer** | Especificaciones funcionales, SRS, interfaces | `.kiro/agents/technical-specification-writer/` |

### Regulación & Derecho

| # | Agente | Descripción | Kiro Path |
|---|--------|-------------|-----------|
| 103 | **PCI DSS** | Alcance del CDE, brechas y evidencia PCI DSS v4.0.1 | `.kiro/agents/pci-dss-compliance/` |
| 104 | **ISO/IEC 27001 (SGSI)** | Riesgos, SoA con Anexo A, auditorías, certificación | `.kiro/agents/iso27001-isms/` |
| 105 | **Regulación Financiera Colombia (SFC)** | Ciberseguridad, nube, tercerización, incidentes | `.kiro/agents/colombia-financial-regulation/` |
| 106 | **AI Governance** | EU AI Act, ISO/IEC 42001, NIST AI RMF | `.kiro/agents/ai-governance/` |
| 107 | **Contratos de Tecnología** | MSA, SOW, SaaS, SLA, DPA, NDA (no es asesoría legal) | `.kiro/agents/tech-contracts-legal/` |
| 108 | **Licencias Open Source** | Obligaciones, compatibilidad, avisos de terceros | `.kiro/agents/open-source-licensing/` |
| 109 | **Derecho Laboral Colombiano** | Contratos, jornada, prestaciones, nómina, reglas de software | `.kiro/agents/colombian-labor-law/` |

### Recursos Humanos

| # | Agente | Descripción | Kiro Path |
|---|--------|-------------|-----------|
| 110 | **Technical Recruiter** | Contratación técnica estructurada y justa | `.kiro/agents/technical-recruiter/` |
| 111 | **People Operations (HRBP)** | Onboarding, desempeño, compensación, políticas | `.kiro/agents/people-operations/` |
| 112 | **Learning & Development** | Rutas de aprendizaje y certificaciones | `.kiro/agents/learning-development/` |

### DevOps & DevSecOps Especializado

| # | Agente | Descripción | Kiro Path |
|---|--------|-------------|-----------|
| 113 | **GitHub Actions** | Workflows seguros, OIDC, entornos protegidos | `.kiro/agents/github-actions-cicd/` |
| 114 | **GitLab CI/CD** | Pipelines DAG, componentes, escáneres, entornos | `.kiro/agents/gitlab-cicd/` |
| 115 | **GitOps & Argo CD** | ApplicationSets, promoción, Argo Rollouts | `.kiro/agents/gitops-argocd/` |
| 116 | **Policy as Code** | OPA/Rego, Kyverno, Gatekeeper, Checkov, Sentinel | `.kiro/agents/policy-as-code/` |
| 117 | **SCA** | Análisis de composición de software y dependencias | `.kiro/agents/sca-security/` |
| 118 | **API Security Testing (DAST)** | OWASP API Top 10 en APIs autorizadas | `.kiro/agents/api-security-testing/` |

### Migración

| # | Agente | Descripción | Kiro Path |
|---|--------|-------------|-----------|
| 119 | **Database Migration** | Cambio de motor o plataforma con CDC, validación y cutover | `.kiro/agents/database-migration/` |
| 120 | **Mainframe Modernization** | COBOL/CICS/IMS/Db2 con corridas en paralelo | `.kiro/agents/mainframe-modernization/` |

### Machine Learning & Datos

| # | Agente | Descripción | Kiro Path |
|---|--------|-------------|-----------|
| 121 | **Machine Learning Engineer** | Modelos de ML sin fugas, contra baseline, reproducibles | `.kiro/agents/machine-learning-engineer/` |
| 122 | **Data Scientist** | EDA, estadística, A/B tests, inferencia causal | `.kiro/agents/data-scientist/` |
| 123 | **Data Governance** | Dueños, catálogo, calidad, clasificación, MDM | `.kiro/agents/data-governance/` |
| 124 | **Data Warehouse** | Redshift, Snowflake, BigQuery, modelado dimensional, dbt | `.kiro/agents/data-warehouse/` |
| 125 | **Kafka & Streaming** | Topics, productores, consumidores, esquemas | `.kiro/agents/kafka-streaming/` |

### Bases de Datos por Motor

| # | Agente | Descripción | Kiro Path |
|---|--------|-------------|-----------|
| 126 | **PostgreSQL** | Diseño, EXPLAIN, autovacuum, migraciones seguras | `.kiro/agents/postgresql-specialist/` |
| 127 | **MongoDB** | Modelado por patrones de acceso, índices ESR, sharding | `.kiro/agents/mongodb-specialist/` |
| 128 | **DynamoDB** | Diseño de llaves, GSIs, particiones calientes | `.kiro/agents/dynamodb-specialist/` |
| 129 | **Redis / Valkey** | Caché, estructuras, eviction, clúster | `.kiro/agents/redis-specialist/` |
| 130 | **SQL Server DBA** | Planes, Query Store, Always On, backups | `.kiro/agents/sql-server-dba/` |
| 131 | **Oracle Database** | AWR/ASH, RAC, Data Guard, RMAN, licenciamiento | `.kiro/agents/oracle-database/` |

### Frontend, Backend & Mobile

| # | Agente | Descripción | Kiro Path |
|---|--------|-------------|-----------|
| 132 | **React** | Hooks, estado, rendimiento, Testing Library | `.kiro/agents/react-developer/` |
| 133 | **Angular** | Signals, standalone, RxJS, OnPush | `.kiro/agents/angular-developer/` |
| 134 | **Vue & Nuxt** | Composition API, Pinia, SSR | `.kiro/agents/vue-developer/` |
| 135 | **Next.js** | App Router, Server Actions, caché | `.kiro/agents/nextjs-developer/` |
| 136 | **Backend Engineering** | Diseño backend independiente del lenguaje | `.kiro/agents/backend-engineering/` |
| 137 | **GraphQL** | Esquemas, DataLoader, autorización por campo, federación | `.kiro/agents/graphql-api/` |
| 138 | **iOS (Swift/SwiftUI)** | Concurrencia, Keychain, privacidad, accesibilidad | `.kiro/agents/ios-developer/` |
| 139 | **Android (Kotlin/Compose)** | Arquitectura, coroutines, Room, Play Store | `.kiro/agents/android-developer/` |
| 140 | **React Native & Expo** | New Architecture, EAS, OTA updates | `.kiro/agents/react-native-developer/` |
| 141 | **Flutter** | Riverpod/Bloc, go_router, rendimiento | `.kiro/agents/flutter-developer/` |

### Observabilidad & SRE Especializado

| # | Agente | Descripción | Kiro Path |
|---|--------|-------------|-----------|
| 142 | **OpenTelemetry** | Instrumentación, propagación de contexto, Collector | `.kiro/agents/opentelemetry/` |
| 143 | **Prometheus & Grafana** | PromQL, alertas, dashboards como código | `.kiro/agents/prometheus-grafana/` |
| 144 | **AWS CloudWatch** | Alarmas por percentiles, Logs Insights, canaries | `.kiro/agents/aws-cloudwatch/` |
| 145 | **Chaos Engineering** | Experimentos con hipótesis y condiciones de parada | `.kiro/agents/chaos-engineering/` |
| 146 | **Incident Management & On-Call** | Severidades, guardias, postmortems | `.kiro/agents/incident-management-oncall/` |
| 147 | **Capacity Planning** | Demanda, saturación, escalamiento, cuotas | `.kiro/agents/capacity-planning/` |

### Infraestructura como Código

| # | Agente | Descripción | Kiro Path |
|---|--------|-------------|-----------|
| 148 | **Terraform / OpenTofu** | Módulos, estado remoto, revisión de planes | `.kiro/agents/terraform-engineer/` |
| 149 | **AWS CDK** | Stacks, constructs, cdk-nag, assertions | `.kiro/agents/aws-cdk-engineer/` |
| 150 | **CloudFormation & SAM** | Change sets, StackSets, Guard | `.kiro/agents/cloudformation-engineer/` |
| 151 | **Ansible** | Playbooks idempotentes, Molecule, Vault | `.kiro/agents/ansible-automation/` |

### IAM Multicloud

| # | Agente | Descripción | Kiro Path |
|---|--------|-------------|-----------|
| 152 | **Azure & Entra ID IAM** | Conditional Access, PIM, RBAC, identidades administradas | `.kiro/agents/azure-entra-iam/` |
| 153 | **Google Cloud IAM** | Sin roles básicos, cuentas de servicio sin llaves | `.kiro/agents/gcp-iam/` |
| 154 | **Multi-Cloud IAM** | Un modelo de identidad para AWS, Azure, GCP, OCI e IBM | `.kiro/agents/multicloud-iam/` |

### Serverless & Colas

| # | Agente | Descripción | Kiro Path |
|---|--------|-------------|-----------|
| 155 | **Azure Functions** | Planes, triggers, Durable Functions | `.kiro/agents/azure-functions/` |
| 156 | **Google Cloud Serverless** | Cloud Run, Pub/Sub, Eventarc, Workflows | `.kiro/agents/gcp-serverless/` |
| 157 | **RabbitMQ** | Exchanges, quorum queues, confirms, dead-lettering | `.kiro/agents/rabbitmq-specialist/` |
| 158 | **AWS Messaging** | SQS, SNS, EventBridge, Kinesis, Amazon MQ | `.kiro/agents/aws-messaging/` |

### Sistemas Operativos & Parcheo

| # | Agente | Descripción | Kiro Path |
|---|--------|-------------|-----------|
| 159 | **Linux Hardening** | CIS/STIG, SELinux/AppArmor, auditd | `.kiro/agents/linux-security-hardening/` |
| 160 | **Windows Server** | PowerShell, IIS, GPO, baselines | `.kiro/agents/windows-server/` |
| 161 | **Active Directory Security** | Tiering, Kerberoasting, AD CS, LAPS | `.kiro/agents/active-directory/` |
| 162 | **Patch Management** | Parcheo por riesgo con anillos y automatización | `.kiro/agents/patch-management/` |

### Videojuegos, Audio & 3D

| # | Agente | Descripción | Kiro Path |
|---|--------|-------------|-----------|
| 163 | **Unity Game Developer** | C#, arquitectura por componentes, profiling | `.kiro/agents/unity-game-developer/` |
| 164 | **Unreal Engine Developer** | C++/Blueprints, GAS, replicación | `.kiro/agents/unreal-engine-developer/` |
| 165 | **Game Designer** | Sistemas, progresión, economías, playtests | `.kiro/agents/game-designer/` |
| 166 | **Game Audio Designer** | FMOD, Wwise, MetaSounds, música adaptativa | `.kiro/agents/game-audio-designer/` |
| 167 | **Audio Engineering** | Grabación, mezcla, mastering, loudness, DSP | `.kiro/agents/audio-engineering/` |
| 168 | **3D Modeling** | Topología, UVs, PBR, LODs, exportación | `.kiro/agents/3d-modeling/` |
| 169 | **Technical Artist** | Shaders, herramientas, contenido procedural | `.kiro/agents/technical-artist/` |

### Blockchain Engineering

| # | Agente | Descripción | Kiro Path |
|---|--------|-------------|-----------|
| 170 | **Ingeniero de Protocolo (Core Blockchain Developer)** | Consenso, P2P, ejecución, estado, rollups | `.kiro/agents/blockchain-protocol-engineer/` |
| 171 | **Smart Contract Engineer** | Solidity/Vyper con Foundry, fuzzing, despliegue seguro | `.kiro/agents/smart-contract-engineer/` |
| 172 | **dApp & Web3 Developer** | wagmi, viem, wallets, SIWE, indexadores | `.kiro/agents/dapp-web3-developer/` |

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
| `subagent` → `allow` | Solo el **Agent Orchestrator**: puede invocar a los otros 174 agentes |

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
│   └── agents/                          # 175 agentes: <agente>.json (config Kiro) + <agente>/agent.md (prompt)
│       ├── 3d-modeling.json + 3d-modeling/agent.md
│       ├── accessibility.json + accessibility/agent.md
│       ├── active-directory.json + active-directory/agent.md
│       ├── agent-orchestrator.json + agent-orchestrator/agent.md
│       ├── ai-agent-developer.json + ai-agent-developer/agent.md
│       ├── ai-governance.json + ai-governance/agent.md
│       ├── ai-llm-security.json + ai-llm-security/agent.md
│       ├── analytics-bi.json + analytics-bi/agent.md
│       ├── android-developer.json + android-developer/agent.md
│       ├── angular-developer.json + angular-developer/agent.md
│       ├── ansible-automation.json + ansible-automation/agent.md
│       ├── api-design.json + api-design/agent.md
│       ├── api-security-testing.json + api-security-testing/agent.md
│       ├── api-testing.json + api-testing/agent.md
│       ├── audio-engineering.json + audio-engineering/agent.md
│       ├── aws-best-practices.json + aws-best-practices/agent.md
│       ├── aws-cdk-engineer.json + aws-cdk-engineer/agent.md
│       ├── aws-cloudwatch.json + aws-cloudwatch/agent.md
│       ├── aws-ecs-fargate.json + aws-ecs-fargate/agent.md
│       ├── aws-landing-zone.json + aws-landing-zone/agent.md
│       ├── aws-messaging.json + aws-messaging/agent.md
│       ├── aws-migration-map.json + aws-migration-map/agent.md
│       ├── aws-networking.json + aws-networking/agent.md
│       ├── aws-organizations-iam.json + aws-organizations-iam/agent.md
│       ├── aws-serverless.json + aws-serverless/agent.md
│       ├── azure-architect.json + azure-architect/agent.md
│       ├── azure-entra-iam.json + azure-entra-iam/agent.md
│       ├── azure-functions.json + azure-functions/agent.md
│       ├── backend-engineering.json + backend-engineering/agent.md
│       ├── blockchain-architecture.json + blockchain-architecture/agent.md
│       ├── blockchain-protocol-engineer.json + blockchain-protocol-engineer/agent.md
│       ├── business-process-analyst.json + business-process-analyst/agent.md
│       ├── capacity-planning.json + capacity-planning/agent.md
│       ├── chaos-engineering.json + chaos-engineering/agent.md
│       ├── cloud-cost-forecasting.json + cloud-cost-forecasting/agent.md
│       ├── cloud-security.json + cloud-security/agent.md
│       ├── cloudformation-engineer.json + cloudformation-engineer/agent.md
│       ├── code-reviewer.json + code-reviewer/agent.md
│       ├── colombia-financial-regulation.json + colombia-financial-regulation/agent.md
│       ├── colombian-labor-law.json + colombian-labor-law/agent.md
│       ├── commitment-management.json + commitment-management/agent.md
│       ├── container-best-practices.json + container-best-practices/agent.md
│       ├── container-reviewer.json + container-reviewer/agent.md
│       ├── cpp-developer.json + cpp-developer/agent.md
│       ├── cryptography-encryption.json + cryptography-encryption/agent.md
│       ├── dapp-web3-developer.json + dapp-web3-developer/agent.md
│       ├── dast-security.json + dast-security/agent.md
│       ├── data-engineering.json + data-engineering/agent.md
│       ├── data-governance.json + data-governance/agent.md
│       ├── data-scientist.json + data-scientist/agent.md
│       ├── data-warehouse.json + data-warehouse/agent.md
│       ├── database-engineering.json + database-engineering/agent.md
│       ├── database-migration.json + database-migration/agent.md
│       ├── debugging-troubleshooting.json + debugging-troubleshooting/agent.md
│       ├── detection-engineering.json + detection-engineering/agent.md
│       ├── dev-best-practices.json + dev-best-practices/agent.md
│       ├── dev-documentation.json + dev-documentation/agent.md
│       ├── devops-reviewer.json + devops-reviewer/agent.md
│       ├── devsecops-reviewer.json + devsecops-reviewer/agent.md
│       ├── disaster-recovery.json + disaster-recovery/agent.md
│       ├── docker-engineering.json + docker-engineering/agent.md
│       ├── dotnet-developer.json + dotnet-developer/agent.md
│       ├── dynamodb-specialist.json + dynamodb-specialist/agent.md
│       ├── engineering-manager.json + engineering-manager/agent.md
│       ├── enterprise-architecture.json + enterprise-architecture/agent.md
│       ├── event-driven-architecture.json + event-driven-architecture/agent.md
│       ├── finops-cost-optimization.json + finops-cost-optimization/agent.md
│       ├── flutter-developer.json + flutter-developer/agent.md
│       ├── frontend-engineering.json + frontend-engineering/agent.md
│       ├── game-audio-designer.json + game-audio-designer/agent.md
│       ├── game-designer.json + game-designer/agent.md
│       ├── gcp-architect.json + gcp-architect/agent.md
│       ├── gcp-iam.json + gcp-iam/agent.md
│       ├── gcp-serverless.json + gcp-serverless/agent.md
│       ├── genai-aws-practices.json + genai-aws-practices/agent.md
│       ├── genai-finops.json + genai-finops/agent.md
│       ├── github-actions-cicd.json + github-actions-cicd/agent.md
│       ├── gitlab-cicd.json + gitlab-cicd/agent.md
│       ├── gitops-argocd.json + gitops-argocd/agent.md
│       ├── go-developer.json + go-developer/agent.md
│       ├── graphql-api.json + graphql-api/agent.md
│       ├── iac-reviewer.json + iac-reviewer/agent.md
│       ├── ibm-cloud-architect.json + ibm-cloud-architect/agent.md
│       ├── identity-federation-sso.json + identity-federation-sso/agent.md
│       ├── identity-governance.json + identity-governance/agent.md
│       ├── incident-management-oncall.json + incident-management-oncall/agent.md
│       ├── incident-response.json + incident-response/agent.md
│       ├── ios-developer.json + ios-developer/agent.md
│       ├── iso27001-isms.json + iso27001-isms/agent.md
│       ├── java-spring-developer.json + java-spring-developer/agent.md
│       ├── kafka-streaming.json + kafka-streaming/agent.md
│       ├── kubernetes-best-practices.json + kubernetes-best-practices/agent.md
│       ├── kubernetes-finops.json + kubernetes-finops/agent.md
│       ├── kubernetes-security.json + kubernetes-security/agent.md
│       ├── learning-development.json + learning-development/agent.md
│       ├── least-privilege.json + least-privilege/agent.md
│       ├── linux-administration.json + linux-administration/agent.md
│       ├── linux-security-hardening.json + linux-security-hardening/agent.md
│       ├── machine-learning-engineer.json + machine-learning-engineer/agent.md
│       ├── mainframe-modernization.json + mainframe-modernization/agent.md
│       ├── microservices-architecture.json + microservices-architecture/agent.md
│       ├── mlops-engineering.json + mlops-engineering/agent.md
│       ├── mobile-engineering.json + mobile-engineering/agent.md
│       ├── mobile-test-automation.json + mobile-test-automation/agent.md
│       ├── mongodb-specialist.json + mongodb-specialist/agent.md
│       ├── multi-cloud-strategy.json + multi-cloud-strategy/agent.md
│       ├── multicloud-iam.json + multicloud-iam/agent.md
│       ├── network-security.json + network-security/agent.md
│       ├── nextjs-developer.json + nextjs-developer/agent.md
│       ├── observability-sre.json + observability-sre/agent.md
│       ├── oci-architect.json + oci-architect/agent.md
│       ├── open-source-licensing.json + open-source-licensing/agent.md
│       ├── opentelemetry.json + opentelemetry/agent.md
│       ├── oracle-database.json + oracle-database/agent.md
│       ├── patch-management.json + patch-management/agent.md
│       ├── pci-dss-compliance.json + pci-dss-compliance/agent.md
│       ├── pentest-security.json + pentest-security/agent.md
│       ├── people-operations.json + people-operations/agent.md
│       ├── performance-engineering.json + performance-engineering/agent.md
│       ├── php-laravel-developer.json + php-laravel-developer/agent.md
│       ├── pki-certificates.json + pki-certificates/agent.md
│       ├── platform-engineering.json + platform-engineering/agent.md
│       ├── policy-as-code.json + policy-as-code/agent.md
│       ├── postgresql-specialist.json + postgresql-specialist/agent.md
│       ├── presales-solutions-architect.json + presales-solutions-architect/agent.md
│       ├── privacy-compliance.json + privacy-compliance/agent.md
│       ├── product-owner.json + product-owner/agent.md
│       ├── project-manager.json + project-manager/agent.md
│       ├── prometheus-grafana.json + prometheus-grafana/agent.md
│       ├── python-developer.json + python-developer/agent.md
│       ├── qa-lead.json + qa-lead/agent.md
│       ├── qa-manual-testing.json + qa-manual-testing/agent.md
│       ├── rabbitmq-specialist.json + rabbitmq-specialist/agent.md
│       ├── react-developer.json + react-developer/agent.md
│       ├── react-native-developer.json + react-native-developer/agent.md
│       ├── redis-specialist.json + redis-specialist/agent.md
│       ├── refactoring-modernization.json + refactoring-modernization/agent.md
│       ├── release-management.json + release-management/agent.md
│       ├── requirements-analyst.json + requirements-analyst/agent.md
│       ├── ruby-rails-developer.json + ruby-rails-developer/agent.md
│       ├── rust-developer.json + rust-developer/agent.md
│       ├── sast-security.json + sast-security/agent.md
│       ├── sca-security.json + sca-security/agent.md
│       ├── scrum-master.json + scrum-master/agent.md
│       ├── secrets-management.json + secrets-management/agent.md
│       ├── secure-development.json + secure-development/agent.md
│       ├── security-audit.json + security-audit/agent.md
│       ├── security-tester.json + security-tester/agent.md
│       ├── shell-scripting-automation.json + shell-scripting-automation/agent.md
│       ├── smart-contract-engineer.json + smart-contract-engineer/agent.md
│       ├── smart-contract-security.json + smart-contract-security/agent.md
│       ├── software-architect.json + software-architect/agent.md
│       ├── software-estimation.json + software-estimation/agent.md
│       ├── sql-server-dba.json + sql-server-dba/agent.md
│       ├── supply-chain-security.json + supply-chain-security/agent.md
│       ├── tagging-governance.json + tagging-governance/agent.md
│       ├── tech-contracts-legal.json + tech-contracts-legal/agent.md
│       ├── tech-lead.json + tech-lead/agent.md
│       ├── technical-artist.json + technical-artist/agent.md
│       ├── technical-recruiter.json + technical-recruiter/agent.md
│       ├── technical-specification-writer.json + technical-specification-writer/agent.md
│       ├── technology-strategy.json + technology-strategy/agent.md
│       ├── terraform-engineer.json + terraform-engineer/agent.md
│       ├── test-automation.json + test-automation/agent.md
│       ├── threat-modeling.json + threat-modeling/agent.md
│       ├── typescript-node-developer.json + typescript-node-developer/agent.md
│       ├── ui-ux-design.json + ui-ux-design/agent.md
│       ├── unity-game-developer.json + unity-game-developer/agent.md
│       ├── unreal-engine-developer.json + unreal-engine-developer/agent.md
│       ├── vue-developer.json + vue-developer/agent.md
│       ├── vulnerability-management.json + vulnerability-management/agent.md
│       ├── waf-ddos-protection.json + waf-ddos-protection/agent.md
│       ├── web-e2e-automation.json + web-e2e-automation/agent.md
│       ├── windows-server.json + windows-server/agent.md
│       └── yaml-best-practices.json + yaml-best-practices/agent.md
├── scripts/
│   └── generate_kiro_agents.py          # genera los <agente>.json (permisos, herramientas, recursos)
└── README.md
```

Para agregar un agente: crea `.kiro/agents/<agente>/agent.md`, agrega su definición `agent(...)` en `scripts/generate_kiro_agents.py` y ejecuta `python3 scripts/generate_kiro_agents.py .`. El script falla si algún agente queda sin configuración. Después, agrega el agente al catálogo del orquestador (`agent-orchestrator/agent.md`).

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

| **Propuesta a cliente (preventa)** | Requirements Analyst → Presales Solutions Architect → Software Estimation ‖ FinOps |
| **Funcionalidad con agentes de IA** | Requirements Analyst → AI Agent Developer → AI & LLM Security ‖ GenAI FinOps → Test Automation |
| **Programa de seguridad base** | Threat Modeling → Secrets Management ‖ Supply Chain Security → Vulnerability Management → Detection Engineering |
| **Incidente de seguridad** | Incident Response ‖ Secrets Management → Detection Engineering → Development Documentation |
| **Fundación AWS** | AWS Landing Zone → AWS Organizations IAM → AWS Networking → Tagging Governance → Disaster Recovery |
| **Migración a AWS (MAP)** | AWS Migration (MAP) → AWS Landing Zone → Refactoring & Modernization → Savings Plans & RIs |
| **Arranque de proyecto** | Requirements Analyst → Project Manager → Software Estimation → Tech Lead → QA Lead |
| **Programa FinOps** | Tagging Governance → FinOps & Cost Optimization → Savings Plans & RIs → Forecasting & Budgets |
| **Gate de calidad de release** | QA Lead → Web E2E ‖ API Testing ‖ Mobile Test Automation → Release Management |
| **Lanzamiento de smart contracts** | Blockchain Architecture → Smart Contract Security → Release Management |

| **Producto Web3** | Blockchain Architecture → Smart Contract Engineer → Smart Contract Security → dApp & Web3 Developer |
| **Cumplimiento de pagos** | PCI DSS → Secure Development ‖ API Security Testing → ISO 27001 |
| **Fintech regulada (Colombia)** | Regulación Financiera Colombia → Privacy by Design → ISO 27001 → Incident Management |
| **Modernización de base de datos** | Database Migration → PostgreSQL (o motor destino) → Performance Engineering |
| **App móvil nativa** | Requirements Analyst → iOS ‖ Android → Mobile Test Automation → Release Management |
| **Plataforma de datos** | Data Governance → Data Warehouse ‖ Kafka & Streaming → Analytics & BI |
| **Producto de ML** | Data Scientist → Machine Learning Engineer → MLOps → AI Governance |
| **Pipeline de plataforma** | GitHub Actions (o GitLab CI/CD) → Policy as Code → GitOps & Argo CD → OpenTelemetry |
| **Infraestructura base** | Terraform → Policy as Code → Linux Hardening ‖ Patch Management |
| **Producción de videojuego** | Game Designer → Unity (o Unreal) ‖ Technical Artist ‖ Game Audio Designer |
| **Construcción de equipo** | Technical Recruiter → People Operations → Learning & Development → Engineering Manager |

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
- **OWASP Top 10 for LLM Applications**, **MITRE ATLAS**, **NIST AI RMF**
- **NIST SP 800-61** (respuesta a incidentes), **NIST SP 800-207** (zero trust), **SSVC**, **EPSS**, **CISA KEV**
- **Azure Well-Architected**, **Google Cloud Architecture Framework**, **OCI** e **IBM Cloud Framework for Financial Services**
- **AWS MAP** (Migration Acceleration Program), **ISO 22301** (continuidad del negocio)
- **Scrum Guide 2020**, **PMBOK**, **TOGAF**, **ArchiMate**, **Team Topologies**
- **SWC Registry** y **OWASP Smart Contract Top 10**
- **PCI DSS v4.0.1**, **ISO/IEC 27001:2022**, **EU AI Act**, **ISO/IEC 42001**, normativa **SFC** (Colombia), **Código Sustantivo del Trabajo**
- **OWASP API Security Top 10 (2023)**, **SLSA**, **OpenSSF Scorecard**, **CIS Benchmarks** (Linux, Windows) y **DISA STIG**
- **BPMN 2.0**, **DMN**, **ISO/IEC/IEEE 29148** (especificación de requerimientos)
- **OpenTelemetry**, **Prometheus**, **Google SRE** (SLOs, error budgets, postmortems sin culpables)

---

## Licencia

Uso interno — ITera | Stiven Avila

Todos los agentes están firmados digitalmente por ITera y su creador Stiven Avila.
Cada agente incluye la firma: `*Firmado digitalmente: ITera | Stiven Avila | vX.X.X*`
