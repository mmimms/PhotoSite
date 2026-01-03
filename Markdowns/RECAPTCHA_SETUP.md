# Google reCAPTCHA v3 Setup Guide

This guide walks you through integrating Google reCAPTCHA v3 into your contact form for bot protection.

## Overview

**reCAPTCHA v3** is an invisible verification system that:
- Analyzes user behavior and returns a **risk score** (0.0 to 1.0)
- Requires **no user interaction** (unlike checkbox CAPTCHAs)
- Is free for up to 1 million assessments/month
- Works seamlessly with your existing form infrastructure

## Step 1: Get Your reCAPTCHA Keys

### Access Google reCAPTCHA Admin Console

1. Go to [Google reCAPTCHA Admin Console](https://www.google.com/recaptcha/admin)
2. Sign in with your Google account (or create one)
3. Click the **+** button to register a new site

### Configure Your Site

**Settings:**
- **Label**: `Mark's Photography Contact Form` (or similar)
- **reCAPTCHA type**: Select **reCAPTCHA v3**
- **Domains**: 
  - Add your production domain: `mimmsphoto.com`
  - Add `www.mimmsphoto.com` (with www)
  - Add `localhost` for local testing

4. Accept the reCAPTCHA Terms of Service
5. Click **Submit**
6. **IMPORTANT**: Verify the checkbox **"Verify the origin of reCAPTCHA solutions"** is enabled

### Copy Your Keys

After registration, you'll see:
- **Site Key** (public) - goes in `contact.html`
- **Secret Key** (private) - goes in `.env` file

⚠️ **IMPORTANT**: Never commit your Secret Key to GitHub. It's already in `.gitignore`.

## Step 2: Update Your Local Configuration

### 1. Create `.env` file from template

```bash
cp .env.example .env
```

### 2. Edit `.env` with your keys

```bash
# .env
RECAPTCHA_SITE_KEY=6LfPYD4sAAAAAPRMlxjWVUfcCqf71v00nsoikDH_
RECAPTCHA_SECRET_KEY=6LfPYD4sAAAAAKtx...your_secret_key_here...
RECAPTCHA_THRESHOLD=0.5
CONTACT_EMAIL=mark.o.mimms@gmail.com
CONTACT_FROM_EMAIL=no-reply@mimmsphoto.com
```

**Score Threshold Explained:**
- `1.0` = Very likely human
- `0.5` = Balanced (recommended)
- `0.0` = Very likely bot

For most sites, `0.5` is a good starting point. Adjust based on your spam statistics.

### 3. Update `contact.html` with your Site Key

**CRITICAL FIX**: The reCAPTCHA v3 script loader must use the `render` parameter with your site key.

Find this line in `contact.html`:

```html
<script src="https://www.google.com/recaptcha/api.js?render=explicit" async defer></script>
```

**Replace it with** (using your actual Site Key):

```html
<script src="https://www.google.com/recaptcha/api.js?render=6LfPYD4sAAAAAPRMlxjWVUfcCqf71v00nsoikDH_" async defer></script>
```

**Why this matters:**
- `?render=explicit` is for reCAPTCHA v2 checkbox mode (WRONG)
- `?render=YOUR_SITE_KEY` is for reCAPTCHA v3 silent mode (CORRECT)
- Without this fix, you'll get "Invalid site key" errors

Also ensure your JavaScript constant matches:

```javascript
const RECAPTCHA_SITE_KEY = '6LfPYD4sAAAAAPRMlxjWVUfcCqf71v00nsoikDH_';
```

Then the form submission flow:

```javascript
const token = await grecaptcha.execute(RECAPTCHA_SITE_KEY, { action: 'submit' });
```

## Step 3: Verify It Works

### Local Testing

1. Start your local server:
   ```bash
   # Using PHP built-in server
   php -S localhost:8000
   ```

2. Open `http://localhost:8000/contact.html`

3. Fill out the form and submit

4. Check browser console (F12) for:
   - ✅ `"reCAPTCHA script loaded successfully"`
   - ✅ `"grecaptcha object available and ready"`
   - ✅ `"Requesting reCAPTCHA token from Google..."`
   - ✅ `"reCAPTCHA token received: 0CAFc..."`
   - ✅ `"Sending form data to contact.php"`
   - ✅ `{ success: true, message: "Thank you! Your message has been sent successfully." }`

5. Check your email inbox for the test message

### What to Look For

- ✅ Form submits without clicking a CAPTCHA checkbox
- ✅ You receive the contact email
- ✅ Green success notification appears
- ✅ No red error banner
- ✅ Console shows token received and form sent

### Troubleshooting

**Red error banner: "Error: Invalid site key or not loaded in api.js"**
- Check script tag uses `?render=YOUR_SITE_KEY` (not `?render=explicit`)
- Verify Site Key is correct in both:
  - `contact.html` script src
  - JavaScript `RECAPTCHA_SITE_KEY` constant
- Ensure both `www.mimmsphoto.com` and `mimmsphoto.com` are in Google reCAPTCHA domains
- Hard refresh browser (Ctrl+Shift+R)
- Wait 5-10 minutes for Google's DNS propagation

**"reCAPTCHA token missing" error:**
- Verify the Site Key is correct in both places
- Check browser console for network errors
- Ensure `grecaptcha` object is available

**"reCAPTCHA verification failed" error:**
- Verify Secret Key is correct in `.env`
- Ensure `.env` file exists in same directory as `contact.php`
- Check that `curl` or `allow_url_fopen` is enabled on your server
- Check server error logs for Google API responses

**Email not received:**
- Check `CONTACT_EMAIL` in `.env`
- Look in spam/junk folder
- Check server mail logs: `tail -f /var/log/mail.log`

## Step 4: Deploy to Production

### Before Deploying

1. **Do NOT commit `.env`** (it's in `.gitignore`)
2. **Create `.env` on production server manually**
3. **Update production domain in Google reCAPTCHA Admin Console**
4. **Ensure script tag in `contact.html` has correct Site Key in render parameter**

### Deployment Steps

1. Pull latest code from GitHub:
   ```bash
   git pull origin main
   ```

2. Create `.env` on production server:
   ```bash
   nano .env
   ```
   
   Copy from `.env.example` and fill in your production values

3. Set proper permissions:
   ```bash
   chmod 600 .env  # Only owner can read
   ```

4. Verify `.env` is in `.gitignore`:
   ```bash
   cat .gitignore | grep "^.env"
   ```

5. Test the form on your live domain

## How It Works

### User Submits Form

```
┌─────────────┐
│ User fills  │
│ contact form│
└──────┬──────┘
       │
       ▼
┌──────────────────┐
│ Browser loads    │
│ reCAPTCHA script │
│ with site key    │
└──────┬───────────┘
       │
       ▼
┌──────────────────┐
│ grecaptcha.      │
│ execute() called │
│ with action      │
└──────┬───────────┘
       │
       ▼
┌──────────────────┐
│ Google returns   │
│ authentication   │
│ token            │
└──────┬───────────┘
       │
       ▼
┌──────────────────┐
│ Form submits     │
│ with token to    │
│ contact.php      │
└──────┬───────────┘
       │
       ▼
┌──────────────────┐
│ contact.php      │
│ verifies token   │
│ with Google      │
└──────┬───────────┘
       │
       ▼
┌──────────────────┐
│ Score received   │
│ Checked against  │
│ threshold        │
└──────┬───────────┘
       │
       ├─ Score >= 0.5 ──► Send email ✓
       │
       └─ Score < 0.5 ──► Reject as bot ✗
```

## Configuration Reference

### `.env` Variables

| Variable | Description | Example |
|----------|-------------|----------|
| `RECAPTCHA_SITE_KEY` | Public key for client-side | `6LfPYD4sAAAAAPRM...` |
| `RECAPTCHA_SECRET_KEY` | Private key for server verification | `6LfPYD4sAAAAAKtx...` |
| `RECAPTCHA_THRESHOLD` | Score threshold (0.0-1.0) | `0.5` |
| `CONTACT_EMAIL` | Where to send contact messages | `mark@example.com` |
| `CONTACT_FROM_EMAIL` | From address for emails | `no-reply@example.com` |

### Code Files Updated

1. **`contact.html`**
   - Loads Google reCAPTCHA v3 script with site key in render parameter
   - Requests token on form submission via `grecaptcha.execute()`
   - Sends token to PHP backend

2. **`contact.php`**
   - Loads `.env` configuration
   - Verifies token with Google API
   - Checks score against threshold
   - Sends email only if verified

3. **`.env.example`**
   - Template for configuration
   - Document your setup

## Security Notes

✅ **What This Protects**
- Automated form spam bots
- Simple scripted attacks
- Behavior-based threats

⚠️ **What This Doesn't Protect**
- Determined human attackers
- Sophisticated bot networks
- SQL injection (still use input validation)
- XSS attacks (still sanitize output)

**Recommendation**: Combine reCAPTCHA v3 with:
- Input validation (already in place)
- Rate limiting (consider adding)
- Email verification (consider adding)
- Honeypot field (already in place)

## Monitoring

### Check Analytics in Google Admin Console

1. Go to [reCAPTCHA Admin Console](https://www.google.com/recaptcha/admin)
2. Select your site
3. View analytics:
   - Request volume
   - Score distribution
   - Detected bot attempts

### Adjust Threshold if Needed

- **Too strict** (many legitimate users blocked):
  - Lower threshold: `0.5` → `0.3`
  - Review false positives in analytics

- **Too lenient** (many bots getting through):
  - Raise threshold: `0.5` → `0.7`
  - Consider additional validation

## Resources

- [Google reCAPTCHA Documentation](https://developers.google.com/recaptcha/docs/v3)
- [reCAPTCHA Admin Console](https://www.google.com/recaptcha/admin)
- [reCAPTCHA Verification API](https://developers.google.com/recaptcha/docs/verify)
- [reCAPTCHA Implementation Guide](https://developers.google.com/recaptcha/docs/implicit_consent)

## Support

For issues:

1. Check the **Troubleshooting** section above
2. Review browser console (F12 > Console tab)
3. Check `.env` file permissions and values
4. Verify BOTH domains (with and without www) are registered in Google reCAPTCHA Admin Console
5. Verify script src uses `?render=YOUR_SITE_KEY` (not `?render=explicit`)
6. Check server error logs: `tail -f /var/log/php-errors.log`
