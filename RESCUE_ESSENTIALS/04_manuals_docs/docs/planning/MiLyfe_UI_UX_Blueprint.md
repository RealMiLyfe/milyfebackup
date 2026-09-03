# MiLyfe — Complete UI/UX & Brand Blueprint

**Design specification · Mobile-first React product · August 18, 2026**  
**Status:** Design direction ready for wireframes and usability testing. No code is included.

---

## 1. Executive design decision

MiLyfe should not look like a crypto wallet, government portal, social network, emergency app, or developer dashboard. It should feel like a **calm neighborhood utility**: useful on an ordinary Tuesday, trustworthy during a crisis, and understandable to someone using it for the first time.

### Product promise

> **Your life, together — privately.**

### Supporting line

> Learn, share, connect, and have a voice in your place.

### The product in one sentence

One account and one profile connect a person to their pocket, learning, street, voice, and private life tools—online or offline—while people, not helpers, make consequential decisions.

### The five design principles

1. **Useful before impressive.** Bread, a class, a ride, a deadline, and a safe walk come before smart-city spectacle.
2. **Private by default, visible by choice.** “Together” never means “public.”
3. **Plain enough to read aloud.** Member UI avoids blockchain, governance, AI, node, wallet, token, DID, multisig, and other builder language.
4. **Calm in normal life; unmistakable in danger.** Most screens are warm and quiet. Crisis actions become high-contrast and direct.
5. **One home, not seventy products.** Five primary destinations and one helper. Modules are capabilities beneath them, not more icons.

---

# 2. Design from everyone’s position

The platform has many participants. They do not have equal time, safety, literacy, hardware, power, or trust. MiLyfe must not make the confident smartphone owner the default human.

## 2.1 Primary people

### A. Neighbor seeking everyday value

**Position:** Limited time; may not understand the platform; wants immediate proof it is useful.  
**Needs:** Nearby food, events, a class, messages, weekly share, simple privacy.  
**Fear:** “This is another app collecting my information.”  
**Design response:** A useful Home within 60 seconds; no forced story posting; visible privacy labels; local content before global content.

### B. Single parent or household coordinator

**Position:** Interrupted, often one-handed, scheduling across children and work.  
**Needs:** Food, childcare swaps, rides, class times, jars, reminders.  
**Fear:** Missing a deadline or exposing a child.  
**Design response:** Large touch targets, save-and-resume, household layer without shared passwords, child location never public, time-aware “Today” cards.

### C. Person in danger or living with an abusive partner

**Position:** Device may be monitored; every extra second and visible trace can create risk.  
**Needs:** Fast exit, hidden location, device removal, freeze shared jars, trusted contacts, real emergency help.  
**Fear:** Retaliation, discoverable history, accidental notification.  
**Design response:** Neutral entry to Safety, discreet mode, notification preview controls, rapid exit, no unsafe “Are you sure?” loops, device/session review, human escalation.

### D. Person without stable housing

**Position:** Shared or old device, weak connection, no fixed address, frequent battery loss.  
**Needs:** Profile without address, kiosk-safe sessions, offline directions, food/showers/mail/learning.  
**Fear:** Losing access after losing a device; being made visible as “homeless.”  
**Design response:** “Where do you spend most days?” instead of address; guest/kiosk privacy; short downloads; recovery friends or keeper; no public status label.

### E. Person returning from jail or under probation

**Position:** High paperwork burden, strict dates, possible low digital confidence and distrust.  
**Needs:** ID steps, food/clothes, deadlines, learning, job leads, a human.  
**Fear:** Missing a legal date because an app was unclear.  
**Design response:** Reentry path as a chronological checklist; date source shown; urgent reminders; “This is information, not your probation officer”; lawyer/public-defender links.

### F. Elder

**Position:** Possible low vision, hearing loss, motor difficulty, unfamiliar gestures.  
**Needs:** Check-ins they control, rides, appointments, trusted people, simple help.  
**Fear:** Tracking, mistakes, being locked out.  
**Design response:** Large mode; no gesture-only actions; read-aloud; trusted-contact shortcuts; explicit check-in schedule and audience.

### G. Disabled person

**Position:** Disability is not one mode. Needs may be visual, auditory, motor, cognitive, speech, or episodic.  
**Needs:** Equal completion of every task.  
**Fear:** “Accessible” shell around inaccessible critical flows.  
**Design response:** WCAG 2.2 AA minimum, AAA where practical for crisis and money; captions/transcripts; screen-reader order; switch/keyboard access; reduced motion; plain-language mode; never encode meaning in color alone.

### H. Person with limited literacy or learning the local language

**Position:** May understand speech or icons better than dense text.  
**Needs:** Short instructions, translation, audio, confirmation by meaning.  
**Fear:** Agreeing to something they did not understand.  
**Design response:** One idea per screen; examples; audio playback; translated legal summaries; comprehension confirmation for high-risk consent—not a trick quiz.

### I. Youth or child

**Position:** Less power than adults; cannot safely assess every risk.  
**Needs:** Learning, trusted grown-ups, play, help.  
**Fear:** Adult contact, public location, exploitation, money pressure.  
**Design response:** Child-safe experience is structural, not a toggle; no adult DMs by default; no public location; no live-money UX; guardian and emergency paths remain distinct; child cannot weaken protections.

## 2.2 Community participants

### J. Local shop owner

**Position:** Busy, thin margins, no patience for a complex back office.  
**Needs:** Hours, accessibility, surplus, accepted payment types, simple till, staff roles, complaints.  
**Fear:** Tax confusion, fraud, bad reviews without a response path.  
**Design response:** Shop mode is a layer on the owner’s profile; five-minute setup; dual-price clarity; accepted-share status has a date; local reputation belongs to the location; tax export clearly labeled.

### K. Teacher, tutor, or class host

**Needs:** Publish time/place, capacity, accessibility, offline lesson packs, attendance without surveillance.  
**Design response:** Lightweight class creation, no unnecessary student profile exposure, downloadable packs, learner-controlled badges.

### L. Caregiver, greeter, recovery friend, or street keeper

**Needs:** Understand the exact responsibility accepted; see requests without becoming an all-powerful moderator.  
**Design response:** Role cards describe “can / cannot / ends on”; expiring roles; conflict-of-interest prompts; no universal admin role.

### M. Mediator or peace-table facilitator

**Needs:** Consent from all parties, safe separation, human notes, victim-centered controls.  
**Design response:** Never recommend mediation in abuse; consent status shown per participant; helpers schedule and summarize but do not adjudicate.

### N. Local shop staff

**Needs:** A revocable work badge without sharing the owner’s account.  
**Design response:** Staff use their own profile; task-scoped access; owner sees active devices; staff sees what the shop can view.

### O. Place treasurer or proposal steward

**Needs:** Explain spending, collect approvals, publish outcomes.  
**Design response:** “3 of 5 people must agree” instead of multisig; approval timeline; conflict disclosure; helper cannot be an approver.

## 2.3 System and oversight participants

### P. Helper user

**Position:** May over-trust conversational output.  
**Needs:** Fast assistance with visible limitations and sources.  
**Design response:** Every helper response is labeled; consequential suggestions include source, date, confidence, and “Ask a person”; helper cannot impersonate a person.

### Q. Builder or maintainer

**Needs:** A clear design system, testable states, accessibility rules, issue paths, open-source constraints.  
**Design response:** Separate builder surface. No infrastructure language leaks into member UI.

### R. Auditor, privacy reviewer, child-safety reviewer, or legal reviewer

**Needs:** Trace decisions without reading private content.  
**Design response:** Permissioned audit trails, policy version, reason for access, retention schedule, redacted exports.

### S. Local government, clinic, school, or nonprofit partner

**Needs:** Truthful claims and clear boundaries.  
**Design response:** Partner badge says exactly what is verified. MiLyfe never visually imitates a state ID, court order, bank, medical diagnosis, or emergency dispatch service.

---

# 3. Brand system

## 3.1 What the current logo communicates

The supplied logo moves from **deep navy through civic blue to living green**. It reads as technology becoming human life. That is the strongest brand idea and should be preserved.

The current mark is a wordmark rather than an app icon. It needs a companion symbol for small spaces.

## 3.2 Brand character

| Trait | Expression | Avoid |
|---|---|---|
| Human | Neighborly copy, real local context | Corporate mission jargon |
| Grounded | Streets, hands, learning, food, repair | Space-age spectacle as the main brand |
| Trustworthy | Clear boundaries, dates, sources, privacy labels | “Unstoppable,” “guaranteed,” “official” |
| Capable | Strong hierarchy and precise states | Cute visuals during serious tasks |
| Hopeful | Fresh green, open space, progress | Neon crypto gradients |
| Independent | Open-source and portable | Anti-government or rebellious visual clichés |

## 3.3 Logo family recommendation

1. **Primary wordmark:** Supplied MiLyfe logo, used on welcome, website masthead, and formal documents.
2. **Compact horizontal mark:** Wordmark without surrounding whitespace for nav bars.
3. **App icon:** Rounded-square field with a custom **Mi bridge** symbol: an “M” whose center path becomes a small leaf or open doorway. Do not shrink the full wordmark into an icon.
4. **One-color mark:** Solid navy on light backgrounds; white on dark backgrounds.
5. **Safety restriction:** Do not place the gradient wordmark on noisy photos or use green alone to imply a completed financial or safety action.

**Clear space:** At least the height of the lowercase “i” around the wordmark.  
**Minimum size:** Full wordmark 112 px digital / 30 mm print. Below that, use the symbol.

## 3.4 Color palette

Colors are derived from the visual character of the supplied logo, then expanded for accessibility.

### Core brand

| Name | Hex | Role |
|---|---:|---|
| Deep Harbor | `#071E40` | Primary text, dark surfaces, trust |
| Civic Blue | `#0B668C` | Links, information, active navigation |
| Living Teal | `#087F73` | Community and connection accents |
| Life Green | `#078B5B` | Positive progress and brand endpoint |
| Mist | `#EEF6F5` | Soft selected surfaces |
| Paper | `#FBFCFC` | Main background |

### Semantic system

| Meaning | Color | Rule |
|---|---|---|
| Action | `#075E82` | Primary button; white text must pass contrast |
| Success | `#087448` | Use with icon + text, never color only |
| Warning | `#9A5B00` | Amber surface, direct next action |
| Danger | `#B4232D` | Crisis/destructive actions only |
| Stage | `#6D4BB3` | Marks capability-gated features (exchange not yet voted open) |
| Offline | `#4E5968` | Neutral, not alarming |
| Focus | `#135FD1` | High-visibility keyboard focus ring |

### Color usage ratio

- 70% neutral Paper / white
- 20% navy and pale teal structure
- 8% civic blue / living green actions
- 2% warning, danger, or stage-gated states

The interface should not be covered in a blue-green gradient. Reserve the gradient for the logo, welcome moment, and occasional progress illustration.

## 3.5 Typography

### Recommended family

- **Primary:** Atkinson Hyperlegible Next or Atkinson Hyperlegible—open, highly legible, warm, and suitable for low vision.
- **Language fallbacks:** Noto Sans family for broad script coverage.
- **Numbers:** Tabular numerals for balances, dates, and approvals.

### Type scale

| Style | Mobile | Use |
|---|---:|---|
| Display | 32/38, bold | Welcome only |
| H1 | 28/34, bold | Page title |
| H2 | 22/28, semibold | Major section |
| H3 | 18/24, semibold | Card/section title |
| Body | 16/24, regular | Default copy |
| Body large | 18/28 | Large/read-aloud mode |
| Label | 14/20, semibold | Controls |
| Support | 13/18 | Metadata; never critical alone |

Never use text smaller than 13 px. Critical consent and crisis instructions remain at least 16 px.

## 3.6 Iconography and imagery

- Rounded 2 px stroke icons, filled only for the current primary tab.
- Every icon has a text label in primary navigation.
- Avoid police shields, gavels, banks, coins, flags, and surveillance-camera imagery as general metaphors.
- Use illustrations of **actions**, not idealized demographics: fixing, learning, carrying food, welcoming, translating, planting.
- Photography must be opt-in, documentary rather than pity-based, and never reveal a vulnerable person’s location.
- Never use a robot head for Mi. Use a small **glowing doorway/spark** mark to communicate assistance without personhood.

## 3.7 Voice and tone

### Voice

Clear, respectful, local, nonjudgmental, and honest about limits.

### Copy rules

- Prefer “you” and a concrete verb.
- One instruction per sentence.
- Explain consequence before confirmation.
- Never shame inactivity, low standing, low balance, missed lessons, or relapse.
- Never use false urgency.
- Say who can see a thing at the point of sharing.
- Distinguish **saved**, **sent**, **still walking**, and **arrived**.

### Examples

| Do | Do not |
|---|---|
| “Your share arrived.” | “UBI emission finalized.” |
| “This thanks is still walking. It will send when a path returns.” | “Transaction pending in mempool.” |
| “Three of five people still need to agree.” | “Multisig threshold unmet.” |
| “Only you can see this.” | “Private by default.” without proof |
| “Rue is a helper, not a lawyer or the police.” | “AI legal assistant” |
| “Leave with a copy of your information.” | “Export sovereign data package.” |

---

# 4. Information architecture

## 4.1 The fixed primary navigation

### Mobile

Bottom navigation with five destinations:

1. **Pocket** — share, thanks, asks, jars, activity
2. **Learn** — path, classes, downloads, badges
3. **Street** — nearby help, food, shops, events, Pulse, Story
4. **Voice** — ideas, talk, try it first, decide, outcomes
5. **You** — profile, household, safety, messages, privacy, devices, exit

**Mi** is a floating but non-obstructive action above the bottom navigation. It can be hidden permanently.

### Desktop/tablet

- Left rail: five destinations + Mi.
- Top bar: place selector, global search, inbox, connection status, profile.
- Main content: maximum 760 px reading width, with optional contextual side panel.

## 4.2 Why Home is not a sixth tab

Opening the product lands on a **Today overview**, not one of the five destinations. The bottom tabs remain visible. Today composes the most important items from all five areas without creating another content silo.

## 4.3 Global objects

- **Today** — personal priority summary
- **Inbox** — messages, requests, approvals, reminders, alerts
- **Search** — searches the member’s own life first, then their place, then the commons
- **Connection status** — Online / Neighbor net / Sending later / Offline
- **Place** — manually chosen; location is never silently public
- **Privacy audience** — Only me / Chosen people / Household / Neighbors / Place / Public

## 4.4 Content map

### Pocket

Overview · Send thanks · Ask · Activity · Shared jars · Weekly credits details · Shop till, when applicable · Stage/exchange info · Tax/export · Freeze

### Learn

My path · Continue · Downloaded · Local classes · Ask for a class · Teach · Badges · Accessibility and language · Reentry path · Child learning

### Street

For you today · Map/list · Food and essentials · Help and rides · Shops · Classes/events · Pulse · Street pot · Story · Safety check-in · Report incorrect information

### Voice

Needs now · Ideas · Talk · Try it first · Decide · Results · Place compact · My delegated voice · Helper circle, optional and hidden by default

### You

Profile · Household · Messages · Safety and defense · Trusted/recovery people · Devices and sessions · Privacy center · Story participation · Roles · Shop layer · Settings · Export and leave

---

# 5. Core interaction model

## 5.1 The priority stack

Every Today screen uses this order:

1. **Immediate safety** — only when relevant
2. **Time-sensitive today** — court/class/check-in/deadline
3. **Money movement requiring the user**
4. **People waiting on the user**
5. **Continue learning/work**
6. **Nearby opportunities**
7. **Community news/story**

The product does not rank posts by outrage or engagement.

## 5.2 Card anatomy

Each card has:

- Domain label and icon
- Plain title
- One-sentence meaning
- Time/distance/source where relevant
- Privacy audience where relevant
- One primary action
- Optional quiet secondary action

No card should contain more than two actions. Additional actions live in the detail page.

## 5.3 Status language

| System state | Member language |
|---|---|
| Draft | Not shared |
| Local-only save | Saved on this device |
| Queued offline | Still walking |
| Submitted | Sent |
| Confirmed | Arrived / Agreed |
| Rejected | Did not go through — reason |
| Expired | Ended on [date] |
| Stage-gated | Feature pending community vote to activate |
| Helper-created | Drafted by Mi; a person must decide |

## 5.4 Confirmation levels

- **Level 0:** No confirmation for reversible navigation/preferences.
- **Level 1:** Inline undo for low-risk actions.
- **Level 2:** Review sheet for money, audience changes, device removal, and approvals.
- **Level 3:** Re-authentication + explicit consequence for leaving, panic freeze, recovery, story publication, child data, or high-value movement.
- **Crisis exception:** Safety escape actions prioritize speed and do not trap the user in long confirmation sequences.

---

# 6. Detailed screen designs

## 6.1 Welcome

**Goal:** Explain value and boundaries before asking for personal information.

**Composition:**

- MiLyfe wordmark
- “Your life, together—privately.”
- Three short benefits: “Learn and find help,” “Share with people nearby,” “Keep control of your information”
- Primary: **Get started**
- Secondary: **Look around first**
- Text links: Accessibility · Language · How privacy works
- Connection badge: “Works offline after setup”

Do not lead with the oath, blockchain, tokens, mesh, or 600 open-source projects.

## 6.2 Look-around visitor mode

Visitors can view public learning, public Street resources, emergency information, and a plain explanation of MiLyfe without creating a profile. Actions that require identity explain why.

## 6.3 Signup — seven short steps

A persistent step label says “Step 2 of 7”; progress is also announced to screen readers.

1. **Language and access**  
   Choose language, text size, read-aloud, captions, reduced motion.
2. **Your name and face**  
   Display name required; photo optional; avatar available; pronunciation optional.
3. **Your home place**  
   “Where do you spend most days?” Search or choose manually. Explain that the place is changeable and exact location is not public.
4. **Your device**  
   Is this device private, shared, or also used by a child? Shared-device advice appears immediately.
5. **Recovery**  
   Choose recovery friends, a keeper-with-delay route, or advanced paper words. Explain responsibility before inviting anyone.
6. **Privacy starting point**  
   Recommended “Quiet start”: profile visible to chosen people, story off, location off, contact discovery off.
7. **Truth and control**  
   Three check statements: “MiLyfe is not the government,” “People make important decisions,” “I can take my information and leave.” Primary: **Enter MiLyfe**.

**After signup:** A simple success moment, then Today. Do not force a tutorial carousel.

## 6.4 First-run Today

**Header:** “Good morning, Jordan” + connection state.  
**Hero:** “What would make today easier?” with six intent chips:

- Find food
- Learn something
- Check my share
- Ask for help
- See my street
- Handle a paper or deadline

Below: “Start here” card for profile recovery completion and a local resource card. Mi offers help only after the first screen appears.

## 6.5 Returning Today

Example hierarchy:

1. **Due today** — “Your class starts at 4:00 PM · 0.6 mi · ramp entrance”
2. **Pocket** — “Your weekly credits arrived: 100 $MLY”
3. **People** — “Mara thanked you for watching the kids”
4. **Continue** — “Repair path · Week 3 · saved offline”
5. **Street** — “Harbor Bakery has 8 bread bags until 6 PM”
6. **Voice** — “Shade proposal closes Friday”

A “Choose what appears here” control gives the member direct ranking control.

## 6.6 Pocket overview

**Top:** Balance plus a prominent stage badge:

- **$MLY Credits** — real, peer-swappable, community-issued
- **Exchange gate status** — shows whether external convert is voted open yet (with tax/legal info link)

**Primary actions:** Thank · Ask · Add to jar  
**Breakdown:** This week · Thanks · In jars  
**Activity:** Sentence-based timeline  
**Safety:** Freeze pocket is visible but not visually alarming

The balance is not styled like an investment chart. No gain/loss graph, market price, confetti, streak, APY, or “portfolio.”

## 6.7 Thank someone

1. Choose a known person or scan their consented code.
2. Enter amount.
3. Optional plain memo: “for watching the kids.”
4. Review: person, amount, stage, memo, connection state.
5. Confirm.
6. Result is **Arrived** or **Still walking**.

If offline, explain that the person may not receive it yet and show how double-spend protection may affect later settlement. Never pretend it is complete.

## 6.8 Ask

Choose a person, household, jar, or visible local request board. Amount may be omitted for an in-kind ask. The recipient sees **Accept**, **Offer something else**, or **Not now**. No guilt language.

## 6.9 Shared jar

**Header:** Purpose, amount, people, privacy.  
**Approval statement:** “3 of 5 people must agree.”  
**Timeline:** Proposed → approvals → movement → receipt/outcome.  
**Conflict control:** Approver can disclose a relationship or abstain.  
**Helper boundary:** “Mi can explain this jar but cannot approve or move it.”

## 6.10 Learn home

**Top:** Current stage in a visible journey:

Welcome → Find your feet → A craft → A role → Teach

**Sections:** Continue · Saved offline · Near you · Asked for by your street · Your badges  
**Filters:** Time available, language, access, online/offline, child-safe, free—though all core learning is free.

Do not gamify learning with public leaderboards. Streaks are private and optional. Completion language celebrates persistence without punishing pauses.

## 6.11 Lesson player

- Clear lesson title and estimated time
- Download status
- Text, audio, transcript, images with descriptions
- “Make text easier” and language controls
- Save position automatically on device
- “I need a person” for tutor/help
- Short knowledge check only when useful
- Exit without losing progress

## 6.12 Class detail

Shows host, time, place, access, language, childcare availability, capacity, materials, safety/contact rules, and whether attendance is visible to others. Primary: **Save my place**. Secondary: **Ask a question** and **Save offline**.

## 6.13 Street home

Two equal views: **List** as default and **Map** as optional. List is safer, more accessible, and lighter offline.

**Top controls:** Place · Today/This week · distance area chosen manually  
**Sections:** Essentials · Help nearby · Shops · Classes · Street pot · Pulse · Story

No infinite social feed. Items expire and show freshness: “Updated 2 hours ago.”

## 6.14 Street map

- Exact private people locations never appear.
- Resources can show verified addresses.
- Personal asks use a broad area until two people agree to share details.
- Children never appear as independent pins.
- Map explains cached/offline freshness.
- A list equivalent exists for every pin.

## 6.15 Shop page

**Header:** Name, distance, open state, freshness.  
**Trust facts:** entrance access, languages, accepted payment types today, staff, complaint response state.  
**Sections:** Available now · Surplus · Jobs · Community day · About this doorway  
**Actions:** Directions · Ask shop · Save · Report incorrect info

If shares are accepted, copy says “Taking shares today—updated at 9:10 AM,” not merely a permanent token badge.

## 6.16 Pulse

Pulse is **weather, not a wanted board**.

Visual: four calm conditions—Connection, Essentials, Check-ins, Peace—shown as words and simple shapes. Example: “Some radios are dark. Messages may take longer.” Never list suspected people, gang rosters, precise vulnerable locations, or predictive-crime scores.

## 6.17 Story

Three clear sources:

- Street book
- People pages, opt-in
- Commons chronicle, aggregated

Every story displays source events and audience. “Add me to this story” and “Take me out” are equally easy. Child faces and abuse-survivor profiles never auto-appear.

## 6.18 Voice home

Pipeline is visible:

**Idea → Talk → Try it first → Decide → What happened**

Top card: “What needs attention now?” based on public, aggregated needs—not private profiles. Each proposal shows:

- Plain title
- Area and people affected
- Who started it; “Drafted with Mi” if applicable
- Cost and pot
- Risks / who could be hurt
- Languages available
- Closing date and sunset date
- Current stage

No popularity-first ranking. Default sorting is local relevance, urgency, and closing date.

## 6.19 Proposal detail

Tabs or anchored sections:

1. In one minute
2. Full idea
3. Who this may help or hurt
4. Cost and approvals
5. Discussion
6. Simulation result
7. Sources and changes

The primary action changes by stage: **Join the talk**, **Try the example**, **Decide privately**, or **See what happened**.

## 6.20 Private ballot

- Restates the exact decision
- Shows options in equal visual weight
- Says “Your choice is secret” only if the mechanism truly supports it
- Allows review before submission
- Provides a private receipt that proves participation without exposing choice where technically possible
- No live horse-race totals before close on sensitive decisions

## 6.21 You

**Header:** Avatar, name, home place, current visibility.  
**Tiles:** Profile · Household · Messages · Safety · Trusted people · Devices · Privacy · Roles · Your story · Settings  
**Footer:** Download your information · Leave MiLyfe

Sensitive items are not buried, but destructive exit is visually separated from daily settings.

## 6.22 Privacy center

A human-readable dashboard:

- **Who can find me**
- **What my street can see**
- **Location and nearby**
- **My story**
- **Helpers and memory**
- **Children and household**
- **Connected devices**
- **Data kept on this device / place / commons**

A “Privacy checkup” walks through actual settings. It does not merely display a long privacy policy.

## 6.23 Devices and sessions

Each device shows friendly name, last active time, approximate place if consented, and access level. Actions: Rename · Make shared-safe · Remove · Report stolen. Removing a device states what becomes unavailable offline.

## 6.24 Safety and defense

Top message:

> If someone may be hurt now, call 911 or your local emergency number.

Primary choices:

- Leave a place safely
- I’m walking home
- Check in with someone
- Freeze shared access
- Understand a paper or deadline
- Record what happened
- Find a lawyer or human helper

Rue is introduced once: “Rue is a helper, not a lawyer or the police.”

## 6.25 Leave-now flow

**Design requirement:** Must be tested with domestic-violence experts before release.

1. Immediate danger? Call emergency / continue quietly.
2. Choose what to secure: location, notifications, shared jars, devices, trusted contact.
3. Create a safe contact method.
4. Save essential files or create an export.
5. Show local shelter/hotline resources with source date.
6. Clear or disguise local traces only with an honest explanation of limits; never promise invisibility from device owners, carriers, or authorities.

A persistent **Quick exit** moves to a neutral page and suppresses the current view. It must not falsely claim to erase browser or network history.

## 6.26 Court paper / deadline flow

- Take a photo or type what the paper says.
- Rue identifies likely document type with confidence and source.
- Show deadline prominently with “Check this date with a human.”
- Actions: Add calendar · Find legal aid · Prepare questions · Export for lawyer
- Never say “you will win,” “ignore this,” or visually turn a generated packet into an official court order.

## 6.27 Mi helper panel

Mi opens as a half-height sheet on mobile and side panel on desktop, preserving context.

**Header:** Mi symbol · “Mi, a helper” · mute/close  
**Starter actions:** Explain this page · Find something nearby · Help me write · Translate · I need a person

Every consequential answer can expose:

- What Mi used
- Date/source
- What Mi cannot do
- Who can help next
- Clear memory control: “Don’t keep this”

Mi never sends, spends, publishes, votes, changes child settings, or turns on a camera without a human action. Drafts are visibly marked **Not sent**.

## 6.28 Inbox

Tabs: **Needs you**, **Messages**, **Updates**.  
Needs you contains approvals, deadlines, recovery requests, and safety check-ins. Updates contains non-urgent system and story notices. Marketing does not exist as a notification category.

## 6.29 Search

Search order:

1. Your information
2. Your chosen people and household
3. Your place
4. Public commons

Sensitive categories require an explicit scope. Search never becomes a people-finder for children, abuse survivors, or precise location.

## 6.30 Shop mode

Shop mode is reached from You, not a sixth global tab.

**Today:** Open state · accepted payment methods · orders/thanks · surplus · staff · unanswered complaint  
**Quick actions:** Update hours · Post surplus · Take payment · Add job · Community day  
**Books:** Plain totals and year export  
**Permissions:** Owner, manager, till-only, surplus-only

## 6.31 Youth mode

Navigation becomes **Learn · Nearby · Ask a grown-up · Me**. Pocket and binding Voice are absent. Nearby excludes unsafe adult contact and precise child visibility. Emergency help remains available even if guardian controls are misconfigured.

## 6.32 Keeper/admin workspace

This is a separate role-scoped workspace, never a secret “god mode.”

- Tasks needing a person
- Expiring roles
- Place health without private content
- Content/resource freshness
- Pot approvals
- Safety escalations with strict need-to-know
- Audit access log
- Policy and legal pack version

Every action shows scope, reason, duration, appeal path, and whether another person must agree.

---

# 7. Offline, low-data, and failure design

## 7.1 Persistent connection chip

- **Online** — normal
- **Neighbor net** — local path available
- **Sending later** — queued actions
- **Offline** — device-only content

Tapping the chip opens a plain explanation and a list of queued items.

## 7.2 Offline behavior by tab

| Area | Still works | Limitation shown |
|---|---|---|
| Pocket | View last confirmed balance; draft thanks | May remain “still walking”; no false confirmation |
| Learn | Downloaded lessons and progress | Sync date shown |
| Street | Cached resources and map | Freshness and expired items shown |
| Voice | Read saved proposals; draft response | Ballot may require a safe connection before deadline |
| You | Local profile, safety pack, trusted contacts | Device-removal requests may wait |
| Mi | Small on-device help where available | “Limited offline” label; no invented current resources |

## 7.3 Error pattern

Every error answers:

1. What happened?
2. What is safe right now?
3. What can I do next?
4. Did anything send or move?
5. Who can help?

Example:

> **Your thanks did not leave this phone.** Nothing moved. Try again when a path returns, or keep it saved for later.

## 7.4 Empty states

Empty states teach without blame:

- “No classes are listed nearby yet. Ask for one or browse saved lessons.”
- “No one is waiting on you.”
- “Your story is off. Nothing about you is published.”
- “This place has no fresh food posts today. Last checked at 10:20 AM.”

---

# 8. Accessibility specification

Accessibility is a release gate, not a later audit.

## 8.1 Minimum requirements

- WCAG 2.2 AA across web and mobile equivalents
- 4.5:1 body text contrast; 3:1 large text and essential graphics
- 44×44 CSS px minimum targets; 48×48 preferred on touch
- Full keyboard and switch navigation
- Visible focus not obscured by sticky headers or sheets
- Screen-reader names, roles, states, errors, and progress
- Logical heading structure
- No gesture-only completion
- Captions and transcripts for all instructional media
- Text resize to 200% without loss; reflow at 320 CSS px
- Reduced-motion mode; no essential parallax
- Timeouts can be extended, except narrowly justified security events
- Authentication does not depend on memory puzzles alone
- Error prevention for money, data publication, and legal deadlines

## 8.2 Built-in access modes

- Large and extra-large text
- High contrast
- Reduced motion
- Plain language
- Read aloud
- Captions always on
- One-handed layout
- Low-data mode
- Color-vision-safe charts

These settings appear during onboarding and remain in the profile. They are not hidden under “advanced.”

## 8.3 Cognitive accessibility

- Stable navigation placement
- One primary action per screen or card
- Step-by-step tasks with save-and-resume
- Concrete date formats: “Friday, August 21 at 4:00 PM”
- Avoid double negatives
- Explain uncommon terms immediately
- Show examples before high-risk choices
- Never use countdown pressure for non-emergencies

---

# 9. Privacy, safety, and trust UX

## 9.1 Audience labels

Every publishable object shows an audience chip before submission:

**Only me · Chosen people · Household · Neighbors · Place · Public**

Audience changes require a review when moving to a broader group. “Public” explains that copies may persist outside MiLyfe.

## 9.2 Location levels

- Off
- Place only
- Broad nearby area
- Exact location for a chosen person and limited time
- Emergency share to selected contacts

There is no universal “always share precise location” default.

## 9.3 Helper trust

- Helper label remains visible.
- Human messages and helper messages have different shapes and labels.
- Sources and dates are available.
- Memory is visible and erasable.
- “Humans only” is available per member and place.
- High-impact action always returns to a human-controlled UI.

## 9.4 Standing

Standing appears as contextual words—Neighbor, Carer, Maker, Teacher, Keeper—not a global score. It never controls rights, emergency access, messages, profile ownership, weekly share, or a compact-rights vote. Harm records require process, date, response, and appeal.

## 9.5 Consent receipts

For child data, story publication, helper memory, location, research, and special-category information, the member can view:

- What they agreed to
- Who receives it
- Why
- Date and policy version
- How to stop
- What cannot be pulled back from external recipients

---

# 10. Responsive behavior

## Mobile, 320–599 px

- Bottom navigation
- One-column content
- Full-screen complex flows
- Bottom sheets for quick choices
- Sticky action only when it does not hide content

## Tablet, 600–1023 px

- Left compact rail in landscape, bottom navigation in portrait
- Two-column cards where reading order remains clear
- Mi side sheet

## Desktop, 1024 px+

- 240 px left rail
- 760 px primary reading column
- Optional 320 px contextual panel
- No stretched full-width paragraphs
- Keyboard shortcuts are discoverable and never required

## Kiosk/shared device

- Prominent session timer
- No saved notification previews
- Exit clears local session where technically possible
- Print/save-to-private-device options
- Recovery and safety paths remain available

---

# 11. Notification strategy

## Default-on only

- Safety check-ins the member requested
- Money movement and recovery events
- Deadlines the member saved
- Direct messages from approved people
- Device/security changes

## Default-off or digest

- Street Story
- New classes
- Proposal discussions
- Shop updates
- Helper suggestions

No engagement streak notifications. No “people are waiting for you” manipulation unless a real person is waiting and that fact is shown.

Notification previews are configurable by sensitivity. Safety and legal notifications default to neutral text on lock screens.

---

# 12. Design system inventory

The first component library should include these design patterns before page-by-page production:

### Foundations

Color · Type · Spacing · Elevation · Shape · Motion · Icon rules · Content width · Focus · Haptics · Sound

### Core controls

Button · Icon button · Link · Input · Text area · Search · Select · Radio · Checkbox · Switch · Slider · Date/time · File/photo capture · Language picker

### Navigation

Bottom tabs · Left rail · Top bar · Breadcrumbs · Stepper · Tabs · Back behavior · Place selector

### Content

Card · List row · Detail header · Empty state · Skeleton · Badge · Audience chip · Source box · Timeline · Receipt · Data table · Map/list switch

### Feedback

Banner · Inline error · Toast with undo · Review sheet · Confirmation · Offline queue · Progress · Success · Warning · Danger · Stage-gated state

### MiLyfe-specific patterns

- Connection chip
- Still-walking receipt
- Weekly-share card
- Jar approval card
- Proposal stage rail
- Private ballot
- Pulse condition
- Privacy audience picker
- Helper disclosure and source panel
- Human escalation card
- Role scope and expiry card
- Child-safe contact card
- Crisis quick-exit pattern

Every component requires normal, hover, focus, active, disabled, loading, error, offline, high-contrast, large-text, and right-to-left states where relevant.

---

# 13. Identity, recovery, households, and place transitions

These flows complete the identity experience. They must be prototyped and tested before live money or public governance.

## 13.1 Personhood journey

Personhood protects one weekly share per human. It must never resemble immigration screening, credit scoring, or a criminal-background check.

**Entry points:** Pocket setup, Voice eligibility, You → Personhood, or a contextual card on Today.

**Methods shown in recommended order:**

1. Introductions from three eligible members
2. In-person hello-day at a participating place
3. Optional government ID check
4. Approved privacy-preserving proof when available

**Status screen:** Not started · Waiting for people · Appointment booked · Under review · Complete · Needs attention · Appealed.

For every method, show what is collected, who sees it, expected time, what it enables, and an alternative route. A failed or delayed check does not remove learning, emergency information, messaging, profile ownership, or export.

**Required exception flows:** duplicate profile, two people sharing one profile, fraudulent introduction, reviewer conflict, inaccessible hello-day, no local greeters, moved during review, youth reaching local money age, temporary pause, restored eligibility, and appeal.

A decision notice must include the reason in plain language, evidence the member may view, what remains available, correction route, appeal route, and response target. Do not show a permanent fraud label.

## 13.2 Recovery-center experience

**Setup:** Invite recovery people individually. Each invitation explains what the person can and cannot do. The profile owner sees Accepted, Waiting, Declined, or Replace.

**Recovery request timeline:**

Request made → recovery people notified → delay in progress → approvals received → final review → old device removed → recovery complete.

The owner can cancel from any still-authorized device. All active devices receive a neutral security notice. Recovery people never receive private messages, balances, child data, or location merely because they hold this role.

**Required paths:**

- Two friends available
- Only one available
- No friends: keeper plus longer delay
- Paper-word recovery
- Friend declines or has left MiLyfe
- Suspected fraudulent request
- Stolen device and urgent pocket freeze
- Abusive recovery person
- Owner is incapacitated
- Death and named steward
- Recovery started offline

Replacing a recovery person has a delay and alerts the other recovery people. An emergency safety path can freeze access quickly but cannot silently transfer ownership.

## 13.3 Authentication and session UX

Offer device passcode, security key where supported, and optional biometrics. Biometrics are convenience, never the only route.

Design states for first login, returning login, shared device, kiosk, failed attempts, unavailable biometric hardware, forgotten local passcode, sensitive-action reauthentication, suspicious device, session expiry, compromised operating system, and panic freeze.

A shared-device session shows a persistent shared-device badge, neutral lock-screen notifications, no saved search history by default, and a clear **Finish and clear this session** action.

## 13.4 Household lifecycle

A household is a consented coordination layer—not an account owned by a “head.” Every person keeps their profile, privacy controls, messages, pocket, export, and ability to leave.

**Household screens:** Members · Children/dependents · Shared jar · Calendar · Devices · Invitations · Privacy boundaries · Roles · Leave or separate.

Design flows for invitation and consent, child guardian links, temporary caregiver, adult dependent, shared device, separate finances, foster/temporary care, guardian replacement, separation, abuse split, incapacity, death, and a household member who moves.

Each shared item names its audience. Joining a household must not automatically reveal private history, exact location, health information, legal papers, or prior messages.

## 13.5 Moving and belonging to places

The place flow distinguishes **Visit**, **Spend time in both**, and **Move home place**.

Before confirmation, show effects on nearby resources, Voice eligibility, local standing, classes, shops, legal information, money features, pending actions, and household members. Craft and care badges can travel by choice; “known on this street” remains local and cools over time.

Members can finish pending actions in an old place where policy permits. Changed laws or unavailable features appear before the move—not after an action fails.

---

# 14. Communication, search, reporting, and moderation

## 14.1 Messaging model

Supported spaces: direct messages, household rooms, class rooms, proposal discussions, trusted circles, and low-bandwidth voice messages.

Every message surface defines who can initiate contact, who can invite, retention, forwarding expectations, report/block behavior, offline delivery, and child rules.

**Message states:** Saved on device · Still walking · Sent · Delivered · Read, if both people allow receipts · Failed. Editing creates a visible edit marker. Deletion states whether the message disappeared only for the sender, for the MiLyfe room, or may remain in another person’s copy.

Unknown contact requests show minimal information and offer Accept · Block · Report. Unknown adults cannot directly contact youth by default. Emergency priority cannot be purchased or used to bypass blocking.

## 14.2 Search specification

Search has visible scopes: **Mine · My people · My place · Public commons**. Sensitive scopes require deliberate selection.

Support misspellings, plain-language synonyms, multilingual terms, local names, voice input, offline results, and list-first presentation. Explain why a result appears and when it was last updated.

Search history is private, erasable, and off by default on shared devices. Children, abuse survivors, exact personal locations, hidden profiles, and private legal or health information never become public people-search results.

No-results pages offer spelling help, translation, broader area, offline resources, or **Ask a person**—not an invented answer.

## 14.3 Report and block flow

Report categories:

- Immediate threat or emergency
- Harassment, stalking, or unwanted contact
- Scam, impersonation, or suspicious money activity
- Child-safety concern
- Hate or targeted abuse
- Illegal public content
- False or dangerous resource information
- Shop or class concern
- Privacy or location exposure
- Other

The first screen separates immediate danger from platform reporting. Blocking is available without requiring a report. A blocked person cannot use a new group or helper to bypass the block.

The reporter sees what information will be attached, who can review it, whether the reported person will be told, expected response time, emergency limitations, and how to add or withdraw information.

## 14.4 Moderation decision and appeal

A decision notice includes the rule, specific content or behavior, evidence available to the member, action taken, scope, duration, what remains available, and appeal deadline.

Possible actions are narrow and proportional: content label, correction request, contact restriction, room removal, place restriction, temporary role suspension, money review, or urgent safety escalation. A place restriction does not erase the global profile or block export.

Appeals go to people who did not make the original decision. The member can add context, request accessibility or language support, identify a conflict of interest, and track the appeal. False reports do not automatically become public scars.

## 14.5 Public-content operations

Public resources, classes, shops, legal links, and emergency contacts display:

- Source or responsible person
- Last checked date
- Applicable place
- Availability and access notes
- **Report incorrect information**

High-risk resources such as shelters, legal aid, hotlines, clinics, and emergency centers require a defined verification owner and expiry. Expired information is hidden from confident recommendations but may remain visible as **Not recently verified** with a safer alternative.

---

# 15. Money disputes, shops, and transparent community decisions

## 15.1 Pocket dispute center

Activity details include **Get help with this**. The dispute flow first establishes what happened:

- Wrong person
- Duplicate movement
- Unknown activity
- Item or service problem
- Refund expected
- Offline movement conflict
- Jar disagreement
- Account or device compromise
- Tax-record correction

Before promising an outcome, state whether the movement is saved, still walking, settled, refundable by the recipient, disputable under shop rules, or technically irreversible.

**Dispute timeline:** Reported → access secured if needed → other party invited to respond → evidence reviewed → proposed resolution → agreement or human appeal → closed.

A helper may organize facts but cannot decide fraud, reverse value, freeze another human permanently, or write a standing scar.

## 15.2 Offline-conflict UX

When conflicting offline actions reconnect, do not silently choose a winner. Show each affected movement, confirmed balance, reason, temporary restrictions if any, and options to resolve. Essential rights and emergency access remain available.

Use the sentence: “Two saved actions used the same available shares. Nothing else will move until this is reviewed.” Avoid accusations before human review.

## 15.3 Refund and correction patterns

A shop refund links to the original receipt and states whether it is full, partial, pending, or declined. Corrected receipts preserve the original in a visible history. Wrong-recipient requests ask the recipient to return value; the UI must not claim an irreversible movement was canceled.

## 15.4 Shop lifecycle

Additional shop flows:

- Verify or claim a location
- Transfer ownership with dual confirmation and delay
- Add and remove staff
- Start/end shift
- Update accepted payment types for today
- Take payment and issue receipt
- Refund or correct sale
- Resolve complaint
- Manage surplus freshness
- Create a job or community day
- Operate temporarily offline
- Close temporarily or permanently
- Resolve remaining jars, receipts, complaints, and exports on closure
- Manage multiple locations without merging local standing

Staff permissions are task-scoped: owner, manager, till-only, surplus-only, schedule-only, or books/export. Staff never share owner credentials.

## 15.5 Proposal integrity

Voice adds flows for duplicate/spam proposals, co-authors, amendments, withdrawal, conflicting evidence, translation disagreement, conflict of interest, discussion harassment, low participation, tie, recount, challenge, emergency decision, sunset, renewal, and outcome review.

Every proposal has a version history. If the meaning changes after discussion or voting begins, the interface clearly resets the affected stage and tells participants.

## 15.6 Delegated voice

Delegation is optional, topic-specific by default, time-limited, visible to the delegator, and instantly revocable before the relevant deadline. The member sees scope, expiry, whether the delegate acted, and how much delegated responsibility that person currently holds.

The UI never pressures delegation, reveals a private ballot choice, or allows a delegate to re-delegate without explicit permission. Hidden concentration warnings are surfaced to auditors and the community in privacy-preserving aggregate form.

## 15.7 Public pots and charts

Use accessible charts plus complete table and text alternatives for pot inflow, approved spending, remaining balance, proposal cost, weekly-share history, participation, Pulse trends, and governance simulations.

Charts show uncertainty, missing data, date range, and source. Do not visualize neighborhood risk as a crime heat map or compare people on a financial leaderboard.

---

# 16. Roles, consent, support, export, and service operations

## 16.1 Permission matrix requirement

A maintained design artifact must cover Member, Youth, Guardian, Household member, Shop owner, Shop staff, Teacher, Recovery friend, Greeter, Keeper, Treasurer, Mediator, Auditor, Partner, and Helper.

For every object and action, define:

- Can view
- Can create or change
- Can invite or delegate
- Needs second-person approval
- Duration and expiry
- Notification to affected people
- Audit visibility
- Revocation
- Appeal

No role receives universal access. Sensitive access is purpose-bound, time-limited, logged, and visible to the affected member where safety permits.

## 16.2 Role card pattern

Every role invitation and active-role screen displays:

**Why this role exists · What you can do · What you cannot do · What you may see · Who reviews you · Ends on · Leave role · Report a conflict**

Temporary and emergency roles automatically expire. Renewal is a new consent event.

## 16.3 Consent lifecycle

Consent is not a permanent checkbox. Design states for requested, understood, granted, declined, expiring, renewed, changed purpose, withdrawn, and impossible to fully retract from external copies.

Youth assent and guardian permission are shown separately. Emergency exceptions identify the legal/policy basis, data used, responsible human, duration, and review route. Read-aloud and witnessed consent routes support people who cannot read or use the standard controls.

## 16.4 Human support handoff

**I need a person** must show the available role, language, accessibility support, expected response time, and what information will be shared. The member approves the context passed from Mi.

Handoff states: Finding someone · Waiting · Connected · Needs another specialist · Closed · No one available. When no one is available, show safe alternatives, realistic timing, and emergency services where relevant—not a false live-support promise.

The human sees only the minimum case context and requests additional access explicitly. The member can end the handoff and rate whether they felt heard, without making support conditional on a rating.

## 16.5 Export and leave flow

1. Choose what to include: profile, settings, messages, Pocket history, jars, learning, badges, standing, proposals, stories, files, consent receipts, and device list.
2. Choose human-readable copy, portable machine-readable copy, or both.
3. Choose encrypted file, trusted device, removable storage, or print-safe subset.
4. Verify destination, file size, and shared-device risk.
5. Create export and verify it opens.
6. Explain what can be deleted, what public/community records must remain, what other people may retain, and what happens to pending actions.
7. Choose leave now, schedule closure, or keep the profile.

Leaving never requires settling an unrelated dispute first. A rejoin flow explains which identity, history, and standing can be restored and which choices begin again.

## 16.6 Service-blueprint standard

Identity recovery, personhood, leave-now, child report, human handoff, offline money, shop dispute, and binding proposal each require a backstage service blueprint with:

Member action → UI response → device/local action → helper action → human role → data stored → policy/legal check → external service → failure recovery → notification → appeal.

A screen is not approved until the real human or service behind its promise has an owner and response expectation.

---

# 17. Visual-system completion, non-app access, and product operations

## 17.1 Remaining visual tokens

Before high-fidelity handoff, define:

- 4-point base spacing with documented component spacing
- Radius tiers for controls, cards, sheets, and containers
- Border and elevation rules
- Light, dark, and high-contrast themes
- Motion duration/easing and reduced-motion substitutes
- Map symbols and accessible chart palette
- Print typography and monochrome behavior
- Haptic and optional sound cues
- Comfortable and compact density modes

Dark mode is designed independently, not mechanically inverted. Stage-gated, warning, danger, focus, maps, and money confirmations require contrast testing in every theme.

## 17.2 International and right-to-left behavior

Support right-to-left navigation and reading order, long translated labels, CJK line breaking, mixed-script names, locale dates/numbers, names without assumed first/last structure, and per-content language changes.

Community translations show language, translator/source, review date, and **Suggest a correction**. Machine translation is labeled. A ballot or high-risk consent cannot rely on unreviewed machine translation without a prominent warning and human-support route.

## 17.3 Print, SMS, voice, and feature-phone subset

Critical non-app journeys:

- Printable rights and emergency cards
- Recovery sheet and role instructions
- Court/deadline packet
- Learning lessons and class ticket
- Shop receipt
- Proposal one-page summary and accessible ballot route where policy allows
- SMS resource lookup and saved-deadline reminder
- Low-bandwidth voice message
- Phone/IVR resource navigation
- Kiosk-to-private-device handoff

These channels use the same source, freshness, privacy, and correction rules. SMS and voice never pretend to provide the full private application.

## 17.4 Ethical product measurement

Collect only what improves reliability, accessibility, safety, and task completion. No advertising identifiers, cross-site tracking, sensitive-page session replay, or engagement optimization.

Analytics are documented by event, purpose, storage location, retention, access, and opt-out. Prefer on-device aggregation and minimum group-size thresholds. Public reports cannot identify a vulnerable person, household, or small street group.

Measure failed sends, stale resources, inaccessible tasks, abandoned high-risk flows, support delays, appeals, and offline conflicts—not time-on-app.

## 17.5 Content operations

Every maintained content type has an owner, jurisdiction/place, review interval, expiry rule, language status, accessibility status, source, and correction route.

Priority review queues cover emergency resources, legal information, child-safety guidance, shops accepting shares, class access information, learning packs, proposal summaries, helper disclaimers, and system errors.

## 17.6 Governance of interface changes

Classify changes as:

- **Maintenance:** reversible copy or visual correction with no rights impact
- **Product change:** tested workflow adjustment with published release note
- **Rights/safety change:** community consultation, specialist review, accessibility review, and staged testing
- **Emergency change:** narrow scope, named humans, public reason, automatic expiry, and retrospective review

Local themes may vary imagery, language, and accent expression but cannot weaken contrast, privacy labels, child protections, helper labels, money-stage labels, export, appeal, or emergency access. Critical transitions retain a supported fallback long enough for members to finish in-progress tasks.

---

# 18. Open-source React implementation shortlist

This is a **design handoff shortlist**, not code and not a guarantee of safety. “Open source” means the repository’s license allows use; it does not mean every release or dependency is secure. Pin versions, verify licenses, generate an SBOM, scan continuously, and maintain an exit plan.

## 18.1 Recommended baseline

| Need | Recommended open-source project | Why it fits | License posture |
|---|---|---|---|
| Web UI primitives | **React Aria / React Spectrum** (`adobe/react-spectrum`) | Accessibility-centered behavior without forcing a generic visual brand | Apache-2.0 repository; verify package |
| Alternative web primitives | **Radix Primitives** (`radix-ui/primitives`) | Mature headless interaction patterns; strong for dialogs, menus, popovers | MIT |
| Mobile/universal runtime | **React Native + Expo** (`expo/expo`) | High-quality universal app foundation and device APIs | Expo source MIT; dependencies vary |
| Component workshop | **Storybook** (`storybookjs/storybook`) | Review every state, accessibility condition, and viewport before pages | MIT |
| Server-state/offline query layer | **TanStack Query** (`TanStack/query`) | Mature async state model; useful for cached/offline experiences | MIT; official repositories were actively updated in August 2026 [TanStack repositories](https://github.com/orgs/TanStack/repositories) |
| Forms | **React Hook Form** (`react-hook-form/react-hook-form`) | Lightweight and widely used; suitable for long save-and-resume flows when designed carefully | MIT; verify release |
| Internationalization | **i18next + react-i18next** (`i18next/i18next`) | Mature language and pluralization system | MIT; verify each package |
| Maps | **MapLibre GL JS / MapLibre React Native** (`maplibre`) | Open map rendering without a proprietary UI dependency | BSD/MIT by project; React Native repo reports MIT [MapLibre React Native](https://github.com/maplibre/maplibre-react-native) |
| Accessibility engine | **axe-core** (`dequelabs/axe-core`) | Automated accessibility checks integrated into test workflows | MPL-2.0; automated checks do not replace human testing [axe-core analysis](https://socket.dev/npm/package/axe-core) |
| End-to-end testing | **Playwright** (`microsoft/playwright`) | Cross-browser flow, keyboard, viewport, and offline scenario testing | Apache-2.0 |
| Visual regression | **Loki** (`oblador/loki`) or self-hosted screenshot diffs | Keeps component states visually stable without a paid cloud requirement | MIT; verify maintenance before adoption |
| Icons | **Lucide** (`lucide-icons/lucide`) | Coherent, customizable open icon set | ISC; check icon-level attribution notes |
| Fonts | **Atkinson Hyperlegible** + **Noto** | Legibility and language coverage | Open Font License families; verify files |
| Dependency vulnerability checks | **OWASP Dependency-Check** (`dependency-check/DependencyCheck`) | Free, Apache-2.0 scanner for known vulnerable components; one layer in a larger process | Official repository is Apache-2.0 [OWASP Dependency-Check](https://github.com/dependency-check/DependencyCheck) |

Expo’s official repository describes the framework as open source under MIT while noting some dependencies use other licenses [Expo](https://github.com/expo/expo). TanStack identifies its stack as MIT and self-hostable [TanStack](https://tanstack.com/).

## 18.2 Choose one primitive strategy

Do **not** combine three component libraries and fight inconsistent behavior.

**Preferred web direction:** React Aria behavior + fully custom MiLyfe visual layer.  
**Acceptable alternative:** Radix Primitives + a strict internal accessibility review.  
**Native direction:** React Native/Expo components sharing tokens, content rules, and interaction specifications—not pretending DOM and native controls are identical.

## 18.3 Avoid by default

- “Free” libraries whose key accessibility, data-grid, map, chart, or design-system features require a commercial tier
- Source-available BSL, SSPL, Commons Clause, or “Sustainable Use” dependencies when MiLyfe requires OSI purity
- Unmaintained React Native ports that imitate a web library but lag on accessibility
- UI kits that make MiLyfe look like a generic admin dashboard
- Crypto-wallet templates, token dashboards, streak engines, and speculative price charts
- Cloud-only analytics, session replay on sensitive pages, and third-party chat widgets

## 18.4 Safety gate for every GitHub dependency

A repository enters the product only if it passes:

1. OSI-approved license confirmed in the exact version and transitive dependencies
2. Active maintainers and recent security response
3. Published security policy and responsible disclosure route where practical
4. No unresolved critical known vulnerabilities
5. Reproducible or locked build with checksums
6. SBOM generated
7. Accessibility behavior tested by humans
8. Offline and low-end-device performance tested
9. Privacy review: telemetry, remote fonts, CDNs, and data calls disabled or understood
10. Replacement/exit plan documented

No GitHub project can honestly be labeled “safe forever.” The UI should never make that claim.

---

# 19. Research and validation plan

## 19.1 Before high-fidelity visual design

Run contextual interviews with at least:

- 6 everyday neighbors across age and digital confidence
- 4 single parents/caregivers
- 4 people with unstable housing or shared-device experience
- 4 reentry/probation participants
- 4 elders
- 6 disabled participants covering screen reader, low vision, motor, hearing, and cognitive access
- 4 local shop workers/owners
- 3 teachers or tutors
- 3 domestic-violence or survivor-safety specialists
- 3 street keepers/mediators
- Legal, child-safety, and privacy reviewers

Compensate people. Do not pay in experimental `$MLY`. Do not recruit vulnerable participants through coercive gatekeepers.

## 19.2 First usability prototype tasks

1. Join with an avatar, Spanish language, and a shared phone.
2. Understand who can see the profile.
3. Find food available today without using the map.
4. Download a lesson and resume offline.
5. Thank a neighbor while offline and explain its status.
6. Join a shared jar and explain who must agree.
7. Read a proposal, find who may be harmed, and vote privately.
8. Turn Story off and verify nothing personal is published.
9. Remove a stolen device.
10. Find legal aid for a paper without assuming Rue is a lawyer.
11. Use quick exit safely.
12. Export information and explain what leaving does.

## 19.3 Success criteria

- 90% can name the five main areas after one session
- 95% understand $MLY credits are real and peer-swappable
- 90% correctly identify audience before publishing
- 100% of crisis participants can reach immediate help without helper chat
- 90% can explain “still walking” after an offline thank
- 90% know Mi is a helper, not a person or authority
- 85% complete signup without assistance; 100% with optional assistance
- Zero critical blockers in keyboard, screen-reader, large-text, and reduced-motion paths
- Median first useful action under 90 seconds

## 19.4 Red-team scenarios

- Abusive partner controls household and recovery friend role
- Child attempts to contact an unknown adult
- Helper invents a local shelter or deadline
- User misunderstands exchange gate status
- Shop falsely claims to accept shares
- Proposal hides who is harmed
- Keeper attempts to use audit access for retaliation
- Lost phone remains connected offline
- Cached map exposes a vulnerable address
- Public story removes a person in UI but leaves a discoverable copy
- Network returns after conflicting offline money actions
- Screen reader reaches destructive action without consequence text

---

# 20. Release sequence

## Design phase 1 — Foundation

Brand refinement · app icon · tokens · typography · navigation · accessibility modes · privacy audience · connection states · helper disclosure

## Design phase 2 — First complete life loop

Welcome/signup → Today → Pocket/weekly share → Thank → Learn/offline → Street/list → Voice/basic proposal → You/privacy → export

## Design phase 3 — Safety and vulnerable contexts

Shared device · youth · leave-now · devices/freeze · court paper · reentry path · elder check-in · kiosk

## Design phase 4 — Community operations

Shop · jar approvals · teacher/class host · keeper workspace · proposal outcomes · Pulse · Story

## Design phase 5 — First Street validation

Full accessibility audit · privacy threat modeling · domestic-violence safety review · child-safety review · offline conflict testing · multilingual testing · low-end Android performance testing

Only after these phases should advanced smart-home, twin, city, vehicle, or infrastructure surfaces enter the member product. They belong under existing areas, not as more global tabs.

---

# 21. Non-negotiable design laws

1. Five primary destinations; no module explosion.
2. One account and profile; household/shop are layers, not shared logins.
3. Visitor value before signup where safe.
4. Story is off for people until they opt in.
5. Children never appear on public maps or receive unknown-adult DMs.
6. Exact location is off by default.
7. Exchange-gated features must be clearly labeled with their activation status.
8. No investment charts, APY, market price, or token hype.
9. Helper messages are always labeled.
10. Mi cannot send, spend, publish, vote, approve, or change child/safety settings alone.
11. Human escalation exists outside helper chat.
12. Offline states tell the truth.
13. Standing never becomes one score and never gates rights.
14. Every public item shows freshness and source.
15. Every sharing action shows audience before confirmation.
16. Every role shows scope and expiry.
17. Every serious system action has an appeal or human review path.
18. Export works even during a dispute.
19. Accessibility blocks release.
20. The visual brand never impersonates a bank, court, government ID, police service, hospital, or emergency dispatcher.

---

# 22. Final product picture

A person opens MiLyfe and sees what matters today—not a feed engineered for attention. They can understand their share without learning crypto, continue a lesson without internet, find nearby food without exposing themselves, ask for help without shame, decide on a street proposal without giving a shop or helper extra citizenship, secure their life from a stolen phone or unsafe household, and leave with their information.

The interface is navy where it must feel dependable, blue where it helps a person move, and green where life improves. The supplied logo becomes the beginning of that story: **technology moving toward life.**

**MiLyfe is not designed as a platform people must serve. It is designed as a tool that serves people.**
