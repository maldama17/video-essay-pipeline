#!/usr/bin/env python3
"""
bet-ev.py — EV "wiggle" sandbox for binary prediction-market contracts (Kalshi/Polymarket style,
$1 settlement). Given YOUR honest probability estimate and the market, it shows how EV moves
across order type (market vs limit), fill price, your estimate range, and stake (Kelly) sizing.

Core identity for a $1-settling binary contract bought at price p (as a probability, 0-1):
    EV per $1 staked   = prob / p - 1
    break-even prob    = p
    full-Kelly fraction = (prob - p) / (1 - p)

A MARKET order pays the current ask (worst price -> lowest EV).
A LIMIT order rests at a better price (higher EV) but may not fill.

Usage:
    python3 bet-ev.py --label "Mexico to advance" --price 41 --est 47
    python3 bet-ev.py --label "Mexico advance" --price 41 --est-low 44 --est-high 50 --limits 40 39 38
    python3 bet-ev.py --label "..." --price 41 --est 47 --fee 1 --bankroll 1000 --kelly 0.5

All prices/estimates are in CENTS / PERCENT (integers or decimals), e.g. 41 = 41c = 41%.
"""
import argparse


def pct(x):
    return f"{x*100:5.1f}%"


def compute(prob, price_eff):
    """EV per $1 staked, break-even, full-Kelly fraction for a $1-settle binary at price_eff."""
    ev = prob / price_eff - 1.0
    be = price_eff
    kelly = (prob - price_eff) / (1.0 - price_eff) if price_eff < 1.0 else 0.0
    return ev, be, kelly


def main():
    ap = argparse.ArgumentParser(description="EV wiggle sandbox for binary prediction-market bets.")
    ap.add_argument("--label", default="bet", help="Name of the bet/market")
    ap.add_argument("--price", type=float, required=True, help="Current market ask in cents (the market-order fill price)")
    ap.add_argument("--est", type=float, help="Your honest probability midpoint in percent")
    ap.add_argument("--est-low", type=float, help="Low end of your estimate range (percent)")
    ap.add_argument("--est-high", type=float, help="High end of your estimate range (percent)")
    ap.add_argument("--limits", type=float, nargs="*", default=[], help="Candidate limit-order fill prices in cents")
    ap.add_argument("--fee", type=float, default=0.0, help="Per-contract fee in cents, added to cost basis (approx)")
    ap.add_argument("--bankroll", type=float, default=0.0, help="Bankroll for Kelly stake sizing (optional)")
    ap.add_argument("--kelly", type=float, default=0.5, help="Kelly fraction to apply (default 0.5 = half-Kelly)")
    args = ap.parse_args()

    # Resolve estimate range
    if args.est is not None:
        mid = args.est
        lo = args.est_low if args.est_low is not None else args.est
        hi = args.est_high if args.est_high is not None else args.est
    elif args.est_low is not None and args.est_high is not None:
        lo, hi = args.est_low, args.est_high
        mid = (lo + hi) / 2.0
    else:
        ap.error("Provide --est, or both --est-low and --est-high.")

    lo, hi, mid = lo / 100.0, hi / 100.0, mid / 100.0
    market = args.price / 100.0
    fee = args.fee / 100.0
    fills = [("MARKET (take ask)", market)] + [(f"LIMIT @ {l:.0f}c", l / 100.0) for l in args.limits]

    print(f"\n=== EV WIGGLE: {args.label} ===")
    print(f"Market ask: {args.price:.0f}c (implied {pct(market)})   "
          f"Your estimate: {pct(lo)}-{pct(hi)} (mid {pct(mid)})"
          + (f"   fee {args.fee:.1f}c" if fee else ""))
    print(f"Edge at mid vs market: {(mid - market)*100:+.1f} pts\n")

    header = f"{'Fill scenario':<20} {'BE':>6} {'EV@low':>8} {'EV@mid':>8} {'EV@high':>9} {'Kelly(mid)':>11}"
    print(header)
    print("-" * len(header))
    best = None
    for name, p in fills:
        p_eff = p + fee
        ev_lo, be, _ = compute(lo, p_eff)
        ev_mid, _, kel = compute(mid, p_eff)
        ev_hi, _, _ = compute(hi, p_eff)
        kel_f = max(0.0, kel) * args.kelly
        print(f"{name:<20} {be*100:5.0f}% {ev_lo*100:+7.1f}% {ev_mid*100:+7.1f}% {ev_hi*100:+8.1f}% {kel_f*100:9.1f}%")
        if best is None or ev_mid > best[1]:
            best = (name, ev_mid, p_eff, kel_f)

    print()
    # Verdict on the best (highest-EV) fill scenario, judged on the LOW end of the range
    name, ev_mid, p_eff, kel_f = best
    ev_lo_best, be_best, _ = compute(lo, p_eff)
    if ev_lo_best > 0.03:
        verdict = "BET — low end of range still clears with room"
    elif ev_mid > 0.0 and ev_lo_best <= 0.03:
        verdict = "SMALL BET — only midpoint clears; thin edge"
    else:
        verdict = "PASS — no reliable edge once you're honest about the range"

    print(f"BEST FILL : {name}  (break-even {be_best*100:.0f}%)")
    print(f"EV        : {ev_lo_best*100:+.1f}% (low)  {ev_mid*100:+.1f}% (mid)")
    print(f"STAKE     : {args.kelly:.2f}-Kelly = {kel_f*100:.1f}% of bankroll"
          + (f"  = ${kel_f*args.bankroll:,.0f}" if args.bankroll else ""))
    print(f"VERDICT   : {verdict}")
    print("\nNote: a MARKET order is the worst row here; patience on a LIMIT is itself an EV lever.\n")


if __name__ == "__main__":
    main()
