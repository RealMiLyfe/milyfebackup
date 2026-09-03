# MiLyfe Feature Gap Analysis — vs. Reference Platforms

**Purpose:** Catalogue every major feature across the reference commercial platforms in
`~/ultimateplatform`, so MiLyfe (Next.js 14 + Supabase, ~96 routes / 145 tables, live)
can decide what to build next. This is a **feature inventory / blueprint**, not code.

> Legal note: Feature lists, data-model concepts, and API surface design are ideas and are
> free to catalogue and reimplement. The reference products' actual source code is
> proprietary (Envato license) and is NOT copied here. Everything below is meant to be
> **built fresh on the MiLyfe stack** as original code we own outright.

Reference products inventoried:
1. **WoWonder** — PHP social network (139 DB tables, 182 REST v2 endpoints, ~980 functions)
2. **PixelPhoto** — image-sharing / photo social network
3. **DigiMuse** — music streaming platform (Spotify/YouTube/MusicBrainz ingest, lyrics)
4. **PlayHub** — Laravel video CMS (shorts, communities, live streaming via LiveKit)
5. **eMart** — Flutter multi-service delivery (food/grocery/pharmacy/flowers, Firebase)
6. **WPLMS** — WordPress learning management system

---

## Legend
- ✅ MiLyfe likely already has (verify)
- 🔴 MISSING — not in MiLyfe today
- 🟡 PARTIAL — exists but shallow vs. reference

## Ground Rules (per MiLyfe constraints)
- **$0 budget.** Everything must be buildable on free/self-hosted infra (Supabase free tier, open-source libs).
- **MiLyfe is the ONLY payment system.** All third-party gateways from the reference products
  (Stripe, PayPal, Razorpay, Paystack, Flutterwave, Coinbase, CoinPayments, Cashfree, Paysera,
  iyzipay, SecurionPay, YooMoney, Braintree, PayFast, aamarpay, ngenius, Fortumo, Twilio-pay, bank
  transfer, etc.) are **excluded**. Money movement routes through the MiLyfe internal wallet/ledger only.
- **No ad systems.** All ad features from the reference products (AdMob, website ads, sponsored/
  boosted-for-pay posts, ad click tracking, `create_ad`/`userads`, ad settings) are **excluded**.
  "Boost/feature" mechanics, if kept, are driven by MiLyfe internal currency, not paid ad buys.

> Excluded-by-rule items are listed in a struck-through / "DROP" column so we have a record, but
> they are **not** part of the MiLyfe build.

---

## 1. Social Core (from WoWonder / PixelPhoto)

| Feature | Status | Notes |
|---|---|---|
| News feed with media filters (text/photo/video/music/files/maps) | 🟡 | WoWonder filters feed 6 ways with privacy levels 0–5 |
| Post privacy levels (public/friends/only-me/custom/page-only) | 🔴 | 5+ privacy modes |
| Reactions (like/love/haha/etc.) beyond simple like | 🟡 | `Wo_GetPostReactions` multi-type |
| Comments + nested replies + comment reactions | 🟡 | |
| Stories (24h) + story views + story reactions + mute stories | 🔴 | `create-story`, `get_story_views`, `react_story` |
| Reels / short video | 🔴 | `reels.php`, `is_reel` feed flag |
| Pinned posts (user/page/group) | 🔴 | `Wo_PinPost` |
| Boosted / promoted posts + boosted pages | 🔴 | `Wo_BoostPost`, `get-promoted-post` |
| Saved posts / bookmarks | 🟡 | `savedPosts.php` |
| Hashtags + trending | 🟡 | `hashtag.php` |
| Memories ("on this day") | 🔴 | `get_memories` |
| Poke | 🔴 | `poke.php` |
| Nearby users / friends nearby / nearby business & shops | 🔴 | geolocation discovery |
| User suggestions / recommended follows | 🟡 | `get-user-suggestions` |
| Follow requests + block/mute users | 🟡 | |
| Multi-account switching | 🔴 | `switch-account.php` |
| Two-factor auth + unusual login detection | 🟡 | `two-factor`, `unusual-login.php` |
| Social login (Google/FB/Twitter/LinkedIn/VK/Instagram/TikTok) | 🟡 | many providers |
| User verification / page verification badges | 🔴 | `verification.php`, `page_verification` |

## 1b. PixelPhoto — FULL FRACTAL AUDIT (image/photo social network)

> Audited to the action level: 18 XHR handlers, 13 mobile API endpoint classes, 45 DB tables.
> This is the deepest layer — every individual action a user or client can trigger.

### Posts / media (xhr/posts.php — 36 actions)
| Feature | Status | Notes |
|---|---|---|
| Upload images (with filters) | 🟡 | `upload-post-images`, `filter_image` |
| Upload video + **360° video** | 🔴 | `new-video`, `video_type=360` |
| FFmpeg server-side video processing | 🔴 | `ffmpeg-video-upload`, `ffmpeg_sys` |
| Reels (short video) upload + explore | 🔴 | `new-reels`, `upload-post-reels`, `explore-reels` |
| Embed external video (PlayTube/YouTube/TikTok) | 🔴 | `new-embed`, `tiktok_fetch`, `url_fetch` |
| Import GIFs | 🔴 | `new-gif`, `import-post-gifs` |
| Post like + view-likes list + add_view counter | 🟡 | `like`, `view-likes`, `add_view` |
| Comments + delete + threaded (see comments handler) | 🟡 | `add-comment` |
| Save post / load saved posts | 🟡 | `save`, `load-saved-posts` |
| Report post | 🟡 | `report` |
| Lightbox viewer | 🔴 | `lightbox` |
| Explore: posts / tags / lives / reels | 🔴 | `explore-*` discovery grid |
| Timeline / user posts / user reels feeds | 🟡 | `load-tl-posts`, `load-user-reels` |
| ~~Boost post (paid)~~ | DROP | ad/paid — excluded; MiLyfe-currency boost only if desired |

### Main / social graph (xhr/main.php — 24 actions)
| Feature | Status | Notes |
|---|---|---|
| Follow / accept-requests / delete-requests (private accounts) | 🟡 | `follow`, `accept_requests` |
| Block user | 🟡 | `block-user` |
| Explore people / search users / posts / blogs | 🟡 | `explore-people`, `search-*` |
| Activity feed + notifications polling | 🟡 | `get_more_activities`, `get_notif` |
| Share post (internal + external) | 🔴 | `share_post_on`, `get-share-modal` |
| Site mode switch (e.g., photo/social) | 🔴 | `change_mode` |
| Last-seen / presence updates | 🟡 | `update_user_lastseen` |
| Contact form | 🟡 | `contact_us` |
| Funding: create/delete/report campaigns | 🔴 | `delete-funding`, `fund_report` |
| ~~get_payment_methods / checkout (gateways)~~ | DROP | route via MiLyfe wallet instead |

### Profile / fundraising / ads (xhr/profile.php — 13 actions)
| Feature | Status | Notes |
|---|---|---|
| Followers / following / subscriptions lists | 🟡 | `load-user-followers`, `-subscriptions` |
| Crowdfunding: create/edit/delete/load fundraisers + recent raises | 🔴 | `create_fund`, `load_more_recent_raise` |
| ~~create_ad / edit_ad / delete_ad / ad_click~~ | DROP | ad system — excluded |

### Story (xhr/story.php) & Live (xhr/live.php)
| Feature | Status | Notes |
|---|---|---|
| Stories: add / show / delete / react (rs) + view tracking | 🔴 | `pxp_story`, `pxp_story_views` |
| Live streaming: create / thumbnail / comments / delete | 🔴 | `pxp_agoravideocall`, `live_sub_users` |
| Story add-limit gating (pro/free) | 🔴 | `canAddStory()` |

### Messages (xhr/messages.php) + calls
| Feature | Status | Notes |
|---|---|---|
| Send / media messages / get old messages | 🟡 | `send`, `get_old_messages` |
| Clear chat / delete chat / delete messages | 🔴 | `clear-chat`, `delete-messages` |
| Audio + video calls (Agora) | 🔴 | `pxp_audiocalls`, `pxp_agoravideocall`, `videocalles` |

### Comments (xhr/comments.php — threaded)
| Feature | Status | Notes |
|---|---|---|
| Comment replies (nested) | 🟡 | `add_comment_reply`, `get_comment_reply` |
| Like/dislike comments AND replies | 🔴 | `like_dislike`, `reply_like_dislike` |

### Blogs (xhr/blogs.php)
| Feature | Status | Notes |
|---|---|---|
| Articles: list / comment / like / delete | 🟡 | `load-tl-articles`, `pxp_blog*` |

### Store (xhr/store.php — digital goods marketplace)
| Feature | Status | Notes |
|---|---|---|
| Sell/buy digital store items + license | 🔴 | `pxp_store`, `item_license`, `store_purchase_history` |
| Explore all-store / user-store | 🔴 | `explore-all-store` |
| Edit / delete store items | 🔴 | `edit-store-item` |
| Seller payout / withdraw | 🔴 | `get_paid`, `withdraw` → **MiLyfe wallet only** |
| ~~stripe/cashfree/iyzipay/paysera/paypal/sms payment~~ | DROP | gateways excluded |

### Settings (xhr/settings.php)
| Feature | Status | Notes |
|---|---|---|
| Profile / avatar / password / privacy / notifications | 🟡 | standard settings |
| Two-factor auth + verify | 🟡 | `two_factor`, `two_factor_verify` |
| Business account + verification request | 🔴 | `business`, `verify` |
| Delete account / delete session | 🟡 | `delete-account`, `delete_session` |
| Block/unblock management | 🟡 | `unblock-user` |
| Withdraw (earnings) | 🔴 | → **MiLyfe wallet only** |

### Mobile API v1 (endpoint/v1 — 13 classes, ~200 actions)
Full parity mobile API: Auth, User, Posts, Reels, Story, Live, Messages, Blog, Settings, Misc,
Startup. Includes `agora_token`, `social_login`, `startup_suggestions`, `fetch_home_posts`,
`create_reel`, `get_story_views`, funding, favorites, boosted/sponsored fetch. **This is the
mobile-app contract** MiLyfe needs its own version of.
> `PaymentEndPoint` and `AdsEndPoint` → **excluded** (MiLyfe wallet + no ads).

### PixelPhoto DB tables (45) worth modeling
`pxp_posts, pxp_media_files, pxp_post_comments, pxp_comments_reply, pxp_comments_reply_likes,
pxp_post_likes, pxp_saved_posts, pxp_hashtags, pxp_story, pxp_story_views, pxp_chats, pxp_messages,
pxp_audiocalls, pxp_agoravideocall, pxp_notifications, pxp_activities, pxp_connectivities (follows),
pxp_blocks, pxp_blacklist, pxp_blog(+comments/likes), pxp_store, pxp_funding(+raise/reports),
pxp_verification_requests, pxp_business_requests, pxp_sessions, pxp_static_pages, pxp_langs,
pxp_config, pxp_subscribers, pxp_user_reports, pxp_post_reports`
> **Excluded tables (rule):** `pxp_payments, pxp_transactions, pxp_pending_payments,
> pxp_bank_receipts, pxp_withdrawal_requests(gateway parts), pxp_userads` → replace money flows with
> a single MiLyfe wallet/ledger; drop ad tables entirely.

---

## 2. Groups / Pages / Events (WoWonder)

| Feature | Status | Notes |
|---|---|---|
| Groups (create, join, admins, members, group chat) | 🔴 | full group system |
| Pages (create, admins, reviews/ratings, likes, page chat) | 🔴 | `page_reviews`, `rate_page` |
| Events (create, going/interested, event feed) | 🔴 | `events`, `go-to-event`, `interest-event` |
| Forums | 🔴 | `sources/forum/` |
| Blogs / articles (+ AI blog generation) | 🟡 | `create-ai-blog.php`, `get-articles` |
| Jobs board (post jobs, open-to-work) | 🔴 | `job.php`, LinkedIn mode |

## 3. Messaging / Real-time (WoWonder + PlayHub)

| Feature | Status | Notes |
|---|---|---|
| 1:1 chat + group chat + page chat | 🟡 | |
| Message reactions, forward, pin, favorite, delete | 🔴 | `react_message`, `forward_message`, `pin_message` |
| Typing status + read receipts + archived/pinned chats | 🔴 | `set-chat-typing-status`, `read_chats` |
| Chat color customization | 🔴 | `change-chat-color` |
| Voice/video calls (Agora) | 🔴 | `agora.php`, `video_call_api` |
| Push notifications (OneSignal) | 🟡 | |
| Broadcast messages | 🔴 | `broadcast.php` |

## 4. Music Streaming (DigiMuse)

| Feature | Status | Notes |
|---|---|---|
| Track / album / artist / genre catalog | 🔴 | `object_track`, `object_album`, `object_artist` |
| Streaming player + infinite scroll | 🔴 | `class_muse_infinite` |
| Spotify / YouTube / MusicBrainz metadata ingest | 🔴 | `class_spotify`, `class_youtube_helper` |
| Lyrics (Musixmatch / AZLyrics / lyrics.ovh) | 🔴 | multiple lyric providers |
| External music sources + search suggestions | 🔴 | `endpoint_external_music`, `searchSuggs` |
| Multi-currency + multi-language | 🟡 | `change_currency`, `change_language` |

## 5. Video Platform (PlayHub — Laravel, modern)

| Feature | Status | Notes |
|---|---|---|
| Video upload + processing + upload sessions (chunked) | 🔴 | `UploadSession`, processing fields |
| Channels (about, cover, featured video) | 🔴 | `create_channel_favorites` |
| Playlists + watch-later + watch progress | 🔴 | `create_playlists`, `video_watch_progress` |
| Community posts (channel community tab) + bookmarks | 🔴 | `create_community_posts` |
| Live streaming (LiveKit) + viewers + moderation + invites | 🔴 | `create_live_streaming_tables`, `livekit/` |
| Super stickers / gifts / virtual currency | 🔴 | `create_gifts`, `create_super_stickers` |
| Subscriptions (channel + paid) | 🔴 | `Subscription` controller |
| Content import metadata + approval moderation | 🔴 | `add_approval_status_to_videos` |
| Video reports / user reports moderation | 🟡 | `create_video_reports` |
| Website ads system | 🔴 | `create_website_ads` |

## 6. Commerce / Delivery (eMart + WoWonder + PixelPhoto marketplace)

> **All money flows through the MiLyfe wallet/ledger. No external gateways. No ads.**

| Feature | Status | Notes |
|---|---|---|
| Marketplace products (create/edit, offers, orders, refunds) | 🟡 | `products.php`, `orders.php`, `refund.php` |
| Digital-goods store (sell files/licenses) | 🔴 | PixelPhoto `pxp_store` |
| Multi-service delivery (food/grocery/pharmacy/flowers) | 🔴 | eMart core |
| Store panel + driver/order tracking | 🔴 | eMart order-tracking (rebuild on Supabase realtime) |
| Cart / checkout / address book | 🟡 | `checkout`, `address` |
| **MiLyfe Wallet** (balance, ledger, internal transfers) | 🔴 | the ONLY payment rail — replaces all gateways |
| Payouts / withdrawals **within MiLyfe wallet** | 🔴 | internal ledger, no bank/gateway calls |
| Funding / crowdfunding campaigns (paid via wallet) | 🔴 | `create_funding`, `pxp_funding` |
| Pro / subscription upgrades (paid via wallet) + expiry cron | 🟡 | `go_pro`, `expire_pro` |
| Gifts / tipping (via wallet currency) | 🔴 | `gift.php` |
| Creator monetization / referrers (wallet payouts) | 🔴 | `monetization.php`, `get_referrers` |
| ~~~25 third-party payment gateways~~ | **DROP** | Stripe/PayPal/Razorpay/Paystack/Flutterwave/Coinbase/CoinPayments/Cashfree/Paysera/iyzipay/SecurionPay/YooMoney/Braintree/PayFast/aamarpay/ngenius/Fortumo/bank-transfer — **all excluded** |
| ~~Ads (AdMob, website ads, click tracking, sponsored posts)~~ | **DROP** | entire ad system **excluded** |

## 7. Learning (WPLMS)

| Feature | Status | Notes |
|---|---|---|
| Courses / lessons / quizzes / assignments | 🔴 | LMS core |
| Certificates + progress tracking | 🔴 | |
| Instructor dashboards + course marketplace | 🔴 | |

## 8. Platform / Admin (all)

| Feature | Status | Notes |
|---|---|---|
| Admin panel (users, content moderation, settings) | 🟡 | verify depth |
| Multi-language (i18n) + RTL | 🟡 | |
| Multi-currency | 🔴 | |
| Site modes (social / LinkedIn / etc.) | 🔴 | `website_mode` |
| PWA / service worker | 🟡 | |
| Cron jobs (expiry, spotify sync, cleanup) | 🟡 | |
| API v2 (mobile-app-ready, 182 endpoints) | 🔴 | biggest gap for a mobile app |
| Games (HTML5 games hub) | 🔴 | `games.php` |
| Movies / watch (VOD) | 🔴 | `get-movies`, `movies/` |
| ~~Ad management (site-wide)~~ | **DROP** | excluded by rule |
| ~~Payment-gateway admin config~~ | **DROP** | excluded; wallet config only |

---

## Biggest gaps for MiLyfe (priority candidates, $0-budget aware)
1. **Stories + Reels + short video (+ 360°)** — table-stakes social, currently missing.
   PixelPhoto shows the full action set (upload, ffmpeg processing, explore, view tracking, reactions).
2. **Groups / Pages / Events** — community backbone, missing.
3. **Rich messaging + audio/video calls** — PixelPhoto/WoWonder both ship calls (Agora);
   free path = WebRTC self-hosted signaling instead of a paid provider.
4. **Music + Video + Live streaming** — entire media pillars missing. Live = self-hosted
   (LiveKit OSS / Owncast) to stay $0.
5. **MiLyfe Wallet as the single money rail** — replaces ~25 gateways with one internal
   ledger. Crowdfunding, tipping, store payouts, pro upgrades all settle in wallet currency.
6. **Threaded comments with reply-level reactions** — PixelPhoto has like/dislike on both
   comments and replies; MiLyfe's is shallow.
7. **A real mobile-ready API layer** — PixelPhoto (~200 actions / 13 endpoint classes) and
   WoWonder (182 endpoints) show the surface a super-app needs. MiLyfe should design its own
   equivalent contract (minus PaymentEndPoint/AdsEndPoint).

## Explicitly OUT of scope (per rules)
- Every third-party payment gateway (Stripe, PayPal, Razorpay, Paystack, Flutterwave,
  Coinbase, CoinPayments, Cashfree, Paysera, iyzipay, SecurionPay, YooMoney, Braintree,
  PayFast, aamarpay, ngenius, Fortumo, bank-transfer, SMS-billing).
- Every ad system (AdMob, website ads, sponsored/paid-boost posts, ad click tracking,
  `create_ad`/`userads` tables, ad admin settings).

## Recommended next step
Turn the priority gaps into a proper Kiro **spec** (requirements → design → tasks) so we
build them cleanly on Next.js + Supabase — original code, feature-complete, wallet-only,
ad-free, and 100% ours.
