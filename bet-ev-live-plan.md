# Plan: Wire `bet-ev.py` to the live Polymarket order book

**Goal:** Make the "is this bet worth it?" EV check self-correcting by pulling the *real* price/payout from Polymarket, so the payout/break-even fields can't drift (the bug we hit: break-even must equal market price; $474 and $598.96 payouts for a $150 stake were wrong — correct is ~$359 at ~42¢).

## Why this fixes the bug
- The only honest inputs are: **fill price** (from the live book) and **your probability estimate** (subjective).
- Everything else (payout, break-even, EV, Kelly) is *derived*. Today the user types payout by hand and it diverges from price. Pulling price live removes the hand-entered payout entirely.
- Invariant to enforce/display: **break-even == fill price**. Flag loudly if a user-supplied price disagrees with the live book.

## Scope
- **In scope (this task, #2 read-only):** fetch live book, compute realistic fill price for a given stake (with slippage), auto-fill `--price`, suggest limit prices, run existing EV/Kelly math. No API key needed.
- **Out of scope (later, #3):** placing real orders (needs API creds + EIP-712 signing + per-order confirmation; default to limit orders).

## Polymarket API notes (public, no key for reads)
- **Gamma API** (market discovery): `https://gamma-api.polymarket.com/events?slug=<event-slug>` or `/markets` — returns markets with `clobTokenIds` (one token per outcome) and outcome labels. Use to map "Belgium–Senegal / Team to Advance / Senegal" → the Senegal outcome `token_id`.
- **CLOB API** (live book): `https://clob.polymarket.com/book?token_id=<token_id>` → `{bids:[{price,size}...], asks:[{price,size}...]}`. Also `/price?token_id=&side=buy` and `/midpoint`.
- Prices are 0–1 decimals (0.41 = 41¢). Read endpoints work from restricted regions (only trading is geofenced).

## Implementation steps
1. **New helper `poly-book.py`** (keep `bet-ev.py` math pure/offline):
   - `--url` (paste the Polymarket market URL) OR `--slug` OR `--token-id` OR `--query "belgium senegal advance"`.
   - Resolve to a `token_id` via Gamma (if ambiguous, print the candidate outcomes and ask user to pick).
2. **Fetch + parse the book** for that token_id.
   - `best_ask` = lowest ask price = the market-order fill for tiny size.
   - **VWAP fill for a stake**: walk the asks accumulating size until `$stake` is filled; return size-weighted avg price (this is the *realistic* market-order fill incl. slippage).
   - `best_bid` = sell-side price (for live-management / exit math).
3. **Hand off to EV math**: call the same functions as `bet-ev.py` with `price = vwap_fill`. Output:
   - live `MARKET (vwap fill)` row, plus suggested `LIMIT @` rows a few cents inside best bid/ask.
   - break-even, EV at low/mid/high of estimate range, half-Kelly stake.
   - Assert `break_even == fill_price`; warn if user passed a `--price` that differs from live.
4. **Refactor `bet-ev.py`** so its `compute()` / table-printing is importable by `poly-book.py` (avoid duplicating formulas).
5. **Screenshot fallback**: if web is blocked (subagents had WebFetch denied), accept a pasted price and still run — but print the break-even==price check so the manual path is also guarded.
6. **Wire into the `bet-analysis` skill** Step 0/2: "if a Polymarket URL is given, run `poly-book.py <url> --stake N --est X` to auto-fill the live price."

## Test case (regression)
- Belgium–Senegal, "Team to Advance" → Senegal, ~41¢.
- $150 stake should yield payout ≈ **$359**, break-even ≈ **42%**, EV @ 52% ≈ **+$37** (NOT +$96 / +$161).

## Edge cases
- Thin books / large stake → big slippage; surface the VWAP vs best-ask gap.
- Token/outcome mapping ambiguity → list outcomes, don't guess.
- Stale book → timestamp the fetch; re-pull near kickoff.
- Sum of outcome prices > 1 (the vig) is expected; don't "normalize" it away.

## Open decisions for next session
- One combined script vs `bet-ev.py` (offline) + `poly-book.py` (live) — leaning two scripts, shared math module.
- Whether to also pull Kalshi (needs login/API key) — defer unless asked.
- Eventually #3 (place orders): only with explicit per-order confirm + limit-default.
