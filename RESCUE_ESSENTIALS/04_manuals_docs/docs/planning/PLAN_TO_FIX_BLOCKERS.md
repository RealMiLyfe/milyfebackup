# MiLyfe Platform - Blocker Fix Plan

## Overview
This plan addresses the critical blockers preventing the MiLyfe platform from delivering immediate value to new users and maintaining proper economic accounting. The fixes ensure users receive their welcome rewards immediately, UBI distributions correctly debit the treasury, and all financial flows are properly tracked.

## Root Causes Identified

1. **Welcome reward not firing**: New users complete onboarding but don't receive the 50 $MLY welcome bonus
2. **UBI not running**: CRON_SECRET missing, treasury not debited, incorrect citizen count
3. **Treasury disconnected**: Balance doesn't reflect actual transactions (inserts vs updates)
4. **Treasury amount incorrect**: Set to 10K instead of global-scale 10M
5. **Rewards system incomplete**: Only welcome reward auto-created; others missing
6. **Landing page stats stale**: Not reflecting real-time treasury and citizen data

## Implementation Plan

### Phase 1: Treasury Initialization & Welcome Flow
**Goal**: New users get immediate value; treasury reflects global ambition

#### 1.1 Set Initial Treasury Balance to $10,000,000
- **File**: `milyfe-platform/scripts/migrate-live.sql`
- **Change**: Update initial treasury insert
  ```sql
  -- Before
  INSERT INTO public.community_treasury (balance, citizen_count) VALUES (10000, 1) ON CONFLICT DO NOTHING;
  
  -- After
  INSERT INTO public.community_treasury (balance, citizen_count) VALUES (10000000, 1) ON CONFLICT DO NOTHING;
  ```
- **Alternative**: Run one-time SQL update on existing row:
  ```sql
  UPDATE public.community_treasury SET balance = 10000000 WHERE id = (SELECT id FROM public.community_treasury ORDER BY snapshot_at LIMIT 1);
  ```

#### 1.2 Modify handle_new_user Trigger for Immediate Value
- **File**: `milyfe-platform/supabase/migrations/001_mvp_schema.sql`
- **Change**: Set initial wallet spending_balance to 50 instead of 0
  ```sql
  -- Before
  INSERT INTO public.wallets (user_id) VALUES (NEW.id);
  
  -- After
  INSERT INTO public.wallets (user_id, spending_balance) VALUES (NEW.id, 50);
  ```
- **Keep**: Welcome reward creation in trigger (provides double assurance)
- **Result**: Users start with 50 $MLY in spending wallet immediately on signup

### Phase 2: UBI Distribution Fixes
**Goal**: Weekly UBI runs automatically, debits treasury, uses real citizen count

#### 2.1 Fix UBI Cron Route Security & Logic
- **File**: `milyfe-platform/src/app/api/cron/ubi/route.ts`
- **Changes**:
  ```typescript
  // Before (incorrect auth check)
  const authHeader = request.headers.get('authorization');
  if (authHeader !== \`Bearer ${process.env.CRON_SECRET}\`) {
    return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
  }

  // After (correct CRON_SECRET header check)
  const cronSecret = request.headers.get('x-cron-secret');
  if (cronSecret !== process.env.CRON_SECRET) {
    return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
  }

  // Before (inserts new treasury row, doesn't debit actual balance)
  // Update treasury snapshot
  await supabase.from('community_treasury').insert({
    balance: distributed * WEEKLY_UBI_AMOUNT, // Wrong - should be actual balance
    total_distributed: distributed * WEEKLY_UBI_AMOUNT,
    citizen_count: eligibleWallets.length,
  });

  // After (UPDATE existing treasury row, decrement balance)
  // Get current treasury state for accurate calculation
  const { data: treasuryData, error: treasuryError } = await supabase
    .from('community_treasury')
    .select('balance, total_distributed')
    .order('snapshot_at', { ascending: false })
    .limit(1)
    .single();

  if (treasuryError) throw treasuryError;

  const newBalance = treasuryData.balance - (distributed * WEEKLY_UBI_AMOUNT);
  const newTotalDistributed = treasuryData.total_distributed + (distributed * WEEKLY_UBI_AMOUNT);

  // Update the existing treasury row (not insert new)
  await supabase
    .from('community_treasury')
    .update({
      balance: newBalance,
      total_distributed: newTotalDistributed,
      citizen_count: await getActualCitizenCount(supabase), // New function
      snapshot_at: new Date().toISOString()
    })
    .order('snapshot_at', { ascending: false })
    .limit(1)
    .maybeSingle(); // Update the most recent row
  ```

#### 2.2 Implement Real Citizen Count Function
- **Add to UBI route file**:
  ```typescript
  async function getActualCitizenCount(supabase: any): Promise<number> {
    const { data, error } = await supabase
      .from('profiles')
      .select('id', { count: 'exact' })
      .eq('onboarding_complete', true);

    if (error) throw error;
    return data.count || 0;
  }
  ```

#### 2.3 Fix UBI Schedule Logic (if needed)
- **Check**: The UBI cron currently checks `last_ubi_at.lt.sixDaysAgo` (6 days)
- **Verify**: If cron runs weekly, this is correct. If changed to daily, adjust to 1 day.
- **Note**: User mentioned cron changed to daily for Hobby plan but logic checks 6 days - needs alignment

### Phase 3: Environmental Configuration
**Goal**: Enable cron execution and external services

#### 3.1 Set CRON_SECRET in Vercel
- **Action**: In Vercel project settings → Environment Variables
- **Add**: 
  - Key: `CRON_SECRET`
  - Value: [Generate secure random string, e.g., UUID]
  - Environment: Production (and Preview if needed)
- **Note**: Value must match what the cron route expects in the `x-cron-secret` header

#### 3.2 Configure Upstash Redis for Production Rate Limiting
- **Action**: 
  1. Create Upstash Redis account
  2. Create new Redis database
  3. Get `UPSTASH_REDIS_REST_URL` and `UPSTASH_REDIS_REST_TOKEN`
- **Vercel Env Vars**:
  - `UPSTASH_REDIS_REST_URL` = [from Upstash]
  - `UPSTASH_REDIS_REST_TOKEN` = [from Upstash]

#### 3.3 Configure AI Chat Backend
- **Action**: Choose LLM provider (OpenAI, Groq, or self-hosted Ollama)
- **Vercel Env Vars**:
  - `OPENAI_API_KEY` = [API key from provider]
  - `OPENAI_API_BASE_URL` = [e.g., `https://api.openai.com/v1` for OpenAI, or `http://localhost:11434` for local Ollama]
  - `MI_MODEL` = [model name, e.g., `gpt-4o` or `llama3`]

### Phase 4: Rewards System Completion
**Goal**: All meaningful actions trigger treasury-backed rewards

#### 4.1 Ensure Welcome Reward Claims Properly
- **File**: `milyfe-platform/src/lib/actions/profile.ts` (completeOnboarding action)
- **Verify**: The welcome reward claiming logic works correctly with immediate wallet balance
- **Note**: With Phase 1.2, users get 50 $MLY immediately, so the welcome reward claim becomes a bonus confirmation

#### 4.2 Add First-Proposal Reward
- **Location**: Where proposals are created (likely in governance actions)
- **Implementation**:
  ```typescript
  // After successfully creating a proposal
  // Check if this is user's first proposal
  const { data: proposalCount } = await supabase
    .from('proposals')
    .select('id', { count: 'exact' })
    .eq('author_id', user.id);

  if (proposalCount === 1) {
    // Create first-proposal reward
    await supabase.from('rewards').insert({
      user_id: user.id,
      type: 'contribution', // or create new 'first-proposal' type
      amount: 25,
      title: 'First Proposal',
      description: 'Thank you for submitting your first community proposal!',
      claimed: false
    });
  }
  ```

#### 4.3 Add First-Attestation Reward
- **Location**: In `giveAttestation` action (profile.ts)
- **Implementation**:
  ```typescript
  // After successfully creating attestation
  // Check if this is user's first attestation given
  const { data: attestationCount } = await supabase
    .from('attestations')
    .select('id', { count: 'exact' })
    .eq('from_user_id', user.id);

  if (attestationCount === 1) {
    // Create first-attestation reward
    await supabase.from('rewards').insert({
      user_id: user.id,
      type: 'attestation',
      amount: 10,
      title: 'First Attestation',
      description: 'You\'ve earned your first recognition reward for recognizing others!',
      claimed: false
    });
  }
  ```

#### 4.4 Add Learning Completion Rewards
- **Location**: Where learning paths are completed
- **Implementation**: Varies by path (20-100 $MLY based on difficulty/length)

#### 4.5 Add Treasury Debit to Quest Rewards
- **Location**: Quest reward claiming logic (likely in wallet or quests actions)
- **Implementation**:
  ```typescript
  // When quest reward is paid out
  // Before crediting user's wallet, debit treasury
  const { data: treasuryData } = await supabase
    .from('community_treasury')
    .select('balance')
    .order('snapshot_at', { ascending: false })
    .limit(1)
    .single();

  const newBalance = treasuryData.balance - questRewardAmount;

  await supabase
    .from('community_treasury')
    .update({ balance: newBalance })
    .order('snapshot_at', { ascending: false })
    .limit(1);

  // Then credit user's wallet as usual
  ```

### Phase 5: Treasury Integration Verification
**Goal**: All financial flows properly debit/credit treasury

#### 5.1 Verify UBI Debits Treasury
- **Test**: Run UBI cron manually, verify treasury balance decreases by total distributed

#### 5.2 Verify Quest Rewards Debit Treasury
- **Test**: Complete a quest, verify treasury balance decreases by reward amount

#### 5.3 Verify Marketplace Fees Credit Treasury
- **Location**: Marketplace transaction flow
- **Check**: When users pay fees for marketplace transactions, amount credits treasury

#### 5.4 Verify Community Contributions Affect Treasury
- **Check**: When users convert spending to community pot, verify treasury logic

### Phase 6: Landing Page & Dashboard Synchronization
**Goal**: All displays show real-time data

#### 6.1 Update Treasury Data Fetching
- **Files**: Treasury page, landing page stats, dashboard
- **Change**: Instead of just reading latest community_treasury row, calculate:
  ```typescript
  // For treasury balance
  const { data: treasuryData } = await supabase
    .from('community_treasury')
    .select('balance, total_distributed, citizen_count')
    .order('snapshot_at', { ascending: false })
    .limit(1)
    .single();

  // For real-time citizen count (more accurate)
  const { data: profilesData, error: profilesError } = await supabase
    .from('profiles')
    .select('id', { count: 'exact' })
    .eq('onboarding_complete', true);

  const realCitizenCount = profilesData.count || 0;
  ```

#### 6.2 Implement Real-Time Stats Component
- **Create**: Reusable stat fetching hook that combines treasury data with live counts
- **Use**: In landing page, dashboard, treasury page

## Verification Checklist

### After Implementation, Verify:
1. **Signup Flow**:
   - [ ] New user gets 50 $MLY immediately in spending wallet (visible in /wallet)
   - [ ] Welcome reward row created in rewards table
   - [ ] Profile shows onboarding_complete = false until onboarding done

2. **Welcome Reward Claim** (on onboarding completion):
   - [ ] completeOnboarding action successfully claims welcome reward
   - [ ] Additional 50 $MLY credited (total 100 $MLY if immediate + claimed)
   - [ ] Welcome reward marked as claimed

3. **UBI Distribution**:
   - [ ] CRON_SECRET set in Vercel env vars
   - [ ] UBI cron returns 200 when called with correct x-cron-secret header
   - [ ] Treasury balance decreases by total UBI distributed
   - [ ] total_distributed in treasury increases by amount distributed
   - [ ] citizen_count reflects actual profiles with onboarding_complete = true
   - [ ] Wallets receive 100 $MLY to spending balance
   - [ ] UBI transactions and rewards records created

4. **Quest Rewards**:
   - [ ] When quest pays out, treasury balance decreases by reward amount
   - [ ] User's wallet increases by reward amount

5. **Landing Page Stats**:
   - [ ] Treasury shows current balance (starting at 10,000,000)
   - [ ] Citizens count shows real number of onboarded profiles
   - [ ] Learning modules shows 35 (from seed data)
   - [ ] "100% Community Owned" statement remains accurate

6. **End-to-End Flow**:
   - [ ] Sign up → see 50 $MLY in wallet immediately
   - [ ] Complete onboarding → claim welcome reward → see additional 50 $MLY
   - [ ] Treasury balance decreases by 100 $MLY
   - [ ] Run UBI cron → see treasury decrease further by distributed amount
   - [ ] Complete quest → see treasury decrease by quest reward amount

## Risk Mitigation

1. **Database Locking**: 
   - Use Supabase's row-level locking in UBI cron batch processing to prevent race conditions
   - Current implementation processes in batches of 50 which helps

2. **Failed Transactions**:
   - UBI cron has error handling - continues processing other wallets if one fails
   - Consider adding retry mechanism for failed transactions

3. **Treasury Going Negative**:
   - Add safety check in UBI cron: don't distribute if balance < amount needed
   - Or implement partial distribution based on available funds

4. **Cron Security**:
   - Ensure CRON_SECRET is strong (minimum 32 characters random string)
   - Rotate periodically if suspected compromised

## Estimated Effort

- **Database Changes**: 30 minutes (SQL updates)
- **Backend Changes**: 2-3 hours (UBI cron fix, treasury updates)
- **Environmental Config**: 15 minutes (Vercel env vars)
- **Rewards System**: 1-2 hours (first-proposal, first-attestation rewards)
- **Testing & Verification**: 1-2 hours
- **Total**: 5-6 hours

## Notes

- The welcome reward duplication (immediate 50 $MLY + claimable 50 $MLY) provides strong UX feedback: "You got money just for signing up!" and "You got more for completing your profile!"
- Treasury now represents real economic flow: seeds - distributions + fees
- Global-scale 10,000,000 $MLY seed sustains ~1,000 citizens for 100 weeks at 100 $MLY/week, giving runway for organic growth
- All changes maintain existing API contracts and frontend compatibility

## Files to Modify

1. `milyfe-platform/scripts/migrate-live.sql` - Treasury initial balance
2. `milyfe-platform/supabase/migrations/001_mvp_schema.sql` - handle_new_user wallet init
3. `milyfe-platform/src/app/api/cron/ubi/route.ts` - UBI cron logic and security
4. `milyfe-platform/src/lib/actions/profile.ts` - Potentially add first-proposal/first-attestation rewards
5. Quest reward actions (location TBD) - Add treasury debit
6. Treasury/landing page components (location TBD) - Use real-time citizen count

## Next Steps

1. Backup current database state
2. Execute SQL updates for treasury balance
3. Modify handle_new_user trigger
4. Fix UBI cron route
5. Set environment variables in Vercel
6. Implement reward additions
7. Test end-to-end flows
8. Deploy to production