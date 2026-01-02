Roadmap


Short-term:

   Fix nav links in all templates to use absolute paths

   Add analytics (Plausible/Fathom/Umami)

   Implement simple "views / favorites" tracking (client-side + lightweight backend)

   Optional per-collection configuration:

   Default print sizes/prices

   Different featured-selection rules

Medium-term:

   Integrate Stripe and/or PayPal for payments

   Implement order pipeline to The Print Space

   Add admin tools for:

      Managing collections and images

      Editing metadata and prices

   Contact form:

       Use PHP and PHPMailer to route inbound/outbound contact emails


Long-term:

   Customer account area (order history)

   More advanced filtering/sorting on browse view



   External Integrations (Planned / In Progress)
   Perplexity API (Active)
   Model: sonar-pro

   Use: image understanding for descriptions + tags

   Cost: ~$0.005 per image

   Perplexity Pro includes $5/mo API credit, sufficient for ~1,000 images/month.

   The Print Space (Planned)
   Orders will be pushed via The Print Space API

   Site will act as:

   Product catalog

   Cart & checkout UI

   Order creation point

   Payments (Planned)
   Stripe for payments

   Backend (Node.js / Python / PHP) will:

   Create payment intents / orders

   On success, forward order details to The Print Space

   Send confirmation emails (via SendGrid/Mailgun/self-hosted)

   Store order data (SQLite initially, PostgreSQL as needed)



Navigation Architecture
   Global nav appears on all main templates:

   Portfolio → /index.html

   Browse → /browse.html (or /browse/)

   About → /about.html

   Contact → /contact.html

   Important: Links should be absolute (starting with /) so they work from:

   Root pages (e.g., /index.html)

   Nested collection pages (e.g., /portfolio/big-bend-2025/index.html)


Future work for the generate-collection.py script:

   CLI flags for:

   Skipping Perplexity calls

   Regenerating thumbnails

   Dry-run mode

