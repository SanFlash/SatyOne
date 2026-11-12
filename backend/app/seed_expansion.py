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
