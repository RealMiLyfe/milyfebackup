# MiLyfe Accessibility Audit Checklist

**Standard:** WCAG 2.2 AA minimum, AAA where practical for crisis and money flows.  
**Rule:** Accessibility blocks release.

---

## Automated Checks (axe-core + Playwright)

### Perception
- [ ] All images have alt text (no decorative images without alt="")
- [ ] Color is never the only indicator (use icon + text)
- [ ] Contrast ratio ≥ 4.5:1 body text, ≥ 3:1 large text
- [ ] Text resizes to 200% without loss of function
- [ ] Content reflows at 320px viewport without horizontal scroll
- [ ] Captions/transcripts for all audio/video content
- [ ] No content flashes more than 3 times per second

### Operation
- [ ] All functions accessible via keyboard
- [ ] No keyboard traps
- [ ] Focus visible and not obscured by sticky elements
- [ ] Touch targets ≥ 44×44 px (prefer 48×48)
- [ ] No gesture-only actions (always a button alternative)
- [ ] Timeouts can be extended (except security events)
- [ ] Reduced motion honored (`prefers-reduced-motion`)

### Understanding
- [ ] Page language declared (`lang` attribute)
- [ ] Content language changes marked inline
- [ ] Error messages identify the field and suggest correction
- [ ] Labels associated with controls
- [ ] Headings in logical order (no skipped levels)
- [ ] Consistent navigation placement across screens
- [ ] One primary action per card/screen

### Robustness
- [ ] Valid HTML/ARIA (no duplicate IDs, proper roles)
- [ ] Status messages announced to screen reader (aria-live)
- [ ] Custom components have correct ARIA roles and states
- [ ] Name, role, value exposed for all interactive elements

---

## Manual Checks (Real Users Required)

### Screen Reader Testing
- [ ] VoiceOver (iOS) — complete signup flow
- [ ] TalkBack (Android) — complete signup flow
- [ ] NVDA/JAWS (Windows) — web version
- [ ] All 5 tabs navigable by screen reader
- [ ] Thank Someone flow completable without vision
- [ ] Safety → Leave Now reachable in under 30 seconds
- [ ] Ballot choice announced without revealing to others
- [ ] Mi helper responses labeled as helper (not person)

### Motor/Switch Access
- [ ] Full app navigable with switch access
- [ ] No timing-dependent interactions (except safety timers)
- [ ] All actions reachable via single switch scanning
- [ ] Save-and-resume for multi-step flows

### Cognitive Accessibility
- [ ] One idea per screen/card
- [ ] Concrete date formats ("Friday, August 21 at 4:00 PM")
- [ ] No double negatives
- [ ] Uncommon terms explained immediately
- [ ] Examples shown before high-risk choices
- [ ] No countdown pressure for non-emergencies
- [ ] MiPlain language passes the grandmother test

### Specific Populations
- [ ] Low vision: Large + Extra Large modes tested
- [ ] Color blind: Charts tested with sim
- [ ] Deaf/HoH: All audio has captions/transcript
- [ ] Dyslexia: Atkinson Hyperlegible renders well
- [ ] ESL: Plain language, short sentences
- [ ] Low literacy: Icons + text, audio playback

---

## MiLyfe-Specific Accessibility Requirements

### Crisis Flows
- [ ] Leave Now reachable from any screen in ≤ 2 taps
- [ ] Quick Exit works with keyboard, switch, and touch
- [ ] Emergency number (911) callable without navigating menus
- [ ] Panic freeze accessible without fine motor control
- [ ] Safety flows never trap user in "Are you sure?" loops

### Money Flows
- [ ] Balance announced correctly ("247 practice shares, no real value")
- [ ] Transaction states use words not just color ("Still walking")
- [ ] Practice badge persistent and announced every time
- [ ] Review sheet reads consequence before confirm button

### Shared Device
- [ ] Session timer visible and announced
- [ ] "Clear and exit" reachable by any input method
- [ ] No sensitive notifications leak during session

---

## Testing Tools

```bash
# Automated accessibility scan
npx jest --testPathPattern=accessibility

# Manual: run against live app
npx playwright test --project=accessibility

# Storybook: test all component states
npx storybook --port 6006
```

## Compensation

Per the blueprint: disabled reviewers must be compensated fairly.
Budget for accessibility testing sessions and do not pay in experimental $MLY.
