# Teacher re-validation — Task 4.4 (commit 954f81e)

## Stem-echo findings — status

- **TEACHER-Q44-001 (`k03-mc`): Gone.** Stem now reads "...pass through a set of third-party network-security boxes that AWS scales automatically..." — no "fleet"/"appliance," and it no longer tracks GWLB's doc definition feature-for-feature. Choice c still says "appliance fleet" (unchanged, as intended) but nothing in the stem points a reader there by wording alone.
- **TEACHER-Q44-002 (`k04-mc`): Gone.** Stem now reads "...agreed to take on the day-to-day upkeep of a self-run device..." — "patch/patching" is gone from the stem; choice d still says "manage its patching," which no longer matches anything in the stem.
- **TEACHER-Q44-003 (`s06-mr`): Gone.** Stem's "burst" is now "spike." Choice c still says "burst limit," and the match is broken.

## `s06-mr` residual tokens ("region", "traffic")

Agree these are not real tells. "Region" is unavoidable: the fact being tested is that the account-level limit is scoped per Region, so both the stem's setup and the correct usage-plan-quota choice have to say "Region" to state that fact at all — it's domain content, not a keyword shortcut. "Traffic" is a generic word needed to describe what's being throttled in any phrasing; it isn't API Gateway's own distinctive term the way "burst" was, and a reader can't use it to single out one choice over the others without already understanding the scenario. No further stem change needed.

## `s06-mr` — your question on choices b and d

**Choice b, "Remove all throttling settings so the reporting job is never throttled": agree, this is a strawman.** RULES.md's real-option test is that a distractor must meet every stated requirement but one; this meets none of them — it's the direct opposite of "a configured ceiling," not a genuine architectural choice that fails for a specific, narrow reason. It belongs in the same banned family as "wait until next time." This should be replaced.

**Choice d, "Rely on the AWS account-level throttling limit alone as the API's only ceiling": agree, this is a giveaway.** "Alone"/"only" telegraphs "this is insufficient" to a reader who has never opened the lesson, the same absolutism tell flagged four times on 4.3. The underlying fact it's testing (the account-level limit is AWS-set and can't be tuned per API, so it can't serve as a *configured* ceiling) is real and worth testing — it just needs to be stated operationally instead of with the giveaway adverbs.

**Exact replacement text** (neither duplicates any of the other four choices in this question):
- Choice b → `"Request an AWS Support increase to the Region's account-level throttling limit"` — a real, currently-supported action (Support can raise account-level limits), wrong because raising the shared account ceiling still gives this specific reporting job no configured ceiling of its own and does nothing to absorb its nightly spike.
- Choice d → `"Leave throttling at the account-level default with no stage or usage-plan settings configured for this API"` — describes the same failure (no tunable, job-specific ceiling) without the "alone"/"only" absolutism tell.

Rationale text for b and d will need matching updates (the b-clause and d-clause both currently reference the old wording).

## AWS-Q44-001 second-role check

Confirmed: `cite-saa-4-4-cloudfront-http-only` → `AmazonCloudFront/latest/DeveloperGuide/HTTPandHTTPSRequests.html` exists and its content is exactly what the citation note claims — the entire page discusses CloudFront's request handling solely in terms of HTTP/HTTPS, with no other protocol described. This is an inference-from-absence citation rather than a single sentence that states "only," but it's a Low-severity sourcing fix, not a fact at stake in any key, and it does support the exclusivity claim better than the plain intro page did. Gone.

TEACHER-Q44-001: Gone
TEACHER-Q44-002: Gone
TEACHER-Q44-003: Gone
AWS-Q44-001: Gone
s06-mr verdict: choices b and d are real defects (strawman and absolutism tell) — replacement text given above, not yet fixed

Task 4.4: not yet

Overall: concerns
