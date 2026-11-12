"""Deterministic cross-industry command expansion.

Creates a broad, searchable starter library from reusable professional task patterns.
These are prompt templates, not claims of tool integrations or licensed professional advice.
"""
from app.models import Category, Command

DOMAINS = [
("business-strategy","Business Strategy","Strategy, operating models and business planning.","briefcase-business"),
("product-management","Product Management","Product discovery, roadmaps and delivery.","package"),
("project-management","Project Management","Project planning, governance and execution.","kanban"),
("finance-accounting","Finance & Accounting","Budgets, controls, reporting and analysis.","calculator"),
("marketing","Marketing","Brand, campaigns, content and growth.","megaphone"),
("sales","Sales & Partnerships","Pipeline, proposals, negotiation and partnerships.","handshake"),
("human-resources","Human Resources","Recruitment, people operations and development.","users"),
("education","Education & Training","Teaching, curriculum and assessment design.","graduation-cap"),
("healthcare-admin","Healthcare Administration","Healthcare operations and patient-facing information workflows.","heart-pulse"),
("legal-operations","Legal Operations","Legal intake, contract operations and compliance support.","scale"),
("science-research","Science & Research","Research design, evidence and scientific communication.","microscope"),
("engineering","Engineering","Systems, reliability and engineering delivery.","cog"),
("manufacturing","Manufacturing","Production, quality and process improvement.","factory"),
("design-media","Design & Media","Design, creative direction and media production.","palette"),
("hospitality","Hospitality & Travel","Guest services, tourism and hospitality operations.","hotel"),
("public-sector","Public Sector","Public services, policy operations and civic programs.","landmark"),
("nonprofit","Nonprofit & NGO","Programs, fundraising and impact measurement.","hand-heart"),
("real-estate","Real Estate","Property, facilities and construction operations.","building"),
("customer-service","Customer Support","Customer experience, support and service operations.","headset"),
("logistics","Supply Chain & Logistics","Procurement, inventory and transportation.","truck"),
("cybersecurity","Cybersecurity","Authorized defensive security and governance.","shield"),
("data-analytics","Data Analytics","Data quality, analytics and reporting.","chart-no-axes-combined"),
("it-operations","IT Operations","IT service management, infrastructure and support.","server"),
("entrepreneurship","Entrepreneurship","Startup validation, operations and growth.","rocket"),
("ecommerce","E-commerce","Digital commerce, merchandising and operations.","shopping-cart"),
("insurance","Insurance Operations","Claims, underwriting support and service workflows.","file-check"),
("banking","Banking Operations","Banking service, risk and operational controls.","landmark"),
("agriculture","Agriculture","Farm operations, agribusiness and sustainability.","wheat"),
("automotive","Automotive","Vehicle service, manufacturing and mobility.","car"),
("energy","Energy & Utilities","Energy operations, projects and sustainability.","zap"),
("architecture-construction","Architecture & Construction","Built environment design and project delivery.","drafting-compass"),
("personal-productivity","Personal Productivity","Personal planning, learning and communication.","calendar-check"),
]

PATTERNS = [
("strategy","Strategic Plan","STRATEGY","Create a strategic plan for {subject}. Define current state, desired outcomes, stakeholders, strategic choices, options rejected, capabilities, dependencies, risks, milestones, metrics, governance and review cadence."),
("research","Research Brief","RESEARCH","Develop a reproducible research brief about {subject}. Define questions, scope, search strategy, source hierarchy, inclusion criteria, evidence table, conflicting findings, confidence and unresolved gaps. Never invent sources."),
("requirements","Requirements Specification","REQUIREMENTS","Specify requirements for {subject}. Separate business, user, functional, non-functional, regulatory and operational requirements. Add unique IDs, rationale, priority, dependencies, acceptance criteria and traceability."),
("workflow","Operating Workflow","WORKFLOW","Design an end-to-end workflow for {subject}. Map triggers, actors, inputs, decisions, handoffs, systems, exceptions, controls, outputs, SLAs, escalation and measurable completion criteria."),
("sop","Standard Operating Procedure","SOP","Write an actionable SOP for {subject}. Include purpose, scope, roles, prerequisites, equipment, numbered procedure, safety controls, exception paths, records, quality checks, training and revision history."),
("risk","Risk Assessment","RISK","Assess risks for {subject}. Build a risk register with cause, event, consequence, likelihood, impact, existing controls, residual exposure, owner, mitigation, trigger and contingency. Explain scoring assumptions."),
("audit","Audit Checklist","AUDIT","Create an evidence-led audit checklist for {subject}. Map control objective, test procedure, evidence required, sample approach, pass/fail criteria, exception severity, owner and remediation. Do not claim certification."),
("analysis","Performance Analysis","ANALYSIS","Analyze {subject}. Define population, period, metric formulas, data quality checks, segmentation, baseline, trends, anomalies, confounders, limitations and actionable findings. Do not infer causation from correlation."),
("roadmap","Implementation Roadmap","ROADMAP","Create a phased roadmap for {subject}. Define outcomes, workstreams, milestones, dependencies, effort ranges, owners by role, risks, decision gates, rollout, rollback and success measures."),
("communication","Communication Plan","COMMUNICATION","Create a stakeholder communication plan for {subject}. Segment audiences, desired behavior, message hierarchy, channels, cadence, owner, feedback loop, accessibility and escalation. Avoid unsupported promises."),
("training","Training Program","TRAINING","Design a training program for {subject}. Define learner profiles, prerequisites, competencies, modules, practice, assessment rubric, accessibility, reinforcement and measurable learning outcomes."),
("evaluation","Evaluation Framework","EVALUATION","Create an evaluation framework for {subject}. Define theory of change, questions, indicators, baseline, data collection, sampling, comparison limits, ethics, reporting and learning actions."),
("proposal","Business Proposal","PROPOSAL","Prepare a decision-ready proposal for {subject}. State problem, evidence, options, recommended approach, scope, exclusions, benefits, cost assumptions, timeline, risks, governance and approval requested."),
("dashboard","KPI Dashboard Specification","DASHBOARD","Specify a dashboard for {subject}. Define users, decisions, KPI formulas, dimensions, data sources, freshness, quality rules, access, visual hierarchy, alerts and interpretation caveats."),
("customer","Customer Journey Review","CUSTOMER","Review the customer journey for {subject}. Map stages, user goals, touchpoints, friction, accessibility, emotions, failure recovery, service ownership and prioritized experiments."),
("quality","Quality Plan","QUALITY","Create a quality plan for {subject}. Define standards, quality objectives, review stages, test methods, sampling, defect severity, evidence, nonconformance handling, owners and release criteria."),
("automation","Automation Blueprint","AUTOMATION","Design an automation blueprint for {subject}. Identify candidate tasks, triggers, interfaces, data contracts, permissions, idempotency, retries, observability, human approvals, fallback and measurable ROI assumptions."),
("architecture","Architecture Review","ARCHITECTURE","Review the architecture of {subject}. Describe components, trust boundaries, data flows, dependencies, scalability, reliability, security, privacy, observability, failure modes, trade-offs and migration sequence."),
("policy","Policy Draft","POLICY","Draft an operational policy for {subject}. Define purpose, scope, terms, responsibilities, mandatory controls, exceptions, escalation, records, review cadence and jurisdiction-specific questions for qualified counsel."),
("budget","Budget Framework","BUDGET","Build a transparent budget for {subject}. List cost categories, quantities, unit assumptions, one-time and recurring costs, contingencies, scenarios, funding constraints and variance controls. Never invent supplier quotes."),
("incident","Incident Response Plan","INCIDENT","Create an incident response plan for {subject}. Define severity, detection, triage, containment, communication, evidence preservation, recovery, escalation, post-incident review and exercise criteria."),
("design","Design Brief","DESIGN","Create a design brief for {subject}. Define audience, user needs, constraints, information hierarchy, interaction principles, accessibility, visual direction, deliverables, review stages and acceptance criteria."),
("contract","Contract Operations Review","CONTRACT","Organize a review of {subject}. Extract parties, obligations, dates, deliverables, dependencies, renewal, termination, service levels and open questions from supplied text only. Flag legal interpretation for counsel."),
("forecast","Forecasting Framework","FORECAST","Build a forecast framework for {subject}. Define horizon, historical data, assumptions, seasonality, drivers, scenarios, error metrics, sensitivity, confidence and review cadence. Label estimates clearly."),
("launch","Launch Readiness Review","LAUNCH","Assess launch readiness for {subject}. Review scope, ownership, dependencies, operational support, security, privacy, accessibility, documentation, monitoring, rollback, training and go/no-go criteria."),
]

def _slug(value):
    return "-".join("".join(ch.lower() if ch.isalnum() else " " for ch in value).split())

def seed_expanded_commands(db):
    """Idempotently add 32 x 24 = 768 role/domain command combinations."""
    created = 0
    for domain_slug, domain_name, description, icon in DOMAINS:
        category = db.query(Category).filter_by(slug=domain_slug).first()
        if not category:
            category = Category(slug=domain_slug, name=domain_name, description=description, icon=icon)
            db.add(category)
            db.flush()
        for key, label, syntax_key, instruction in PATTERNS:
            slug = f"{domain_slug}-{key}"
            if db.query(Command.id).filter_by(slug=slug).first():
                continue
            name = f"{domain_name}: {label}"
            syntax = f"/{_slug(domain_slug).replace('-', '_').upper()}_{syntax_key}"
            detailed = (
                f"Act as a senior {domain_name.lower()} specialist. {instruction}\n\n"
                "Execution requirements: first restate the intended outcome and identify missing inputs; "
                "list explicit assumptions instead of silently filling gaps; propose a logical sequence; "
                "show concrete examples, tables or templates where useful; identify decision points and dependencies; "
                "separate verified facts, user-provided facts, estimates and recommendations; include edge cases, "
                "failure modes and mitigations; define measurable acceptance criteria; finish with prioritized next actions. "
                "Use current authoritative sources when research access is available and cite only sources actually consulted. "
                "If tools, files or external systems are unavailable, say so and provide a practical manual alternative."
            )
            db.add(Command(
                slug=slug, name=name, syntax=syntax,
                description=f"{label} tailored to {domain_name.lower()} roles.",
                instruction_template=detailed,
                example_input=f"Prepare a {label.lower()} for a {domain_name.lower()} team.",
                example_output=f"A structured {label.lower()} with scope, steps, evidence, risks and success criteria.",
                difficulty="advanced" if key in {"architecture","audit","risk","incident","contract","forecast"} else "intermediate",
                status="reviewed", tags=[domain_slug, key, "cross-industry", "professional"],
                limitations="Reusable prompt pattern only. Validate against current law, professional standards, source evidence and organization policy; not a substitute for licensed judgment.",
                category_id=category.id,
            ))
            created += 1
    return created


# Focused QA and QA Automation command packs (40 + 40).
QA_SPECIALIST_TASKS = [
    ("requirements-analysis", "Requirements Analysis", """Convert supplied requirements into atomic, testable statements; identify ambiguity, conflicts, dependencies and missing acceptance criteria."""),
    ("test-strategy", "Test Strategy", """Define test levels, types, scope, exclusions, environments, data, tools, roles, risks, entry/exit criteria and measurable coverage."""),
    ("test-plan", "Test Plan", """Create a project test plan with objectives, scope, schedule, resources, dependencies, deliverables, risks and sign-off gates."""),
    ("test-scenarios", "Test Scenario Design", """Derive end-to-end, integration, negative, alternate and exception scenarios from the stated business flows."""),
    ("test-cases", "Detailed Test Cases", """Write uniquely identified test cases with preconditions, data, numbered steps, expected results, priority and traceability."""),
    ("boundary-value", "Boundary Value Analysis", """Identify valid and invalid boundaries, adjacent values, inclusive/exclusive limits and representative test data."""),
    ("equivalence-partition", "Equivalence Partitioning", """Partition inputs into valid and invalid classes and justify the minimum representative tests."""),
    ("decision-table", "Decision Table Testing", """Model combinations of conditions and expected actions; remove impossible rules and expose missing combinations."""),
    ("state-transition", "State Transition Testing", """Model states, events, guards, transitions, invalid transitions and state coverage for the feature."""),
    ("pairwise-testing", "Pairwise Testing", """Identify parameter dimensions and create a risk-aware pairwise coverage set; state combinations intentionally omitted."""),
    ("exploratory-charter", "Exploratory Testing Charter", """Create time-boxed charters with mission, risks, heuristics, data, observations and session debrief."""),
    ("usability-review", "Usability Testing", """Evaluate task completion, learnability, feedback, error recovery, accessibility and user friction with evidence."""),
    ("accessibility-testing", "Accessibility Testing", """Plan keyboard, focus, semantics, labels, contrast, zoom, reduced motion and screen-reader checks; distinguish automated from manual coverage."""),
    ("responsive-testing", "Responsive Testing", """Build viewport/device coverage for layout, navigation, overflow, touch targets, orientation and content reflow."""),
    ("cross-browser", "Cross-Browser Testing", """Define browser/OS coverage, rendering risks, feature compatibility, reproducibility and evidence capture."""),
    ("mobile-testing", "Mobile Application Testing", """Cover install, upgrade, permissions, lifecycle, interruptions, network changes, gestures, device variation and app state."""),
    ("regression-suite", "Regression Suite Design", """Select regression coverage by change impact, business criticality, defect history, dependencies and execution cost."""),
    ("smoke-sanity", "Smoke and Sanity Testing", """Define build verification and focused change checks with clear pass/fail gates and escalation rules."""),
    ("integration-testing", "Integration Testing", """Test service boundaries, contracts, data mapping, retries, timeouts, partial failures and downstream effects."""),
    ("system-testing", "System Testing", """Build end-to-end system coverage across functional and non-functional requirements and realistic user journeys."""),
    ("uat-planning", "UAT Planning", """Prepare business scenarios, representative roles/data, acceptance evidence, defect triage and stakeholder sign-off."""),
    ("api-manual-testing", "Manual API Testing", """Design API checks for methods, status codes, headers, payloads, auth, validation, pagination and error contracts."""),
    ("database-testing", "Database Testing", """Validate persistence, constraints, relationships, transactions, data integrity, migrations and rollback behavior."""),
    ("sql-validation", "SQL Data Validation", """Write read-only SQL checks for counts, duplicates, nulls, referential integrity and reconciliation; explain expected results."""),
    ("security-test-planning", "Security Test Planning", """Create authorized, bounded security checks for authentication, authorization, session handling, input validation and information exposure."""),
    ("performance-test-planning", "Performance Test Planning", """Define workload, concurrency, ramp-up, duration, percentiles, resource metrics, thresholds and realistic data assumptions."""),
    ("reliability-testing", "Reliability and Recovery Testing", """Plan resilience checks for service interruption, restart, retry, recovery, data consistency and graceful degradation."""),
    ("data-migration-testing", "Data Migration Testing", """Compare source and target records, mappings, transformations, totals, rejected rows, reconciliation and rollback evidence."""),
    ("localization-testing", "Localization Testing", """Check language, date/time, currency, number formats, text expansion, encoding, sorting and locale-specific behavior."""),
    ("installation-upgrade", "Installation and Upgrade Testing", """Test clean install, upgrade paths, configuration retention, permissions, rollback and uninstall cleanup."""),
    ("defect-report", "Defect Report Writing", """Create reproducible defects with environment, build, preconditions, steps, actual/expected results, evidence and impact."""),
    ("severity-priority", "Severity and Priority Triage", """Classify impact and urgency consistently; explain rationale, workaround, affected users and release implications."""),
    ("root-cause-analysis", "Root Cause Analysis", """Use evidence-based 5 Whys/fishbone analysis; separate trigger, contributing factors and systemic cause."""),
    ("test-metrics", "QA Metrics Dashboard", """Define execution, pass rate, escaped defects, reopen rate, coverage and cycle time with formulas and interpretation caveats."""),
    ("traceability-matrix", "Requirements Traceability Matrix", """Map requirements to scenarios, cases, execution results and defects; highlight uncovered and obsolete requirements."""),
    ("release-readiness", "Release Readiness Assessment", """Evaluate test evidence, open defects, residual risk, environment stability, rollback and explicit go/no-go criteria."""),
    ("test-data-design", "Test Data Design", """Create privacy-safe representative datasets including valid, invalid, boundary, duplicate and masked records."""),
    ("risk-based-testing", "Risk-Based Testing", """Rank features by likelihood, impact, exposure, complexity and change; translate ranking into test depth."""),
    ("qa-estimation", "QA Estimation", """Estimate test design, setup, execution, automation and retest effort using assumptions, ranges and contingency."""),
    ("agile-qa", "Agile QA Sprint Planning", """Integrate QA into refinement, definition of ready/done, story acceptance, daily collaboration and sprint exit."""),
    ("production-validation", "Production Smoke Validation", """Prepare safe post-deployment checks, monitoring signals, rollback triggers and evidence without destructive production actions."""),
]
QA_AUTOMATION_TASKS = [
    ("playwright-framework", "Playwright Framework Design", """Design a maintainable Playwright framework with fixtures, config, projects, POM, utilities, data and reporting."""),
    ("playwright-locators", "Playwright Locator Strategy", """Choose resilient role, label, text and test-id locators; avoid brittle XPath and explain strict-mode behavior."""),
    ("playwright-waits", "Playwright Synchronization", """Use auto-waiting, web-first assertions and event-based waits; remove fixed sleeps and diagnose race conditions."""),
    ("playwright-fixtures", "Playwright Fixtures", """Design isolated fixtures with clear setup/teardown scope, dependency injection and failure-safe cleanup."""),
    ("playwright-pom", "Playwright Page Object Model", """Generate typed page objects with encapsulated locators, user-focused actions and assertions in tests."""),
    ("playwright-api", "Playwright API Testing", """Build APIRequestContext tests for auth, schema, status, headers, negative cases and shared setup."""),
    ("playwright-auth", "Playwright Authentication", """Create safe storage-state workflows, role-based sessions, expiry checks and secret handling."""),
    ("playwright-network", "Playwright Network Mocking", """Intercept, modify and fulfill requests for deterministic tests; validate both mocked and real integration paths."""),
    ("playwright-download", "Playwright File Download", """Automate download events, filename/content checks, temporary paths and cleanup."""),
    ("playwright-upload", "Playwright File Upload", """Test single/multiple uploads, type/size validation, progress, failure handling and secure fixtures."""),
    ("playwright-frames", "Playwright Frames and Dialogs", """Handle iframes, alerts, confirms, prompts and popup pages using event-safe patterns."""),
    ("playwright-trace", "Playwright Trace Debugging", """Configure traces, screenshots, videos and logs; diagnose failures from artifacts without leaking secrets."""),
    ("playwright-parallel", "Playwright Parallel Execution", """Configure workers, sharding, retries and resource limits while preserving test isolation."""),
    ("playwright-mobile-emulation", "Playwright Mobile Emulation", """Configure device profiles, viewport, touch, locale, timezone and network conditions; state emulation limits."""),
    ("playwright-accessibility", "Playwright Accessibility Automation", """Combine automated accessibility scans with keyboard and assistive-technology manual checks; avoid claiming full conformance."""),
    ("playwright-visual", "Playwright Visual Regression", """Set screenshot baselines, masking, thresholds, deterministic data and review workflow for visual diffs."""),
    ("playwright-ci", "Playwright CI Pipeline", """Create CI stages for install, browser caching, lint, tests, artifacts, reports and failure diagnostics."""),
    ("playwright-flaky", "Flaky Test Diagnosis", """Classify flakiness causes across data, timing, environment and concurrency; propose evidence-led fixes."""),
    ("playwright-data", "Playwright Test Data Management", """Create factories, API seeding, unique data, cleanup and parallel-safe isolation."""),
    ("playwright-tags", "Playwright Test Organization", """Structure tags, annotations, projects, grep filters, smoke/regression suites and ownership."""),
    ("selenium-framework", "Selenium Framework Design", """Design Selenium architecture with driver factory, config, waits, page objects, utilities and reporting."""),
    ("selenium-waits", "Selenium Wait Strategy", """Implement explicit waits for observable conditions; diagnose stale elements, overlays and synchronization failures."""),
    ("selenium-grid", "Selenium Grid Execution", """Configure remote sessions, browser capabilities, node health, parallel limits and artifact collection."""),
    ("selenium-pom", "Selenium Page Object Model", """Generate maintainable page objects with stable locators, reusable components and clean test assertions."""),
    ("selenium-js", "Selenium JavaScript Automation", """Create Node.js Selenium tests with async control, driver lifecycle, assertions and deterministic cleanup."""),
    ("pytest-architecture", "Pytest Framework Architecture", """Design conftest, fixtures, markers, config, test layers, plugins and reusable utilities."""),
    ("pytest-parametrize", "Pytest Parametrization", """Create readable parameterized cases with IDs, data sources and failure diagnostics."""),
    ("pytest-fixtures", "Pytest Fixture Strategy", """Select fixture scopes, dependency ordering, yield teardown and isolation without shared mutable state."""),
    ("pytest-mocking", "Pytest Mocking", """Use monkeypatch and mocks at correct boundaries; assert interactions without over-mocking implementation details."""),
    ("pytest-coverage", "Pytest Coverage Strategy", """Measure branch/line coverage and identify meaningful untested behavior; do not equate coverage percentage with quality."""),
    ("api-automation", "API Automation Framework", """Build reusable API clients, auth helpers, schema validation, contract assertions and environment configuration."""),
    ("requests-api", "Python Requests API Tests", """Generate requests-based tests for methods, payloads, headers, auth, timeouts and response validation."""),
    ("contract-testing", "API Contract Testing", """Validate consumer/provider contracts, schema evolution, compatibility and breaking-change detection."""),
    ("database-automation", "Database Automation", """Automate safe database assertions and transaction cleanup using isolated test data and least privilege."""),
    ("appium-framework", "Appium Framework Design", """Design Appium cross-platform architecture, capabilities, driver lifecycle, page objects and device allocation."""),
    ("appium-android", "Appium Android Automation", """Automate Android flows with UiAutomator2, accessibility IDs, permissions, activity lifecycle and logs."""),
    ("appium-ios", "Appium iOS Automation", """Automate iOS flows with XCUITest, WDA, signing prerequisites, simulator/device capabilities and accessibility locators."""),
    ("mobile-cloud", "Cloud Device Testing", """Plan device-farm matrix, OS/device coverage, concurrency, artifacts, cost and reproducibility."""),
    ("automation-reporting", "Automation Reporting", """Create actionable reports with suite status, failure category, screenshots, traces, logs and trend metrics."""),
    ("automation-maintenance", "Automation Maintenance Review", """Identify brittle tests, duplication, poor abstractions, flaky dependencies and maintenance hotspots."""),
    ("ai-test-generation", "AI Test Generation", """Use an LLM to derive tests from requirements with traceability, uncertainty labels, human review and duplicate detection."""),
]

def seed_qa_specialist_commands(db):
    """Add focused QA and QA automation prompt templates idempotently."""
    created = 0
    packs = [
        ("qa", "Quality Assurance", "Manual QA, test design, quality strategy and release assurance.", "clipboard-check", "QA", QA_SPECIALIST_TASKS),
        ("qa-automation", "QA Automation", "Browser, API, mobile and framework automation engineering.", "bot", "QAA", QA_AUTOMATION_TASKS),
    ]
    for category_slug, category_name, description, icon, prefix, tasks in packs:
        category = db.query(Category).filter_by(slug=category_slug).first()
        if not category:
            category = Category(slug=category_slug, name=category_name, description=description, icon=icon)
            db.add(category)
            db.flush()
        for key, label, focus in tasks:
            slug = f"{category_slug}-specialist-{key}"
            if db.query(Command.id).filter_by(slug=slug).first():
                continue
            syntax = f"/{prefix}_{key.replace('-', '_').upper()}"
            instruction = (
                f"Act as a senior QA engineer specializing in {label.lower()}. {focus}\\n\\n"
                "Work from the supplied application context, requirements, artifacts and authorized scope. "
                "Start by listing assumptions and missing inputs. Provide a step-by-step method, concrete examples, "
                "test data or code where appropriate, expected outcomes, negative and boundary cases, and traceability "
                "to business risk. Explain setup and execution prerequisites. Define observable pass/fail criteria, "
                "evidence to capture, failure triage, cleanup and follow-up regression coverage. Distinguish automated "
                "checks from manual judgment. For automation, use stable locators, explicit synchronization, isolated data, "
                "reliable teardown, readable assertions, diagnostics and CI suitability. Never claim a test was executed "
                "unless execution evidence is provided; never invent product behavior, test results or coverage. "
                "For security testing, require explicit authorization and stay within the approved target and scope."
            )
            db.add(Command(
                slug=slug, name=f"{category_name}: {label}", syntax=syntax,
                description=f"{label} for practical QA engineering teams.", instruction_template=instruction,
                example_input=f"Apply {label.lower()} to a web application with documented requirements.",
                example_output=f"A practical {label.lower()} deliverable with steps, examples, evidence and acceptance criteria.",
                difficulty="advanced" if key in {"security-test-planning","performance-test-planning","playwright-framework","selenium-grid","appium-ios","contract-testing","pytest-architecture"} else "intermediate",
                status="reviewed", tags=[category_slug, key, "quality-engineering", "testing"],
                limitations="Reusable prompt template, not proof of test execution or a native provider integration. Validate against the actual application, tool versions and approved test scope.",
                category_id=category.id,
            ))
            created += 1
    return created
