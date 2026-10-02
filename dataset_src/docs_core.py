"""Clean policy documents for the fictional store 'Brightwell Market' (US + Canada).
Facts here are the CURRENT truth as of 2026-10-01 unless a doc is marked superseded elsewhere."""

def D(id, title, tier, eff, body, **kw):
    d = dict(id=id, title=title, tier=tier, eff=eff, body=body.strip(), audience="public", trap=None)
    d.update(kw)
    return d

CORE = []

CORE.append(D("terms-of-sale", "Terms of Sale", "terms", "2026-01-15", """
These Terms of Sale apply to every order placed on brightwellmarket.example. By placing an order you agree to them.

## Who we sell to
Brightwell Market sells to customers in the United States and Canada. You must be at least 18 years old or have a parent or guardian place the order.

## Prices and payment
All prices are shown in US dollars for US orders and in Canadian dollars for Canadian orders. Your card is charged when the order is placed. If we find a pricing error before the order ships, we may cancel the order and refund you in full.

## Gift cards
Brightwell Market gift cards are non-refundable and cannot be exchanged for cash, except where required by law. A gift card that has been redeemed in part keeps its remaining balance. Gift cards do not expire.

## Final sale and personalized items
Items marked "Final Sale" at the time of purchase, and personalized or engraved items, cannot be returned or exchanged unless they arrive defective or damaged.

## Order of precedence
If two Brightwell Market documents give different answers to the same question, the following order decides which one applies, from highest to lowest authority: (1) these Terms of Sale, (2) policy documents, (3) FAQ pages, (4) help articles, (5) promotional pages. Promotional pages never change a standard policy unless the promotion is also published in a policy document.

If two documents of the same level disagree and carry the same effective date, neither one overrides the other. In that case a support specialist must confirm the correct answer, and the customer should be told the information is being confirmed rather than being given a guess.

## Changes
We may update these terms. The version in force for an order is the one in effect on the date the order was placed.

## Contact
Questions about these terms can be sent to support@brightwellmarket.example.
"""))

CORE.append(D("company-overview", "About Brightwell Market and How to Reach Us", "help", "2026-01-10", """
Brightwell Market is an online retailer of everyday electronics accessories, apparel, home and kitchen goods, and outdoor gear. We ship to customers in the United States and Canada from fulfilment centres in Ohio and Ontario.

## Ways to contact support
Customers can reach support in two ways:

- **Email:** support@brightwellmarket.example. We aim to answer within one business day.
- **Live chat:** available Monday to Friday, 9:00 am to 6:00 pm Eastern Time, from the Help page of our website after you sign in.

Our AI assistant can answer questions about orders, shipping, returns and refunds at any hour. It can look up your orders and start some requests for you, and it hands the conversation to a human specialist whenever a request needs a person to decide.

## What we sell
Our catalogue is organised into four categories: Electronics, Apparel, Home and Kitchen, and Outdoor. Each product page lists its category, price, and whether the item is final sale.

## Business days
When our documents mention business days, they mean Monday to Friday, excluding public holidays in the United States. Orders placed after 2:00 pm Eastern Time are treated as placed on the next business day for shipping purposes.

## Where to find your information
Your orders, return requests and loyalty points are all in your account under the Orders and Rewards tabs. You will also receive an email for every status change on an order.
"""))

CORE.append(D("order-status-tracking", "Order Statuses and Tracking", "help", "2026-02-02", """
Every order moves through a small number of statuses. You can see the current one under Account > Orders, and we email you each time it changes.

## Statuses
- **Placed:** we have received your order and your payment was accepted.
- **Processing:** the warehouse is picking and packing your items. Orders usually spend up to 24 hours in this status.
- **Shipped:** the carrier has the package. A tracking number is added to the order at this point.
- **Delivered:** the carrier has marked the package as delivered. The delivery date is the date shown in the carrier's final scan.
- **Cancelled:** the order was cancelled before it shipped.
- **Return requested:** you have asked to return one or more items and we are waiting to receive them.
- **Returned:** we received the return and the refund has been issued.

## Tracking
Tracking numbers appear on the order page once the order has shipped. Tracking may take up to 12 hours to show its first scan. We use UPS and USPS for orders in the United States and Canada Post for orders in Canada.

## If tracking has not moved
If the tracking page shows no movement for 5 business days while the order is marked Shipped, contact support and we will ask the carrier for a trace. See the lost packages article for what happens after that.

## Split shipments
An order can ship in more than one package. Each package has its own tracking number, and the order only becomes Delivered once every package has been delivered.
"""))

CORE.append(D("payment-methods", "Accepted Payment Methods", "policy", "2026-01-20", """
## What you can pay with
We accept Visa, Mastercard and American Express credit and debit cards, PayPal, Apple Pay and Brightwell Market gift cards. We do not accept cheques, money orders or cash.

## When you are charged
Your payment method is charged when you place the order, with the exception of pre-orders, which are charged when the item ships. If a payment is declined, the order stays in a Placed status for up to 2 hours so you can try another method, after which it is cancelled automatically.

## Using more than one method
You can combine a gift card with one other payment method on a single order. You cannot split a purchase across two cards.

## Currency
US orders are charged in US dollars. Canadian orders are charged in Canadian dollars. Your bank may add a foreign-exchange fee if your card is issued in another currency; we do not control that fee.

## Security
We never store your full card number. Card details are handled by our payment processor and shown on your account only as the card brand and last four digits. Brightwell Market staff will never ask you for a full card number, security code or password in chat or by email.

## Failed or duplicate charges
If you see two charges for one order, one of them is usually a temporary authorisation hold that your bank releases within 3 to 5 business days. If it has not disappeared after 5 business days, contact support with your order number.
"""))

CORE.append(D("gift-cards-how-to", "Buying and Using Gift Cards", "help", "2026-02-12", """
## Buying a gift card
Digital gift cards are available in amounts from $10 to $500. They are delivered by email within a few minutes of purchase, to the address you enter at checkout. Physical gift cards are not available.

## Redeeming a gift card
Enter the 16-character code in the payment step at checkout. If the card balance is lower than your order total, the remainder can be paid with one other payment method. If the balance is higher than your order total, the leftover stays on the card for next time.

## Checking your balance
Sign in and open Account > Gift cards to see the remaining balance on any card you have redeemed. If you have not yet redeemed a card, enter the code on the same page to check it.

## Expiry
Our gift cards do not expire and have no inactivity fees.

## Lost or stolen codes
Treat a gift card code like cash. If an email with a code is deleted, support can resend it to the original recipient address after confirming the order number. We cannot replace a code that has already been redeemed by someone else.

## Using a gift card on a returned order
When an order paid with a gift card is returned, the refund goes back to the same gift card as store credit.
"""))

CORE.append(D("account-management", "Managing Your Account", "help", "2026-03-04", """
## Creating an account
You can create an account with an email address and a password of at least 12 characters. Guest checkout is also available, but guest orders do not appear in an account and cannot be returned online; contact support instead.

## Resetting your password
Select "Forgot password" on the sign-in page. We email a reset link that works once and expires after 60 minutes. If you do not receive it within 10 minutes, check your spam folder and confirm the address with support.

## Two-step sign-in
Two-step sign-in with an authenticator app or text message code can be switched on under Account > Security. We recommend it for every account.

## Updating details
Name, email address, saved addresses and communication preferences can be changed under Account > Profile. Changing the email address requires confirming a link sent to the new address.

## Closing your account
You can ask to close your account by emailing support. We delete personal data we are not required to keep within 30 days of confirming the request. Order records needed for tax and warranty purposes are kept for 7 years.

## Verifying who you are
Support staff and the AI assistant only discuss an order with the account that placed it. If you are signed in to a different account than the one that placed the order, we cannot share its details.
"""))

CORE.append(D("lost-packages", "What To Do If Your Package Has Not Arrived", "help", "2026-02-20", """
## Before you contact us
Check the tracking page. Carriers sometimes mark a package as delivered a few hours before it reaches your door, and packages are often left with a neighbour or in a mail room. Please check these places first.

## When to contact support
If the order shows Delivered but you cannot find the package, contact us within 7 days of the delivery date shown. If the order is still in transit more than 10 business days after the estimated delivery date, contact us as soon as that date has passed.

## What we do
Once you contact us, we open a trace with the carrier. Carriers usually take up to 5 business days to finish a trace. When the trace confirms the package is lost, we choose between sending a replacement at no cost or refunding the order in full, depending on stock. You can tell us which you would prefer, but we cannot guarantee it.

## Wrong address
If the package was delivered to an address typed incorrectly at checkout, the carrier trace may not recover it. We review these cases individually, and a specialist decides on the outcome.

## Protecting packages
Customers can add delivery instructions, such as a safe place, to an order only before it ships.
"""))

CORE.append(D("wrong-item-received", "Received the Wrong Item", "help", "2026-02-24", """
If the item that arrived is not the item you ordered, we will fix it at no cost to you.

## What to do
Contact support or the AI assistant within the 30-day return window with your order number. A photo of the item and its packing slip helps but is not required.

## What we do
We email you a prepaid return label. The return shipping fee is not charged for wrong items. As soon as the carrier scans the package we ship the correct item, so you do not have to wait for the return to arrive. If the correct item is out of stock, we refund the item instead.

## Keep the packaging
Please keep the wrong item in its original packaging until the label arrives. You do not need to pay for any damage to the packaging caused by the mix-up on our side.

## Duplicate items
If you received two of an item you ordered once, the second is treated as a wrong item and the same process applies. You may not keep the extra item.

## Related
Items that arrive broken are covered by our damaged items policy, and items you simply do not want are covered by the returns policy.
"""))

CORE.append(D("sales-tax", "Sales Tax and Duties", "policy", "2026-01-25", """
## United States
We collect sales tax on US orders according to the rate at the delivery address. The tax amount is shown on the last step of checkout and again on your order confirmation. Tax is calculated on the item price after discounts and, in some states, on shipping charges as well.

## Canada
For Canadian orders we collect the GST or HST, and PST or QST where it applies, based on the delivery province. These taxes are shown at checkout. Brightwell Market pays import duties on Canadian orders, so there are no extra customs charges on delivery.

## Tax-exempt purchases
We do not currently process tax-exempt orders. If you believe you are exempt, please contact support before ordering.

## Returns and tax
When you return an item, the tax paid on that item is refunded along with it. If only part of an order is returned, the tax refund is proportional to the items returned.

## Receipts
A tax receipt is attached to every order confirmation email, and a copy is stored under Account > Orders. Copies for orders older than 7 years are not available.
"""))

CORE.append(D("promo-codes", "Promo Codes and Sales", "policy", "2026-03-12", """
## Using a promo code
Enter your code in the discount box at checkout. Only one promo code can be used per order, and promo codes cannot be combined with each other. Codes are case-insensitive.

## What codes apply to
Unless a code says otherwise, it applies to regular-priced items only. Items already marked down, and items marked Final Sale, are excluded. Gift cards cannot be bought with a promo code.

## Expiry
Each code shows its expiry date in the promotion's description. A code that has expired cannot be applied, and we cannot honour an expired code after the fact.

## No retroactive discounts
Promo codes cannot be added to an order after it has been placed. If you forgot to enter a code, you may cancel the order if it has not shipped and place it again with the code.

## Price adjustments
If an item you bought goes on sale shortly after delivery, see the price adjustment policy.

## Returns of discounted orders
When you return an item bought with a promo code, the refund is the price you actually paid for that item after the discount, not its list price. If the discount was spread across several items, it is divided in proportion to the item prices.
"""))

CORE.append(D("privacy-summary", "Privacy Summary", "policy", "2026-01-30", """
This summary describes in plain words how Brightwell Market handles your information. The full privacy notice is on our website.

## What we collect
We collect the details needed to run your order: name, delivery and billing address, email, phone number if you give one, and the items you buy. We also collect basic device and browsing information to keep the site secure and working.

## What we do not collect
We do not store your full card number. We do not sell personal information.

## Who we share it with
We share the minimum needed with carriers to deliver your order, with our payment processor to take payment, and with fraud-prevention services to protect accounts.

## Your choices
You can opt out of marketing emails at any time through the unsubscribe link or Account > Profile. You can ask for a copy of your data, a correction, or deletion by emailing support. We reply within 30 days.

## Support conversations
Chats with the AI assistant are stored so that a human specialist can continue your case. They are kept for 12 months and are used to improve our service. Please do not type your full card number, passwords or government ID numbers into chat.
"""))

CORE.append(D("product-care-apparel", "Caring for Your Apparel", "help", "2026-02-18", """
Good care keeps clothes looking new and also keeps them eligible for return, because only unwashed items with tags attached can be returned.

## Washing
Wash dark colours separately for the first three washes. Use cold water unless the label says otherwise. Turn printed items inside out to protect the print. Avoid fabric softener on technical fabrics such as fleece and waterproof shells, because it clogs the fibres.

## Drying
Tumble dry on low only if the care label allows it. Air drying flat is best for knitwear and for anything with elastic. Never tumble dry waterproof jackets on high heat.

## Ironing and stains
Use the lowest iron setting that removes creases, with a cloth between the iron and printed areas. Treat stains quickly with cold water and a small amount of mild detergent before washing.

## Storage
Fold knitwear instead of hanging it to avoid shoulder stretching. Keep outdoor shells loosely hung in a dry cupboard. Avoid storing damp clothes in sealed bags.

## Care labels
The care label sewn into each garment is the final authority on how to look after it. If a product page and a label disagree, follow the label.
"""))

CORE.append(D("size-fit-guide", "Apparel Size and Fit Guide", "help", "2026-02-25", """
## How our sizing works
Our apparel is cut to standard unisex sizing from XS to 3XL, with a separate women's range from size 0 to 18. Each product page has a size chart showing chest, waist and length measurements in inches and centimetres.

## Measuring yourself
Measure your chest at the fullest part, your waist at the narrowest part, and compare with the chart. If you are between two sizes, choose the larger size for jackets and the smaller size for base layers.

## Fit labels
Product pages describe the fit as Slim, Regular or Relaxed. Slim fits sit close to the body, Regular fits allow a layer underneath, and Relaxed fits are cut roomier through the chest and hips.

## If it does not fit
You can exchange an item for another size at no charge within the exchange period described in our exchanges article. If the size you want is out of stock, you can return the item for a refund instead.

## Shoes
Footwear is listed in US sizes. Half sizes are available on most styles. If a shoe runs large or small, the product page says so near the size selector.
"""))

CORE.append(D("order-modifications", "Changing or Adding to an Order", "help", "2026-03-18", """
## Changing the delivery address
You can change the delivery address on an order only while it is in Placed or Processing status. Once an order is Shipped, the address cannot be changed by us or by the carrier, and the package will go to the original address.

## Adding items
Items cannot be added to an existing order. Place a second order instead. If you want the two orders to travel together, contact support before the first one ships; we cannot promise to combine them.

## Changing items or sizes
To change an item or a size on an order that has not shipped, cancel the order and place a new one. See the cancellation policy for how long you have.

## Changing shipping speed
Shipping speed can be upgraded to an expedited option before the order ships. Contact support with your order number and we will calculate the difference. Speed cannot be downgraded for a refund of the difference once the order has shipped.

## Changing payment method
The payment method on an order cannot be changed after the order is placed. If you need to use a different card, cancel the order and place it again.
"""))

CORE.append(D("preorders-backorders", "Pre-orders and Back-ordered Items", "policy", "2026-03-20", """
## Pre-orders
Some new products can be ordered before they are in stock. A pre-order shows an expected ship date on the product page. You are charged when the item ships, not when you order. You can cancel a pre-order at any time before it ships at no cost.

## Back-orders
If an item you ordered sells out before we pack it, we mark it back-ordered and email you with a new estimate. You can wait for the item or cancel that item for a full refund. If you do nothing, the item stays on the order.

## Estimated dates
Expected ship dates are estimates, not promises. They may move if our supplier is delayed. We will email you every time the estimate changes.

## Mixed orders
If one order contains a pre-order and an in-stock item, the in-stock item ships right away by default, and the pre-order ships separately when ready. Standard shipping charges are applied once per order, not once per package.

## Returns of pre-ordered items
The 30-day return window for a pre-ordered item starts on the day it is delivered, the same as for any other item.
"""))

CORE.append(D("split-shipments", "Orders That Arrive in More Than One Package", "help", "2026-03-25", """
Sometimes an order is packed and sent in several parcels. This happens when items are stored in different fulfilment centres or when one item is bulky.

## How you will know
The order page lists every package with its own tracking number. You will receive a separate Shipped email for each package.

## Delivery dates
Packages in one order can arrive on different days. Each package shows its own estimated delivery date. The order is marked Delivered only after the last package is delivered.

## Shipping charges
You are charged once for shipping on an order, no matter how many packages it travels in. You are never charged extra for splitting.

## Returning part of a split order
The 30-day return window runs from the delivery date of the package containing the item you want to return, not from the delivery date of the last package. This is one of the few cases where two items from one order can have different return deadlines.

## Missing one package
If one package is delayed, follow the lost packages guidance for that package only. The rest of the order is not affected.
"""))

CORE.append(D("exchanges", "Exchanges", "policy", "2026-03-01", """
## What an exchange is
An exchange lets you swap an item for a different size or colour of the same product. It is free and does not require paying the return shipping fee.

## How long you have
You can request an exchange within 30 days of delivery, using the same window as returns. The item must be unused, in its original packaging, with all tags attached.

## How to start
Open Account > Orders, choose the item and select Exchange. We email a prepaid label. When the carrier scans the package, we ship the replacement.

## If the replacement is out of stock
We cancel the exchange and refund the item instead. The refund follows the refunds timeline in our refunds policy.

## Price differences
If the replacement costs more than the original, we charge the difference. If it costs less, we refund the difference.

## What cannot be exchanged
Final Sale items, gift cards, and personalized items cannot be exchanged. Electronics can be exchanged only for the same product, for example in another colour, never for a different product.
"""))
