# State divergence enables unauthorized access: Provenance marker module anyone-can-pass check

## Summary

Trail of Bits researchers **Paweł Płatek** and **Denys Pakizh** published an August 25, 2026 writeup of a smart-contract access-control bug they found in **Provenance Blockchain** (a public proof-of-stake chain built on **Cosmos SDK**) and reported on April 1, 2026. The bug lived in the **marker module** — Provenance's core primitive for fungible tokens, where each marker is a special account holding a denomination, an access control list, a stored **supply** field, and an escrow balance.

The `AddAccess` message handler authorizes ACL modifications when **any one** of three conditions holds: the caller is the manager on a Finalized marker, the caller holds `ACCESS_ADMIN`, or the caller "controls 100% of the marker's circulating supply." Condition 3 was implemented by `accountControlsAllSupply`, which compared the caller's balance against `m.GetSupply()` — the **stored** supply field on the marker struct. For **non-fixed-supply markers activated with zero supply**, that field is always zero (the live circulating count lives in the bank module and is never written back), so the check reduced to `0 == 0` and passed for **any caller with zero balance** — no tokens needed. The exploit was two transactions: one `MsgAddAccessRequest` granting the attacker `ACCESS_ADMIN`/`ACCESS_MINT`/`ACCESS_WITHDRAW`, then a `MsgMintRequest` (arbitrary inflation) or `MsgWithdrawRequest` (drain the marker's escrow).

At discovery, **82 live markers with real circulating supply or escrowed assets on mainnet** were exploitable, spanning multiple independent parties. The largest exposure was escrow: ~30 × 10¹⁵ nhash (~$500,000 at the time), concentrated in three Provenance Foundation governance markers (grant0051 ~19.2 × 10¹⁵, provenance.validator.incentive.program ~8.6 × 10¹⁵, grant0077 ~2.5 × 10¹⁵). The remaining 74 affected markers spanned bridged stablecoins and wrapped assets, consortium deposits, tokenized mortgage participations, and yield tokens — for which `ACCESS_MINT` meant arbitrary supply inflation or, for restricted KYC tokens, a solvency/integrity threat. The bug affected versions before 1.28.0: **PR #2627** (commit c81fd65, shipped in v1.28.0 on May 1, 2026) added a guard failing the check on zero supply — a mitigation that blocked the reported attack but left the stale field in place; **PR #2734** (v1.29.0, June 8, 2026) made the one-line fix, reading live supply from the bank module (`k.bankKeeper.GetSupply`) on both sides of the comparison.

## Tags
- patterns
- blockchain
- smart contract
- Cosmos SDK
- access control
- authorization
- state divergence
- state desynchronization
- stale state
- Provenance
- marker
- mint
- escrow
- financial
- Trail of Bits
- Paweł Płatek
- Denys Pakizh
- bug bounty
- supply chain
- zero-balance
- fail-closed

## Why this matters
- **Authorization must fail from the default state**: the check compared two representations of the same quantity from two different sources (stored marker struct vs. bank module) and silently trusted the stale one; when both sides read zero, the "100% of supply" gate became open to the entire chain.
- **Denormalized state is a security primitive**: any design that mirrors a live value (supply, balances, counters) into a struct for convenience must treat the mirror as untrusted input; a write-back gap turns a read into an authz decision.
- **Zero-default states are the most dangerous defaults**: the exploit required nothing — no tokens, no ownership, no privileged state — because the vulnerable branch fired exactly at the default/empty state of non-fixed markers.
- **Mitigations that only close the observed case are not fixes**: PR #2627's zero-guard passed the audit's reported attack but still passed whenever the stale field was non-zero and a caller's balance matched it; the durable fix was changing the data source, not adding a guard.
- **Two-transaction exploit shape is cheap to hunt for**: an ACL self-grant followed by mint/withdraw within a short window on a token account, where the caller held no tokens before the grant, is a near-unambiguous anomaly in ledger/transaction analytics.
- **Exposure was governance-concentrated**: the largest sums sat in foundation grant and validator-incentive markers, so a single self-grant would have hit public trust and solvency, not just a single user.

## Related pages
- [AI agent memory poisoning](ai-agent-memory-poisoning.md) — another "stale persisted state drives later decisions" pattern, from the agent-memory side
- [Crypto supply-chain transaction authority](crypto-supply-chain-transaction-authority.md) — token/mint authority abuse patterns in crypto ecosystems

## Sources
- Trail of Bits, "State divergence enables unauthorized access" (Paweł Płatek, Denys Pakizh, August 25, 2026): [https://blog.trailofbits.com/2026/08/25/state-divergence-enables-unauthorized-access/](https://blog.trailofbits.com/2026/08/25/state-divergence-enables-unauthorized-access/)
- Provenance mitigation PR #2627 (v1.28.0, May 1, 2026) and full fix PR #2734 (v1.29.0, June 8, 2026)
