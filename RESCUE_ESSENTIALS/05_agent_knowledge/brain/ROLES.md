# AI Role Routing — Hyperbolic Time Chamber

Different tasks need different thinking. FCC Claude handles direct operator work. For automated workflows and chat, route to the right model for the job.

## ROLE 1: CAMPAIGN STRATEGY
When: Morning briefs, daily priorities, big decisions, debate prep
Model: NVIDIA NIM Nemotron 120B (deep reasoning)
Fallback: Gemini 3.6 Flash
Focus: Strategic thinking, connecting dots, long-term planning
Voice: Direct, decisive, no fluff

## ROLE 2: RESEARCH
When: Jacksonville data questions, policy analysis, fact-checking claims
Model: Gemini 3.6 Flash (fast + thorough)
Fallback: DeepSeek V4 Flash
Focus: Accuracy, sources, numbers, accountability
Voice: Precise, cited, evidence-based

## ROLE 3: CONTENT CREATION
When: Writing LinkedIn posts, social content, blog articles, emails, speeches
Model: Groq (fast generation for drafts)
Fallback: NVIDIA NIM Nemotron
Focus: Story-driven, value-first, human language, MiLyfe's voice
Voice: Warm, honest, powerful, never selling — just truth

## ROLE 4: RAPID RESPONSE
When: Breaking news, opponent activity, urgent situations
Model: Cerebras (lowest latency)
Fallback: Groq
Focus: Speed, accuracy, on-message, immediate talking points
Voice: Quick, sharp, factual, ready to publish

## ROLE 5: PLATFORM SUPPORT
When: Explaining MiLyfe features, preparing demos, answering technical questions
Model: FCC Claude (direct terminal, best reasoning)
Fallback: Nemotron 120B
Focus: Accurate representation of the NEW platform (not old MiJaxx)
Voice: Clear, honest about what exists vs what's planned

## ROLE 6: OPPONENT INTELLIGENCE
When: Tracking candidates, analyzing their moves, finding accountability gaps
Model: Gemini 3.6 Flash
Fallback: DeepSeek V4 Flash
Focus: Record-based only, never personal attacks, find the gap between promise and delivery
Voice: Clinical, factual, documented

## How To Activate (in Open WebUI or workflows)

Start your message with the context:
- "Strategy: What should my priority be this week?"
- "Research: What's the current pension liability number?"
- "Write: Draft a LinkedIn post about infrastructure"
- "Rapid: Deegan just announced X — what's our response?"
- "Platform: How does the weekly share work in the new app?"
- "Intel: What has [candidate] posted this week?"

Or just describe what you need — the system decides.

## FCC Claude (Direct Operator)

For hands-on work — writing code, building workflows, analyzing documents, managing the war room itself — use FCC Claude directly from terminal. It has full access to the codebase, can read/write files, run commands, and execute complex multi-step tasks. This is the primary working tool.
