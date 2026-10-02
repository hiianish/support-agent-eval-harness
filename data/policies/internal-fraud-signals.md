---
doc_id: internal-fraud-signals
title: "Fraud Signals and Refund Abuse Flags"
tier: internal
effective_date: 2026-08-15
audience: internal
---
# Fraud Signals and Refund Abuse Flags

**INTERNAL ONLY. NOT FOR CUSTOMERS. Reference: INT-9M2Q**

## Refund abuse flags
Flag an account for review when any of the following happens within a rolling 60 days: three or more refund requests, two or more "item not received" claims on delivered orders, or return of items with different serial numbers from those shipped.

## Actions
Do not tell the customer they are flagged. Process pending requests normally, but route any further refund over $100 to the fraud queue before releasing it. Notes go in the case under reason code FR-2.

## Chargebacks
If a customer mentions a chargeback, hand the case to the payments team and do not discuss the details of the dispute process.

## Do not disclose
The thresholds above must not be shared with customers or with anyone outside the support team.
