"""Genera .kiro/agents/<slug>.json (esquema Kiro CLI v3 / IDE) para cada agente de la suite.

Cada agente se define abajo con agent(...): descripción, mensaje de bienvenida,
herramientas, carpetas con escritura libre y comandos de shell en allow / ask /
deny, sobre unas reglas comunes de modo seguro. El prompt de cada agente es
.kiro/agents/<slug>/agent.md.

Al agregar un agente nuevo: crea su carpeta con agent.md, agrega su agent(...)
aquí y vuelve a ejecutar el script. Falla si algún agente no tiene definición.

Uso (desde la raíz del repo):  python3 scripts/generate_kiro_agents.py .
"""
import json
import os
import sys

REPO = sys.argv[1]
AGENTS_DIR = os.path.join(REPO, ".kiro", "agents")

# ─── Reglas comunes a todos los agentes ────────────────────────────────────────
GIT_READ = ["git status*", "git diff*", "git log*", "git show*", "git blame*", "git branch*", "git ls-files*", "git grep *"]
GIT_WRITE_ASK = ["git add*", "git commit*", "git checkout *", "git switch *", "git stash*", "git merge*", "git rebase*", "git push*"]

SECRETS_READ_DENY = [
    "**/.env", "**/.env.*", "~/.aws/**", "**/.aws/**", "~/.ssh/**", "**/.ssh/**",
    "**/*.pem", "**/*.key", "**/id_rsa*", "**/id_ed25519*", "**/*.tfstate", "**/*.tfstate.*",
    "**/credentials.json", "**/*.p12", "**/*.pfx",
]
SECRETS_READ_EXCLUDE = ["**/.env.example", "**/.env.sample", "**/.env.template"]

SHELL_DENY = [
    "rm -rf *", "sudo *", "chmod -R 777*", "curl * | sh*", "curl * | bash*", "wget * | sh*",
    "terraform apply*", "terraform destroy*", "terraform import*", "terraform state rm*",
    "kubectl delete *", "kubectl get secret*", "kubectl describe secret*", "helm uninstall*",
    "git push --force*", "git push -f*", "git reset --hard*", "git clean -f*",
    "aws * delete-*", "aws * terminate-*", "aws s3 rm*", "aws s3 rb*",
    "aws secretsmanager get-secret-value*", "aws ssm get-parameter*",
    "docker push*", "docker system prune*", "npm publish*",
]

BASE_RESOURCES = [
    "file://README.md",
    "file://.kiro/steering/**/*.md",
    "skill://.kiro/skills/**/SKILL.md",
]

JS_CHECKS = ["npm run lint*", "npm run test*", "npm test*", "npm run build*", "npm run typecheck*",
             "npx tsc*", "npx eslint*", "npx vitest*", "npx jest*",
             "pnpm lint*", "pnpm test*", "pnpm build*", "yarn lint*", "yarn test*", "yarn build*"]
PY_CHECKS = ["pytest*", "python -m pytest*", "ruff check*", "mypy *"]
OTHER_TESTS = ["go test*", "go vet*", "mvn test*", "mvn verify*", "./gradlew test*", "dotnet test*"]
INSTALL_ASK = ["npm install*", "npm i *", "npm ci*", "pnpm add*", "pnpm install*", "yarn add*", "yarn install*",
               "pip install*", "poetry add*", "go get *"]
AWS_READ = ["aws * describe-*", "aws * list-*", "aws * get-*"]
TF_READ = ["terraform fmt -check*", "terraform validate*", "terraform plan*"]
K8S_READ = ["kubectl get *", "kubectl describe *", "kubectl top *", "kubectl explain *", "kubectl auth can-i*"]

# ─── Definición por agente ─────────────────────────────────────────────────────
# tools: categorías de herramientas; write: rutas con escritura libre;
# allow/ask/deny: comandos de shell adicionales; extra_res: recursos extra.
A = {}

def agent(slug, description, welcome, tools=("read", "write", "shell"), write=(), allow=(), ask=(), deny=(),
          extra_res=(), subagents=None):
    A[slug] = dict(description=description, welcome=welcome, tools=list(tools), write=list(write),
                   allow=list(allow), ask=list(ask), deny=list(deny), extra_res=list(extra_res), subagents=subagents)

R, W, S, WEB = "read", "write", "shell", "web"

# Orquestación y requerimientos
agent("requirements-analyst",
      "Understands and translates raw requests, RFPs, emails, and transcripts into testable requirements, user stories, Gherkin acceptance criteria, and NFRs (business ↔ technical, ES ↔ EN).",
      "Listo. Pásame el correo, RFP, transcripción o idea y lo convierto en requerimientos listos para desarrollo.",
      tools=(R, W, S, WEB), write=["docs/requirements/**", "docs/specs/**", "docs/**"],
      extra_res=["file://docs/requirements/**/*.md"])

# Arquitectura y diseño
agent("software-architect",
      "Designs and reviews software architectures: styles and trade-offs, DDD, integration patterns, ADRs, and C4 diagrams.",
      "Listo. Cuéntame los objetivos y restricciones y diseñamos la arquitectura con sus trade-offs y ADRs.",
      tools=(R, W, S, WEB), write=["docs/architecture/**", "docs/adr/**", "docs/**"],
      extra_res=["file://docs/architecture/**/*.md", "file://docs/adr/**/*.md"])
agent("api-design",
      "Designs and reviews REST, GraphQL, gRPC, and event-driven APIs: OpenAPI/AsyncAPI contracts, versioning, and API security.",
      "Listo. Diseño contract-first: muéstrame la API o el caso de uso.",
      tools=(R, W, S, WEB),
      write=["docs/api/**", "api/**", "openapi/**", "**/openapi.yaml", "**/openapi.yml", "**/openapi.json",
             "**/*.openapi.yaml", "**/asyncapi.yaml", "**/*.proto", "**/*.graphql"],
      allow=["npx @redocly/cli lint*", "npx @stoplight/spectral-cli lint*", "spectral lint*", "buf lint*", "buf breaking*"])
agent("database-engineering",
      "Designs and reviews SQL and NoSQL data models, indexes, query plans, zero-downtime migrations, and backups.",
      "Listo. Revisamos modelo, consultas y migraciones; nada se ejecuta contra la base sin tu confirmación.",
      write=["migrations/**", "**/migrations/**", "db/**", "prisma/**", "sql/**", "docs/**"],
      allow=["prisma validate*", "prisma format*", "alembic history*", "alembic check*", "flyway info*",
             "flyway validate*", "sqlfluff lint*"],
      ask=["psql *", "mysql *", "mongosh *", "alembic upgrade*", "prisma migrate dev*", "prisma db push*", "flyway migrate*"],
      deny=["prisma migrate reset*", "dropdb *", "flyway clean*", "alembic downgrade base*"])
agent("data-engineering",
      "Designs and reviews data pipelines, lakehouses, streaming, dbt/Airflow/Glue/Spark jobs, and data quality controls.",
      "Listo. Revisamos pipelines, modelos y calidad de datos; las ejecuciones reales piden confirmación.",
      write=["dags/**", "models/**", "pipelines/**", "jobs/**", "glue/**", "sql/**", "tests/**", "docs/**"],
      allow=["dbt compile*", "dbt parse*", "dbt ls*", "dbt test*", "sqlfluff lint*"] + PY_CHECKS,
      ask=["dbt run*", "dbt build*", "dbt seed*", "aws glue start-job-run*", "airflow dags trigger*", "spark-submit*"])

# Construcción
agent("frontend-engineering",
      "Builds and reviews web frontends (React, Next.js, Vue, Angular, TypeScript): state, performance, Core Web Vitals, and frontend security.",
      "Listo. Trabajo sobre la UI con lint, tipos y tests; instalar dependencias pide confirmación.",
      tools=(R, W, S, WEB),
      write=["src/**", "app/**", "components/**", "pages/**", "public/**", "styles/**", "tests/**", "e2e/**", "docs/**"],
      allow=JS_CHECKS + ["npx playwright test*"], ask=INSTALL_ASK + ["npm run dev*", "pnpm dev*", "yarn dev*"])
agent("mobile-engineering",
      "Builds and reviews iOS, Android, React Native, and Flutter apps: architecture, offline-first, OWASP MASVS, and store readiness.",
      "Listo. Lint y tests libres; dependencias y Fastlane piden confirmación, publicar en tiendas está bloqueado.",
      tools=(R, W, S, WEB),
      write=["ios/**", "android/**", "lib/**", "src/**", "app/**", "test/**", "tests/**", "docs/**"],
      allow=["./gradlew lint*", "./gradlew test*", "./gradlew assembleDebug*", "flutter analyze*", "flutter test*",
             "xcodebuild test*", "xcodebuild -list*", "swiftlint*", "ktlint*", "npm test*", "npx react-native doctor*"],
      ask=["pod install*", "flutter pub get*", "fastlane *"] + INSTALL_ASK,
      deny=["fastlane deliver*", "fastlane supply*", "fastlane pilot upload*"])
agent("refactoring-modernization",
      "Refactors legacy code, prioritizes technical debt, plans framework upgrades, and leads incremental cloud migrations (7 Rs, Strangler Fig).",
      "Listo. Primero tests que protejan el comportamiento, después pasos pequeños y reversibles.",
      write=["src/**", "lib/**", "app/**", "tests/**", "test/**", "docs/**"],
      allow=JS_CHECKS + PY_CHECKS + OTHER_TESTS,
      ask=["npx jscodeshift*", "mvn rewrite:run*", "./gradlew rewriteRun*"] + INSTALL_ASK)
agent("dev-best-practices",
      "Reviews and guides code quality: clean code, SOLID, design patterns, testing, and maintainable architecture.",
      "Listo. Revisemos el código con foco en claridad, diseño y mantenibilidad.",
      write=["src/**", "lib/**", "app/**", "tests/**", "docs/**", "reports/**"],
      allow=JS_CHECKS + PY_CHECKS + OTHER_TESTS + ["golangci-lint run*"])
agent("secure-development",
      "Guides and reviews secure coding: OWASP, input validation, cryptography, secure defaults, and CI/CD security gates.",
      "Listo. Código seguro desde el diseño: muéstrame el módulo o la funcionalidad.",
      tools=(R, W, S, WEB), write=["src/**", "lib/**", "app/**", "tests/**", "docs/**", "reports/**"],
      allow=["semgrep *", "bandit *", "gosec *", "npm audit*", "pip-audit*", "osv-scanner*"] + JS_CHECKS + PY_CHECKS)
agent("genai-aws-practices",
      "Designs and reviews generative AI on AWS: Amazon Bedrock, RAG, agents, guardrails, cost, and responsible AI.",
      "Listo. Listar y describir recursos de Bedrock es libre; invocar modelos (cuesta dinero) pide confirmación.",
      tools=(R, W, S, WEB), write=["src/**", "prompts/**", "infra/**", "docs/**"],
      allow=["aws bedrock list-*", "aws bedrock get-*", "aws bedrock-agent list-*", "aws bedrock-agent get-*"] + TF_READ,
      ask=["aws bedrock-runtime invoke-model*", "aws bedrock-agent-runtime *"])

# Calidad
agent("code-reviewer",
      "Reviews code and pull requests for correctness, security, performance, design, and testability.",
      "Listo. Pásame el diff, el PR o la carpeta y lo reviso con hallazgos priorizados.",
      write=["reports/**", "docs/reviews/**"],
      allow=JS_CHECKS + PY_CHECKS + ["golangci-lint run*", "gh pr view*", "gh pr diff*"])
agent("test-automation",
      "Designs test strategies and writes unit, integration, contract, and E2E tests; finds coverage gaps and flaky tests.",
      "Listo. Los runners de pruebas corren libres; instalar dependencias pide confirmación.",
      write=["tests/**", "test/**", "e2e/**", "__tests__/**", "**/*.test.*", "**/*.spec.*", "**/*_test.*",
             "**/test_*.py", "playwright/**", "cypress/**", "docs/**"],
      allow=JS_CHECKS + PY_CHECKS + OTHER_TESTS + ["npx playwright test*", "npx cypress run*"],
      ask=INSTALL_ASK + ["npx playwright install*"])
agent("performance-engineering",
      "Profiles applications, designs and interprets load tests, defines latency/throughput budgets, and finds bottlenecks.",
      "Listo. Medimos antes de optimizar; las pruebas de carga piden confirmación porque generan tráfico real.",
      write=["perf/**", "load-tests/**", "k6/**", "benchmarks/**", "docs/**", "reports/**"],
      allow=["k6 inspect*"],
      ask=["k6 run*", "locust*", "artillery run*", "gatling*", "jmeter*", "ab *", "hey *", "wrk *"])
agent("debugging-troubleshooting",
      "Finds root causes of errors, stack traces, failing tests, and production issues with a systematic, evidence-based method.",
      "Listo. Pégame el error completo, el stack trace o los logs y buscamos la causa raíz.",
      write=["src/**", "lib/**", "app/**", "tests/**", "test/**", "docs/**"],
      allow=["git bisect*", "git reflog*", "kubectl logs *", "docker ps*", "docker logs *", "docker inspect *",
             "dig *", "nslookup *", "openssl s_client*", "aws logs filter-log-events*", "aws logs get-log-events*",
             "aws logs start-query*", "aws logs get-query-results*", "aws cloudtrail lookup-events*"]
            + K8S_READ + JS_CHECKS + PY_CHECKS + OTHER_TESTS,
      ask=["kubectl exec *", "docker exec *", "kubectl rollout restart*", "curl *"])
agent("accessibility",
      "Audits and fixes web and mobile interfaces against WCAG 2.2 Level AA, with concrete code fixes.",
      "Listo. Auditamos contra WCAG 2.2 AA con herramientas automáticas y revisión manual.",
      tools=(R, W, S, WEB), write=["src/**", "app/**", "components/**", "docs/**", "reports/**"],
      allow=["npx @axe-core/cli*", "npx pa11y*", "npx lighthouse*", "npx eslint*", "npm run lint*", "npx playwright test*"])
agent("yaml-best-practices",
      "Writes and reviews YAML correctly: syntax pitfalls, Kubernetes manifests, CI/CD workflows, and Helm values.",
      "Listo. Valido y corrijo YAML de Kubernetes, CI/CD y Helm.",
      write=["**/*.yaml", "**/*.yml", "docs/**"],
      allow=["yamllint*", "yq *", "kubeconform*", "actionlint*", "helm lint*", "helm template*"])

# Seguridad
agent("sast-security",
      "Static application security testing: data flow, taint tracking, and CWE-mapped findings with fixes.",
      "Listo. Análisis estático de seguridad del código; los hallazgos van a reports/.",
      tools=(R, W, S, WEB), write=["reports/**", "docs/security/**"],
      allow=["semgrep *", "bandit *", "gosec *", "njsscan*", "brakeman*", "codeql *", "npm audit*", "pip-audit*", "osv-scanner*"])
agent("dast-security",
      "Dynamic application security testing of running applications: headers, sessions, input fuzzing, and APIs.",
      "Listo. Solo contra objetivos autorizados: cada escaneo o petición pide confirmación.",
      tools=(R, W, S, WEB), write=["reports/**", "docs/security/**"],
      ask=["zap*", "nuclei*", "nikto*", "curl *", "httpx *", "ffuf *"])
agent("pentest-security",
      "Penetration testing and red-team analysis: attack chains, MITRE ATT&CK, CVSS scoring, and proofs of concept.",
      "Listo. Solo contra objetivos con autorización escrita: toda herramienta activa pide confirmación.",
      tools=(R, W, S, WEB), write=["reports/**"],
      ask=["nmap *", "nuclei*", "sqlmap*", "ffuf*", "gobuster*", "nikto*", "curl *", "hydra*", "msfconsole*"])
agent("security-tester",
      "General application security testing (legacy all-in-one); prefer the specialized SAST, DAST, and pentest agents.",
      "Listo. Agente legacy de seguridad general; para análisis profundos usa SAST, DAST o Pentest.",
      tools=(R, W, S, WEB), write=["reports/**"],
      allow=["semgrep *", "bandit *", "npm audit*", "pip-audit*"], ask=["curl *"])
agent("security-audit",
      "Audits systems against ISO 27001, SOC 2, PCI DSS, and NIST with evidence-based findings.",
      "Listo. Auditoría de solo lectura contra marcos de cumplimiento; la evidencia va a reports/.",
      tools=(R, W, S, WEB), write=["reports/**", "docs/compliance/**"],
      allow=["prowler*", "aws configservice describe-*", "aws configservice get-*", "aws securityhub get-*",
             "aws securityhub describe-*", "aws guardduty list-*", "aws guardduty get-*",
             "aws iam generate-credential-report*", "aws iam get-credential-report*",
             "aws cloudtrail describe-trails*", "aws cloudtrail get-*"])
agent("cloud-security",
      "Assesses cloud security posture on AWS, Azure, and GCP: IAM, network, data protection, and compliance.",
      "Listo. Modo seguro: plan sí, apply no.",
      tools=(R, W, S, WEB), write=["infra/**", "k8s/**", "docs/**", "reports/**"],
      allow=TF_READ + AWS_READ + ["checkov*", "tfsec*", "trivy config*", "prowler*"] + K8S_READ)
agent("least-privilege",
      "Designs and reviews least-privilege access: AWS IAM policies, Kubernetes RBAC, and application-level authorization.",
      "Listo. Analizo permisos en modo lectura; crear o cambiar políticas IAM está bloqueado.",
      write=["infra/**", "iam/**", "policies/**", "k8s/**", "docs/**", "reports/**"],
      allow=["aws iam get-*", "aws iam list-*", "aws iam simulate-*", "aws accessanalyzer validate-policy*",
             "aws accessanalyzer list-*", "aws accessanalyzer get-*", "parliament*"] + K8S_READ + TF_READ,
      deny=["aws iam create-*", "aws iam put-*", "aws iam attach-*", "aws iam update-*", "aws iam detach-*"])
agent("privacy-compliance",
      "Privacy by design and personal data protection: Colombian Law 1581, GDPR, LGPD, CCPA; consent, data subject rights, and retention.",
      "Listo. Revisamos el tratamiento de datos personales; doy guía de ingeniería, no asesoría legal.",
      tools=(R, W, S, WEB), write=["docs/privacy/**", "docs/**", "reports/**"],
      extra_res=["file://docs/privacy/**/*.md"])

# Infraestructura y operación
agent("aws-best-practices",
      "Reviews AWS architectures and configurations against the Well-Architected Framework's six pillars.",
      "Listo. Revisión Well-Architected en modo lectura: plan sí, apply no.",
      tools=(R, W, S, WEB), write=["docs/**", "reports/**", "infra/**"],
      allow=TF_READ + AWS_READ + ["cfn-lint*", "checkov*"])
agent("iac-reviewer",
      "Reviews Terraform, CloudFormation, CDK, Helm, and Ansible for security, correctness, and best practices.",
      "Listo. Modo seguro: validate y plan sí, apply y destroy no.",
      write=["infra/**", "terraform/**", "cloudformation/**", "cdk/**", "helm/**", "charts/**", "ansible/**", "docs/**", "reports/**"],
      allow=TF_READ + ["tflint*", "checkov*", "tfsec*", "trivy config*",
                       "cfn-lint*", "helm lint*", "helm template*", "ansible-lint*"],
      ask=["terraform init*"])
agent("devops-reviewer",
      "Reviews CI/CD pipelines, deployment strategies, and operational practices against DORA metrics and SRE principles.",
      "Listo. Revisamos pipelines y despliegues; nada se dispara sin tu confirmación.",
      write=[".github/**", ".gitlab-ci.yml", "ci/**", "pipelines/**", "docs/**", "reports/**"],
      allow=["actionlint*", "yamllint*", "gh run list*", "gh run view*", "gh workflow list*", "gh workflow view*"],
      ask=["gh workflow run*", "gh run rerun*"])
agent("devsecops-reviewer",
      "Embeds security in the SDLC: pipeline security gates, supply chain (SBOM, SLSA, signing), and compliance-as-code.",
      "Listo. Escáneres de seguridad y supply chain en modo lectura; secretos siempre redactados.",
      write=[".github/**", "ci/**", "pipelines/**", "docs/**", "reports/**"],
      allow=["actionlint*", "gitleaks detect --redact*", "semgrep *", "trivy fs*", "syft *", "grype *",
             "cosign verify*", "osv-scanner*", "npm audit*", "pip-audit*"],
      ask=["gitleaks *", "trufflehog *"])
agent("container-reviewer",
      "Reviews Dockerfiles, container images, and runtime configuration for security and efficiency.",
      "Listo. Analizo Dockerfiles e imágenes; publicar imágenes está bloqueado.",
      write=["reports/**", "docs/**"],
      allow=["hadolint*", "trivy image*", "trivy fs*", "grype *", "syft *", "dockle *", "docker inspect *", "docker history *", "docker images*"])
agent("container-best-practices",
      "Guides container design: 12-factor apps, image building, networking, storage, and registries.",
      "Listo. Diseñamos contenedores de producción; construir pide confirmación, publicar está bloqueado.",
      write=["**/Dockerfile*", "**/.dockerignore", "**/docker-compose*.yml", "**/compose*.yaml", "docs/**"],
      allow=["hadolint*", "docker images*", "docker inspect *", "dive *", "trivy image*"],
      ask=["docker build*", "docker compose up*", "docker run*"],
      deny=["docker rm -f*"])
agent("kubernetes-best-practices",
      "Guides Kubernetes workloads: resources, probes, scaling, networking, storage, and observability.",
      "Listo. kubectl en modo lectura y dry-run; aplicar cambios pide confirmación y borrar está bloqueado.",
      write=["k8s/**", "manifests/**", "helm/**", "charts/**", "kustomize/**", "docs/**"],
      allow=K8S_READ + ["kubectl diff *", "kubectl apply --dry-run*", "kubectl kustomize*", "helm lint*",
                        "helm template*", "kubeconform*", "kube-score*", "polaris audit*", "pluto detect*"],
      ask=["kubectl apply*", "helm upgrade*", "helm install*", "kubectl rollout*", "kubectl scale*"],
      deny=["kubectl drain*", "kubectl cordon*"])
agent("kubernetes-security",
      "Analyzes Kubernetes attack vectors, kill chains, detection, and response for clusters and workloads.",
      "Listo. Análisis de seguridad del clúster en modo lectura; leer Secrets y exec están bloqueados.",
      tools=(R, W, S, WEB), write=["reports/**", "docs/**"],
      allow=K8S_READ + ["kubescape scan*", "trivy k8s*", "kube-bench*", "rbac-tool*", "kubectl-who-can*"],
      deny=["kubectl exec *", "kubectl cp *"])
agent("observability-sre",
      "Designs logs, metrics, and traces (OpenTelemetry), SLOs and error budgets, actionable alerting, and incident response.",
      "Listo. Consultas de métricas y logs libres; borrar alarmas o logs está bloqueado.",
      write=["observability/**", "monitoring/**", "dashboards/**", "alerts/**", "runbooks/**", "infra/**", "docs/**"],
      allow=["promtool check*", "amtool check-config*", "aws cloudwatch describe-alarms*", "aws cloudwatch get-metric-data*",
             "aws cloudwatch list-*", "aws logs describe-*", "aws logs start-query*", "aws logs get-query-results*",
             "aws xray get-*"] + K8S_READ + TF_READ,
      deny=["aws cloudwatch delete-*", "aws logs delete-*"])
agent("release-management",
      "Defines branching, commit and PR conventions, semantic versioning, changelogs, and release plans; recovers Git history safely.",
      "Listo. Git de lectura es libre; commits, tags, push y merges piden confirmación, y force-push está bloqueado.",
      write=["CHANGELOG.md", "RELEASE*.md", ".github/**", "docs/**"],
      allow=["git fetch*", "git reflog*", "git shortlog*", "git tag -l*", "gh pr view*", "gh pr list*",
             "gh release view*", "gh release list*"],
      ask=["git tag *", "git cherry-pick*", "git revert*", "git filter-repo*", "gh pr create*", "gh pr merge*",
           "gh release create*", "npx semantic-release*"],
      extra_res=["file://CHANGELOG.md", "file://CONTRIBUTING.md"])
agent("finops-cost-optimization",
      "Finds cloud cost savings: cost visibility and tagging, right-sizing, Savings Plans, waste removal, and cost-aware design.",
      "Listo. Solo lectura de costos y uso; ningún recurso se modifica desde aquí.",
      tools=(R, W, S, WEB), write=["reports/**", "docs/**", "infra/**", "terraform/**"],
      allow=["aws ce get-*", "aws compute-optimizer get-*", "aws budgets describe-*", "aws pricing get-*",
             "aws cloudwatch get-metric-statistics*", "aws cloudwatch get-metric-data*", "infracost *"] + AWS_READ + TF_READ,
      deny=["aws * modify-*", "aws * stop-*", "aws * put-*", "aws * create-*", "aws * update-*"])

# Documentación
agent("dev-documentation",
      "Writes and reviews technical documentation: READMEs, ADRs, API docs, runbooks, and changelogs (Diátaxis).",
      "Listo. Escribo y reviso documentación técnica; solo toco archivos de documentación.",
      tools=(R, W, S, WEB), write=["docs/**", "**/README.md", "README*.md", "CHANGELOG.md", "CONTRIBUTING.md", "adr/**"],
      allow=["npx markdownlint*", "markdownlint*", "vale *", "npx @redocly/cli lint*"],
      extra_res=["file://CONTRIBUTING.md", "file://CHANGELOG.md"])

# ─── Ciberseguridad especializada ──────────────────────────────────────────────
agent("threat-modeling",
      "Builds threat models with STRIDE, PASTA, and LINDDUN: data flow diagrams, trust boundaries, risk-rated threats, and testable security requirements.",
      "Listo. Cuéntame el sistema o la funcionalidad y modelamos sus amenazas antes de construir.",
      tools=(R, W, S, WEB), write=["docs/security/**", "docs/threat-models/**", "threat-models/**", "docs/**"],
      extra_res=["file://docs/threat-models/**/*.md"])
agent("incident-response",
      "Guides security incident response and forensics (DFIR): triage, containment, evidence preservation, eradication, recovery, and post-incident review.",
      "Listo. Primero contener y preservar evidencia: cuéntame qué detectaste. Todo comando que cambie algo pide confirmación.",
      tools=(R, W, S, WEB), write=["incidents/**", "reports/**", "docs/**"],
      allow=["aws cloudtrail lookup-events*", "aws guardduty list-*", "aws guardduty get-*", "aws securityhub get-*",
             "aws logs start-query*", "aws logs get-query-results*", "aws logs filter-log-events*",
             "aws iam get-*", "aws iam list-*", "aws sts get-caller-identity*"] + K8S_READ + ["kubectl logs *"],
      ask=["aws iam update-access-key*", "aws iam delete-login-profile*", "aws iam put-role-policy*",
           "aws ec2 modify-instance-attribute*", "aws ec2 create-snapshot*", "aws ec2 stop-instances*",
           "kubectl cordon *", "kubectl label *"])
agent("secrets-management",
      "Finds and eliminates exposed secrets and designs secret storage, delivery, and rotation with Secrets Manager, Vault, Key Vault, and workload identity.",
      "Listo. Escaneo secretos siempre redactados; nunca muestro ni repito un valor secreto.",
      tools=(R, W, S, WEB), write=["infra/**", "k8s/**", "docs/**", "reports/**", ".github/**"],
      allow=["gitleaks detect --redact*", "trufflehog * --no-verification*", "detect-secrets scan*",
             "aws secretsmanager list-secrets*", "aws secretsmanager describe-secret*"] + TF_READ,
      ask=["aws secretsmanager rotate-secret*", "aws iam update-access-key*"],
      deny=["aws secretsmanager put-secret-value*", "trufflehog * --no-redact*"])
agent("supply-chain-security",
      "Secures the software supply chain: dependency risk, SBOMs, SLSA provenance, artifact signing, CI/CD hardening, and base image hygiene.",
      "Listo. Analizo dependencias, pipelines y artefactos; publicar o firmar artefactos pide confirmación.",
      tools=(R, W, S, WEB), write=[".github/**", "ci/**", "docs/**", "reports/**"],
      allow=["syft *", "grype *", "osv-scanner*", "npm audit*", "pip-audit*", "govulncheck*", "trivy fs*", "trivy image*",
             "cosign verify*", "scorecard *", "actionlint*"],
      ask=["cosign sign*", "cosign attest*"])
agent("vulnerability-management",
      "Prioritizes and tracks vulnerability remediation with CVSS, EPSS, CISA KEV, exposure, and asset criticality; defines SLAs and program metrics.",
      "Listo. Paso de miles de hallazgos a una lista corta de qué arreglar primero y por qué.",
      tools=(R, W, S, WEB), write=["reports/**", "docs/**"],
      allow=["trivy *", "grype *", "osv-scanner*", "aws inspector2 list-*", "aws inspector2 get-*",
             "aws securityhub get-*", "aws ssm describe-instance-patch*", "aws ssm list-*"])
agent("waf-ddos-protection",
      "Designs and tunes WAF rules, rate limiting, bot management, and DDoS resilience on AWS WAF/Shield, CloudFront, Cloudflare, Front Door, and Cloud Armor.",
      "Listo. Reglas nuevas siempre primero en modo count; bloquear tráfico real pide confirmación.",
      tools=(R, W, S, WEB), write=["infra/**", "terraform/**", "docs/**", "reports/**"],
      allow=["aws wafv2 list-*", "aws wafv2 get-*", "aws wafv2 describe-*", "aws shield describe-*", "aws shield list-*",
             "aws cloudfront list-*", "aws cloudfront get-*", "aws logs start-query*", "aws logs get-query-results*"] + TF_READ,
      ask=["aws wafv2 update-*", "aws wafv2 create-*", "aws wafv2 associate-*"])
agent("detection-engineering",
      "Builds security detections as code (Sigma, KQL, SPL, CloudWatch Logs Insights) mapped to MITRE ATT&CK, tested with attack simulation and tuned for low noise.",
      "Listo. Detecciones como código, mapeadas a ATT&CK y probadas; las simulaciones de ataque piden confirmación.",
      tools=(R, W, S, WEB), write=["detections/**", "rules/**", "sigma/**", "docs/**", "reports/**"],
      allow=["sigma check*", "sigma convert*", "aws logs start-query*", "aws logs get-query-results*",
             "aws cloudtrail lookup-events*", "aws guardduty list-*", "aws guardduty get-*"],
      ask=["stratus *", "atomic-red-team*", "Invoke-AtomicTest*"])
agent("network-security",
      "Designs and reviews network segmentation, firewalls, private connectivity, egress control, and zero trust access for cloud and hybrid environments.",
      "Listo. Analizo exposición y movimiento lateral en modo lectura: plan sí, apply no.",
      tools=(R, W, S, WEB), write=["infra/**", "terraform/**", "k8s/**", "docs/**", "reports/**"],
      allow=["aws ec2 describe-*", "aws network-firewall describe-*", "aws network-firewall list-*",
             "aws route53resolver list-*", "aws ec2 start-network-insights-analysis*",
             "aws ec2 describe-network-insights-*"] + TF_READ + K8S_READ,
      deny=["aws ec2 authorize-security-group-ingress*", "aws ec2 revoke-security-group-*"])
agent("cryptography-encryption",
      "Reviews and guides applied cryptography: algorithm choices, authenticated encryption, password hashing, KMS key hierarchies, rotation, and post-quantum readiness.",
      "Listo. Revisamos cifrado, hashing, firmas y gestión de llaves; nunca criptografía casera.",
      tools=(R, W, S, WEB), write=["src/**", "lib/**", "infra/**", "docs/**", "reports/**"],
      allow=["aws kms list-*", "aws kms describe-key*", "aws kms get-key-policy*", "aws kms get-key-rotation-status*",
             "openssl s_client*", "openssl x509*", "semgrep *"] + TF_READ,
      deny=["aws kms schedule-key-deletion*", "aws kms disable-key*", "aws kms decrypt*"])
agent("pki-certificates",
      "Manages PKI and TLS: certificate inventory, automated renewal, CA hierarchies, TLS/mTLS configuration, and expiry monitoring.",
      "Listo. Inventario y revisión de certificados y TLS; emitir o revocar certificados pide confirmación.",
      tools=(R, W, S, WEB), write=["infra/**", "k8s/**", "docs/**", "reports/**"],
      allow=["openssl s_client*", "openssl x509*", "openssl verify*", "testssl*", "aws acm list-*", "aws acm describe-*",
             "aws acm-pca list-*", "aws acm-pca describe-*", "kubectl get certificate*", "kubectl describe certificate*"]
            + K8S_READ,
      ask=["aws acm request-certificate*", "aws acm-pca issue-certificate*", "aws acm-pca revoke-certificate*",
           "certbot *", "cmctl renew*"],
      deny=["aws acm delete-certificate*", "aws acm-pca delete-*"])
agent("ai-llm-security",
      "Secures LLM, RAG, and agent applications against the OWASP Top 10 for LLMs: prompt injection, excessive agency, data leakage, and unsafe output handling.",
      "Listo. Tratamos toda salida del modelo como no confiable; las pruebas de red team piden confirmación.",
      tools=(R, W, S, WEB), write=["src/**", "prompts/**", "tests/**", "docs/**", "reports/**"],
      allow=["semgrep *"] + PY_CHECKS + JS_CHECKS,
      ask=["garak *", "promptfoo *", "pyrit *"])

# ─── IAM ───────────────────────────────────────────────────────────────────────
agent("identity-federation-sso",
      "Designs and reviews authentication, SSO, and federation with OAuth 2.0, OIDC, SAML, passkeys, and IdPs such as Entra ID, Okta, Cognito, and IAM Identity Center.",
      "Listo. Revisamos flujos de login, tokens y MFA; los cambios en el IdP no se hacen desde aquí.",
      tools=(R, W, S, WEB), write=["src/**", "infra/**", "docs/**", "reports/**"],
      allow=["aws cognito-idp describe-*", "aws cognito-idp list-*", "aws sso-admin list-*", "aws sso-admin describe-*",
             "aws identitystore list-*"] + TF_READ + JS_CHECKS,
      deny=["aws cognito-idp admin-*", "aws cognito-idp delete-*", "aws sso-admin delete-*"])
agent("aws-organizations-iam",
      "Designs AWS organization-wide permission guardrails: SCPs, RCPs, data perimeters, permission boundaries, Identity Center permission sets, and Access Analyzer.",
      "Listo. Analizo guardrails y permisos en modo lectura; aplicar SCPs o cambiar IAM está bloqueado.",
      tools=(R, W, S, WEB), write=["infra/**", "policies/**", "scp/**", "terraform/**", "docs/**", "reports/**"],
      allow=["aws organizations describe-*", "aws organizations list-*", "aws iam get-*", "aws iam list-*",
             "aws iam simulate-*", "aws accessanalyzer validate-policy*", "aws accessanalyzer list-*",
             "aws accessanalyzer get-*", "aws accessanalyzer check-*", "aws sso-admin list-*",
             "aws sso-admin describe-*"] + TF_READ,
      deny=["aws organizations attach-policy*", "aws organizations detach-policy*", "aws organizations create-*",
            "aws organizations update-*", "aws organizations move-account*", "aws iam create-*", "aws iam put-*",
            "aws iam attach-*", "aws iam update-*"])
agent("identity-governance",
      "Designs identity governance: joiner-mover-leaver processes, role models, access requests, periodic access reviews, segregation of duties, and privileged access management.",
      "Listo. Diseñamos el ciclo de vida de accesos y las revisiones periódicas con evidencia para auditoría.",
      tools=(R, W, WEB), write=["docs/**", "reports/**", "policies/**"])

# ─── FinOps especializado ──────────────────────────────────────────────────────
agent("tagging-governance",
      "Designs and enforces cloud tagging and cost allocation: tag dictionaries, tag policies, IaC defaults, Cost Categories, shared cost splits, and showback.",
      "Listo. Medimos la asignación de costos por porcentaje del gasto y la hacemos obligatoria por código.",
      tools=(R, W, S, WEB), write=["infra/**", "terraform/**", "policies/**", "docs/**", "reports/**"],
      allow=["aws ce get-*", "aws ce list-*", "aws resourcegroupstaggingapi get-*", "aws organizations describe-*",
             "aws organizations list-*"] + TF_READ,
      deny=["aws organizations attach-policy*", "aws organizations create-policy*", "aws * tag-resource*",
            "aws * untag-resource*"])
agent("commitment-management",
      "Optimizes cloud rates with Savings Plans, Reserved Instances, and committed use discounts: coverage, utilization, laddered purchase plans, and expiration tracking.",
      "Listo. Solo análisis: ninguna compra de compromisos se hace desde aquí.",
      tools=(R, W, S, WEB), write=["reports/**", "docs/**"],
      allow=["aws ce get-*", "aws savingsplans describe-*", "aws ec2 describe-reserved-instances*",
             "aws rds describe-reserved-*", "aws elasticache describe-reserved-*"],
      deny=["aws savingsplans create-*", "aws ec2 purchase-*", "aws rds purchase-*", "aws elasticache purchase-*",
            "aws * purchase-*"])
agent("kubernetes-finops",
      "Optimizes Kubernetes costs: request right-sizing, autoscaling, Karpenter/Spot/Graviton node strategy, idle capacity, and cost allocation by namespace and team.",
      "Listo. Analizo costos del clúster en modo lectura; aplicar cambios a los workloads pide confirmación.",
      tools=(R, W, S, WEB), write=["k8s/**", "manifests/**", "helm/**", "charts/**", "docs/**", "reports/**"],
      allow=K8S_READ + ["kubectl get --raw /apis/metrics.k8s.io*", "aws ce get-*", "helm template*", "helm lint*"],
      ask=["kubectl apply*", "kubectl scale*", "kubectl patch*", "helm upgrade*"],
      deny=["kubectl drain*", "kubectl cordon*"])
agent("cloud-cost-forecasting",
      "Forecasts and budgets cloud spend with driver-based models, explains variances, sets budgets and anomaly alerts, and tracks unit economics.",
      "Listo. Pronósticos con rangos y supuestos explícitos; crear presupuestos o alertas pide confirmación.",
      tools=(R, W, S, WEB), write=["reports/**", "docs/**", "forecasts/**"],
      allow=["aws ce get-*", "aws ce list-*", "aws budgets describe-*", "aws ce get-anomalies*"],
      ask=["aws budgets create-*", "aws budgets update-*", "aws ce create-anomaly-*"],
      deny=["aws budgets delete-*", "aws ce delete-*"])
agent("genai-finops",
      "Makes generative AI economically sustainable: cost per request and feature, model routing, prompt caching, batching, context reduction, and spending guardrails.",
      "Listo. Medimos costo por tarea y lo reducimos sin bajar la calidad; invocar modelos pide confirmación.",
      tools=(R, W, S, WEB), write=["reports/**", "docs/**", "prompts/**", "src/**"],
      allow=["aws ce get-*", "aws bedrock list-*", "aws bedrock get-*", "aws cloudwatch get-metric-data*",
             "aws cloudwatch get-metric-statistics*"],
      ask=["aws bedrock-runtime invoke-model*", "aws bedrock-runtime converse*"])

# ─── Cloud ─────────────────────────────────────────────────────────────────────
AZ_READ = ["az account show*", "az account list*", "az group list*", "az resource list*", "az * show*", "az * list*",
           "az policy * list*", "az bicep build*", "az deployment * what-if*"]
GCP_READ = ["gcloud config list*", "gcloud projects list*", "gcloud * list*", "gcloud * describe*",
            "gcloud asset search-all-*"]
agent("azure-architect",
      "Designs and reviews Microsoft Azure workloads and landing zones with the Azure Well-Architected Framework, Azure Policy, Entra ID, and Bicep/Terraform.",
      "Listo. Lectura y what-if de Azure libres; desplegar o borrar recursos está bloqueado o pide confirmación.",
      tools=(R, W, S, WEB), write=["infra/**", "bicep/**", "terraform/**", "docs/**", "reports/**"],
      allow=AZ_READ + TF_READ + ["bicep build*", "bicep lint*"],
      ask=["az deployment * create*", "az group create*"],
      deny=["az * delete*", "az group delete*", "az keyvault secret show*"])
agent("gcp-architect",
      "Designs and reviews Google Cloud workloads with the Architecture Framework: resource hierarchy, org policies, IAM, VPC Service Controls, and Terraform.",
      "Listo. Lectura de Google Cloud libre; crear o borrar recursos está bloqueado o pide confirmación.",
      tools=(R, W, S, WEB), write=["infra/**", "terraform/**", "docs/**", "reports/**"],
      allow=GCP_READ + TF_READ,
      ask=["gcloud * create*", "gcloud * update*", "gcloud * deploy*"],
      deny=["gcloud * delete*", "gcloud secrets versions access*", "gcloud iam service-accounts keys create*"])
agent("ibm-cloud-architect",
      "Designs and reviews IBM Cloud workloads: VPC, Red Hat OpenShift, Code Engine, IBM Cloud Databases, Key Protect/HPCS, and the Framework for Financial Services.",
      "Listo. Lectura de IBM Cloud libre; cambios en recursos piden confirmación y borrar está bloqueado.",
      tools=(R, W, S, WEB), write=["infra/**", "terraform/**", "docs/**", "reports/**"],
      allow=["ibmcloud target*", "ibmcloud resource * list*", "ibmcloud is * list*", "ibmcloud is *s", "ibmcloud iam * list*",
             "ibmcloud ks cluster ls*", "ibmcloud oc cluster ls*"] + TF_READ,
      ask=["ibmcloud * create*", "ibmcloud * update*"],
      deny=["ibmcloud * delete*", "ibmcloud * rm *"])
agent("oci-architect",
      "Designs and reviews Oracle Cloud Infrastructure workloads: compartments, IAM policies, networking, Autonomous Database and Exadata, licensing, and Terraform.",
      "Listo. Lectura de OCI libre; cambios en recursos piden confirmación y borrar está bloqueado.",
      tools=(R, W, S, WEB), write=["infra/**", "terraform/**", "docs/**", "reports/**"],
      allow=["oci iam * list*", "oci iam * get*", "oci network * list*", "oci compute * list*", "oci db * list*",
             "oci db * get*"] + TF_READ,
      ask=["oci * create*", "oci * update*"],
      deny=["oci * delete*", "oci * terminate*", "oci secrets secret-bundle get*"])
agent("multi-cloud-strategy",
      "Advises on multi-cloud and hybrid strategy: when it is justified, workload placement, service mapping across AWS/Azure/GCP/OCI/IBM, and cross-cloud foundations.",
      "Listo. Multicloud solo cuando un motivo concreto justifica su costo; lo analizamos con criterios explícitos.",
      tools=(R, W, WEB), write=["docs/**", "reports/**"])
agent("aws-landing-zone",
      "Designs and reviews AWS multi-account landing zones: Organizations OUs, Control Tower, Account Factory, centralized logging and security, and account baselines.",
      "Listo. Revisión de la base multi-cuenta en modo lectura; cambios a la organización están bloqueados.",
      tools=(R, W, S, WEB), write=["infra/**", "terraform/**", "aft/**", "customizations/**", "docs/**", "reports/**"],
      allow=["aws organizations describe-*", "aws organizations list-*", "aws controltower list-*",
             "aws controltower get-*", "aws servicecatalog list-*", "aws servicecatalog describe-*"] + AWS_READ + TF_READ,
      deny=["aws organizations create-*", "aws organizations move-account*", "aws organizations remove-*",
            "aws organizations attach-policy*", "aws controltower disable-*", "aws controltower reset-*"])
agent("aws-serverless",
      "Designs, builds, and reviews serverless applications on AWS Lambda, API Gateway, Step Functions, EventBridge, SQS/SNS, and DynamoDB.",
      "Listo. Build, validate y tests locales libres; deploy pide confirmación y borrar stacks está bloqueado.",
      tools=(R, W, S, WEB), write=["src/**", "functions/**", "lib/**", "infra/**", "template.yaml", "tests/**", "docs/**"],
      allow=["sam validate*", "sam build*", "sam local *", "cdk synth*", "cdk diff*", "cfn-lint*",
             "aws lambda get-*", "aws lambda list-*", "aws stepfunctions describe-*", "aws stepfunctions list-*",
             "aws events list-*", "aws events describe-*", "aws sqs get-queue-attributes*", "aws sqs list-*"]
            + JS_CHECKS + PY_CHECKS + TF_READ,
      ask=["sam deploy*", "cdk deploy*", "aws lambda invoke*", "aws lambda update-*", "aws sqs send-message*"],
      deny=["sam delete*", "cdk destroy*", "aws cloudformation delete-stack*", "aws sqs purge-queue*"])
agent("aws-networking",
      "Designs and troubleshoots AWS networking: VPC and IPAM, Transit Gateway, Cloud WAN, Direct Connect, VPN, PrivateLink, Route 53, and load balancing.",
      "Listo. Diagnóstico de red en modo lectura: plan sí, apply no.",
      tools=(R, W, S, WEB), write=["infra/**", "terraform/**", "network/**", "docs/**", "reports/**"],
      allow=["aws ec2 describe-*", "aws ec2 get-*", "aws ec2 search-transit-gateway-routes*",
             "aws ec2 start-network-insights-analysis*", "aws networkmanager get-*", "aws networkmanager list-*",
             "aws directconnect describe-*", "aws route53 list-*", "aws route53 get-*", "aws route53resolver list-*",
             "aws elbv2 describe-*", "dig *", "nslookup *", "traceroute *", "mtr *"] + TF_READ,
      deny=["aws ec2 delete-*", "aws ec2 replace-route*", "aws route53 change-resource-record-sets*",
            "aws directconnect delete-*"])
agent("aws-migration-map",
      "Leads migrations to AWS with the MAP methodology: discovery, business case, 7 Rs per workload, wave planning, MGN/DMS tooling, and cutover runbooks.",
      "Listo. Planeamos la migración por olas con rollback probado; las acciones sobre la replicación piden confirmación.",
      tools=(R, W, S, WEB), write=["docs/**", "reports/**", "migration/**", "infra/**"],
      allow=["aws mgn describe-*", "aws dms describe-*", "aws discovery describe-*", "aws discovery list-*",
             "aws migrationhub-strategy get-*", "aws migrationhub-strategy list-*"] + TF_READ,
      ask=["aws mgn start-*", "aws mgn launch-*", "aws dms start-*", "aws mgn finalize-cutover*"],
      deny=["aws mgn delete-*", "aws dms delete-*"])
agent("disaster-recovery",
      "Designs disaster recovery and business continuity: RTO/RPO per process, DR strategies, ransomware-resilient backups, failover, and recovery testing.",
      "Listo. Un backup que nunca se restauró no cuenta: diseñamos y probamos la recuperación. Los failover piden confirmación.",
      tools=(R, W, S, WEB), write=["docs/**", "runbooks/**", "infra/**", "terraform/**", "reports/**"],
      allow=["aws backup list-*", "aws backup describe-*", "aws backup get-*", "aws drs describe-*",
             "aws route53-recovery-readiness get-*", "aws rds describe-*", "aws dynamodb describe-*"] + TF_READ,
      ask=["aws backup start-restore-job*", "aws backup start-backup-job*", "aws drs start-recovery*",
           "aws route53-recovery-cluster update-routing-control-state*", "aws rds failover-*"],
      deny=["aws backup delete-*", "aws drs delete-*", "aws rds delete-*"])

# ─── Arquitectura ──────────────────────────────────────────────────────────────
agent("presales-solutions-architect",
      "Turns client problems and RFPs into proposals: discovery questions, solution options, scope with assumptions and exclusions, effort and cloud cost estimates, and plan.",
      "Listo. Pásame la necesidad del cliente o el RFP y armamos una propuesta realista y defendible.",
      tools=(R, W, WEB), write=["docs/**", "proposals/**", "reports/**"],
      extra_res=["file://docs/proposals/**/*.md"])
agent("event-driven-architecture",
      "Designs event-driven and asynchronous systems: event modeling, brokers and topologies, outbox, idempotency, sagas, schema evolution, and tracing.",
      "Listo. Diseñamos eventos que sobreviven a duplicados, desorden y fallas parciales.",
      tools=(R, W, S, WEB), write=["docs/**", "schemas/**", "asyncapi/**", "**/asyncapi.yaml"],
      allow=["npx @asyncapi/cli validate*", "asyncapi validate*"])
agent("microservices-architecture",
      "Designs and reviews microservice architectures: when to use them, service boundaries, data ownership, communication, resilience, and distributed-monolith detection.",
      "Listo. Microservicios solo cuando se justifican; revisamos límites, datos y acoplamiento.",
      tools=(R, W, S, WEB), write=["docs/**", "docs/architecture/**", "docs/adr/**"],
      extra_res=["file://docs/architecture/**/*.md"])
agent("enterprise-architecture",
      "Connects business strategy to technology: capability maps, application portfolio rationalization, target architectures, roadmaps, principles, and governance.",
      "Listo. Partimos de capacidades de negocio y llegamos a un roadmap con valor, costo y dependencias.",
      tools=(R, W, WEB), write=["docs/**", "reports/**"])
agent("platform-engineering",
      "Builds internal developer platforms: golden paths, service templates, developer portals (Backstage), self-service infrastructure, and guardrails as code.",
      "Listo. Hacemos que el camino seguro sea también el más fácil para los equipos.",
      tools=(R, W, S, WEB),
      write=["templates/**", "platform/**", "catalog-info.yaml", "**/catalog-info.yaml", ".github/**", "modules/**",
             "infra/**", "docs/**"],
      allow=TF_READ + ["helm lint*", "helm template*", "kubeconform*", "actionlint*", "npx @backstage/cli*"],
      ask=["argocd app sync*", "kubectl apply*"])

# ─── Desarrollo por lenguaje y especialidad ────────────────────────────────────
agent("python-developer",
      "Writes and reviews idiomatic, typed, tested modern Python: FastAPI, Django, Flask, Pydantic, SQLAlchemy, asyncio, pytest, Ruff, and mypy.",
      "Listo. Ruff, mypy y pytest corren libres; instalar dependencias pide confirmación.",
      write=["src/**", "app/**", "tests/**", "pyproject.toml", "docs/**"],
      allow=PY_CHECKS + ["ruff format*", "uv run pytest*", "uv run ruff*", "poetry run pytest*", "pip-audit*"],
      ask=INSTALL_ASK + ["uv add*", "uv sync*", "poetry install*"])
agent("typescript-node-developer",
      "Writes and reviews strictly typed TypeScript and Node.js services: Express, Fastify, NestJS, Prisma/Drizzle, Zod, Vitest, and AWS SDK v3.",
      "Listo. tsc, ESLint y tests corren libres; instalar dependencias pide confirmación.",
      write=["src/**", "lib/**", "tests/**", "test/**", "package.json", "tsconfig*.json", "docs/**"],
      allow=JS_CHECKS + ["npm audit*"], ask=INSTALL_ASK)
agent("java-spring-developer",
      "Writes and reviews modern Java (17/21) and Spring Boot services: JPA and transactions, Spring Security, resilience, observability, and testing.",
      "Listo. Compilar y probar con Maven/Gradle es libre; publicar artefactos está bloqueado.",
      write=["src/**", "pom.xml", "build.gradle*", "settings.gradle*", "docs/**"],
      allow=["mvn test*", "mvn verify*", "mvn compile*", "mvn -q test*", "./mvnw test*", "./mvnw verify*",
             "./gradlew test*", "./gradlew build*", "./gradlew check*"],
      ask=["mvn install*", "./mvnw install*", "./gradlew bootRun*", "mvn spring-boot:run*"],
      deny=["mvn deploy*", "./mvnw deploy*", "./gradlew publish*"])
agent("dotnet-developer",
      "Writes and reviews modern C# and .NET: ASP.NET Core APIs, async correctness, dependency injection, Entity Framework Core, and testing.",
      "Listo. dotnet build y test corren libres; publicar paquetes está bloqueado.",
      write=["src/**", "tests/**", "*.sln", "**/*.csproj", "docs/**"],
      allow=["dotnet build*", "dotnet test*", "dotnet format --verify-no-changes*", "dotnet list package*"],
      ask=["dotnet add package*", "dotnet restore*", "dotnet ef migrations add*", "dotnet run*"],
      deny=["dotnet nuget push*", "dotnet ef database drop*"])
agent("go-developer",
      "Writes and reviews simple, explicit, concurrent Go: error handling, goroutine lifecycles, context, HTTP servers, testing with the race detector.",
      "Listo. go test -race, vet y golangci-lint corren libres.",
      write=["cmd/**", "internal/**", "pkg/**", "go.mod", "go.sum", "docs/**"],
      allow=["go test*", "go vet*", "go build*", "gofmt -l*", "golangci-lint run*", "staticcheck*", "govulncheck*"],
      ask=["go get *", "go mod tidy*", "go run *"])
agent("ai-agent-developer",
      "Builds production LLM applications: prompt and context engineering, tool design, RAG, agent loops, MCP servers, evaluations, and observability.",
      "Listo. Empezamos por el patrón más simple que resuelva la tarea; llamar modelos pide confirmación.",
      tools=(R, W, S, WEB), write=["src/**", "agents/**", "prompts/**", "evals/**", "tests/**", "docs/**"],
      allow=JS_CHECKS + PY_CHECKS,
      ask=INSTALL_ASK + ["aws bedrock-runtime *", "promptfoo eval*"])
agent("ui-ux-design",
      "Designs and reviews user flows, information architecture, interfaces, and design systems with tokens and components ready for implementation.",
      "Listo. Revisamos flujos y pantallas con heurísticas y entregamos guía lista para implementar.",
      tools=(R, W, WEB), write=["docs/**", "design/**", "src/styles/**", "tokens/**", "**/*.stories.*"])
agent("shell-scripting-automation",
      "Writes and reviews robust Bash, POSIX sh, and PowerShell automation: strict mode, quoting, idempotency, dry-run, ShellCheck-clean scripts.",
      "Listo. ShellCheck y dry-runs libres; ejecutar scripts que cambian sistemas pide confirmación.",
      write=["scripts/**", "bin/**", "**/*.sh", "**/*.ps1", "Makefile", "justfile", "Taskfile.yml", "docs/**"],
      allow=["shellcheck *", "shfmt -d*", "shfmt -l*", "bash -n *", "Invoke-ScriptAnalyzer*"],
      ask=["bash *", "sh *", "./*.sh*", "pwsh *", "make *"])
agent("linux-administration",
      "Administers, troubleshoots, and hardens Linux servers: systemd, performance diagnostics, CIS hardening, SSH/SSM access, and Ansible automation.",
      "Listo. Diagnóstico con comandos de solo lectura; todo cambio al sistema pide confirmación y sudo está bloqueado.",
      tools=(R, W, S, WEB), write=["ansible/**", "playbooks/**", "roles/**", "scripts/**", "docs/**", "runbooks/**"],
      allow=["uptime*", "vmstat *", "iostat *", "mpstat *", "pidstat *", "free *", "df *", "du -sh *", "ss -*",
             "ip a*", "ip r*", "journalctl *", "systemctl status *", "systemctl list-*", "dmesg*", "lsblk*",
             "ansible-lint*", "ansible-playbook * --check*", "ansible-inventory --list*"],
      ask=["systemctl restart *", "systemctl stop *", "systemctl enable *", "ansible-playbook *", "kill *"])

# ─── Datos e IA ────────────────────────────────────────────────────────────────
agent("mlops-engineering",
      "Takes ML models to reliable production: reproducible pipelines, feature stores, model registry, deployment patterns, and drift monitoring.",
      "Listo. Pipelines reproducibles y modelos con rollback; lanzar entrenamientos o endpoints pide confirmación.",
      tools=(R, W, S, WEB), write=["pipelines/**", "src/**", "notebooks/**", "tests/**", "infra/**", "docs/**"],
      allow=PY_CHECKS + ["aws sagemaker list-*", "aws sagemaker describe-*", "mlflow models list*", "dvc status*", "dvc diff*"],
      ask=["aws sagemaker create-*", "aws sagemaker start-*", "aws sagemaker update-endpoint*", "dvc push*", "dvc repro*"],
      deny=["aws sagemaker delete-*"])
agent("analytics-bi",
      "Defines trustworthy KPIs and semantic models and designs decision-oriented dashboards in QuickSight, Power BI, Looker, Tableau, and Metabase.",
      "Listo. Cada métrica con definición precisa y dueño; las consultas pesadas piden confirmación.",
      tools=(R, W, S, WEB), write=["models/**", "sql/**", "dashboards/**", "semantic/**", "docs/**"],
      allow=["dbt compile*", "dbt parse*", "dbt test*", "sqlfluff lint*", "aws quicksight list-*", "aws quicksight describe-*"],
      ask=["aws athena start-query-execution*", "bq query*", "dbt run*"])

# ─── Gestión y liderazgo ───────────────────────────────────────────────────────
agent("project-manager",
      "Plans and controls technology projects: charter, WBS, schedule, scope changes, RAID log, budget, stakeholder communication, and honest status reports.",
      "Listo. Armamos plan, RAID y reportes de estado honestos con decisiones claras.",
      tools=(R, W, WEB), write=["docs/**", "project/**", "reports/**"])
agent("scrum-master",
      "Facilitates Scrum and Kanban: effective events, flow metrics, Monte Carlo forecasts, retrospectives, impediment removal, and team coaching.",
      "Listo. Mejoramos el flujo del equipo con experimentos pequeños y medibles.",
      tools=(R, W, WEB), write=["docs/**", "reports/**", "team/**"])
agent("product-owner",
      "Maximizes product value: product goal and roadmap, discovery, ordered backlog, user stories, prioritization (WSJF/RICE), and outcome metrics.",
      "Listo. Conectamos estrategia, usuarios y backlog con métricas de resultado.",
      tools=(R, W, WEB), write=["docs/**", "product/**", "backlog/**"],
      extra_res=["file://docs/product/**/*.md"])
agent("engineering-manager",
      "Advises engineering managers on people and teams: one-on-ones, feedback, growth and performance, hiring and onboarding, team design, and delivery health.",
      "Listo. Consejos concretos con guiones y plantillas, con respeto y confidencialidad.",
      tools=(R, W, WEB), write=["docs/**"])
agent("tech-lead",
      "Leads a team's technical direction: RFCs and ADRs, work breakdown into vertical slices, engineering standards, code review culture, and technical risk.",
      "Listo. Armamos el plan técnico, el RFC y el desglose del trabajo para el equipo.",
      tools=(R, W, S, WEB), write=["docs/**", "docs/rfcs/**", "docs/adr/**", "CONTRIBUTING.md"],
      extra_res=["file://CONTRIBUTING.md", "file://docs/adr/**/*.md"])
agent("technology-strategy",
      "Advises CTOs and CIOs on strategic technology decisions: build vs buy, platform bets, AI adoption, organization design, budgets, and board communication.",
      "Listo. Decisiones estratégicas con opciones, costos, riesgos y reversibilidad.",
      tools=(R, W, WEB), write=["docs/**", "reports/**"])
agent("software-estimation",
      "Produces honest software estimates: work breakdown including hidden work, three-point/PERT and analogous techniques, risk contingency, and confidence ranges.",
      "Listo. Estimaciones como rangos con nivel de confianza y supuestos explícitos.",
      tools=(R, W, WEB), write=["docs/**", "estimates/**", "proposals/**", "reports/**"])

# ─── QA especializado ──────────────────────────────────────────────────────────
agent("qa-manual-testing",
      "Designs test cases, runs structured exploratory testing, writes reproducible bug reports, and gives evidence-based release recommendations.",
      "Listo. Casos de prueba, sesiones exploratorias y reportes de bugs reproducibles.",
      tools=(R, W, WEB), write=["tests/manual/**", "docs/qa/**", "docs/**", "reports/**"])
agent("web-e2e-automation",
      "Builds stable web end-to-end test suites with Playwright, Cypress, or Selenium: robust selectors, isolation, no sleeps, CI parallelism, and reports.",
      "Listo. Los tests E2E corren libres; instalar navegadores o dependencias pide confirmación.",
      write=["tests/**", "e2e/**", "playwright/**", "cypress/**", "playwright.config.*", "cypress.config.*", "docs/**"],
      allow=["npx playwright test*", "npx playwright show-report*", "npx cypress run*", "npm run test:e2e*"] + JS_CHECKS,
      ask=["npx playwright install*"] + INSTALL_ASK)
agent("api-testing",
      "Tests REST, GraphQL, and gRPC APIs: functional, negative, authorization (BOLA/IDOR), contract (Pact), and schema-based fuzzing.",
      "Listo. Pruebas de API libres contra entornos de prueba; peticiones a otros destinos piden confirmación.",
      write=["tests/**", "api-tests/**", "postman/**", "collections/**", "pact/**", "docs/**"],
      allow=["newman run*", "npx newman run*", "schemathesis run*", "st run*", "pytest*", "npx vitest*", "npm test*",
             "mvn test*", "./gradlew test*"],
      ask=["curl *", "http *", "httpie *"])
agent("mobile-test-automation",
      "Builds mobile UI test automation for iOS and Android with Espresso, XCUITest, Appium, Maestro, Detox, and Flutter integration tests on device farms.",
      "Listo. Tests en emuladores y simuladores libres; granjas de dispositivos piden confirmación.",
      write=["tests/**", "e2e/**", ".maestro/**", "maestro/**", "android/app/src/androidTest/**", "ios/**UITests/**", "docs/**"],
      allow=["maestro test*", "./gradlew connectedAndroidTest*", "xcodebuild test*", "npx detox test*",
             "flutter test integration_test*", "adb devices*", "xcrun simctl list*"],
      ask=["aws devicefarm schedule-run*", "maestro cloud*", "npx detox build*"] + INSTALL_ASK)
agent("qa-lead",
      "Owns quality strategy: risk-based test strategy, automation targets, environments and test data, quality metrics, and go/no-go release recommendations.",
      "Listo. Estrategia de calidad y decisiones de release basadas en criterios y riesgo.",
      tools=(R, W, WEB), write=["docs/**", "docs/qa/**", "reports/**"])

# ─── Blockchain ────────────────────────────────────────────────────────────────
agent("smart-contract-security",
      "Audits Solidity/EVM smart contracts: reentrancy, access control, oracle and flash-loan attacks, upgradeability, with Slither, Foundry fuzzing, and PoCs.",
      "Listo. Auditoría con pruebas locales; desplegar o enviar transacciones a redes reales está bloqueado.",
      tools=(R, W, S, WEB), write=["src/**", "contracts/**", "test/**", "audits/**", "reports/**", "docs/**"],
      allow=["forge build*", "forge test*", "forge coverage*", "forge fmt --check*", "slither *", "aderyn *",
             "echidna *", "medusa fuzz*", "npx hardhat compile*", "npx hardhat test*", "solhint *"],
      ask=["anvil*", "forge script*", "npx hardhat run*"],
      deny=["forge script * --broadcast*", "cast send*", "npx hardhat run * --network mainnet*", "cast wallet *"])
agent("blockchain-architecture",
      "Designs blockchain solutions only when justified: platform selection, on-chain vs off-chain split, custody and wallets, oracles, tokenization, and compliance.",
      "Listo. Primero validamos si blockchain es la herramienta correcta; enviar transacciones está bloqueado.",
      tools=(R, W, S, WEB), write=["docs/**", "contracts/**", "reports/**"],
      allow=["forge build*", "forge test*", "npx hardhat compile*"],
      deny=["cast send*", "forge script * --broadcast*", "cast wallet *"])


# ═══ Lote 3 (78 agentes) ═══════════════════════════════════════════════════════
DOCS_ONLY = dict(tools=(R, W, WEB), write=["docs/**", "reports/**"])
DB_DENY = ["DROP DATABASE*", "dropdb *", "* DROP DATABASE*", "* drop database*", "* TRUNCATE *", "* truncate *"]

# ─── Contenedores ──────────────────────────────────────────────────────────────
agent("docker-engineering",
      "Writes and reviews Dockerfiles, Compose files, and image builds: multi-stage, BuildKit caching and secrets, multi-arch with buildx, and runtime hardening.",
      "Listo. Lint y análisis de imágenes libres; construir pide confirmación y publicar imágenes está bloqueado.",
      write=["**/Dockerfile*", "**/.dockerignore", "**/docker-compose*.yml", "**/compose*.yaml", "docs/**"],
      allow=["hadolint*", "docker images*", "docker inspect *", "docker history *", "dive *", "trivy image*", "trivy fs*",
             "docker buildx ls*", "docker compose config*"],
      ask=["docker build*", "docker buildx build*", "docker compose up*", "docker compose down*", "docker run*"],
      deny=["docker rm -f*", "docker volume rm*", "docker compose down -v*"])
agent("aws-ecs-fargate",
      "Designs and reviews Amazon ECS on Fargate/EC2: task definitions, roles, secrets, networking, deployments with circuit breaker, autoscaling, and cost.",
      "Listo. Lectura de ECS libre; desplegar o escalar servicios pide confirmación.",
      tools=(R, W, S, WEB), write=["infra/**", "lib/**", "terraform/**", "task-definitions/**", "docs/**"],
      allow=["aws ecs describe-*", "aws ecs list-*", "aws ecr describe-*", "aws elbv2 describe-*", "cdk synth*", "cdk diff*"] + TF_READ,
      ask=["aws ecs update-service*", "aws ecs register-task-definition*", "aws ecs run-task*", "cdk deploy*"],
      deny=["aws ecs delete-*", "aws ecs deregister-*", "aws ecs execute-command*", "cdk destroy*"])

# ─── Programación ──────────────────────────────────────────────────────────────
agent("rust-developer",
      "Writes and reviews safe, idiomatic Rust: ownership, error handling, async with Tokio, unsafe justification, Clippy, and testing.",
      "Listo. cargo check, clippy y test corren libres; publicar crates está bloqueado.",
      write=["src/**", "tests/**", "benches/**", "examples/**", "Cargo.toml", "docs/**"],
      allow=["cargo check*", "cargo clippy*", "cargo test*", "cargo fmt --check*", "cargo build*", "cargo audit*", "cargo deny*"],
      ask=["cargo add*", "cargo update*", "cargo run*"], deny=["cargo publish*"])
agent("php-laravel-developer",
      "Writes and reviews modern PHP and Laravel: Eloquent without N+1, Form Requests, policies, queues, security, PHPStan, and Pest/PHPUnit tests.",
      "Listo. PHPStan, Pint y tests corren libres; migraciones e instalaciones piden confirmación.",
      write=["app/**", "routes/**", "database/**", "resources/**", "config/**", "tests/**", "composer.json", "docs/**"],
      allow=["php artisan test*", "vendor/bin/phpunit*", "vendor/bin/pest*", "vendor/bin/phpstan*", "vendor/bin/pint --test*",
             "php artisan route:list*", "composer audit*", "composer validate*"],
      ask=["composer require*", "composer update*", "php artisan migrate*", "php artisan db:seed*"],
      deny=["php artisan migrate:fresh*", "php artisan migrate:reset*", "php artisan db:wipe*"])
agent("ruby-rails-developer",
      "Writes and reviews Ruby on Rails applications: Active Record without N+1, safe migrations, jobs, Brakeman-clean security, and RSpec tests.",
      "Listo. RSpec, RuboCop y Brakeman corren libres; migraciones piden confirmación.",
      write=["app/**", "config/**", "db/migrate/**", "lib/**", "spec/**", "test/**", "Gemfile", "docs/**"],
      allow=["bundle exec rspec*", "bin/rails test*", "bundle exec rubocop*", "bundle exec brakeman*", "bundle audit*",
             "bin/rails routes*"],
      ask=["bundle add*", "bundle install*", "bundle update*", "bin/rails db:migrate*", "bin/rails db:rollback*"],
      deny=["bin/rails db:drop*", "bin/rails db:reset*", "bin/rails db:schema:load*"])
agent("cpp-developer",
      "Writes and reviews modern C++ (17/20/23): RAII, ownership, undefined behavior, sanitizers, concurrency, CMake, and performance.",
      "Listo. Compilar, probar y analizar con sanitizers es libre.",
      write=["src/**", "include/**", "tests/**", "CMakeLists.txt", "**/CMakeLists.txt", "cmake/**", "docs/**"],
      allow=["cmake *", "ctest*", "make *", "ninja*", "clang-tidy*", "clang-format --dry-run*", "cppcheck*"],
      ask=["conan install*", "vcpkg install*"])

# ─── Requerimientos ────────────────────────────────────────────────────────────
agent("business-process-analyst",
      "Maps and improves business processes with BPMN and DMN: as-is analysis, waste and bottlenecks, to-be design, controls, and KPIs.",
      "Listo. Mapeamos el proceso real, encontramos el desperdicio y lo traducimos a requerimientos.",
      **dict(DOCS_ONLY, write=["docs/**", "processes/**", "reports/**"]))
agent("technical-specification-writer",
      "Writes precise, testable, traceable specifications: functional specs, SRS, interface and data specifications, and acceptance test specs.",
      "Listo. Convertimos requerimientos acordados en especificaciones sin ambigüedad.",
      **dict(DOCS_ONLY, write=["docs/**", "specs/**"]))

# ─── Regulación y derecho ──────────────────────────────────────────────────────
agent("pci-dss-compliance",
      "Guides PCI DSS v4.0.1 compliance: CDE scoping and scope reduction, requirement-by-requirement gap analysis, controls, and evidence.",
      "Listo. Guía de cumplimiento PCI DSS; no reemplaza la evaluación de un QSA.",
      **dict(DOCS_ONLY, write=["docs/compliance/**", "docs/**", "reports/**"]))
agent("iso27001-isms",
      "Designs and implements ISO/IEC 27001:2022 ISMS: scope, risk assessment, Statement of Applicability with Annex A, audits, and certification.",
      "Listo. Un SGSI proporcional y útil, no una carpeta de documentos.",
      **dict(DOCS_ONLY, write=["docs/compliance/**", "docs/isms/**", "docs/**", "reports/**"]))
agent("colombia-financial-regulation",
      "Maps Colombian financial sector technology obligations (SFC: cybersecurity, cloud, outsourcing, incidents; Law 1581; SARLAFT) to controls and evidence.",
      "Listo. Mapeo regulatorio de la SFC a controles técnicos; verifica siempre la norma vigente con tu área legal.",
      **dict(DOCS_ONLY, write=["docs/compliance/**", "docs/**", "reports/**"]))
agent("ai-governance",
      "Builds AI governance aligned with the EU AI Act, ISO/IEC 42001, and NIST AI RMF: inventories, risk classification, impact assessments, oversight.",
      "Listo. Gobierno de IA por caso de uso y riesgo; las decisiones legales requieren revisión jurídica.",
      **dict(DOCS_ONLY, write=["docs/ai-governance/**", "docs/**", "reports/**"]))
agent("tech-contracts-legal",
      "Reviews technology contracts (MSA, SOW, SaaS, SLA, DPA, NDA): plain-language summaries, risks, missing protections, and alternative wording.",
      "Listo. Revisión de contratos en lenguaje claro; no es asesoría legal, valida siempre con un abogado.",
      **dict(DOCS_ONLY, write=["docs/legal/**", "docs/**"]))
agent("open-source-licensing",
      "Manages open source license compliance: license identification, obligations by distribution model, compatibility, notices, and license choice.",
      "Listo. Analizo licencias de dependencias; los casos dudosos van a revisión legal.",
      tools=(R, W, S, WEB), write=["docs/**", "reports/**", "THIRD_PARTY_NOTICES*", "NOTICE*", "LICENSE*"],
      allow=["scancode *", "license-checker*", "npx license-checker*", "pip-licenses*", "go-licenses *", "syft *"])
agent("colombian-labor-law",
      "Explains Colombian labor obligations (contracts, hours, surcharges, benefits, social security, payroll, termination) and turns them into HR software rules.",
      "Listo. Normativa laboral colombiana aplicada; confirma los valores del año vigente y consulta a un abogado laboral en casos sensibles.",
      **dict(DOCS_ONLY, write=["docs/**", "docs/hr/**", "reports/**"]))

# ─── RRHH ──────────────────────────────────────────────────────────────────────
agent("technical-recruiter",
      "Designs fair, structured technical hiring: role intake, inclusive job descriptions, sourcing, interview plans, scorecards, and offers.",
      "Listo. Contratación estructurada, justa y rápida para roles técnicos.",
      **dict(DOCS_ONLY, write=["docs/**", "hiring/**"]))
agent("people-operations",
      "Designs people processes for tech companies: onboarding/offboarding, performance cycles, compensation frameworks, policies, and engagement.",
      "Listo. Procesos de personas claros y justos; lo sensible legalmente va a revisión jurídica.",
      **dict(DOCS_ONLY, write=["docs/**", "docs/hr/**"]))
agent("learning-development",
      "Designs learning paths, onboarding curricula, certification plans, and workshops for tech teams, measured by job outcomes.",
      "Listo. Rutas de aprendizaje prácticas, medidas por resultados en el trabajo.",
      **dict(DOCS_ONLY, write=["docs/**", "learning/**", "training/**"]))

# ─── DevOps / DevSecOps ────────────────────────────────────────────────────────
agent("github-actions-cicd",
      "Designs and secures GitHub Actions workflows: reusable workflows, caching, least-privilege permissions, SHA pinning, OIDC, and protected environments.",
      "Listo. Revisión de workflows libre; ejecutar workflows pide confirmación.",
      write=[".github/**", "docs/**"],
      allow=["actionlint*", "zizmor *", "yamllint*", "gh run list*", "gh run view*", "gh workflow list*", "gh workflow view*"],
      ask=["gh workflow run*", "gh run rerun*", "gh run cancel*"],
      deny=["gh secret *", "gh variable delete*"])
agent("gitlab-cicd",
      "Designs and secures GitLab CI/CD: rules and DAG pipelines, components, caching, protected variables, ID tokens, scanners, and environments.",
      "Listo. Revisión de pipelines libre; disparar pipelines pide confirmación.",
      tools=(R, W, S, WEB), write=[".gitlab-ci.yml", ".gitlab/**", "ci/**", "templates/**", "docs/**"],
      allow=["yamllint*", "glab ci lint*", "glab ci list*", "glab ci view*"],
      ask=["glab ci run*", "glab ci retry*"],
      deny=["glab variable delete*"])
agent("gitops-argocd",
      "Runs GitOps with Argo CD and Flux: repository structure, ApplicationSets, sync policies, secrets, environment promotion, and Argo Rollouts.",
      "Listo. Git es la fuente de verdad: lectura del clúster libre, sincronizar pide confirmación.",
      write=["apps/**", "clusters/**", "k8s/**", "manifests/**", "helm/**", "charts/**", "docs/**"],
      allow=K8S_READ + ["argocd app list*", "argocd app get*", "argocd app diff*", "kustomize build*", "helm template*",
                        "helm lint*", "kubeconform*"],
      ask=["argocd app sync*", "argocd app rollback*", "kubectl argo rollouts promote*"],
      deny=["argocd app delete*", "argocd cluster rm*"])
agent("policy-as-code",
      "Turns standards into tested, automated policies with OPA/Rego, Conftest, Kyverno, Gatekeeper, Checkov, and Sentinel, rolled out audit-first.",
      "Listo. Políticas con pruebas y mensajes claros; primero en modo auditoría, después enforce.",
      write=["policies/**", "policy/**", "rego/**", "kyverno/**", "docs/**"],
      allow=["opa test*", "opa eval*", "opa fmt*", "conftest *", "kyverno test*", "kyverno apply*", "checkov *"] + TF_READ,
      ask=["kubectl apply*"])
agent("sca-security",
      "Software composition analysis: finds and prioritizes vulnerable, malicious, and outdated dependencies with reachability, EPSS, and KEV; automates updates.",
      "Listo. Escaneo de dependencias libre; actualizar dependencias pide confirmación.",
      tools=(R, W, S, WEB), write=["reports/**", "docs/**", "renovate.json", ".github/dependabot.yml"],
      allow=["osv-scanner*", "npm audit*", "pip-audit*", "govulncheck*", "cargo audit*", "grype *", "trivy fs*", "syft *",
             "snyk test*", "dependency-check*"],
      ask=["npm audit fix*", "npm update*", "pip install*"],
      deny=["npm audit fix --force*"])
agent("api-security-testing",
      "Dynamically tests REST, GraphQL, and gRPC APIs against the OWASP API Security Top 10, with multi-user authorization testing, on authorized targets only.",
      "Listo. Solo contra APIs autorizadas por escrito: cada petición o escaneo pide confirmación.",
      tools=(R, W, S, WEB), write=["reports/**", "docs/security/**"],
      ask=["curl *", "http *", "zap*", "nuclei*", "schemathesis run*", "ffuf*", "restler*"])

# ─── Migración, ML y datos ─────────────────────────────────────────────────────
agent("database-migration",
      "Migrates databases across engines and platforms with schema conversion, CDC replication (AWS DMS, native), validation, cutover, and rollback.",
      "Listo. Lectura de DMS libre; iniciar replicación o cutover pide confirmación y borrar está bloqueado.",
      tools=(R, W, S, WEB), write=["migration/**", "sql/**", "docs/**", "reports/**"],
      allow=["aws dms describe-*", "aws dms test-connection*", "aws rds describe-*", "pgloader --dry-run*"],
      ask=["aws dms start-replication-task*", "aws dms stop-replication-task*", "aws dms modify-*", "pgloader *", "psql *"],
      deny=["aws dms delete-*", "aws rds delete-*"] + DB_DENY)
agent("mainframe-modernization",
      "Modernizes COBOL/PL/I, CICS, IMS, and Db2 workloads incrementally: discovery, strategy per domain, data conversion, and parallel-run validation.",
      "Listo. Modernización incremental, con reglas de negocio protegidas y corridas en paralelo.",
      tools=(R, W, S, WEB), write=["docs/**", "reports/**", "migration/**"],
      allow=["aws m2 list-*", "aws m2 get-*"])
agent("machine-learning-engineer",
      "Builds production ML models: problem framing, leakage-free data prep, baselines, training and tuning, evaluation, and reproducible packaging.",
      "Listo. Siempre contra un baseline y sin fugas de datos; los entrenamientos en la nube piden confirmación.",
      tools=(R, W, S, WEB), write=["src/**", "notebooks/**", "models/**", "training/**", "tests/**", "docs/**"],
      allow=PY_CHECKS + ["jupyter nbconvert --to script*"],
      ask=["python train*", "python -m train*", "aws sagemaker create-training-job*"] + INSTALL_ASK)
agent("data-scientist",
      "Turns data into decisions: EDA, statistics, A/B test design and analysis, causal inference, forecasting, and clear communication of uncertainty.",
      "Listo. Respuesta primero, con tamaño del efecto e incertidumbre; nada de causalidad sin diseño que la respalde.",
      tools=(R, W, S, WEB), write=["notebooks/**", "analysis/**", "reports/**", "docs/**"],
      allow=PY_CHECKS + ["jupyter nbconvert --to script*"],
      ask=["aws athena start-query-execution*", "bq query*"] + INSTALL_ASK)
agent("data-governance",
      "Makes data trustworthy and compliant: ownership, catalogs and glossaries, quality rules, classification, access policies, lineage, and MDM.",
      "Listo. Gobierno de datos automatizado: dueños, calidad, clasificación y acceso.",
      tools=(R, W, S, WEB), write=["docs/**", "governance/**", "reports/**", "models/**"],
      allow=["aws lakeformation list-*", "aws lakeformation get-*", "aws glue get-*", "aws datazone list-*",
             "dbt test*", "dbt ls*"],
      deny=["aws lakeformation grant-permissions*", "aws lakeformation revoke-permissions*"])
agent("data-warehouse",
      "Designs analytical warehouses on Redshift, Snowflake, BigQuery, Synapse/Fabric: dimensional modeling, dbt layers, performance, cost, and security.",
      "Listo. Modelos con grano explícito y pruebas; las consultas pesadas o cargas completas piden confirmación.",
      tools=(R, W, S, WEB), write=["models/**", "macros/**", "sql/**", "tests/**", "docs/**"],
      allow=["dbt compile*", "dbt parse*", "dbt ls*", "dbt test*", "sqlfluff lint*"],
      ask=["dbt run*", "dbt build*", "bq query*", "aws redshift-data execute-statement*", "snowsql *"],
      deny=["dbt run --full-refresh*"] + DB_DENY)
agent("kafka-streaming",
      "Designs and operates Apache Kafka (MSK, Confluent, Redpanda): topics and partitions, durable producers, idempotent consumers, schemas, and stream processing.",
      "Listo. Lectura del clúster libre; crear o modificar topics pide confirmación y borrar está bloqueado.",
      tools=(R, W, S, WEB), write=["schemas/**", "src/**", "infra/**", "docs/**"],
      allow=["aws kafka describe-*", "aws kafka list-*", "kafka-topics.sh --describe*", "kafka-topics.sh --list*",
             "kafka-consumer-groups.sh --describe*", "kcat -L*"] + TF_READ,
      ask=["kafka-topics.sh --create*", "kafka-topics.sh --alter*", "kafka-configs.sh --alter*",
           "kafka-consumer-groups.sh --reset-offsets*"],
      deny=["kafka-topics.sh --delete*", "aws kafka delete-*"])

# ─── Bases de datos ────────────────────────────────────────────────────────────
def db_agent(slug, description, welcome, read_cmds, ask_cmds, extra_deny=()):
    agent(slug, description, welcome, tools=(R, W, S, WEB),
          write=["migrations/**", "**/migrations/**", "db/**", "sql/**", "schema/**", "docs/**", "reports/**"],
          allow=read_cmds, ask=ask_cmds, deny=DB_DENY + list(extra_deny))

db_agent("postgresql-specialist",
         "PostgreSQL DBA and performance specialist: schema design, EXPLAIN ANALYZE, indexes, autovacuum, lock-safe migrations, replication, and PITR.",
         "Listo. Diagnóstico con planes y estadísticas; conectarse a la base pide confirmación.",
         ["aws rds describe-*", "pg_dump --schema-only*", "sqlfluff lint*"], ["psql *", "pg_restore *"],
         ["aws rds delete-*"])
db_agent("mongodb-specialist",
         "MongoDB specialist: access-pattern document modeling, ESR indexes, aggregation tuning, shard keys, write concerns, and secure operations.",
         "Listo. Modelado y rendimiento de MongoDB; conectarse al clúster pide confirmación.",
         ["atlas clusters list*", "atlas clusters describe*"], ["mongosh *", "mongodump *", "mongorestore *"],
         ["* dropDatabase*", "* .drop()*", "atlas clusters delete*"])
db_agent("dynamodb-specialist",
         "Amazon DynamoDB specialist: access-pattern-first key design, single-table design, GSIs, conditional writes, capacity modes, and hot partitions.",
         "Listo. Diseño de llaves desde los patrones de acceso; escribir datos pide confirmación.",
         ["aws dynamodb describe-*", "aws dynamodb list-*", "aws cloudwatch get-metric-data*"],
         ["aws dynamodb query*", "aws dynamodb get-item*", "aws dynamodb put-item*", "aws dynamodb update-*",
          "aws dynamodb create-table*"],
         ["aws dynamodb delete-*", "aws dynamodb scan*"])
db_agent("redis-specialist",
         "Redis/Valkey specialist (ElastiCache, MemoryDB): data structures, caching with stampede protection, eviction, persistence, and cluster operations.",
         "Listo. Diseño y diagnóstico de Redis; comandos destructivos como FLUSHALL o KEYS están bloqueados.",
         ["aws elasticache describe-*", "aws memorydb describe-*"],
         ["redis-cli *", "valkey-cli *"],
         ["* FLUSHALL*", "* FLUSHDB*", "* flushall*", "* flushdb*", "* KEYS *", "aws elasticache delete-*"])
db_agent("sql-server-dba",
         "SQL Server DBA: execution plans, Query Store, indexing, T-SQL quality, Always On, backups and restores, security, and licensing.",
         "Listo. Diagnóstico con planes y Query Store; conectarse a la instancia pide confirmación.",
         ["aws rds describe-*", "az sql * show*", "az sql * list*"], ["sqlcmd *", "Invoke-Sqlcmd*"],
         ["aws rds delete-*", "az sql * delete*"])
db_agent("oracle-database",
         "Oracle Database specialist: AWR/ASH diagnostics, execution plans, partitioning, RAC and Data Guard, RMAN, security, and licensing.",
         "Listo. Diagnóstico con AWR y planes reales; conectarse a la base pide confirmación.",
         ["aws rds describe-*", "oci db * list*", "oci db * get*"], ["sqlplus *", "sql *", "rman *"],
         ["aws rds delete-*", "oci db * delete*", "oci db * terminate*"])

# ─── Frontend / Backend / Mobile ───────────────────────────────────────────────
FRONT_WRITE = ["src/**", "app/**", "components/**", "pages/**", "public/**", "styles/**", "tests/**", "e2e/**", "docs/**"]
agent("react-developer",
      "Builds and reviews React 18/19 + TypeScript: hooks, state and server state, forms, performance profiling, accessibility, and Testing Library.",
      "Listo. Lint, tipos y tests libres; instalar dependencias pide confirmación.",
      write=FRONT_WRITE, allow=JS_CHECKS + ["npx playwright test*"], ask=INSTALL_ASK + ["npm run dev*"])
agent("angular-developer",
      "Builds and reviews modern Angular: standalone components, signals, control flow, OnPush, RxJS, typed forms, and testing.",
      "Listo. ng lint/test/build libres; instalar dependencias pide confirmación.",
      write=FRONT_WRITE + ["angular.json"], allow=JS_CHECKS + ["npx ng lint*", "npx ng test*", "npx ng build*", "ng lint*", "ng test*", "ng build*"],
      ask=INSTALL_ASK + ["ng add*", "ng update*", "ng serve*"])
agent("vue-developer",
      "Builds and reviews Vue 3 and Nuxt: Composition API, reactivity pitfalls, Pinia, routing, SSR, security, and Vitest.",
      "Listo. Lint, tipos y tests libres; instalar dependencias pide confirmación.",
      write=FRONT_WRITE + ["nuxt.config.*", "composables/**", "stores/**"], allow=JS_CHECKS + ["npx vue-tsc*", "npx nuxi typecheck*"],
      ask=INSTALL_ASK + ["npm run dev*"])
agent("nextjs-developer",
      "Builds and reviews Next.js App Router apps: Server/Client Components, Server Actions with validation and authorization, caching, and deployment.",
      "Listo. Lint, build y tests libres; desplegar pide confirmación.",
      write=FRONT_WRITE + ["next.config.*", "middleware.ts"], allow=JS_CHECKS + ["npx next lint*", "npx next build*"],
      ask=INSTALL_ASK + ["npm run dev*", "vercel deploy*", "npx vercel*"])
agent("backend-engineering",
      "Designs and reviews server-side systems across languages: structure, transactions, async work, resilience, security, and observability.",
      "Listo. Revisión de backend independiente del lenguaje; tests y lint corren libres.",
      write=["src/**", "app/**", "internal/**", "tests/**", "docs/**"], allow=JS_CHECKS + PY_CHECKS + OTHER_TESTS)
agent("graphql-api",
      "Designs and reviews GraphQL schemas and resolvers: client-driven design, DataLoader, field-level authorization, limits, and federation checks.",
      "Listo. Validación y chequeo de cambios de esquema libres.",
      write=["schema/**", "**/*.graphql", "src/**", "docs/**"],
      allow=JS_CHECKS + ["npx graphql-inspector*", "rover subgraph check*", "rover graph check*"],
      ask=["rover subgraph publish*"])
MOBILE_WRITE = ["ios/**", "android/**", "lib/**", "src/**", "app/**", "test/**", "tests/**", "docs/**"]
agent("ios-developer",
      "Builds and reviews iOS apps with Swift and SwiftUI: concurrency, data, networking, Keychain security, privacy, accessibility, and tests.",
      "Listo. Compilar y probar es libre; publicar en App Store está bloqueado.",
      write=MOBILE_WRITE + ["**/*.swift", "Package.swift"],
      allow=["xcodebuild test*", "xcodebuild build*", "xcodebuild -list*", "swift build*", "swift test*", "swiftlint*", "xcrun simctl list*"],
      ask=["pod install*", "swift package update*", "fastlane *"],
      deny=["fastlane deliver*", "fastlane pilot upload*", "xcrun altool --upload*"])
agent("android-developer",
      "Builds and reviews Android apps with Kotlin and Jetpack Compose: architecture, coroutines/Flow, Room, WorkManager, security, and Play readiness.",
      "Listo. Gradle lint y tests libres; publicar en Play Store está bloqueado.",
      write=MOBILE_WRITE + ["**/*.kt", "**/build.gradle.kts", "gradle/**"],
      allow=["./gradlew lint*", "./gradlew test*", "./gradlew assembleDebug*", "./gradlew detekt*", "./gradlew ktlintCheck*", "adb devices*"],
      ask=["./gradlew connectedAndroidTest*", "./gradlew bundleRelease*", "fastlane *"],
      deny=["fastlane supply*", "./gradlew publish*"])
agent("react-native-developer",
      "Builds and reviews React Native and Expo apps: New Architecture, navigation, list performance, secure storage, EAS builds, and OTA updates.",
      "Listo. Lint y tests libres; builds y OTA updates piden confirmación.",
      write=MOBILE_WRITE + ["app.json", "app.config.*", "eas.json"], allow=JS_CHECKS + ["npx expo-doctor*"],
      ask=INSTALL_ASK + ["npx expo install*", "eas build*", "eas update*", "npx expo prebuild*"],
      deny=["eas submit*"])
agent("flutter-developer",
      "Builds and reviews Flutter apps: widget composition, Riverpod/Bloc, go_router, performance, platform channels, secure storage, and tests.",
      "Listo. flutter analyze y test libres; publicar en tiendas está bloqueado.",
      write=MOBILE_WRITE + ["pubspec.yaml", "integration_test/**"],
      allow=["flutter analyze*", "flutter test*", "dart format --set-exit-if-changed*", "dart analyze*", "flutter doctor*"],
      ask=["flutter pub get*", "flutter pub add*", "flutter build*", "flutter run*"],
      deny=["fastlane deliver*", "fastlane supply*"])

# ─── Observabilidad / SRE ──────────────────────────────────────────────────────
agent("opentelemetry",
      "Instruments applications with OpenTelemetry: auto and manual tracing, metrics, log correlation, context propagation, Collector pipelines, and sampling.",
      "Listo. Instrumentación neutral al proveedor; sin secretos ni PII en la telemetría.",
      write=["src/**", "otel/**", "collector/**", "k8s/**", "infra/**", "docs/**"],
      allow=["otelcol validate*", "otelcol-contrib validate*"] + JS_CHECKS + PY_CHECKS)
agent("prometheus-grafana",
      "Builds monitoring with Prometheus, Alertmanager, Grafana, Loki, and Tempo: PromQL, recording and alerting rules, dashboards as code, cardinality control.",
      "Listo. Validación de reglas y consultas libre; recargar configuración pide confirmación.",
      write=["monitoring/**", "dashboards/**", "alerts/**", "rules/**", "k8s/**", "docs/**"],
      allow=["promtool check*", "promtool test*", "amtool check-config*", "jsonnet *"] + K8S_READ,
      ask=["kubectl apply*", "curl -X POST *"])
agent("aws-cloudwatch",
      "Designs AWS observability with CloudWatch: metrics and percentile alarms, Logs Insights, retention, X-Ray/Application Signals, canaries, and cost.",
      "Listo. Consultas de métricas y logs libres; crear o borrar alarmas pide confirmación o está bloqueado.",
      tools=(R, W, S, WEB), write=["infra/**", "monitoring/**", "dashboards/**", "docs/**"],
      allow=["aws cloudwatch describe-*", "aws cloudwatch get-*", "aws cloudwatch list-*", "aws logs describe-*",
             "aws logs start-query*", "aws logs get-query-results*", "aws xray get-*", "aws synthetics describe-*"] + TF_READ,
      ask=["aws cloudwatch put-metric-alarm*", "aws logs put-retention-policy*", "aws cloudwatch put-dashboard*"],
      deny=["aws cloudwatch delete-*", "aws logs delete-*"])
agent("chaos-engineering",
      "Designs hypothesis-driven chaos experiments with AWS FIS, Chaos Mesh, LitmusChaos, and Toxiproxy, with limited blast radius and stop conditions.",
      "Listo. Diseño experimentos con condiciones de parada; ejecutarlos pide confirmación y en producción requiere tu autorización.",
      tools=(R, W, S, WEB), write=["chaos/**", "experiments/**", "docs/**", "reports/**"],
      allow=["aws fis list-*", "aws fis get-*"] + K8S_READ,
      ask=["aws fis start-experiment*", "aws fis create-experiment-template*", "kubectl apply*"],
      deny=["aws fis delete-*"])
agent("incident-management-oncall",
      "Designs incident management and on-call: severity levels, roles, communications, rotations, alert quality, and blameless postmortems.",
      "Listo. Mitigar primero, investigar después; postmortems sin culpables.",
      **dict(DOCS_ONLY, write=["docs/**", "runbooks/**", "postmortems/**", "incidents/**"]))
agent("capacity-planning",
      "Plans capacity for growth and peaks: demand models from business drivers, measured saturation points, scaling plans, quotas, and cost.",
      "Listo. Capacidad basada en límites medidos y escenarios de falla en el pico.",
      tools=(R, W, S, WEB), write=["docs/**", "reports/**", "capacity/**"],
      allow=["aws service-quotas get-*", "aws service-quotas list-*", "aws cloudwatch get-metric-data*",
             "aws cloudwatch get-metric-statistics*"] + K8S_READ,
      ask=["aws service-quotas request-service-quota-increase*"])

# ─── IaC ───────────────────────────────────────────────────────────────────────
IAC_DENY_EXTRA = ["terraform state *", "tofu apply*", "tofu destroy*"]
agent("terraform-engineer",
      "Writes and reviews Terraform/OpenTofu: modules, remote locked state, plan review of replacements, pinning, testing, and CI with policy checks.",
      "Listo. fmt, validate, plan y tests libres; apply y destroy están bloqueados.",
      write=["infra/**", "terraform/**", "modules/**", "**/*.tf", "**/*.tfvars.example", "docs/**"],
      allow=TF_READ + ["terraform test*", "terraform show*", "terraform providers*", "tflint*", "checkov *", "trivy config*",
                       "tofu fmt -check*", "tofu validate*", "tofu plan*", "tofu test*"],
      ask=["terraform init*", "tofu init*"], deny=IAC_DENY_EXTRA)
agent("aws-cdk-engineer",
      "Builds AWS infrastructure with CDK v2 (TypeScript/Python): stacks and constructs, grant-based IAM, cdk-nag, assertions, and diff-reviewed delivery.",
      "Listo. synth, diff y tests libres; deploy pide confirmación y destroy está bloqueado.",
      write=["lib/**", "bin/**", "src/**", "test/**", "cdk.json", "docs/**"],
      allow=["cdk synth*", "cdk diff*", "cdk ls*", "cdk doctor*"] + JS_CHECKS + PY_CHECKS,
      ask=["cdk deploy*", "cdk bootstrap*"] + INSTALL_ASK, deny=["cdk destroy*"])
agent("cloudformation-engineer",
      "Writes and reviews CloudFormation and SAM: parameters and conditions, change sets, retain policies, StackSets, cfn-lint and Guard.",
      "Listo. Lint, Guard y creación de change sets libres; ejecutarlos pide confirmación y borrar stacks está bloqueado.",
      write=["templates/**", "cloudformation/**", "**/*.template.yaml", "template.yaml", "docs/**"],
      allow=["cfn-lint*", "cfn-guard *", "sam validate*", "aws cloudformation validate-template*",
             "aws cloudformation describe-*", "aws cloudformation list-*", "aws cloudformation get-*",
             "aws cloudformation create-change-set*"],
      ask=["aws cloudformation execute-change-set*", "aws cloudformation deploy*", "sam deploy*"],
      deny=["aws cloudformation delete-stack*", "aws cloudformation delete-stack-set*", "sam delete*"])
agent("ansible-automation",
      "Writes and reviews Ansible playbooks, roles, and collections: idempotency, check mode, rolling execution, Vault secrets, and Molecule tests.",
      "Listo. Lint y --check libres; ejecutar playbooks pide confirmación.",
      write=["ansible/**", "playbooks/**", "roles/**", "inventories/**", "collections/**", "docs/**"],
      allow=["ansible-lint*", "yamllint*", "ansible-playbook * --check*", "ansible-playbook * --syntax-check*",
             "ansible-inventory --list*", "molecule test*", "molecule lint*"],
      ask=["ansible-playbook *", "ansible *", "molecule converge*"],
      deny=["ansible-vault view*", "ansible-vault decrypt*"])

# ─── IAM multicloud ────────────────────────────────────────────────────────────
agent("azure-entra-iam",
      "Secures Microsoft Entra ID and Azure RBAC: Conditional Access, phishing-resistant MFA, PIM, managed identities, app registrations, and least privilege.",
      "Listo. Análisis de identidades y roles en modo lectura; asignar o quitar roles está bloqueado.",
      tools=(R, W, S, WEB), write=["infra/**", "docs/**", "reports/**"],
      allow=["az ad * list*", "az ad * show*", "az role assignment list*", "az role definition list*", "az account show*"] + TF_READ,
      deny=["az role assignment create*", "az role assignment delete*", "az ad * delete*", "az ad app credential reset*",
            "az ad sp credential reset*"])
agent("gcp-iam",
      "Secures Google Cloud IAM: hierarchy bindings, no basic roles, keyless service accounts with Workload Identity Federation, PAM, and Recommender.",
      "Listo. Análisis de IAM en modo lectura; cambiar políticas o crear llaves está bloqueado.",
      tools=(R, W, S, WEB), write=["infra/**", "terraform/**", "docs/**", "reports/**"],
      allow=["gcloud * get-iam-policy*", "gcloud iam * list*", "gcloud iam * describe*", "gcloud recommender * list*",
             "gcloud asset analyze-iam-policy*"] + TF_READ,
      deny=["gcloud * set-iam-policy*", "gcloud * add-iam-policy-binding*", "gcloud * remove-iam-policy-binding*",
            "gcloud iam service-accounts keys create*"])
agent("multicloud-iam",
      "Designs one identity model across AWS, Azure, GCP, OCI, and IBM Cloud: single IdP federation, role mapping, workload federation, JIT, and central audit.",
      "Listo. Un modelo de identidad coherente entre nubes; todo análisis en modo lectura.",
      tools=(R, W, S, WEB), write=["docs/**", "reports/**", "infra/**"],
      allow=["aws iam list-*", "aws iam get-*", "aws sso-admin list-*", "az role assignment list*", "az ad * list*",
             "gcloud * get-iam-policy*", "oci iam * list*", "ibmcloud iam * list*"],
      deny=["aws iam create-*", "aws iam put-*", "aws iam attach-*", "az role assignment create*",
            "gcloud * set-iam-policy*", "oci iam * create*", "ibmcloud iam * create*"])

# ─── Serverless y mensajería ───────────────────────────────────────────────────
agent("azure-functions",
      "Designs and reviews Azure Functions and Azure serverless: hosting plans, triggers and bindings, Durable Functions, identity-based connections, monitoring.",
      "Listo. Lectura de Azure y pruebas locales libres; publicar funciones pide confirmación.",
      tools=(R, W, S, WEB), write=["src/**", "functions/**", "infra/**", "bicep/**", "tests/**", "docs/**"],
      allow=AZ_READ + ["func --version*"] + JS_CHECKS + PY_CHECKS + ["dotnet build*", "dotnet test*"],
      ask=["func azure functionapp publish*", "func start*", "az functionapp deploy*"],
      deny=["az functionapp delete*", "az * delete*"])
agent("gcp-serverless",
      "Designs and reviews Google Cloud serverless: Cloud Run services/jobs/functions, Pub/Sub, Eventarc, Workflows, Cloud Tasks, and IAM-based invocation.",
      "Listo. Lectura de Google Cloud libre; desplegar servicios pide confirmación.",
      tools=(R, W, S, WEB), write=["src/**", "infra/**", "terraform/**", "tests/**", "docs/**"],
      allow=GCP_READ + JS_CHECKS + PY_CHECKS,
      ask=["gcloud run deploy*", "gcloud run services update*", "gcloud functions deploy*", "gcloud pubsub * create*"],
      deny=["gcloud * delete*"])
agent("rabbitmq-specialist",
      "Designs and operates RabbitMQ: exchanges and routing, quorum queues and streams, publisher confirms, acks, dead-lettering, and monitoring.",
      "Listo. Inspección del broker libre; cambiar topología pide confirmación y purgar o borrar colas está bloqueado.",
      tools=(R, W, S, WEB), write=["src/**", "definitions/**", "infra/**", "docs/**"],
      allow=["rabbitmqctl list_*", "rabbitmqctl status*", "rabbitmqctl cluster_status*", "rabbitmq-diagnostics *",
             "rabbitmqadmin list *", "aws mq describe-*", "aws mq list-*"],
      ask=["rabbitmqadmin declare *", "rabbitmqctl set_policy*", "rabbitmqctl add_user*", "rabbitmqctl set_permissions*"],
      deny=["rabbitmqctl purge_queue*", "rabbitmqctl delete_*", "rabbitmqadmin delete *", "rabbitmqadmin purge *",
            "rabbitmqctl reset*", "aws mq delete-*"])
agent("aws-messaging",
      "Chooses and configures AWS messaging: SQS (standard/FIFO), SNS, EventBridge, Kinesis, Amazon MQ, and MSK with DLQs, idempotency, and security.",
      "Listo. Lectura de colas y buses libre; enviar mensajes o cambiar configuración pide confirmación.",
      tools=(R, W, S, WEB), write=["infra/**", "terraform/**", "lib/**", "src/**", "docs/**"],
      allow=["aws sqs get-queue-attributes*", "aws sqs list-*", "aws sns list-*", "aws sns get-*", "aws events list-*",
             "aws events describe-*", "aws kinesis describe-*", "aws kinesis list-*"] + TF_READ,
      ask=["aws sqs send-message*", "aws sns publish*", "aws events put-events*", "aws sqs set-queue-attributes*",
           "aws events put-rule*", "aws sqs start-message-move-task*"],
      deny=["aws sqs purge-queue*", "aws sqs delete-*", "aws sns delete-*", "aws events delete-*", "aws kinesis delete-*"])

# ─── Sistemas operativos y parcheo ─────────────────────────────────────────────
agent("linux-security-hardening",
      "Hardens Linux against CIS Benchmarks and STIGs: SSH/SSM access, attack surface, kernel and MAC (SELinux/AppArmor), auditd, FIM, and automation.",
      "Listo. Auditoría con OpenSCAP/Lynis libre; aplicar cambios al sistema pide confirmación y sudo está bloqueado.",
      tools=(R, W, S, WEB), write=["ansible/**", "roles/**", "playbooks/**", "image-builder/**", "packer/**", "docs/**", "reports/**"],
      allow=["lynis audit*", "oscap *", "ansible-lint*", "ansible-playbook * --check*", "sestatus*", "getenforce*",
             "aa-status*", "ss -*", "systemctl list-*", "systemctl status *"],
      ask=["ansible-playbook *", "systemctl restart *", "systemctl disable *"])
agent("windows-server",
      "Administers and hardens Windows Server: PowerShell automation, IIS, Group Policy baselines, updates, clustering, and EC2/Azure specifics.",
      "Listo. Diagnóstico en modo lectura; los cambios se entregan como scripts con -WhatIf para que los ejecutes tú.",
      tools=(R, W, S, WEB), write=["scripts/**", "dsc/**", "gpo/**", "docs/**", "runbooks/**"],
      allow=["Invoke-ScriptAnalyzer*", "Get-*", "aws ssm describe-*", "aws ssm list-*"],
      ask=["Set-*", "Install-*", "Enable-*", "Disable-*", "Restart-*", "Invoke-Command*", "aws ssm send-command*"],
      deny=["Remove-*", "Format-*", "Clear-*", "Stop-Computer*", "Restart-Computer*"])
agent("active-directory",
      "Secures Active Directory and hybrid identity: tiering, Kerberoasting, delegation, AD CS, ACL attack paths, LAPS, gMSA, and monitoring.",
      "Listo. Análisis de rutas de ataque en modo lectura; la recolección ofensiva requiere autorización y confirmación.",
      tools=(R, W, S, WEB), write=["docs/**", "reports/**", "scripts/**"],
      allow=["Get-AD*", "Get-GPO*", "Get-GPResultantSetOfPolicy*"],
      ask=["SharpHound*", "bloodhound-python*", "certipy find*", "Set-AD*", "New-AD*"],
      deny=["Remove-AD*", "Disable-AD*", "Reset-*Password*", "certipy req*", "certipy auth*"])
agent("patch-management",
      "Runs risk-based patch management: SLAs by exploitation, rings, pre/post checks, automation with SSM Patch Manager, Azure Update Manager, WSUS, Ansible.",
      "Listo. Cumplimiento y planes de parcheo en modo lectura; desplegar parches pide confirmación.",
      tools=(R, W, S, WEB), write=["docs/**", "reports/**", "ansible/**", "playbooks/**", "infra/**"],
      allow=["aws ssm describe-*", "aws ssm list-*", "aws ssm get-*", "aws inspector2 list-*", "az * list*", "az * show*",
             "ansible-playbook * --check*"],
      ask=["aws ssm send-command*", "aws ssm start-automation-execution*", "ansible-playbook *",
           "aws ssm create-maintenance-window*"],
      deny=["aws ssm delete-*", "aws ssm deregister-*"])

# ─── Videojuegos, sonido y 3D ──────────────────────────────────────────────────
agent("unity-game-developer",
      "Builds and reviews Unity games in C#: component architecture, ScriptableObjects, allocation-free gameplay code, profiling, Addressables, and builds.",
      "Listo. Revisamos código y rendimiento con evidencia del profiler.",
      write=["Assets/**", "Packages/manifest.json", "ProjectSettings/**", "docs/**"],
      allow=["dotnet format --verify-no-changes*"],
      ask=["Unity *", "unity-editor *", "*/Unity -batchmode*"])
agent("unreal-engine-developer",
      "Builds and reviews Unreal Engine 5 projects in C++ and Blueprints: gameplay framework, GAS, replication, Nanite/Lumen, and Unreal Insights.",
      "Listo. Revisamos gameplay, red y rendimiento; compilar el proyecto pide confirmación.",
      write=["Source/**", "Config/**", "Plugins/**", "docs/**"],
      ask=["*/RunUAT.sh*", "*/RunUAT.bat*", "*/Build.sh*", "UnrealEditor-Cmd*"])
agent("game-designer",
      "Designs game systems, mechanics, progression, economies, and levels; writes GDDs, balances with spreadsheets, plans playtests, and respects players.",
      "Listo. Diseño de juego validado con playtests, con economías justas y accesibilidad desde el inicio.",
      **dict(DOCS_ONLY, write=["docs/**", "design/**", "balance/**"]))
agent("game-audio-designer",
      "Designs and implements interactive game audio with FMOD, Wwise, MetaSounds, and Unity Audio: SFX, adaptive music, mixing, and platform budgets.",
      "Listo. Audio interactivo con presupuestos de memoria y CPU por plataforma.",
      tools=(R, W, S, WEB), write=["docs/**", "audio/**", "Assets/Audio/**", "Content/Audio/**"],
      allow=["ffprobe *", "sox --i *"],
      ask=["ffmpeg *", "sox *"])
agent("audio-engineering",
      "Guides recording, mixing, mastering, and delivery to loudness standards, and helps developers with digital audio and DSP fundamentals.",
      "Listo. Medimos loudness y true peak; procesar archivos pide confirmación para no sobrescribir originales.",
      tools=(R, W, S, WEB), write=["docs/**", "audio/**", "exports/**"],
      allow=["ffprobe *", "sox --i *", "ffmpeg -i * -af ebur128* -f null*"],
      ask=["ffmpeg *", "sox *"])
agent("3d-modeling",
      "Guides 3D modeling for games, web, and print: topology, UVs, PBR texturing, baking, LODs, budgets, and export to engines and glTF.",
      "Listo. Assets con presupuestos definidos y validados en el motor de destino.",
      tools=(R, W, S, WEB), write=["docs/**", "art/**", "assets/**", "scripts/**"],
      allow=["gltf-validator*", "npx gltf-validator*", "npx @gltf-transform/cli inspect*"],
      ask=["blender -b*", "blender --background*", "npx @gltf-transform/cli *"])
agent("technical-artist",
      "Bridges art and engineering: shaders and materials, DCC and engine tools, procedural content, rigging support, and GPU performance budgets.",
      "Listo. Shaders y herramientas medidos en hardware objetivo, con controles simples para artistas.",
      tools=(R, W, S, WEB), write=["Assets/**", "Content/**", "Shaders/**", "tools/**", "scripts/**", "docs/**"],
      allow=["python -m py_compile*", "ruff check*"],
      ask=["blender -b*", "blender --background*", "hython *"])

# ─── Blockchain ────────────────────────────────────────────────────────────────
agent("blockchain-protocol-engineer",
      "Core blockchain protocol engineering: consensus, P2P networking, execution and state, rollups and data availability, client implementation in Go/Rust.",
      "Listo. Código crítico de consenso con pruebas exhaustivas; nodos locales y devnets piden confirmación.",
      tools=(R, W, S, WEB), write=["src/**", "crates/**", "cmd/**", "internal/**", "pkg/**", "specs/**", "tests/**", "docs/**"],
      allow=["go test*", "go vet*", "go build*", "cargo test*", "cargo check*", "cargo clippy*", "golangci-lint run*"],
      ask=["geth *", "reth *", "anvil*", "kurtosis *", "docker compose up*"],
      deny=["cast send*", "geth * --mainnet*"])
agent("smart-contract-engineer",
      "Builds production smart contracts in Solidity/Vyper with Foundry and Hardhat: OpenZeppelin reuse, fuzz and invariant tests, gas, upgrades, safe deployment.",
      "Listo. Compilar y probar en local es libre; desplegar en testnet pide confirmación y mainnet está bloqueado.",
      tools=(R, W, S, WEB), write=["src/**", "contracts/**", "test/**", "script/**", "foundry.toml", "hardhat.config.*", "docs/**"],
      allow=["forge build*", "forge test*", "forge coverage*", "forge fmt*", "forge snapshot*", "slither *", "aderyn *",
             "solhint *", "npx hardhat compile*", "npx hardhat test*"],
      ask=["anvil*", "forge script*", "npx hardhat run*", "forge verify-contract*"],
      deny=["forge script * --broadcast --rpc-url *mainnet*", "cast send*", "cast wallet *", "npx hardhat run * --network mainnet*"])
agent("dapp-web3-developer",
      "Builds dApp front ends and backends with wagmi, viem, ethers, WalletConnect, SIWE, indexers, and account abstraction, with safe transaction UX.",
      "Listo. Desarrollo contra cadenas locales y testnets; enviar transacciones a mainnet está bloqueado.",
      tools=(R, W, S, WEB), write=FRONT_WRITE + ["subgraph/**", "indexer/**", "abis/**"],
      allow=JS_CHECKS + ["npx playwright test*", "graph codegen*", "graph build*"],
      ask=INSTALL_ASK + ["anvil*", "npm run dev*", "graph deploy*"],
      deny=["cast send*", "cast wallet *"])

# Orquestador (se define al final para conocer a todos los demás)
specialists = sorted(A.keys())
agent("agent-orchestrator",
      "Orchestrates the ITera Agent Suite: decomposes any development request, routes each task to the right specialist agent, and consolidates the results.",
      "Listo. Cuéntame el objetivo y armo el plan con los agentes adecuados.",
      tools=(R, W, S, WEB, "subagent"), write=["docs/**", "reports/**"],
      subagents=specialists)

# ─── Construcción del JSON ─────────────────────────────────────────────────────
def build(slug, a):
    rules = []
    if a["write"]:
        rules.append({"capability": "fs_write", "match": a["write"], "effect": "allow"})
    rules.append({"capability": "fs_read", "match": SECRETS_READ_DENY, "exclude": SECRETS_READ_EXCLUDE, "effect": "deny"})
    rules.append({"capability": "shell", "match": GIT_READ + a["allow"], "effect": "allow"})
    rules.append({"capability": "shell", "match": GIT_WRITE_ASK + a["ask"], "effect": "ask"})
    rules.append({"capability": "shell", "match": SHELL_DENY + a["deny"], "effect": "deny"})
    if a["subagents"]:
        rules.append({"capability": "subagent", "match": a["subagents"], "effect": "allow"})
    return {
        "name": slug,
        "description": a["description"],
        "prompt": f"file://./{slug}/agent.md",
        "tools": a["tools"],
        "includeMcpJson": False,
        "resources": BASE_RESOURCES + a["extra_res"],
        "permissions": {"rules": rules},
        "welcomeMessage": a["welcome"],
    }

def dedupe(xs):
    seen, out = set(), []
    for x in xs:
        if x not in seen:
            seen.add(x); out.append(x)
    return out

def dump(obj):
    """JSON legible: cada regla de permisos en una sola línea, como la plantilla original."""
    rules = obj["permissions"]["rules"]
    head = {k: v for k, v in obj.items() if k != "permissions" and k != "welcomeMessage"}
    lines = json.dumps(head, indent=2, ensure_ascii=False)[:-2].rstrip()  # sin la llave final
    rule_lines = ",\n".join("      " + json.dumps(r, ensure_ascii=False) for r in rules)
    return (lines + ',\n  "permissions": {\n    "rules": [\n' + rule_lines + "\n    ]\n  },\n"
            + '  "welcomeMessage": ' + json.dumps(obj["welcomeMessage"], ensure_ascii=False) + "\n}\n")

on_disk = sorted(d for d in os.listdir(AGENTS_DIR) if os.path.isdir(os.path.join(AGENTS_DIR, d)))
missing = sorted(set(on_disk) - set(A)); extra = sorted(set(A) - set(on_disk))
assert not missing and not extra, f"faltan definiciones: {missing} / sin carpeta: {extra}"

for slug, a in A.items():
    for k in ("write", "allow", "ask", "deny"):
        a[k] = dedupe(a[k])
    obj = build(slug, a)
    text = dump(obj)
    json.loads(text)  # el formato personalizado sigue siendo JSON válido
    assert os.path.isfile(os.path.join(AGENTS_DIR, slug, "agent.md"))
    with open(os.path.join(AGENTS_DIR, f"{slug}.json"), "w") as f:
        f.write(text)
print(f"{len(A)} configuraciones generadas en {AGENTS_DIR}")
