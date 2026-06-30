# Prediction-Market Bet Analysis

A repeatable rubric for turning facts about a match into an honest probability **range**, then into a bet/pass decision. Built around one core idea:

> **You only make money when YOUR honest probability estimate is meaningfully higher than the price. The team you like is irrelevant. Only the gap between your number and the market's number matters.**

Most of the time the honest answer is **pass**, and that is a success, not a failure.

## Activation

Use this skill when the user wants to:
- Evaluate a specific sports / prediction-market bet (Kalshi, Polymarket, sportsbook moneyline, totals, cards, "to advance", etc.)
- Turn a game/event preview or a per-game breakdown into bet/pass decisions
- Pressure-test a betting "edge" against the market price
- Convert a transcript analysis (e.g. a `sports-betting` domain breakdown) into actual probability estimates

It pairs naturally with the `sports-betting` domain: run a `/fetch` breakdown first, then run this rubric per game.

Work through the steps **in order**. Do not skip the ⚠️ flags — they are the whole point.

---

## Step 0 — Name the exact bet

- **Which market am I actually betting?** "To advance" (includes extra time + penalties) is a *different* market and price than "to win in 90 minutes" (moneyline). Never mix them. Pull the price for the *exact* market you'll place.
- **What is the real current price?** Use the live price for that specific market, in cents (e.g. 41¢ = 41% implied). Not yesterday's, not the moneyline, not a sportsbook's different line.
- **Write down the price now.** This is the number you must beat.

⚠️ **Flag:** The single most common error is feeding the wrong price into your math — using the cheaper moneyline number when you're actually betting the advance market. Double-check you have the right market's price.

---

## Step 1 — Establish the baseline (start from the market, not from zero)

The market price already aggregates thousands of informed bettors and most public information. Treat it as the **default correct answer** until you find a specific, concrete reason it's wrong.

- Write the market's implied probability as your starting estimate.
- Your job is NOT to build a probability from scratch. It's to decide whether to nudge the market's number **up or down**, and by how much, based on something the market may be underweighting.

⚠️ **Flag — the biggest trap of all:** If your reasoning just re-states things everyone already knows ("Senegal has good attackers"), the market has already priced that. Restating public narrative is NOT an edge — it's an echo of the price. An edge requires something the market is plausibly *missing or underweighting*.

---

## Step 2 — Gather online research & sentiment (NEW)

Before listing your own facts, pull in current external information. Use `WebSearch` (and `WebFetch` for specific pages) to gather, for this exact fixture and market:

1. **Hard news / availability** — confirmed injuries, suspensions, "ruled out for tournament", predicted/confirmed lineups, keeper status, manager quotes. Search e.g. `"<team A> vs <team B> team news"`, `"<key player> injury"`, `"<team> predicted lineup"`.
2. **Market & line movement** — has the price/line moved, and which way? Opening vs current. Search the specific market on the relevant book/exchange (Kalshi, Polymarket, etc.). Movement toward your side that *isn't* explained by public news can hint at sharp money; movement you can fully explain by news is already priced.
3. **Public vs sharp sentiment** — what % of public bets/tickets are on each side, consensus picks, and where "sharps" are reportedly leaning. Search e.g. `"<matchup> betting splits"`, `"<matchup> sharp money"`, `"<matchup> consensus pick"`.
4. **Contextual factors** — venue/altitude/crowd, weather, travel/rest days, referee assignment and card tendencies, motivation/dead-rubber situations.

For each item gathered, **tag its reliability** (see Step 3 table) and **timestamp it** (how fresh is this?). Capture the *source* so it can be re-checked.

⚠️ **Flag — sentiment ≠ edge.** Heavy public money on one side is a *crowd* signal, not automatically a fade signal. And an online analyst (or AI) sounding confident is still a fallible input downstream of the same public info the price already reflects. Use sentiment to find what's *underweighted*, not to follow the crowd or to defer to a pundit.

⚠️ **Flag — staleness kills edges.** Injury/lineup info goes stale fast. A "five players out" story from two days ago may be false by kickoff. **Re-verify any injury/lineup fact within a few hours of the game.**

---

## Step 3 — Tag each fact's reliability

For each relevant fact (yours + the ones gathered in Step 2), write it down AND tag how much you trust it:

| Reliability | Examples | How to treat it |
|---|---|---|
| **High** (verifiable, settled) | Final scores, confirmed results, a player ruled out for the tournament | Use with confidence |
| **Medium** (interpretation) | "Creates chances but can't finish", xG-vs-goals reads, form narratives | Use, but discount — opinions dressed as facts |
| **Low** (unconfirmed / time-sensitive) | Predicted lineups, "doubtful" injuries, sentiment drift, anything not yet locked | Provisional; re-check near kickoff |

⚠️ **Flag:** If your whole edge rests on one low-reliability fact, you don't have a reliable edge.

---

## Step 4 — Sort facts into "pulls up" vs "pulls down"

Make two columns for the team you're considering backing.

**Pulls the probability UP** (better than the price implies) — **Pulls the probability DOWN** (worse than the price implies)

Weight these *more* heavily:
- **Individual quality / top-end talent** — single moments from elite players decide tight knockout games.
- **Defensive reliability** — "can't defend" is more decisive than "can attack" in knockouts.
- **Confirmed availability of key players** (keeper, main creator, main scorer).
- **Game-state logic** — who is forced to chase, who can sit deep, who altitude/crowd favors.

Weight these *less* heavily (seductive but weak):
- **Recent blowout scorelines** (check the opponent — a 5-0 vs 10 men means little).
- **"Momentum" / "form"** without underlying numbers.
- **One-game upsets** ("they beat a big team once") — usually already priced, high-variance.
- **xG over-/under-performance** as destiny — it regresses, but slowly and noisily.

⚠️ **Flag — possession ≠ goals.** Dominating the ball without scoring can mean the opponent's defensive plan is working. Don't convert "controls the game" into "will win".

---

## Step 5 — Make your honest estimate (as a RANGE)

Start from the market number (Step 1) and adjust:

- "Pulls up" heavier AND rests on something the market plausibly underweights → nudge **above** market.
- "Pulls down" heavier → nudge **below**.
- Roughly cancel, or everything is already public → **leave it at market price** (the most common honest outcome).

Be conservative. A 3–5 point move is a strong opinion. A 10+ point move means you think the entire market got it badly wrong — that should be **rare** and backed by a high-reliability fact, not a narrative.

Express your estimate as a **low–high range** that reflects your uncertainty (e.g. 42–48%), with a **point/midpoint** for the EV math. A wide range = more uncertainty = smaller stake (or pass).

⚠️ **Flag — motivated reasoning.** If you slide your estimate up *specifically so the bet clears*, stop. Form the estimate first, *then* check the price. If you only get a "bet" using the top of your range, you don't have a real edge.

---

## Step 6 — The one-sentence justification test

Write a single sentence stating your estimate and *why it beats the market*, not depending on any one fragile fact or on someone else being right.

- ✅ *"I estimate Team X at 44–48% because their elite keeper is back AND the opponent's only creator is confirmed out — two confirmed availability facts the price hasn't fully absorbed."*
- ❌ *"I think Team X is 46% because I like them and they beat a big team once."* (narrative, already priced)
- ❌ *"Because the analyst I read said so."* (deferring to a fallible source downstream of the price)

If you can't write the passing version honestly, **pass the bet.**

---

## Step 7 — Run the EV math

Using the **real market price** (Step 0) and your **honest estimate** (Step 5, run it at the low end AND the midpoint):

```
profit_if_win   = payout_if_win − stake
EV              = (your_prob × profit_if_win) − ((1 − your_prob) × stake)
break_even_prob = stake ÷ payout_if_win
```

Decision:
- **Even the LOW end of your range clears break-even with room** → strong bettable edge.
- **Midpoint clears but low end doesn't** → thin edge → small stake at most.
- **Estimate around break-even** → no real edge → **pass**.
- **Below break-even** → **pass**, even if you like the team.

⚠️ **Flag — break-even is the hinge, not the market price.** A bet you "beat" slightly can still sit below break-even once spread/fee is included.

---

## Step 8 — Size the bet to the edge (only if it's a bet)

- Bigger, more confident (narrower-range) edge → larger stake. Thin/wide edge → small stake or pass.
- Never bet an amount whose loss would tempt a "get it back" bet.
- Treat money in the account as **real money**, not "house money." A $250 stake risks $250 regardless of your day's P&L.

⚠️ **Flag — concentration.** A side-market (totals, BTTS, corners) on a game you already hold is NOT diversification — it doubles exposure to the same 90 minutes.

---

## Step 9 — Live management (if you hold into the game)

- **Your team scores / leads:** price jumps — a sell window. Trim a *partial* slice to bank profit; late-game leads sell richer than fragile early ones.
- **Opponent scores:** don't panic-sell on a *single* knockout goal — comeback/extra-time path is live. Cut only if clearly lost (two down late).
- **Still level late:** in an "advance" bet, a draw heading to ET/penalties may *favor* you.
- **Never "buy more" to average down** a loser to "make it back" — the most expensive instinct in the game.

⚠️ **Flag — you cannot out-thumb a goal.** Prices reprice in milliseconds. Decide trims on the *current* state, not in hope of reacting faster than the market.

---

## Step 10 — Honesty checklist (every single time)

- [ ] Using the price of the **exact market** I'm betting (advance vs moneyline).
- [ ] My estimate was formed **before** I checked whether the bet clears.
- [ ] My edge rests on something the market plausibly **underweights**, not public narrative or pure sentiment.
- [ ] I **re-verified** any time-sensitive fact (injuries, lineups) close to kickoff.
- [ ] Even the **low end** of my range clears break-even with room.
- [ ] I can write the **one-sentence justification** honestly.
- [ ] The stake is money I'm fine losing, treated as real money.
- [ ] I'm not betting just because games are happening / I want action.

If any box is unchecked → **pass, or shrink to entertainment size.**

---

## Final output — print the probability estimate range

End every run with a compact verdict block, one per bet evaluated:

```
MATCH:        <Team A> vs <Team B> — <competition / round>
MARKET:       <exact market, e.g. "Team A to advance">
MARKET PRICE: <price>¢  (implied <X>%)
MY ESTIMATE:  <low>%–<high>%   (midpoint <mid>%)
BREAK-EVEN:   <be>%
EDGE:         <midpoint − break-even, in points>   (low-end edge: <low − be>)
DECISION:     BET (<stake size>) | SMALL BET | PASS
ONE-LINE WHY: <the Step 6 sentence>
KEY RISK:     <the single most likely way this is wrong>
```

If multiple games were analyzed, print one block per game, then a one-line portfolio note on total exposure and correlation.

---

## Meta-truths to keep in front of you

1. **The market is usually right.** Most games have no edge. Passing is the default correct move.
2. **Edges are rare and smaller than they feel.** Even a genuine-looking injury angle can be stale.
3. **Confidence is not accuracy.** A confident source (including an AI, including yourself) is still fallible and downstream of the same public info. Hold every estimate loosely.
4. **Resulting is a trap.** Judge *decision quality* (was EV positive on an honest estimate?), not the outcome.
5. **Discipline compounds; action erodes.** Taking profit, sizing to edge, and passing on coin flips is what keeps a good run from being given back.
