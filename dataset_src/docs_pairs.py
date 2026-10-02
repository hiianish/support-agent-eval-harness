"""Superseded version pairs (trap type: superseded). Old and new versions share a template; only the
planted values differ, so the stale/current choice is the only thing that matters.
hide=True -> neither version carries a status/supersedes field; only effective_date and body text tell them apart."""
from docs_core import D

def pair(slug, title, tier, old_eff, new_eff, tmpl, old, new, trap, hide=False):
    out = []
    for ver, eff, vals in ((1, old_eff, old), (2, new_eff, new)):
        body = tmpl.format(eff=eff_text(eff), **vals)
        kw = dict(trap=trap, version=ver)
        if not hide:
            kw["status"] = "superseded" if ver == 1 else "current"
            if ver == 2:
                kw["supersedes"] = f"{slug}-v1"
        out.append(D(f"{slug}-v{ver}", title, tier, eff, body, **kw))
    return out

MONTHS = ["January","February","March","April","May","June","July","August","September","October","November","December"]
def eff_text(iso):
    y, m, d = iso.split("-")
    return f"{MONTHS[int(m)-1]} {int(d)}, {y}"

PAIRS = []

# ---------- S1 returns policy ----------
RETURNS = """
**Effective {eff}.**

## Return window
You may return most items within **{win} days** of the delivery date. The window is counted from the day the carrier marks the package as delivered. This policy applies to orders delivered in both the United States and Canada.

## Condition of returned items
Items must be unused, in their original packaging, and with all tags and accessories included. Apparel must be unwashed. We may refuse or partially refund a return that comes back used, damaged by the customer, or missing parts.

## How to start a return
Open Account > Orders, choose the item and select Start a return. You will receive a return authorization number and a prepaid shipping label by email. Pack the item securely, attach the label, and drop it off with the carrier shown on the label. Returns sent without an authorization number may be delayed.

## Return shipping
If your item is defective, damaged on arrival, or not the item you ordered, the return label is free. For every other return, a return shipping fee of **{fee}** is deducted from your refund.

## Restocking fees
Some opened electronics are subject to a restocking fee. See the restocking fee policy for the current rate.

## Items that cannot be returned
Final Sale items, personalized items, gift cards, and items returned after the window has closed cannot be returned. Defective or damaged items are always handled under our damaged items and warranty policies, whatever their sale status.

## Refunds
Refunds go back to the original payment method. See the refunds policy for timing.

## Exchanges
If you would rather swap an item for another size or colour, see the exchanges policy. Exchanges follow the same window as returns.

## Partial returns
You can return some items from an order and keep others. The return window for each item is counted from its own delivery date.
"""
PAIRS += pair("returns-policy", "Returns Policy", "policy", "2025-01-01", "2026-03-01", RETURNS,
              dict(win=45, fee="$4.95"), dict(win=30, fee="$6.95"), "S1")

# ---------- S2 refunds policy (hidden status) ----------
REFUNDS = """
**Effective {eff}.**

## When you are refunded
After you ship a return, we refund you once our warehouse has received and inspected the package. Inspection normally takes 1 to 2 business days after the package arrives.

## How long refunds take
We issue your refund within **{days} business days** of the warehouse receiving your return. The refund goes back to the payment method you used for the order. Gift card payments are refunded to the same gift card as store credit.

## Time to appear on your statement
After we issue a refund, your bank or card company may need additional time to show it. Most banks post refunds within 3 to 5 business days. We cannot speed up your bank's processing.
{review}
## Partial refunds
If a returned item is used, damaged, or missing parts, we may refund only part of its price. We email you a short explanation whenever we do.

## Refunds without a return
When an order is cancelled before it ships, or a package is confirmed lost, we refund the full order total without needing a return. These refunds follow the same timing as above, counted from the cancellation or the date the loss is confirmed.

## What is refunded
Refunds cover the item price and the tax paid on it. Original shipping charges are refunded only when the return is due to our error, such as a defective, damaged or wrong item.

## Checking the status
Under Account > Orders, an order shows Return requested until we receive the package, and Returned once the refund has been issued.
"""
SPEC_NEW = "\n## Larger refunds\nRefunds above $200 are reviewed by a specialist before they are released. This review can add up to 2 business days to the timing above.\n"
PAIRS += pair("refunds-policy", "Refunds Policy", "policy", "2025-04-01", "2026-04-15", REFUNDS,
              dict(days=10, review=""), dict(days=5, review=SPEC_NEW), "S2", hide=True)

# ---------- S3 shipping rates ----------
SHIPPING = """
**Effective {eff}.**

## Standard shipping rates
Standard shipping on US orders costs $5.99. Standard shipping on orders to Canada costs $9.99.

## Free shipping
US orders qualify for free standard shipping when the order subtotal is **{us} or more**, after discounts and before tax. Canadian orders qualify for free standard shipping at {ca} or more. Gift cards do not count towards the threshold.

## Delivery estimates
Standard shipping to US addresses is estimated at 3 to 5 business days after the order ships. Standard shipping to Canadian addresses is estimated at 6 to 10 business days after the order ships. Estimates start from the day the order ships, not the day you place it.

## Expedited options
Two-day and overnight shipping are available on US orders. Rates and cut-off times are listed in the expedited shipping articles.

## Where we ship
We ship to street addresses in all 50 US states and the 10 Canadian provinces. Delivery to territories and to the three northern Canadian territories is not available.

## Multiple items
Shipping is charged once per order. If your order is split into several packages, you are not charged again.

## Changes to shipping charges
Shipping charges are shown on the last step of checkout. The charge shown when you place the order is the charge that applies, even if our rates change afterwards.
"""
PAIRS += pair("shipping-rates", "Shipping Rates and Free Shipping", "policy", "2025-01-01", "2026-05-01", SHIPPING,
              dict(us="$35", ca="$60"), dict(us="$50", ca="$75"), "S3")

# ---------- S4 electronics warranty ----------
WARRANTY = """
**Effective {eff}.**

## What is covered
Brightwell Market electronics accessories, such as chargers, cables, headphones and power banks, are covered against manufacturing defects for **{period}** from the delivery date. If a covered product stops working through no fault of yours during that time, we will replace it or refund it.

## What is not covered
The warranty does not cover damage from drops, liquids, misuse or unauthorised repairs, normal wear such as cable fraying from regular use, cosmetic scratches, or loss and theft. It also does not cover batteries that have lost capacity through normal ageing after the first year of use.

## Replacement or refund
We choose between a replacement and a refund. If we replace a product, the replacement is covered for the remainder of the original warranty period.

## How to make a claim
Email support or tell the AI assistant your order number and describe the problem. A photo or short video of the fault is usually requested. See the warranty claims process for the steps and deadlines.

## Proof of purchase
Your Brightwell Market order record is your proof of purchase. You do not need to keep a paper receipt.

## Other products
This warranty applies to the Electronics category only. Outdoor gear and home and kitchen products have their own warranty terms.

## Your legal rights
This warranty is in addition to any rights you have under consumer law where you live.
"""
PAIRS += pair("warranty-electronics", "Electronics Warranty", "policy", "2025-01-01", "2026-02-01", WARRANTY,
              dict(period="90 days"), dict(period="12 months"), "S4")

# ---------- S5 restocking fee (hidden status) ----------
RESTOCK = """
**Effective {eff}.**

## When a restocking fee applies
A restocking fee applies when an **opened** electronics item is returned for a reason other than a defect, damage or a shipping error. The fee is **{pct} of the item price** and is deducted from the refund, in addition to the standard return shipping fee.

## When no fee applies
No restocking fee is charged for unopened electronics in their sealed original packaging, for apparel, home and kitchen items or outdoor gear, or for any item that is defective, damaged on arrival or the wrong item. No fee is charged on exchanges for the same product.

## What counts as opened
An item is opened if its sealed packaging or tamper tape has been broken, or if the product has been used. Trying a cable or an accessory out of its box counts as opening it.

## Example
A $40 pair of earbuds is returned opened because the customer changed their mind. The restocking fee is {pct} of $40. This amount is deducted from the refund before the return shipping fee.

## How it appears on your refund
The restocking fee is shown as a separate line on the refund email so you can see exactly what was deducted.

## Questions
If you believe a restocking fee was applied by mistake, contact support with your order number and a description of the item's condition when it was returned.
"""
PAIRS += pair("restocking-fee", "Restocking Fee Policy", "policy", "2025-03-01", "2026-03-01", RESTOCK,
              dict(pct="20%"), dict(pct="15%"), "S5", hide=True)

# ---------- S6 price adjustment ----------
PRICEADJ = """
**Effective {eff}.**

## What a price adjustment is
If an item you bought from Brightwell Market goes on sale for a lower price shortly after it is delivered, you can ask for the difference to be refunded instead of returning and rebuying it.

## How long you have
You can request a price adjustment within **{days} days of delivery**. Requests made after that cannot be accepted.

## How to request one
Contact support or the AI assistant with your order number and the item. We check that the item's current price on our site is lower than the price you paid, and that the lower price is a regular sale price rather than a limited-time doorbuster or a promo code.

## What is refunded
We refund the difference between what you paid and the current lower price, to your original payment method. Only one adjustment can be made per item.

## What is excluded
Price adjustments are not available for Final Sale items, for promo-code discounts, for gift cards, or for prices on other websites. Pre-order items are adjusted against the price on the day they ship.

## Interaction with returns
If you return an item, any price adjustment already paid on it is deducted from the refund.
"""
PAIRS += pair("price-adjustment", "Price Adjustment Policy", "policy", "2025-01-01", "2026-06-01", PRICEADJ,
              dict(days=7), dict(days=14), "S6")

# ---------- S7 order cancellation (hidden status) ----------
CANCEL = """
**Effective {eff}.**

## Cancelling an order
You can cancel an order yourself from Account > Orders, or by contacting support, within **{window}** of placing it, as long as the order has not shipped.

## After that period
Once that period has passed, we cannot guarantee the order can be stopped, because it may already be packed. Contact support quickly with your order number and we will try to stop it. If the order has already shipped, it cannot be cancelled. You can refuse the delivery or return the items under the returns policy.

## What you get back
A cancelled order is refunded in full, including shipping and tax, to your original payment method. See the refunds policy for timing.

## Cancelling part of an order
Individual items can be cancelled under the same conditions. If you cancel only some items, the order total is recalculated, and you may lose free shipping if the remaining items fall below the free shipping threshold.

## Pre-orders
Pre-orders can be cancelled at any time before they ship, regardless of the period above.

## Declined payments
Orders with a declined payment are cancelled automatically after 2 hours if no valid payment has been added.
"""
PAIRS += pair("order-cancellation", "Order Cancellation Policy", "policy", "2025-02-01", "2026-05-15", CANCEL,
              dict(window="2 hours"), dict(window="24 hours"), "S7", hide=True)

# ---------- S8 loyalty points ----------
LOYALTY = """
**Effective {eff}.**

## Earning points
Brightwell Rewards members earn 1 point for every $1 spent on eligible items, after discounts and before tax. Shipping charges, gift cards and Final Sale items do not earn points. Points are added to your account when the order is delivered.

## Using points
Every 100 points is worth $1 off a future order. Points can be applied at checkout in multiples of 100 and cannot be exchanged for cash.

## Expiry
Points expire **{months} months** after the date they were earned. Points that expire first are used first. Your Rewards tab shows the expiry date for each batch of points.

## Returns
If you return an item, the points earned on it are removed from your account. If you have already spent those points, the equivalent value is deducted from your refund.

## Cancelled orders
Points are only added on delivery, so cancelling an order before it ships never affects your points.

## Closing your account
All points are forfeited when an account is closed. Points cannot be transferred between accounts.

## Changes to the programme
We may change the rewards programme. We will email members at least 30 days before any change that reduces the value of points already earned.
"""
PAIRS += pair("loyalty-points", "Brightwell Rewards: Earning and Expiry", "policy", "2025-01-01", "2026-07-01", LOYALTY,
              dict(months=12), dict(months=18), "S8")
