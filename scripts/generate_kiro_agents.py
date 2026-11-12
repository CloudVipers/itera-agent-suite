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
