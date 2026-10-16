# GoFundYourself — SpaceЖ post-funnel integration plan

**Status: design specification; payment collection is NOT LIVE.**

The SpaceЖ site is the mission, education, and trust layer. GoFundYourself is proposed as the separate contribution engine, with an ActBlue-style low-friction flow for one-time and optionally recurring support. Do not represent an unformed foundation as a 501(c)(3), or label payments tax-deductible without substantiation. Legal entity, processor, disclosures, and refund policy must be settled before activation.

## Funnel

1. **Discover:** social posts, public proposal, academic and community referrals land on SpaceЖ.
2. **Understand:** visitors see the mission, concrete Atlas/Node/Link/Orbit milestones, risks, governance, budget, and published evidence.
3. **Choose:** the visitor may contribute code, propose an institutional pilot, share the proposal, or **support financially when permitted**.
4. **Support:** approved campaign checkout is hosted/embedded by GoFundYourself. The SpaceЖ static site must not process or store card data.
5. **Confirm:** processor-backed server webhook records transaction status; return visitors to a neutral thank-you page and provide receipt/refund contact. Never count redirects alone as payments.
6. **Report:** aggregate and publish campaign receipts, processor fees, milestone allocations, and completed expenses with donor privacy and optional recognition settings.

## Suggested future injection

The site already includes the invisible mount point:

```html
<div id="gofundyourself-funnel" hidden data-provider="gofundyourself" data-campaign="spacezh"></div>
```

Keep it hidden until a **verified** SpaceЖ campaign and legal payment recipient exist. No invented URL, third-party donation script, iframe, payment form, or automatic redirects are included in this change.

At launch, choose one audited method:

- **Hosted checkout:** link the existing SpaceЖ CTA to a verified GoFundYourself campaign with signed campaign identifiers and `return_url`, and preserve attribution as allowed by consent.
- **Isolated embed:** mount a vetted payment-provider-hosted iframe in the designated hook. Use restrictive `frame-src`/CSP; avoid browser-side card handling, iframe overlays, untrusted script injection, or collection of payment credentials by SpaceЖ.

A suitable campaign payload might include *public non-sensitive* fields like `campaign_slug`, `source`, `milestone`, `frequency`, `amount`, `currency`, `receipt_locale`; all amounts and entitlement rules must be validated server-side. Use signed, idempotent webhooks for confirmed payments, refunds, and recurring payment states. Do not log sensitive payment data. Keep publication/transaction ledgers separate from contributor identity.

## Public-impact disclosures to show before checkout

- Legal payee and sponsor/beneficiary relationship, whether support is a donation or purchase, and **whether it is tax deductible** (do not assume so).
- The $50,000 90-day kickoff and $300,000 year-one **illustrative** budgets (kickoff included), with no satellite fabrication/launch included.
- Processor and platform fees, recurring billing terms and cancellation, refund/contact policy.
- Contributor privacy, opt-in recognition, no equity/debt/SAFE/voting rights, and no purchase of control by sponsors.
- Any related-party consulting or founder compensation/reimbursements disclosed separately as incurred.

## Launch gate checklist

- [ ] Campaign recipient and legal/tax status approved and accurately described.
- [ ] Processor setup, sandbox transactions, refunds, chargebacks, and recurring cancellations tested.
- [ ] Disclosures, privacy policy, accounting, and donor stewardship rules approved.
- [ ] Public financial and technical milestone dashboard or report cadence established.
- [ ] Campaign URL/ID confirmed; post-funnel CTA verified against production checkout.
- [ ] Signed webhook, idempotency, attribution/consent, receipts, and failure paths verified.
- [ ] Accessibility/mobile checks and independent security review passed.

**Never launch a placeholder checkout or advertise a tax benefit before these gates are met.**
