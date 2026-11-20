const APP_URL='https://satyone.vercel.app';
const $=id=>document.getElementById(id);let latest='';
function buildPrompt(objective,audience,tone){return [
'# SATYONE QUICK PROMPT','## ROLE AND STANDARD','Act as a capable subject-matter expert and practical delivery partner. Be accurate, specific, structured and transparent about uncertainty. Do not invent facts, sources, tool access or completed actions.',
'## OBJECTIVE',objective.trim(),'## AUDIENCE AND COMMUNICATION','Audience: '+(audience.trim()||'General professional audience'),'Tone: '+tone+'. Match terminology, depth and examples to the audience.',
'## CONTEXT AND ASSUMPTIONS','Use supplied information as context. Identify missing, ambiguous or contradictory inputs. Ask only material clarification questions; otherwise state reasonable assumptions and continue.',
'## EXECUTION','Break the task into logical steps. Explain important decisions and trade-offs. Produce the requested deliverable itself, not merely advice about producing it. Include examples, templates, code or tables when useful.',
'## SCENARIOS AND QUALITY CHECKS','Cover normal success, alternate paths, invalid and missing inputs, boundary conditions, duplicates, permissions, concurrency, timeouts, dependency failures, interruption, recovery and rollback where relevant. Add domain-specific cases rather than irrelevant filler.',
'## RISK AND RESPONSIBLE HANDLING','Protect confidential information. Respect authorization and safety boundaries. Flag high-impact decisions, compliance concerns and specialist review needs.',
'## ACCEPTANCE CRITERIA','Define observable completion criteria. Check completeness, correctness, consistency, feasibility, clarity and alignment with every stated constraint.',
'## OUTPUT CONTRACT','Lead with the result. Use clear headings and actionable steps. Separate verified facts, assumptions, estimates and recommendations. State limitations and unresolved questions.',
'## FINAL SELF-REVIEW','Verify the objective, constraints, edge cases and factual integrity. Never fabricate citations, tests, metrics or execution results.'
].join('\\n\\n')}
async function init(){try{const d=await chrome.storage.local.get('selectedText');if(d.selectedText){$('objective').value=d.selectedText;await chrome.storage.local.remove('selectedText');$('status').textContent='Selected webpage text loaded.'}}catch{}}
$('generate').addEventListener('click',()=>{const v=$('objective').value.trim();if(v.length<5){$('status').textContent='Enter a task with at least five characters.';return}latest=buildPrompt(v,$('audience').value,$('tone').value);$('result').textContent=latest;$('resultWrap').classList.remove('hidden');$('status').textContent='Prompt generated locally.'});
$('copy').addEventListener('click',async()=>{if(!latest)return;try{await navigator.clipboard.writeText(latest);$('status').textContent='Prompt copied to clipboard.'}catch{$('status').textContent='Copy unavailable. Select the generated text manually.'}});
$('openApp').addEventListener('click',()=>chrome.tabs.create({url:APP_URL}));init();