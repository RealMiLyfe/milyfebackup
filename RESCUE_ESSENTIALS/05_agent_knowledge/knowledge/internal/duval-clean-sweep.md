# THE DUVAL CLEAN SWEEP — Operational Reference

## THE SIX STONES (Investigation Domains)

### STONE 1: The Poverty Tax
- Jail telecom (Securus/GTL/ViaPath) — kickback commission to city
- Commissary (Keefe Group) — contract markup
- Private probation fees — violation-to-jail pipeline
- License suspensions for unpaid fees (not driving offenses)
- Civil asset forfeiture — seizure without conviction
- Cash bail — millions extracted, never returned after acquittal
- Walking While Black: 55% of pedestrian tickets → 29% of population. 982 licenses suspended.

### STONE 2: The Courtroom Cartel
- Angela Corey era (2009-17): 77 children charged as adults in 2016. Death sentences highest in FL.
- Melissa Nelson era (2017-present): CIR established. 200+ innocence letters. ONE release (43 years).
- Brady/Giglio list — officers who can't testify but are still on payroll
- 95%+ plea rate = overcharge pressure (trial tax)
- Judicial campaign finance: FOP, bail bond, prosecutor donations to judges

### STONE 3: Jail Death Ecosystem
- 12 in-custody deaths in 2023 alone
- Deaths TRIPLED after private medical vendor hired (2017)
- Armor: terminated after criminal conviction disclosure failure
- NaphCare: current provider, facing lawsuits
- 217 corrections officer vacancies
- Florida has NO mandatory third-party review of in-custody deaths
- JSO cold case unit investigates its own jail deaths

### STONE 4: JSO & FOP Power
- Black = 30% population but 56% of people killed by police
- 5,510 complaints 2017-22, 7% ruled for civilians
- 0% of use-of-force complaints ruled for civilians (out of 50)
- JSO OPTS OUT of FBI UCR database (deliberate opacity)
- 14 JSO employees arrested in 2024
- FOP Lodge 530 dictates discipline terms
- 2024 FL law dissolved 15+ civilian review boards statewide

### STONE 5: Youth & Mental Health Pipelines
- Black students 3x more likely to be arrested at school
- Black girls = 21% of FL female 10-17 but 45% of girls arrested
- Truancy ordinance: 5+ absences = parents face 60 days jail
- Baker Act: children as young as 6 involuntarily committed from schools

### STONE 6: ICE Pipeline
- Ordinance 2025-0147: FIRST city to criminalize undocumented presence locally
- 30-day mandatory jail for first offense, 60 for repeat
- $76,250 for 25 mobile fingerprint scanners
- 602 detained in 2024, 334 transferred to ICE
- Baker County: 259 complaints since 2017, over half of state total
- Whistleblower documented systemic neglect, falsified records, sexual harassment
- 88 days solitary to pressure deportation signing
- Deegan allowed ordinance without her signature

## THE SEVEN DATABASES TO BUILD
1. Officer Profiles (arrested/terminated/sued, 10 years)
2. Wrongful Conviction Queue (200+ CIR letters)
3. Jail Death Ledger (2017-present, every name)
4. Judicial Sentencing Patterns (4th Circuit, race/geography disparity)
5. Contract Vendor Scrutiny (medical, food, telecom, commissary, bail, monitoring)
6. ICE Pipeline Tracker (bookings → detainers → Baker transfers)
7. Coalition CRM (all orgs, contact logs, engagement)

## GRAPH DATABASE SCHEMA (Neo4j)
Nodes: PERSON, ORGANIZATION, CASE, CONTRACT, DONATION, LOCATION, INCIDENT
Edges: DONATED_TO, PROSECUTED, PRESIDED_OVER, EMPLOYED_BY, ARRESTED, DIED_IN_CUSTODY_OF, TRANSFERRED_TO, CONTRACTED_WITH, COMPLAINED_AGAINST, REPRESENTED_BY, OCCURRED_IN

## PUBLIC RECORDS SOURCES
- Duval Clerk of Courts (duvalclerk.com)
- JSO Inmate Search (inmatesearch.jaxsheriff.org)
- Jacksonville Legistar (jaxcityc.legistar.com)
- Jacksonville.gov Budget
- Council Auditor
- FDLE, Florida Bar, JQC, Commission on Ethics
- FL Div of Elections, Florida Sunshine Portal
- PACER (Middle District FL, 300 N Hogan St)
- Sunbiz.org (LLC ownership)
- ICE FOIA + DHS OIG

## LEGAL GUARDRAILS
- Only public records
- Never impersonate
- Document every source
- Respect sealed/juvenile/mental health/adoption records
- Route around Marsy's Law victim data
- Publish with dignity
- Right of response for named officials
- Never fabricate — mark uncertain as "unverified"
- Never dox private individuals
- Only public roles in public actions

## NARRATIVE WEAPONS
1. The Body Count: "How many people have to die in our jail?"
2. The Letter Stack: "200 letters. 1 release. That's Duval's math of hope."
3. The Officer Arrest Pace: "A dozen of his own in two years."
4. The Walking Tax: "55% of tickets. 29% of the population."
5. The Baker Pipeline: "First city to jail people for existing."

## KEY CONTACTS FOR THIS WORK
- Sen. Tracie Davis (co-signed DOJ letter on jail deaths)
- Rep. Angie Nixon (co-signed DOJ letter)
- Isaiah Rumlin (NAACP Jax president)
- Ben Frazier (Northside Coalition)
- Shelley Thibodeau (CIR Director, 200+ letters)
- ACLU of Florida (Baker County litigation lead)
- Jacksonville Community Action Committee (jaxtakesaction.org)
- The Bail Project Jax (Adrienne Johnson, Regional Director)
- Pace Center for Girls (Black girls diversion)
- Sanctuary of the South (Baker County co-litigant)
- The Tributary (broke jail death rate story)
- ProPublica (Walking While Black reporters)
