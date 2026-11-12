from sqlalchemy.orm import Session
from app.models import Category, Command, Provider, Workflow

CATALOG=[
("general","General Intelligence","Explain, reason, summarize and compare.","brain",[
("deep-dive","Deep Dive","/DEEPDIVE","Ask for a comprehensive explanation.","Explain {topic} comprehensively. Organize the response into concepts, examples, trade-offs, practical applications, and a concise summary.","Explain API testing.","A structured guide to API testing with examples.","beginner",["explanation","learning"]),
("eli5","Explain Simply","/ELI5","Explain a complex topic in beginner-friendly language.","Explain {topic} in simple language. Define unfamiliar terms, use a relatable analogy, and finish with three key takeaways.","Explain neural networks.","A simple analogy-led explanation.","beginner",["learning","simplification"]),
("verify","Verify & Qualify","/VERIFY","Separate supported facts from assumptions and uncertainty.","Review the answer to {topic}. Identify factual claims, assumptions, uncertainty, and what evidence would be needed. Do not invent citations or claim verification without evidence.","Review this technical recommendation.","A claim-by-claim review with uncertainty noted.","advanced",["accuracy","research"])]),
("development","Development","Build, debug, review and improve software.","code",[
("debug","Debug","/DEBUG","Investigate a code issue systematically.","Act as a careful debugging partner. Given {code_or_error}, identify the likely root cause, explain why it occurs, propose the smallest safe fix, and provide a test that confirms the fix. State assumptions.","Fix this Python traceback.","Root cause, patch and regression test.","intermediate",["python","debugging"]),
("refactor","Refactor","/REFACTOR","Improve code structure without changing intended behavior.","Refactor {code} for readability and maintainability while preserving behavior. Explain changes and provide tests that demonstrate behavioral equivalence.","Refactor this API handler.","Cleaner implementation and tests.","intermediate",["code-quality"]),
("architecture","Architecture Review","/ARCHITECTURE","Review a system design and identify trade-offs.","Review this system design: {design}. Identify components, data flows, failure modes, security boundaries, scaling risks, and practical improvements. Distinguish requirements from assumptions.","Review a SaaS architecture.","Architecture review with risks and recommendations.","advanced",["system-design"])]),
("qa","Quality Assurance","Testing, automation, coverage and defect reporting.","flask-conical",[
("testcase","Generate Test Cases","/TESTCASE","Create traceable test cases from requirements.","Create test cases for {requirement}. Include ID, scenario, preconditions, steps, test data, expected result, priority, and positive, negative and boundary coverage. Flag ambiguities.","Test a login page.","A traceable test case matrix.","beginner",["testing","test-design"]),
("automation","Automation Plan","/AUTOMATE","Design a maintainable test automation approach.","Design an automation plan for {application}. Recommend tools, architecture, test selection, fixtures, page objects where appropriate, data strategy, reporting, CI integration, and risks. Include a phased implementation.","Automate a web checkout flow.","A practical automation blueprint.","advanced",["playwright","selenium"]),
("api-test","API Test Design","/APITEST","Design API validation and negative tests.","Design API tests for {endpoint_or_contract}. Cover status codes, schema, authentication, authorization, validation, boundary values, error handling, idempotency and rate limits where applicable.","Test a user registration endpoint.","API test matrix and sample assertions.","intermediate",["api","testing"])]),
("creative","Creative Studio","Writing, design and creative production.","palette",[
("creative-brief","Creative Brief","/CREATIVE","Turn an idea into a detailed creative brief.","Create a creative brief for {idea}. Define audience, objective, message, visual direction, tone, deliverables, constraints and evaluation criteria.","Create a campaign concept.","A structured creative brief.","beginner",["design","content"])]),
("productivity","Productivity","Emails, planning, documentation and meetings.","calendar-check",[
("stepwise","Stepwise Plan","/STEPWISE","Break a goal into actionable stages.","Turn {goal} into an actionable sequence. For each step provide the outcome, actions, dependencies, estimated effort, and completion criteria. Highlight blockers.","Launch a small web app.","A sequenced implementation plan.","beginner",["planning"]),
("professional","Professional Rewrite","/PROFESSIONAL","Improve clarity and professional tone.","Rewrite {text} in a clear, concise and professional tone. Preserve meaning, factual details, links and commitments. Do not add unsupported claims.","Polish a hiring email.","A polished ready-to-send draft.","beginner",["writing"])]),
("data","Data Intelligence","SQL, analysis and data interpretation.","chart-no-axes-combined",[
("data-analysis","Data Analysis","/ANALYZE","Analyze a dataset with explicit assumptions.","Analyze {dataset_or_data}. Explain data quality, methodology, key patterns, limitations and actionable findings. Do not infer causation from correlation.","Analyze monthly sales.","Findings with caveats and recommendations.","intermediate",["analytics"])]),
("security","Security & Safety","Defensive security, secure design and risk assessment.","shield-check",[
("secure-review","Secure Code Review","/SECURE_REVIEW","Review code for defensive security issues.","Review {code_or_design} for security weaknesses. Focus on authorized defensive assessment, explain impact, evidence, remediation and safe validation. Do not provide exploit instructions for unauthorized targets.","Review an authentication handler.","Prioritized findings and fixes.","advanced",["security","defensive"])])]
PROVIDERS=[
("openai","OpenAI","Official API integration can be enabled with a server-side API key.","https://platform.openai.com/docs","directory"),
("anthropic","Anthropic Claude","Directory entry; adapter integration is a future module.","https://docs.anthropic.com/","directory"),
("google","Google Gemini","Directory entry; adapter integration is a future module.","https://ai.google.dev/gemini-api/docs","directory"),
("microsoft","Microsoft Copilot","Availability depends on product/API.","https://learn.microsoft.com/","directory"),
("perplexity","Perplexity","Verify API capabilities in official documentation.","https://docs.perplexity.ai/","directory"),
("deepseek","DeepSeek","Directory entry; adapter integration is a future module.","https://api-docs.deepseek.com/","directory"),
("xai","xAI Grok","Directory entry; adapter integration is a future module.","https://docs.x.ai/","directory"),
("mistral","Mistral","Directory entry; adapter integration is a future module.","https://docs.mistral.ai/","directory")]
WORKFLOWS=[
("qa-web-audit","Web QA Audit","A structured, authorized workflow for assessing a website's quality.","quality-assurance","intermediate",["Clarify scope and authorization","Map critical user journeys","Design functional and responsive checks","Run approved tests and capture evidence","Prioritize defects and produce a report"]),
("new-feature-build","Build a New Feature","Plan and implement a software feature with quality gates.","development","intermediate",["Clarify requirements and acceptance criteria","Design API and data model","Implement the smallest vertical slice","Add automated tests","Review security, accessibility and deployment"]),
("research-brief","Research Brief","Turn a question into a structured research plan.","research","beginner",["Define the research question","List claims that require evidence","Gather authoritative sources","Compare evidence and uncertainty","Produce a cited summary"])]

def seed_catalog(db:Session):
    for slug,name,desc,icon,items in CATALOG:
        category=db.query(Category).filter_by(slug=slug).first()
        if not category:
            category=Category(slug=slug,name=name,description=desc,icon=icon);db.add(category);db.flush()
        for c in items:
            cslug,cname,syntax,description,template,exin,exout,difficulty,tags=c
            if not db.query(Command).filter_by(slug=cslug).first():
                db.add(Command(slug=cslug,name=cname,syntax=syntax,description=description,instruction_template=template,
                    example_input=exin,example_output=exout,difficulty=difficulty,status="reviewed",tags=tags,
                    limitations="A reusable prompt pattern, not a guaranteed model capability.",category_id=category.id))
    for slug,name,desc,docs,status in PROVIDERS:
        if not db.query(Provider).filter_by(slug=slug).first():
            db.add(Provider(slug=slug,name=name,description=desc,docs_url=docs,integration_status=status))
    for slug,name,desc,category,difficulty,steps in WORKFLOWS:
        if not db.query(Workflow).filter_by(slug=slug).first():
            db.add(Workflow(slug=slug,name=name,description=desc,category=category,difficulty=difficulty,steps=steps))
    db.commit()
