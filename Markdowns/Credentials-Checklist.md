# Mimmsphoto Backend - Credentials Gathering Checklist

**Date:** January 3, 2026  
**Purpose:** Collect all API keys and credentials needed for implementation  
**Time to Complete:** 30-60 minutes (mostly account creation)

---

## Overview: What You Need to Gather

You'll need credentials from **5 sources**:
1. Your hosting provider (database access)
2. Stripe (payment processing)
3. Print Space (fine art prints)
4. Prodigi (canvas prints)
5. Your server (FTP/SSH access)

**After gathering these, we can implement all 7 stages.**

---

## PART 1: Hosting & Database Access

### Source: Your Father-in-Law's Server (cPanel)

**What to Ask Your Father-in-Law:**

I need you to access cPanel and provide:

```
DATABASE CREDENTIALS:
□ Database Host: _______________________________
  (Usually: localhost)

□ Database Name: _______________________________
  (Name of the OpenCart database)

□ Database Username: _______________________________

□ Database Password: _______________________________

FILEZILLA FTP ACCESS:
□ FTP/SFTP Host: _______________________________
  (Server hostname or IP)

□ FTP Username: _______________________________
  (Your cPanel username or FTP user)

□ FTP Password: _______________________________

□ Port: _______________________________
  (Usually 21 for FTP, 22 for SFTP)

PHP VERSION:
□ PHP Version: _______________________________
  (Should be 7.4+)
  
ADDITIONAL INFO:
□ cPanel URL: _______________________________
  (For direct access if needed)

□ Email to access cPanel: _______________________________
```

**How to Find These:**

1. **Log into cPanel** at: `yourdomain.com/cpanel` or `yourdomain.com:2083`

2. **For Database Info:**
   - Go to: MySQL® Databases
   - Look for your OpenCart database
   - Username/password are shown there
   - Host is typically `localhost`

3. **For FTP Info:**
   - Go to: FTP Accounts
   - Select your main account
   - Click "Configure FTP Client"
   - All credentials displayed

4. **For PHP Version:**
   - Go to: Select PHP Version
   - Shows current version (confirm 7.4+)

---

## PART 2: Stripe Account & API Keys

### Create Free Stripe Account

**Step 1: Sign Up**
- Go to: https://stripe.com/register
- Email: info@mimmsphoto.com (or personal email)
- Password: Create a strong one
- Country: United States
- Business Type: Sole Proprietor (or your choice)

**Step 2: Verify Email**
- Check email for verification link
- Click link to activate

**Step 3: Get API Keys**

Once logged in to Stripe Dashboard:

```
STRIPE API KEYS (TEST MODE FIRST):
□ Publishable Key (pk_test_...): _______________________________
  Location: Developers → API Keys → Publishable key

□ Secret Key (sk_test_...): _______________________________
  Location: Developers → API Keys → Secret key

STRIPE WEBHOOK SECRET:
□ Webhook Secret (whsec_...): _______________________________
  Location: Developers → Webhooks → signing secret
  
  To create webhook:
  1. Click "Add endpoint"
  2. URL: https://mimmsphoto.com/shop/custom/webhook/stripe
  3. Events: payment_intent.succeeded
  4. Copy the signing secret shown
```

**Note:** These are TEST keys. After going live, you'll generate LIVE keys (pk_live_..., sk_live_...) and swap them in `.env`

**Keep Track:**
```
TEST MODE (Initial Setup):
Stripe Public: pk_test_____________
Stripe Secret: sk_test_____________
Stripe Webhook: whsec_____________

LIVE MODE (Later, after testing):
Stripe Public: pk_live_____________
Stripe Secret: sk_live_____________
Stripe Webhook: whsec_____________
```

---

## PART 3: Print Space Account & API Key

### Create Print Space Account

**Step 1: Sign Up**
- Go to: https://www.theprintspace.com/
- Click: Account → Sign Up
- Business Email: info@mimmsphoto.com
- Company: Mimmsphoto (or your photography name)
- Website: https://mimmsphoto.com

**Step 2: Verify Account**
- Check email for verification
- Activate account

**Step 3: Get API Credentials**

Once logged in to Print Space CreativeHub Dashboard:

```
PRINT SPACE API CREDENTIALS:
□ API Key: _______________________________
  Location: Account Settings → API Keys → Your API Key
  
  Steps:
  1. Click "Generate API Key" (or "Create New Key")
  2. Name it: "mimmsphoto-opencart"
  3. Leave webhook URI blank for now (we'll add after deployment)
  4. Copy the API key shown
  5. Save it securely

□ Merchant ID: _______________________________
  (OPTIONAL - not always visible in CreativeHub)
  If not visible in Account Settings, leave blank
  API Key alone is sufficient for integration

ENDPOINT:
Print Space API Base: https://api.theprintspace.com/v1
(Already configured in our code)
```

**About Webhook URI:**
- Leave blank when creating the key
- We'll add it AFTER Stage 5 deployment
- Print Space will test the connection once it's live
- Don't add until the webhook handler code is deployed

**Test Submission (Optional but Recommended):**
- After creating account, test a small order
- Add product to cart
- Place test order
- Verify Print Space receives it
- This confirms your account works

---

## PART 4: Prodigi Account & API Key

### Create Prodigi Account

**Step 1: Sign Up**
- Go to: https://www.prodigi.com/signup
- Email: info@mimmsphoto.com
- Name: Mimmsphoto
- Business Type: Self-employed/Freelancer
- Country: United States

**Step 2: Verify Email**
- Check email and activate

**Step 3: Get API Credentials**

Once logged in to Prodigi Dashboard:

```
PRODIGI API CREDENTIALS:
□ API Key: _______________________________
  Location: Settings → Integrations → API → API Key
  
  If not visible:
  1. Click "Create New Key"
  2. Name: "mimmsphoto-opencart"
  3. Select Scope: "Full Access"
  4. Copy the key

□ Merchant ID: _______________________________
  (OPTIONAL - use if available, otherwise leave blank)

ENDPOINT:
Prodigi API Base: https://api.prodigi.com/v4.0
(Already configured in our code)
```

**Test Submission (Optional):**
- After account created, test a canvas order
- Verify Prodigi receives it
- Check quality of test print
- Confirms integration readiness

---

## PART 5: Your Server Access

### Confirm FTP/SSH Access

**Test Your Filezilla Connection:**

1. Open Filezilla
2. File → Site Manager → New Site
3. Enter credentials from PART 1:
   - Protocol: SFTP (port 22) or FTP (port 21)
   - Host: [from cPanel]
   - Username: [from cPanel]
   - Password: [from cPanel]
4. Click "Connect"
5. Navigate to: `/public_html/shop/`
6. Verify you can see OpenCart files

**Confirm SSH Access (If Available):**

If your host provides SSH:
1. Open Terminal (Mac/Linux) or PuTTY (Windows)
2. `ssh [username]@[host]`
3. Enter password
4. `cd /public_html/shop`
5. `ls -la` (verify files visible)

```
SSH/SFTP ACCESS (for direct uploads):
□ SSH/SFTP Enabled: YES / NO
□ Tested Connection: YES / NO
□ Can access /public_html/shop/: YES / NO
```

---

## PART 6: Email Configuration (Already Done ✅)

You mentioned self-hosted email is already working at `info@mimmsphoto.com`

**Confirm:**
```
SELF-HOSTED EMAIL:
□ Email Address: info@mimmsphoto.com
□ Already Configured: YES ✅
□ Can receive mail: YES ✅
□ Can send mail: YES ✅
```

No action needed here - we'll use this for order confirmations.

---

## Complete Checklist

### Print This Out or Save Locally

Once you gather all credentials, check them off:

```
═══════════════════════════════════════════════════════════

HOSTING & DATABASE:
□ Database Host: ________________
□ Database Name: ________________
□ Database User: ________________
□ Database Password: ________________
□ FTP Host: ________________
□ FTP User: ________________
□ FTP Password: ________________
□ FTP Port: ________________
□ PHP Version (7.4+?): ________________

STRIPE (TEST):
□ Public Key (pk_test_...): ________________
□ Secret Key (sk_test_...): ________________
□ Webhook Secret (whsec_...): ________________

PRINT SPACE:
□ API Key: ________________
(Merchant ID: optional if not visible in CreativeHub)

PRODIGI:
□ API Key: ________________
(Merchant ID: optional if not available)

EMAIL:
□ Order Email: info@mimmsphoto.com ✅

═══════════════════════════════════════════════════════════
```

---

## Security Notes ⚠️

**CRITICAL: Protect These Credentials**

1. **Never commit to GitHub:**
   - `.env` file is in `.gitignore` (we handled this)
   - Never paste credentials in pull requests
   - Never share in Slack/Discord/email

2. **API Key Rotation:**
   - Print Space: Regenerate key if accidentally exposed
   - Prodigi: Regenerate key if accidentally exposed
   - Stripe: Can revoke and create new keys anytime

3. **FTP Password:**
   - Change after implementation if used
   - Or use SSH keys instead of password

4. **Database Password:**
   - Keep secure
   - Consider changing after implementation for production

---

## Timeline: How Fast Can You Gather These?

| Credential | Time | Difficulty |
|------------|------|------------|
| Database (from hosting) | 5 min | Easy - ask father-in-law |
| Stripe account | 10 min | Easy - sign up online |
| Stripe API keys | 5 min | Easy - dashboard |
| Print Space account | 10 min | Easy - sign up online |
| Print Space API key | 5 min | Easy - generate key |
| Prodigi account | 10 min | Easy - sign up online |
| Prodigi API key | 5 min | Easy - generate key |
| Test FTP connection | 10 min | Easy - verify access |
| **TOTAL** | **~60 min** | **Easy** |

---

## What Happens After You Gather These?

Once you provide all credentials:

**We proceed immediately to:**

1. ✅ Stage 1: Create `.env` file with your keys
2. ✅ Stage 2: Execute database schema
3. ✅ Stage 3: Upload API classes
4. ✅ Stage 4-7: Complete remaining stages

**Each stage will include:**
- Exact copy-paste code
- Specific upload instructions
- Testing procedures
- Confirmation of success

---

## Ready to Gather?

**Here's what to do now:**

### Immediately (Next 30 minutes):
1. Contact father-in-law for database credentials
2. Ask him to access cPanel and provide DB info
3. While waiting, create Stripe account
4. Create Print Space account
5. Create Prodigi account

### Next Step:
Reply to me with:

```
DATABASE:
Host: 
Database:
User:
Password:

STRIPE (TEST):
Public Key: 
Secret Key:
Webhook Secret:

PRINT SPACE:
API Key:

PRODIGI:
API Key:

FTP WORKS: YES / NO
```

**Or just say:** "Gathering credentials now, will send when ready"

---

## If You Get Stuck

**Common Issues:**

**"I can't find the database credentials"**
→ Ask hosting provider support or father-in-law to check cPanel

**"Stripe account creation won't accept my email"**
→ Use personal email + Stripe can send to info@mimmsphoto.com later

**"Print Space won't let me generate API key"**
→ Check account is verified (check email)

**"I don't see Merchant ID in Print Space/CreativeHub"**
→ That's normal! Merchant ID is optional. Just use the API Key.

**"Can't connect via FTP"**
→ Verify port number (21 vs 22)
→ Check credentials are correct
→ Try SFTP instead of FTP

**"I don't have SSH access"**
→ No problem - we'll use FTP for uploads

---

## Document Version

**Status:** Ready to use  
**Date:** January 3, 2026  
**Updated:** January 3, 2026 (Print Space Merchant ID noted as optional)
**Purpose:** Credential gathering for Stages 1-7 implementation

---

## Next Document in This Series

After gathering credentials → `Backend-Strategy.md` (Implementation)

---

**Questions about what you need to gather? Ask now before collecting credentials.**

Otherwise: **Go gather these credentials and come back with them. We'll implement immediately.**

We can do this in one focused 10-hour session or spread over 2-3 weeks. Your choice! 🚀