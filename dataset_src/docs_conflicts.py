"""Contradiction docs (C*) and near-duplicate docs (N*)."""
from docs_core import D
from docs_pairs import eff_text

CONFLICTS = []

# ---- Resolvable by the Terms of Sale order of precedence (higher level wins) ----
CONFLICTS.append(D("faq-gift-cards", "FAQ: Gift Cards", "faq", "2026-03-10", """
## Can I use a gift card for any purchase?
Yes. A Brightwell Market gift card can be used on any item sold on our site, except on the purchase of another gift card.

## Do gift cards expire?
No. Our gift cards never expire.

## Can I get a refund on a gift card?
Yes. If you bought a gift card by mistake and it has not been used, you can ask for a refund within 30 days of purchase. Contact support with the order number and we will return the money to your original payment method.

## Can I buy a gift card for someone in Canada?
Yes. Gift cards are issued in the currency of the store where they are bought, so a card bought on the US store is in US dollars and a card bought on the Canadian store is in Canadian dollars.

## What if the recipient did not get the email?
Check the spam folder first. Support can resend the email to the original address once we confirm your order number.

## Can I combine gift cards?
You can use up to two gift cards on a single order, together with one other payment method.
""", trap="C1"))

CONFLICTS.append(D("help-international-returns", "Help: Returning Items From Canada", "help", "2026-03-15", """
This article explains how to return an order that was delivered to a Canadian address.

## Return window
Canadian orders follow the same return window as US orders. The window is counted from the delivery date shown in the carrier's final scan.

## Starting the return
Open Account > Orders, select the item and choose Start a return. A prepaid label for Canada Post is emailed to you. Please include the return authorization number inside the parcel.

## Who pays for return shipping
We cover the cost of return shipping on all Canadian returns, so there is no return shipping fee for customers in Canada, whatever the reason for the return.

## Customs forms
The label email includes a customs declaration. Print it and attach it to the outside of the parcel so it clears customs smoothly.

## Refunds in Canadian dollars
Refunds are issued in Canadian dollars, using the amount you were charged. We do not recalculate the amount using a new exchange rate.

## Track your return
Return parcels can be tracked with the number on the label. When the warehouse scans the package, the order status changes to Returned and you receive an email.
""", trap="C2"))

CONFLICTS.append(D("promo-holiday-shipping", "Holiday Offer: Free Shipping", "promo", "2026-09-15", """
## Brightwell Holiday Shipping Offer
Get ready for the season! From September 15 through December 31, 2026, enjoy **free standard shipping on all US orders over $25.** No code needed, and the offer is applied automatically at checkout.

## Order early
Our fulfilment centres are busiest between mid-November and the end of December. Order early to make sure your gifts arrive in time. Standard shipping to US addresses is estimated at 3 to 5 business days, but carriers may be slower in peak weeks.

## Gift ideas
Explore our curated gift pages for outdoor adventurers, home cooks, commuters and anyone who loves a good power bank. Every page lists the final sale status of each product.

## Cut-off dates
We will publish last-order dates for standard, two-day and overnight shipping in early December.

## Good to know
Gift cards do not count towards the free shipping amount. The offer cannot be combined with other free-shipping promotions.
""", trap="C3"))

# ---- Unresolvable: same level, same effective date ----
CONFLICTS.append(D("warranty-claims-process", "Warranty Claims Process", "policy", "2026-02-01", """
## Who can make a claim
Any customer whose order includes a product covered by a Brightwell Market warranty can make a claim. The product must still be within its warranty period.

## Deadline for reporting a defect
You must report a suspected defect within **30 days of discovering it**. Reports made later than that cannot be accepted, even if the product is still within its warranty period.

## What to send
Email support or tell the AI assistant your order number, the product name, when you first noticed the fault, and a photo or short video showing it. We may ask a few follow-up questions.

## Our decision
A specialist reviews each claim within 3 business days. We email you the outcome. If the claim is accepted, we send a replacement or refund the product, whichever applies under the warranty terms.

## Returning the faulty product
We may ask you to send the faulty product back using a prepaid label. We will not ask you to pay for this shipping.

## Appeals
If your claim is declined and you disagree, reply to the decision email and a second specialist will look at it again.
""", trap="C4"))

CONFLICTS.append(D("defect-reporting-guide", "Guide: Reporting a Defective Product", "policy", "2026-02-01", """
## Why report a defect
Telling us about a faulty product lets us replace it, refund it, and flag problems to the supplier.

## Time limit
Please report a defect within **60 days of discovering it**. If you are past that point, the claim cannot be processed, whether or not the warranty period is still running.

## How to report
Use Account > Orders > Report a problem, or contact support. Include your order number and a clear description of what is wrong. Photos help us decide faster.

## Safety issues
If a product overheats, smokes, or could cause injury, stop using it straight away and tell us at once. We treat safety reports as urgent and handle them ahead of other claims.

## What happens next
You will receive a confirmation email with a case number. A specialist reviews the case within 3 business days and contacts you with the result.

## Products from other brands
For products made by other brands that we resell, the manufacturer's own warranty may also apply. We are happy to share the manufacturer's contact details when you report the problem.
""", trap="C4"))

CONFLICTS.append(D("faq-po-box-shipping", "FAQ: Shipping to PO Boxes", "faq", "2026-03-10", """
## Do you ship to PO boxes?
Yes. We can ship standard-shipping orders to PO boxes in the United States using USPS. Choose USPS delivery at checkout and enter the PO box in the address line.

## Is there an extra charge?
No. PO box deliveries cost the same as other standard shipping orders.

## Can I use expedited shipping with a PO box?
No. Two-day and overnight shipping are not available for PO boxes, because those services use carriers that do not deliver to them.

## What about Canada?
Canada Post delivers to postal boxes in Canada, and we can ship standard orders to them in the same way.

## Will tracking work?
USPS tracking works for PO box deliveries. You will see the package as delivered when it reaches the post office.

## Can I change an address to a PO box later?
Only while the order is in Placed or Processing status. After the order ships, the address cannot be changed.
""", trap="C5"))

CONFLICTS.append(D("faq-shipping-addresses", "FAQ: Delivery Addresses", "faq", "2026-03-10", """
## What kinds of address can I ship to?
We deliver to street addresses in the United States and Canada, including homes, apartments, workplaces and mail rooms. Please include any apartment or unit number.

## Can you deliver to a PO box?
No. We cannot deliver to PO boxes. Our carriers need a street address with someone able to receive the package, so orders to PO boxes will be cancelled and refunded.

## Can I ship to a hotel or a friend?
Yes. You can ship to any street address. Make sure the recipient name matches the name on the package so the carrier can hand it over.

## Can I ship to a freight forwarder?
We do not offer international forwarding. Orders must be delivered to an address in the United States or Canada.

## What if my address is not recognised?
Check for typing mistakes and use the suggestion shown at checkout. If the problem continues, contact support and we will help you place the order.

## Can I add delivery instructions?
Yes. Add them at checkout, or before the order ships through Account > Orders.
""", trap="C5"))

CONFLICTS.append(D("damaged-items-policy", "Damaged Items Policy", "policy", "2026-03-01", """
## What counts as damaged
An item is damaged if it arrives broken, cracked, torn, leaking, or otherwise unusable because of how it was packed or shipped.

## Reporting deadline
You must report damage within **7 days of delivery**. Reports made after 7 days cannot be accepted under this policy.

## What to send us
Tell support or the AI assistant your order number and which items are damaged. Please attach clear photos of the item and of the outer packaging, which helps us claim against the carrier.

## What we do
We offer a free replacement or a full refund, whichever you prefer, as long as the replacement is in stock. You do not pay for return shipping on damaged items, and we may ask you to keep the packaging until the carrier's claim is finished.

## Items damaged after delivery
Damage caused after the package has been delivered, for example by drops, spills or normal use, is not covered by this policy. Defects in how a product was made are covered by our warranty policies.

## Multiple items
If several items in one order are damaged, report them together to speed things up.
""", trap="C6"))

CONFLICTS.append(D("delivery-issues-policy", "Delivery Issues Policy", "policy", "2026-03-01", """
## Types of delivery issue
This policy covers packages that arrive with missing contents, packages that arrive visibly damaged, and orders marked as delivered that were not received.

## Reporting deadline
Report any delivery issue within **14 days of delivery**. After 14 days, we cannot investigate a claim for missing or damaged contents.

## How to report
Contact support or the AI assistant with your order number. Describe what is missing or damaged. Photos of the item and the packaging are helpful, and an unopened outer box should be kept until the case is closed.

## What we do
For missing contents, we send the missing items at no cost, or refund them if they are out of stock. For damaged items, we offer a free replacement or a refund. For packages that were not received, we start a carrier trace, as described in the lost packages guidance.

## Split orders
If an order was split into several packages, report each package separately with its own tracking number.

## Fraud checks
To protect customers, we may ask for extra confirmation before replacing a high-value order.
""", trap="C6"))

# ---------------- Near-duplicates ----------------
NEARDUPS = []

def nd(id_a, id_b, title_a, title_b, tmpl, va, vb, eff, trap, tier="policy"):
    for id_, title, vals in ((id_a, title_a, va), (id_b, title_b, vb)):
        NEARDUPS.append(D(id_, title, tier, eff, tmpl.format(eff=eff_text(eff), **vals), trap=trap))

RET_CAT = """
**Effective {eff}.** This page gives the extra rules that apply when you return {cat}. The general returns policy still applies for everything not mentioned here.

## Return window
You may return {cat} within 30 days of delivery.

## Condition
{cond}

## Packaging
{pack}

## Return shipping
A return shipping fee of $6.95 is deducted from your refund unless the item is defective, damaged or the wrong item, in which case the label is free.

## Inspection
Our warehouse inspects every return. {inspect}

## Refunds and exchanges
Approved returns are refunded to the original payment method under the refunds policy. {cat_cap} can also be exchanged for a different size within the same 30-day window.

## Final sale
Items marked Final Sale at the time of purchase cannot be returned.
"""
nd("returns-apparel", "returns-footwear", "Returns: Apparel", "Returns: Footwear", RET_CAT,
   dict(cat="apparel", cat_cap="Apparel", cond="Garments must be unworn and unwashed, with all tags attached and any hygiene liner or sticker intact.",
        pack="Pack the garment in the bag or box it arrived in, or in any clean bag. The original packaging is not required.",
        inspect="Garments with perfume, deodorant marks, pet hair or signs of washing are refused."),
   dict(cat="footwear", cat_cap="Footwear", cond="Shoes must be unworn outdoors. You may try them on indoors on a clean surface, and the soles must show no marks.",
        pack="Footwear must be returned in the original shoebox with its lid. Do not stick the return label directly on the shoebox; place the shoebox inside a shipping bag or box.",
        inspect="Shoes with scuffed soles, dirt or odours are refused."),
   "2026-03-05", "N1")

SHIP_STD = """
**Effective {eff}.** This page describes standard shipping to {region}.

## Cost
Standard shipping to {region} costs {cost}. It is free when your order subtotal is {free} or more, after discounts and before tax.

## Delivery time
Orders ship within 1 business day of being placed. Standard delivery takes {days} business days after the order ships.

## Carriers
{carrier}

## Tracking
A tracking number is emailed as soon as the order ships. Tracking can take up to 12 hours to show its first scan.

## Taxes and duties
{tax}

## Delivery attempts
The carrier makes {attempts} delivery attempts. If delivery fails, the package is held at a local depot for a few days and then returned to us. We refund returned undelivered orders, minus the original shipping charge.
"""
nd("shipping-us-standard", "shipping-canada-standard", "Standard Shipping to the United States", "Standard Shipping to Canada", SHIP_STD,
   dict(region="the United States", cost="$5.99", free="$50", days="3 to 5", carrier="UPS or USPS delivers US orders, chosen automatically based on the destination.",
        tax="Sales tax is calculated at checkout based on the delivery address. No customs charges apply.", attempts="up to 3"),
   dict(region="Canada", cost="$9.99", free="$75", days="6 to 10", carrier="Canada Post delivers all Canadian orders.",
        tax="GST, HST, PST or QST is calculated at checkout based on the province. Brightwell Market pays import duties, so no customs charges are collected on delivery.", attempts="up to 2"),
   "2026-05-01", "N2")

WAR_CAT = """
**Effective {eff}.** This warranty applies to {cat} sold by Brightwell Market.

## Coverage period
{cat_cap} are covered against manufacturing defects for **{period}** from the delivery date.

## What is covered
Defects in materials or workmanship that affect how the product works, such as {covered}.

## What is not covered
{notcovered}

## Making a claim
Follow the warranty claims process. Keep your order record, which serves as proof of purchase.

## Remedy
We choose between repairing, replacing or refunding the product. Replacements are covered for the remainder of the original period.

## Your legal rights
This warranty is in addition to any rights you have under consumer law where you live.
"""
nd("warranty-outdoor-gear", "warranty-kitchen", "Warranty: Outdoor Gear", "Warranty: Home and Kitchen", WAR_CAT,
   dict(cat="outdoor gear", cat_cap="Outdoor gear", period="24 months", covered="failed seams, broken zips, faulty buckles, or frames that crack under normal use",
        notcovered="Normal wear to fabrics, fading from sunlight, damage from fire or sharp objects, and use outside the product's stated conditions are not covered."),
   dict(cat="home and kitchen products", cat_cap="Home and kitchen products", period="36 months", covered="motors that stop working, handles that detach, or non-stick coatings that peel under normal use",
        notcovered="Damage from dishwashers on items not labelled dishwasher-safe, scratches from metal utensils, and misuse beyond the stated capacity are not covered."),
   "2026-02-10", "N3")

EXP = """
**Effective {eff}.** This page describes {name} shipping, available on US orders only.

## Cost
{name_cap} shipping costs {cost}, charged once per order.

## Order cut-off
Orders placed before {cutoff} Eastern Time on a business day ship that same day. Orders placed later ship the next business day.

## Delivery
{delivery}

## Not available for
Expedited shipping is not available for PO boxes, Canadian addresses, or pre-orders that have not shipped.

## Changing to expedited
You can upgrade an order to this service before it ships by contacting support with the order number. We will charge the difference in shipping cost.

## Delays
Weather and carrier delays are outside our control. We do not offer a refund of the shipping charge for carrier delays.
"""
nd("expedited-two-day", "expedited-overnight", "Two-Day Shipping", "Overnight Shipping", EXP,
   dict(name="two-day", name_cap="Two-day", cost="$14.95", cutoff="2:00 pm", delivery="Orders arrive 2 business days after they ship. Available Monday to Friday."),
   dict(name="overnight", name_cap="Overnight", cost="$24.95", cutoff="12:00 pm", delivery="Orders arrive the next business day after they ship. Available Monday to Thursday only, so that packages are not held over a weekend."),
   "2026-05-10", "N4")
