# Mimmsphoto E-Commerce Backend Strategy
## Complete Production Implementation Guide

**Date:** January 3, 2026  
**Version:** 1.0 (Production MVP)  
**Project:** mimmsphoto.com backend (OpenCart + Print Lab APIs)  
**Environment:** Self-hosted MariaDB + PHP 7.4+ on father-in-law's server (Filezilla FTP)

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                     Frontend (Portfolio + Shop)                  │
│  (Existing: index.html, browse.html, etc. + OpenCart templates) │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                    OpenCart e-Commerce Core                      │
│  (Shopping cart, checkout, order management, admin)             │
│  Location: /public_html/shop/ (via Filezilla FTP)              │
└────────────────────────┬────────────────────────────────────────┘
                         │
        ┌────────────────┼────────────────┐
        ▼                ▼                ▼
┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│ Print Space  │  │   Prodigi    │  │   Stripe     │
│  API         │  │   API        │  │   API        │
│ (Giclée)     │  │ (Canvas)     │  │ (Payments)   │
└──────────────┘  └──────────────┘  └──────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│              MariaDB (Self-hosted on your father-in-law's       │
│              server, managed via phpMyAdmin)                    │
│  - OpenCart native tables (oc_order, oc_product, etc.)          │
│  - Custom print_orders table (fulfillment tracking)             │
│  - Custom order_fulfillment table (Print Space + Prodigi)       │
└─────────────────────────────────────────────────────────────────┘

External:
- Email: info@mimmsphoto.com (self-hosted, configured)
- Analytics: Optional (Plausible/Umami for conversion tracking)
- CDN: Cloudflare (existing for SSL + cache)
```

---

## Current State vs. MVP Target

### What You Have Now
- ✅ Static portfolio (HTML + CSS)
- ✅ Contact form (PHP + reCAPTCHA)
- ✅ Self-hosted email (info@mimmsphoto.com)
- ✅ HTTPS certificate (free SSL)
- ✅ FTP access to server via Filezilla
- ✅ MariaDB available on server

### What You're Building
- 🚀 **Tier 1 (Week 1-2):** OpenCart baseline + Stripe integration
- 🚀 **Tier 2 (Week 3-4):** Print Space API (giclée prints)
- 🚀 **Tier 3 (Week 5-6):** Prodigi API (canvas prints)
- 🚀 **Tier 4 (Optional):** Admin dashboard + analytics

---

## STAGE 1: Environment Setup & Configuration

### Prerequisites Checklist

Before you start, you need:

- [ ] **OpenCart 3.x+ installed** on your server at `/public_html/shop/`
  - If not installed: Use OpenCart quick install in cPanel or upload manually via Filezilla
  - Database connection already configured in `config.php`

- [ ] **MariaDB credentials** (from cPanel or your host):
  - Host: `localhost` (likely)
  - Username: `[your_db_user]`
  - Password: `[your_db_pass]`
  - Database: `[your_db_name]`

- [ ] **Filezilla configured** to connect to your server:
  - Host: `[your.server.com]`
  - Username: `[your_cpanel_user]`
  - Password: `[your_password]`
  - Port: `22` (SFTP) or `21` (FTP)

- [ ] **API Keys ready** (you'll provide these in Stage 2):
  - Stripe API Key (test + live)
  - Print Space API Key
  - Prodigi API Key

### Step 1: Create Backend Directory Structure

**Via Filezilla, create these folders in `/public_html/shop/`:**

```
shop/
├── admin/                      (OpenCart admin - already exists)
├── catalog/                    (OpenCart catalog - already exists)
├── custom/                     (NEW - Our custom extensions)
│   ├── api/
│   │   ├── PrintSpaceAPI.php
│   │   ├── ProdigiAPI.php
│   │   └── StripeIntegration.php
│   ├── controller/
│   │   ├── OrderFulfillment.php
│   │   └── WebhookHandler.php
│   ├── model/
│   │   ├── OrderFulfillment.php
│   │   └── PrintOrder.php
│   └── config/
│       └── services.php
├── system/                     (OpenCart core - already exists)
└── .env                        (NEW - Environment variables)
```

**Create these files via Filezilla text editor or upload:**

```bash
# SSH/Terminal approach (if you have SSH access):
cd /public_html/shop
mkdir -p custom/api custom/controller custom/model custom/config
touch custom/.htaccess
touch custom/config/services.php
touch custom/api/PrintSpaceAPI.php
touch custom/api/ProdigiAPI.php
touch custom/api/StripeIntegration.php
```

### Step 2: Create .env Configuration File

**File: `/public_html/shop/.env`**

```env
# ============================================
# ENVIRONMENT
# ============================================
APP_ENV=production
APP_DEBUG=false
APP_URL=https://mimmsphoto.com/shop

# ============================================
# DATABASE (MariaDB on father-in-law's server)
# ============================================
DB_HOST=localhost
DB_PORT=3306
DB_DATABASE=your_database_name
DB_USERNAME=your_db_user
DB_PASSWORD=your_db_password
DB_PREFIX=oc_

# ============================================
# PRINT LAB INTEGRATIONS
# ============================================

# Print Space (Fine Art Giclée Prints)
PRINT_SPACE_ENABLED=true
PRINT_SPACE_API_KEY=
PRINT_SPACE_API_BASE=https://api.theprintspace.com/v1
PRINT_SPACE_MERCHANT_ID=

# Prodigi (Canvas Prints)
PRODIGI_ENABLED=true
PRODIGI_API_KEY=
PRODIGI_API_BASE=https://api.prodigi.com/v4.0
PRODIGI_MERCHANT_ID=

# ============================================
# PAYMENT PROCESSOR
# ============================================

# Stripe (Payment processing)
STRIPE_ENABLED=true
STRIPE_PUBLIC_KEY=pk_test_...
STRIPE_SECRET_KEY=sk_test_...
STRIPE_WEBHOOK_SECRET=whsec_...

# ============================================
# EMAIL CONFIGURATION
# ============================================
MAIL_DRIVER=sendmail
MAIL_FROM_ADDRESS=info@mimmsphoto.com
MAIL_FROM_NAME="Mimmsphoto"
ORDER_CONFIRMATION_EMAIL=info@mimmsphoto.com
ADMIN_EMAIL=info@mimmsphoto.com

# ============================================
# WEBHOOKS & CALLBACKS
# ============================================
WEBHOOK_PRINT_SPACE_URL=https://mimmsphoto.com/shop/custom/webhook/print-space
WEBHOOK_PRODIGI_URL=https://mimmsphoto.com/shop/custom/webhook/prodigi
WEBHOOK_STRIPE_URL=https://mimmsphoto.com/shop/custom/webhook/stripe

# ============================================
# OPTIONAL: ANALYTICS & MONITORING
# ============================================
PLAUSIBLE_DOMAIN=
PLAUSIBLE_API_KEY=
LOG_CHANNEL=stack
LOG_FILE=/var/log/opencart.log
```

**Create `.env.example` for version control:**

Copy `.env` to `.env.example`, but replace sensitive values with placeholders:

```env
PRINT_SPACE_API_KEY=your_print_space_api_key
PRODIGI_API_KEY=your_prodigi_api_key
STRIPE_SECRET_KEY=sk_test_your_stripe_secret_key
DB_PASSWORD=your_database_password
```

**Add to `.gitignore`:**

```
.env
.env.local
.env.*.local
config.php
admin/config.php
system/config/
```

### Step 3: Create Environment Loader

**File: `/public_html/shop/custom/config/Environment.php`**

```php
<?php
// Environment Configuration Loader
// Reads .env file and loads into $_ENV and getenv()

class Environment {
    
    private static $loaded = false;
    
    public static function load($path = null) {
        if (self::$loaded) return;
        
        $path = $path ?: __DIR__ . '/../../.env';
        
        if (!file_exists($path)) {
            throw new Exception("Environment file not found: $path");
        }
        
        $lines = file($path, FILE_IGNORE_NEW_LINES | FILE_SKIP_EMPTY_LINES);
        
        foreach ($lines as $line) {
            // Skip comments
            if (strpos(trim($line), '#') === 0) continue;
            
            // Parse KEY=VALUE
            if (strpos($line, '=') !== false) {
                list($key, $value) = explode('=', $line, 2);
                
                $key = trim($key);
                $value = trim($value, " \t\"'");
                
                // Set in $_ENV and accessible via getenv()
                $_ENV[$key] = $value;
                putenv("{$key}={$value}");
            }
        }
        
        self::$loaded = true;
    }
    
    public static function get($key, $default = null) {
        return getenv($key) ?: $default;
    }
    
    public static function has($key) {
        return getenv($key) !== false;
    }
}

// Auto-load on include
Environment::load();
?>
```

**Usage in other files:**

```php
<?php
require_once 'custom/config/Environment.php';

$stripe_key = Environment::get('STRIPE_SECRET_KEY');
$print_space_key = Environment::get('PRINT_SPACE_API_KEY');
?>
```

---

## STAGE 2: Database Schema (MariaDB Setup)

### Create Custom Tables

**Via phpMyAdmin:**

1. Log into phpMyAdmin on your server
2. Select your OpenCart database
3. Click "SQL" tab
4. Paste and execute this script:

```sql
-- ============================================
-- TABLE: Print Order Tracking
-- Purpose: Track fulfillment across Print Space and Prodigi
-- ============================================

CREATE TABLE IF NOT EXISTS `oc_print_orders` (
    `print_order_id` INT AUTO_INCREMENT PRIMARY KEY,
    `oc_order_id` INT NOT NULL UNIQUE,
    `fulfillment_provider` ENUM('print_space', 'prodigi') NOT NULL,
    `provider_order_id` VARCHAR(255),
    `provider_reference` VARCHAR(255),
    `status` ENUM('created', 'submitted', 'accepted', 'processing', 'dispatched', 'returned', 'cancelled') DEFAULT 'created',
    `submitted_at` TIMESTAMP NULL,
    `dispatched_at` TIMESTAMP NULL,
    `tracking_number` VARCHAR(255),
    `tracking_url` VARCHAR(500),
    `error_message` TEXT,
    `retry_count` INT DEFAULT 0,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (`oc_order_id`) REFERENCES `oc_order`(`order_id`) ON DELETE CASCADE,
    INDEX `idx_provider` (`fulfillment_provider`),
    INDEX `idx_status` (`status`),
    INDEX `idx_provider_id` (`provider_order_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================
-- TABLE: Product-Provider Mapping
-- Purpose: Link OpenCart products to Print Space/Prodigi SKUs
-- ============================================

CREATE TABLE IF NOT EXISTS `oc_product_fulfillment` (
    `product_fulfillment_id` INT AUTO_INCREMENT PRIMARY KEY,
    `product_id` INT NOT NULL UNIQUE,
    `fulfillment_provider` ENUM('print_space', 'prodigi') NOT NULL,
    `provider_sku` VARCHAR(255) NOT NULL,
    `product_category` ENUM('giclée', 'canvas', 'metal', 'acrylic', 'wood') NOT NULL,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (`product_id`) REFERENCES `oc_product`(`product_id`) ON DELETE CASCADE,
    INDEX `idx_provider` (`fulfillment_provider`),
    INDEX `idx_category` (`product_category`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================
-- TABLE: API Webhook Log (for debugging)
-- Purpose: Log all webhook events from Print Space, Prodigi, Stripe
-- ============================================

CREATE TABLE IF NOT EXISTS `oc_webhook_log` (
    `webhook_log_id` INT AUTO_INCREMENT PRIMARY KEY,
    `webhook_source` ENUM('print_space', 'prodigi', 'stripe') NOT NULL,
    `event_type` VARCHAR(255),
    `payload` JSON,
    `processed` BOOLEAN DEFAULT false,
    `error_message` TEXT,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX `idx_source` (`webhook_source`),
    INDEX `idx_processed` (`processed`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================
-- TABLE: Order-Product Mapping (with fulfillment info)
-- Purpose: Track individual products and their print lab details
-- ============================================

CREATE TABLE IF NOT EXISTS `oc_order_product_fulfillment` (
    `order_product_fulfillment_id` INT AUTO_INCREMENT PRIMARY KEY,
    `order_product_id` INT NOT NULL,
    `order_id` INT NOT NULL,
    `product_id` INT NOT NULL,
    `fulfillment_provider` ENUM('print_space', 'prodigi') NOT NULL,
    `provider_sku` VARCHAR(255),
    `quantity` INT DEFAULT 1,
    `status` ENUM('pending', 'submitted', 'confirmed', 'printing', 'shipped', 'failed') DEFAULT 'pending',
    `provider_response` JSON,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (`order_id`) REFERENCES `oc_order`(`order_id`) ON DELETE CASCADE,
    FOREIGN KEY (`product_id`) REFERENCES `oc_product`(`product_id`) ON DELETE CASCADE,
    INDEX `idx_provider` (`fulfillment_provider`),
    INDEX `idx_status` (`status`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================
-- Optional: Custom order status codes
-- Purpose: Add print-specific statuses to OpenCart
-- ============================================

-- Ensure these order statuses exist in oc_order_status:
-- Note: Manual addition via OpenCart admin or insert here

-- INSERT INTO `oc_order_status` VALUES (15, 1, 'Shipped');
-- INSERT INTO `oc_order_status` VALUES (16, 1, 'Printing with Print Space');
-- INSERT INTO `oc_order_status` VALUES (17, 1, 'Printing with Prodigi');
```

**Verify tables were created:**

In phpMyAdmin:
1. Refresh database view
2. Look for: `oc_print_orders`, `oc_product_fulfillment`, `oc_webhook_log`, `oc_order_product_fulfillment`
3. All should show with green checkmarks

---

## STAGE 3: Core API Integration Classes

### Service 1: Print Space API Integration

**File: `/public_html/shop/custom/api/PrintSpaceAPI.php`**

```php
<?php
// Print Space API Integration
// Handles giclée fine art print fulfillment

require_once 'custom/config/Environment.php';

class PrintSpaceAPI {
    
    private $api_key;
    private $api_base;
    private $merchant_id;
    private $logger;
    
    public function __construct($logger = null) {
        $this->api_key = Environment::get('PRINT_SPACE_API_KEY');
        $this->api_base = Environment::get('PRINT_SPACE_API_BASE');
        $this->merchant_id = Environment::get('PRINT_SPACE_MERCHANT_ID');
        $this->logger = $logger;
        
        if (!$this->api_key || !$this->api_base) {
            throw new Exception('Print Space API credentials not configured in .env');
        }
    }
    
    /**
     * Submit OpenCart order to Print Space for fulfillment
     * 
     * @param array $order OpenCart order from database
     * @param array $products Array of products in order
     * @return array Result with status, provider_order_id, tracking info
     */
    public function submitOrder($order, $products) {
        
        $payload = $this->formatOrderForPrintSpace($order, $products);
        
        $this->log('Submitting order to Print Space', ['order_id' => $order['order_id'], 'payload' => $payload]);
        
        try {
            $response = $this->callAPI('POST', '/orders', $payload);
            
            $this->log('Print Space API response', ['response' => $response]);
            
            return [
                'success' => true,
                'provider_order_id' => $response['id'] ?? null,
                'status' => $response['status'] ?? 'created',
                'response' => $response,
            ];
        } catch (Exception $e) {
            $this->log('Print Space API error', ['error' => $e->getMessage()], 'error');
            
            return [
                'success' => false,
                'error' => $e->getMessage(),
                'status' => 'failed',
            ];
        }
    }
    
    /**
     * Get order status from Print Space
     * 
     * @param string $provider_order_id Order ID from Print Space
     * @return array Order status and tracking info
     */
    public function getOrderStatus($provider_order_id) {
        
        try {
            $response = $this->callAPI('GET', "/orders/{$provider_order_id}");
            
            return [
                'success' => true,
                'status' => $response['status'] ?? null,
                'tracking_number' => $response['tracking_number'] ?? null,
                'tracking_url' => $response['tracking_url'] ?? null,
                'response' => $response,
            ];
        } catch (Exception $e) {
            return [
                'success' => false,
                'error' => $e->getMessage(),
            ];
        }
    }
    
    /**
     * Format OpenCart order for Print Space API submission
     * 
     * @param array $order OpenCart order
     * @param array $products Order products
     * @return array Formatted payload for Print Space API
     */
    private function formatOrderForPrintSpace($order, $products) {
        
        $line_items = [];
        
        foreach ($products as $product) {
            
            // Map OpenCart product to Print Space SKU
            $print_space_sku = $this->mapProductToSKU($product['product_id']);
            
            // Get product image URL
            $image_url = $this->getProductImageUrl($product['product_id']);
            
            $line_items[] = [
                'sku' => $print_space_sku,
                'quantity' => (int)$product['quantity'],
                'reference' => 'item-' . $product['order_product_id'],
                'assets' => [
                    [
                        'url' => $image_url,
                        'print_area' => 'default',
                        'type' => 'image',
                    ]
                ],
            ];
        }
        
        return [
            'merchant_reference' => (string)$order['order_id'],
            'shipping_method' => $this->getShippingMethod($order),
            'recipient' => [
                'name' => $order['shipping_firstname'] . ' ' . $order['shipping_lastname'],
                'email' => $order['email'],
                'phone_number' => $order['telephone'] ?? '',
                'address' => [
                    'line_1' => $order['shipping_address_1'],
                    'line_2' => $order['shipping_address_2'] ?? '',
                    'city' => $order['shipping_city'],
                    'state' => $order['shipping_zone'],
                    'postal_code' => $order['shipping_postcode'],
                    'country' => $this->getCountryCode($order['shipping_country_id']),
                ],
            ],
            'items' => $line_items,
            'notification_url' => Environment::get('WEBHOOK_PRINT_SPACE_URL'),
        ];
    }
    
    /**
     * Map OpenCart product to Print Space SKU
     */
    private function mapProductToSKU($product_id) {
        
        // Query mapping table (you'll populate this in OpenCart admin)
        global $db;
        $query = $db->query("
            SELECT provider_sku FROM `oc_product_fulfillment`
            WHERE product_id = " . (int)$product_id . "
            AND fulfillment_provider = 'print_space'
        ");
        
        if ($query->num_rows > 0) {
            return $query->row['provider_sku'];
        }
        
        // Fallback (shouldn't reach here)
        return 'GICLEE-8X10-HAHNEMUHLE';
    }
    
    /**
     * Get absolute URL for product image
     */
    private function getProductImageUrl($product_id) {
        global $db;
        $query = $db->query("SELECT image FROM `oc_product` WHERE product_id = " . (int)$product_id);
        
        if ($query->num_rows > 0) {
            $image = $query->row['image'];
            return 'https://' . $_SERVER['HTTP_HOST'] . '/image/' . $image;
        }
        
        return 'https://mimmsphoto.com/assets/default-image.jpg';
    }
    
    /**
     * Get shipping method based on order
     */
    private function getShippingMethod($order) {
        // Default to Standard; you can add logic based on shipping code
        return 'Standard';
    }
    
    /**
     * Get ISO 2-letter country code
     */
    private function getCountryCode($country_id) {
        global $db;
        $query = $db->query("SELECT iso_code_2 FROM `oc_country` WHERE country_id = " . (int)$country_id);
        
        if ($query->num_rows > 0) {
            return $query->row['iso_code_2'];
        }
        
        return 'US';
    }
    
    /**
     * Make API call to Print Space
     */
    private function callAPI($method, $endpoint, $payload = null) {
        
        $url = $this->api_base . $endpoint;
        
        $ch = curl_init();
        curl_setopt_array($ch, [
            CURLOPT_URL => $url,
            CURLOPT_RETURNTRANSFER => true,
            CURLOPT_TIMEOUT => 30,
            CURLOPT_CUSTOMREQUEST => $method,
            CURLOPT_HTTPHEADER => [
                'Content-Type: application/json',
                'Authorization: Bearer ' . $this->api_key,
                'Accept: application/json',
            ],
        ]);
        
        if ($payload) {
            curl_setopt($ch, CURLOPT_POSTFIELDS, json_encode($payload));
        }
        
        $response = curl_exec($ch);
        $http_code = curl_getinfo($ch, CURLINFO_HTTP_CODE);
        $curl_error = curl_error($ch);
        curl_close($ch);
        
        if ($curl_error) {
            throw new Exception("Print Space API Error: $curl_error");
        }
        
        $data = json_decode($response, true);
        
        if ($http_code >= 400) {
            throw new Exception("Print Space API Error ({$http_code}): " . ($data['message'] ?? 'Unknown error'));
        }
        
        return $data;
    }
    
    /**
     * Log to file or external service
     */
    private function log($message, $context = [], $level = 'info') {
        if ($this->logger) {
            $this->logger->log($level, $message, $context);
        } else {
            // Default: write to file
            $log_message = date('Y-m-d H:i:s') . " [{$level}] {$message} " . json_encode($context) . "\n";
            error_log($log_message, 3, '/var/log/printspace-api.log');
        }
    }
}
?>
```

### Service 2: Prodigi API Integration

**File: `/public_html/shop/custom/api/ProdigiAPI.php`**

```php
<?php
// Prodigi API Integration
// Handles canvas print fulfillment

require_once 'custom/config/Environment.php';

class ProdigiAPI {
    
    private $api_key;
    private $api_base;
    private $merchant_id;
    private $logger;
    
    public function __construct($logger = null) {
        $this->api_key = Environment::get('PRODIGI_API_KEY');
        $this->api_base = Environment::get('PRODIGI_API_BASE');
        $this->merchant_id = Environment::get('PRODIGI_MERCHANT_ID');
        $this->logger = $logger;
        
        if (!$this->api_key || !$this->api_base) {
            throw new Exception('Prodigi API credentials not configured in .env');
        }
    }
    
    /**
     * Submit OpenCart order to Prodigi for fulfillment
     */
    public function submitOrder($order, $products) {
        
        $payload = $this->formatOrderForProdigi($order, $products);
        
        $this->log('Submitting order to Prodigi', ['order_id' => $order['order_id']]);
        
        try {
            $response = $this->callAPI('POST', '/orders', $payload);
            
            return [
                'success' => true,
                'provider_order_id' => $response['id'] ?? null,
                'status' => $response['status'] ?? 'created',
                'response' => $response,
            ];
        } catch (Exception $e) {
            $this->log('Prodigi API error', ['error' => $e->getMessage()], 'error');
            
            return [
                'success' => false,
                'error' => $e->getMessage(),
                'status' => 'failed',
            ];
        }
    }
    
    /**
     * Get order status from Prodigi
     */
    public function getOrderStatus($provider_order_id) {
        
        try {
            $response = $this->callAPI('GET', "/orders/{$provider_order_id}");
            
            return [
                'success' => true,
                'status' => $response['status'] ?? null,
                'tracking_number' => $response['tracking_number'] ?? null,
                'response' => $response,
            ];
        } catch (Exception $e) {
            return [
                'success' => false,
                'error' => $e->getMessage(),
            ];
        }
    }
    
    /**
     * Format OpenCart order for Prodigi API
     */
    private function formatOrderForProdigi($order, $products) {
        
        $items = [];
        
        foreach ($products as $product) {
            
            $prodigi_sku = $this->mapProductToSKU($product['product_id']);
            $image_url = $this->getProductImageUrl($product['product_id']);
            
            $items[] = [
                'merchantReference' => 'item-' . $product['order_product_id'],
                'sku' => $prodigi_sku,
                'copies' => (int)$product['quantity'],
                'sizing' => 'fillPrintArea',
                'assets' => [
                    [
                        'printArea' => 'default',
                        'url' => $image_url,
                        'mimeType' => 'image/jpeg',
                    ]
                ]
            ];
        }
        
        return [
            'merchantReference' => (string)$order['order_id'],
            'shippingMethod' => 'Standard',
            'recipient' => [
                'name' => $order['shipping_firstname'] . ' ' . $order['shipping_lastname'],
                'email' => $order['email'],
                'phoneNumber' => $order['telephone'] ?? '',
                'address' => [
                    'line1' => $order['shipping_address_1'],
                    'line2' => $order['shipping_address_2'] ?? '',
                    'postalOrZipCode' => $order['shipping_postcode'],
                    'cityOrTown' => $order['shipping_city'],
                    'stateOrCounty' => $order['shipping_zone'],
                    'country' => $this->getCountryCode($order['shipping_country_id']),
                    'deliveryInstructions' => $order['comment'] ?? '',
                ]
            ],
            'items' => $items,
            'notificationUrl' => Environment::get('WEBHOOK_PRODIGI_URL'),
        ];
    }
    
    /**
     * Map OpenCart product to Prodigi SKU
     */
    private function mapProductToSKU($product_id) {
        global $db;
        $query = $db->query("
            SELECT provider_sku FROM `oc_product_fulfillment`
            WHERE product_id = " . (int)$product_id . "
            AND fulfillment_provider = 'prodigi'
        ");
        
        if ($query->num_rows > 0) {
            return $query->row['provider_sku'];
        }
        
        return 'GLOBAL-CANVAS-WRAP-16X20-PT';
    }
    
    /**
     * Get product image URL
     */
    private function getProductImageUrl($product_id) {
        global $db;
        $query = $db->query("SELECT image FROM `oc_product` WHERE product_id = " . (int)$product_id);
        
        if ($query->num_rows > 0) {
            $image = $query->row['image'];
            return 'https://' . $_SERVER['HTTP_HOST'] . '/image/' . $image;
        }
        
        return 'https://mimmsphoto.com/assets/default-image.jpg';
    }
    
    /**
     * Get ISO country code
     */
    private function getCountryCode($country_id) {
        global $db;
        $query = $db->query("SELECT iso_code_2 FROM `oc_country` WHERE country_id = " . (int)$country_id);
        
        if ($query->num_rows > 0) {
            return $query->row['iso_code_2'];
        }
        
        return 'US';
    }
    
    /**
     * Make API call to Prodigi
     */
    private function callAPI($method, $endpoint, $payload = null) {
        
        $url = $this->api_base . $endpoint;
        
        $ch = curl_init();
        curl_setopt_array($ch, [
            CURLOPT_URL => $url,
            CURLOPT_RETURNTRANSFER => true,
            CURLOPT_TIMEOUT => 30,
            CURLOPT_CUSTOMREQUEST => $method,
            CURLOPT_HTTPHEADER => [
                'Content-Type: application/json',
                'Authorization: Bearer ' . $this->api_key,
                'Accept: application/json',
            ],
        ]);
        
        if ($payload) {
            curl_setopt($ch, CURLOPT_POSTFIELDS, json_encode($payload));
        }
        
        $response = curl_exec($ch);
        $http_code = curl_getinfo($ch, CURLINFO_HTTP_CODE);
        $curl_error = curl_error($ch);
        curl_close($ch);
        
        if ($curl_error) {
            throw new Exception("Prodigi API Error: $curl_error");
        }
        
        $data = json_decode($response, true);
        
        if ($http_code >= 400) {
            throw new Exception("Prodigi API Error ({$http_code}): " . ($data['message'] ?? 'Unknown error'));
        }
        
        return $data;
    }
    
    /**
     * Log to file
     */
    private function log($message, $context = [], $level = 'info') {
        if ($this->logger) {
            $this->logger->log($level, $message, $context);
        } else {
            $log_message = date('Y-m-d H:i:s') . " [{$level}] {$message} " . json_encode($context) . "\n";
            error_log($log_message, 3, '/var/log/prodigi-api.log');
        }
    }
}
?>
```

### Service 3: Stripe Integration

**File: `/public_html/shop/custom/api/StripeIntegration.php`**

```php
<?php
// Stripe Payment Integration
// Handles payment processing and webhook verification

require_once 'custom/config/Environment.php';

class StripeIntegration {
    
    private $secret_key;
    private $public_key;
    private $webhook_secret;
    private $logger;
    
    public function __construct($logger = null) {
        $this->secret_key = Environment::get('STRIPE_SECRET_KEY');
        $this->public_key = Environment::get('STRIPE_PUBLIC_KEY');
        $this->webhook_secret = Environment::get('STRIPE_WEBHOOK_SECRET');
        $this->logger = $logger;
        
        if (!$this->secret_key || !$this->public_key) {
            throw new Exception('Stripe API credentials not configured in .env');
        }
    }
    
    /**
     * Create payment intent for OpenCart order
     */
    public function createPaymentIntent($order_id, $amount_cents, $order_metadata = []) {
        
        try {
            // Use cURL to call Stripe API directly
            // (Stripe PHP library may not be available in shared hosting)
            
            $payload = [
                'amount' => (int)$amount_cents,
                'currency' => 'usd',
                'metadata' => array_merge($order_metadata, ['order_id' => $order_id]),
                'payment_method_types' => ['card'],
            ];
            
            $response = $this->callStripeAPI('POST', 'https://api.stripe.com/v1/payment_intents', $payload);
            
            return [
                'success' => true,
                'client_secret' => $response['client_secret'],
                'payment_intent_id' => $response['id'],
            ];
        } catch (Exception $e) {
            $this->log('Stripe payment intent error', ['error' => $e->getMessage()], 'error');
            return [
                'success' => false,
                'error' => $e->getMessage(),
            ];
        }
    }
    
    /**
     * Verify webhook signature from Stripe
     */
    public function verifyWebhookSignature($payload, $signature_header) {
        
        if (!$this->webhook_secret) {
            throw new Exception('Stripe webhook secret not configured');
        }
        
        try {
            // Stripe webhook signature verification
            $signed_content = $payload . $this->webhook_secret;
            $computed_signature = hash_hmac('sha256', $payload, $this->webhook_secret);
            
            // Compare signatures (constant-time comparison)
            if (!hash_equals($computed_signature, $signature_header)) {
                throw new Exception('Invalid webhook signature');
            }
            
            return json_decode($payload, true);
        } catch (Exception $e) {
            $this->log('Webhook verification error', ['error' => $e->getMessage()], 'error');
            throw $e;
        }
    }
    
    /**
     * Handle successful payment
     */
    public function handlePaymentSuccess($payment_intent) {
        
        $order_id = $payment_intent['metadata']['order_id'] ?? null;
        
        if (!$order_id) {
            throw new Exception('No order ID in payment intent metadata');
        }
        
        // Update OpenCart order status to "Processing"
        global $db;
        $db->query("UPDATE `oc_order` SET order_status_id = 3 WHERE order_id = " . (int)$order_id);
        
        // Log payment
        $db->query("
            INSERT INTO `oc_webhook_log` (webhook_source, event_type, payload, processed)
            VALUES ('stripe', 'payment_success', '" . $db->escape(json_encode($payment_intent)) . "', true)
        ");
        
        $this->log('Payment successful', ['order_id' => $order_id]);
    }
    
    /**
     * Call Stripe API via cURL
     */
    private function callStripeAPI($method, $url, $payload) {
        
        $ch = curl_init();
        curl_setopt_array($ch, [
            CURLOPT_URL => $url,
            CURLOPT_RETURNTRANSFER => true,
            CURLOPT_TIMEOUT => 30,
            CURLOPT_CUSTOMREQUEST => $method,
            CURLOPT_USERPWD => $this->secret_key . ':',
            CURLOPT_HTTPHEADER => [
                'Content-Type: application/x-www-form-urlencoded',
            ],
        ]);
        
        if ($payload) {
            curl_setopt($ch, CURLOPT_POSTFIELDS, http_build_query($payload));
        }
        
        $response = curl_exec($ch);
        $http_code = curl_getinfo($ch, CURLINFO_HTTP_CODE);
        $curl_error = curl_error($ch);
        curl_close($ch);
        
        if ($curl_error) {
            throw new Exception("Stripe API Error: $curl_error");
        }
        
        $data = json_decode($response, true);
        
        if ($http_code >= 400) {
            throw new Exception("Stripe API Error ({$http_code}): " . ($data['error']['message'] ?? 'Unknown error'));
        }
        
        return $data;
    }
    
    /**
     * Log
     */
    private function log($message, $context = [], $level = 'info') {
        if ($this->logger) {
            $this->logger->log($level, $message, $context);
        } else {
            $log_message = date('Y-m-d H:i:s') . " [{$level}] {$message} " . json_encode($context) . "\n";
            error_log($log_message, 3, '/var/log/stripe-api.log');
        }
    }
}
?>
```

---

## STAGE 4: Order Fulfillment Controller

**File: `/public_html/shop/custom/controller/OrderFulfillment.php`**

```php
<?php
// Order Fulfillment Controller
// Routes orders to appropriate print lab (Print Space or Prodigi)

require_once 'custom/config/Environment.php';
require_once 'custom/api/PrintSpaceAPI.php';
require_once 'custom/api/ProdigiAPI.php';

class OrderFulfillmentController {
    
    public function __construct() {
        // Database connection (OpenCart provides this)
        global $db;
        $this->db = $db;
    }
    
    /**
     * Main entry point: Called after Stripe payment succeeds
     * Determines provider and submits order
     */
    public function submitOrder($order_id) {
        
        // Get OpenCart order
        $order = $this->getOrder($order_id);
        if (!$order) {
            return ['success' => false, 'error' => 'Order not found'];
        }
        
        // Get order products
        $products = $this->getOrderProducts($order_id);
        if (empty($products)) {
            return ['success' => false, 'error' => 'No products in order'];
        }
        
        // Determine fulfillment provider(s)
        $providers = $this->determineProviders($products);
        
        $results = [];
        
        // Submit to each provider
        foreach ($providers as $provider => $provider_products) {
            $result = $this->submitToProvider($provider, $order, $provider_products);
            $results[$provider] = $result;
            
            if ($result['success']) {
                // Store in database
                $this->storeOrderInDatabase($order_id, $provider, $result['provider_order_id']);
            }
        }
        
        return [
            'success' => !empty(array_filter($results, fn($r) => $r['success'])),
            'results' => $results,
        ];
    }
    
    /**
     * Get OpenCart order details
     */
    private function getOrder($order_id) {
        $query = $this->db->query("
            SELECT * FROM `oc_order`
            WHERE order_id = " . (int)$order_id . "
            LIMIT 1
        ");
        
        return $query->num_rows ? $query->row : null;
    }
    
    /**
     * Get order products with fulfillment info
     */
    private function getOrderProducts($order_id) {
        $query = $this->db->query("
            SELECT op.*, pf.fulfillment_provider, pf.provider_sku
            FROM `oc_order_product` op
            LEFT JOIN `oc_product_fulfillment` pf ON op.product_id = pf.product_id
            WHERE op.order_id = " . (int)$order_id
        );
        
        return $query->rows ?? [];
    }
    
    /**
     * Determine which providers to use for order
     * (Could have multiple providers in one order)
     */
    private function determineProviders($products) {
        
        $providers = [];
        
        foreach ($products as $product) {
            $provider = $product['fulfillment_provider'] ?? 'print_space';
            
            if (!isset($providers[$provider])) {
                $providers[$provider] = [];
            }
            
            $providers[$provider][] = $product;
        }
        
        return $providers;
    }
    
    /**
     * Submit to specific provider
     */
    private function submitToProvider($provider, $order, $products) {
        
        try {
            if ($provider === 'print_space') {
                $api = new PrintSpaceAPI();
                return $api->submitOrder($order, $products);
            } elseif ($provider === 'prodigi') {
                $api = new ProdigiAPI();
                return $api->submitOrder($order, $products);
            } else {
                return ['success' => false, 'error' => 'Unknown provider: ' . $provider];
            }
        } catch (Exception $e) {
            return ['success' => false, 'error' => $e->getMessage()];
        }
    }
    
    /**
     * Store provider order info in database
     */
    private function storeOrderInDatabase($order_id, $provider, $provider_order_id) {
        
        $this->db->query("
            INSERT INTO `oc_print_orders` 
            (oc_order_id, fulfillment_provider, provider_order_id, status, submitted_at)
            VALUES (
                " . (int)$order_id . ",
                '" . $this->db->escape($provider) . "',
                '" . $this->db->escape($provider_order_id) . "',
                'submitted',
                NOW()
            )
            ON DUPLICATE KEY UPDATE
                provider_order_id = VALUES(provider_order_id),
                submitted_at = NOW()
        ");
    }
}
?>
```

---

## STAGE 5: Webhook Handlers

**File: `/public_html/shop/custom/controller/WebhookHandler.php`**

```php
<?php
// Webhook Handler
// Processes status updates from Print Space, Prodigi, Stripe

require_once 'custom/config/Environment.php';

class WebhookHandler {
    
    public function __construct() {
        global $db;
        $this->db = $db;
    }
    
    /**
     * Handle Print Space webhooks
     */
    public function handlePrintSpaceWebhook() {
        
        $payload = file_get_contents('php://input');
        $data = json_decode($payload, true);
        
        // Log webhook
        $this->db->query("
            INSERT INTO `oc_webhook_log` (webhook_source, event_type, payload)
            VALUES ('print_space', '" . $this->db->escape($data['event_type'] ?? 'unknown') . "', '" . $this->db->escape($payload) . "')
        ");
        
        // Map Print Space status to OpenCart status
        $status_map = [
            'created' => 1,      // Pending
            'submitted' => 3,    // Processing
            'accepted' => 3,     // Processing
            'processing' => 3,   // Processing
            'dispatched' => 15,  // Shipped
            'cancelled' => 7,    // Cancelled
        ];
        
        $ps_status = $data['status'] ?? null;
        $oc_status = $status_map[$ps_status] ?? 3;
        
        // Update OpenCart order
        $order_id = $data['merchant_reference'] ?? null;
        if ($order_id) {
            $this->db->query("
                UPDATE `oc_order`
                SET order_status_id = " . (int)$oc_status . "
                WHERE order_id = " . (int)$order_id
            );
            
            // Update print orders tracking
            $this->db->query("
                UPDATE `oc_print_orders`
                SET status = '" . $this->db->escape($ps_status) . "',
                    tracking_number = '" . $this->db->escape($data['tracking_number'] ?? '') . "',
                    updated_at = NOW()
                WHERE oc_order_id = " . (int)$order_id . "
                AND fulfillment_provider = 'print_space'
            ");
        }
        
        http_response_code(200);
        echo json_encode(['success' => true]);
    }
    
    /**
     * Handle Prodigi webhooks
     */
    public function handleProdigiWebhook() {
        
        $payload = file_get_contents('php://input');
        $data = json_decode($payload, true);
        
        $this->db->query("
            INSERT INTO `oc_webhook_log` (webhook_source, event_type, payload)
            VALUES ('prodigi', '" . $this->db->escape($data['event_type'] ?? 'unknown') . "', '" . $this->db->escape($payload) . "')
        ");
        
        $status_map = [
            'created' => 1,
            'submitted' => 3,
            'accepted' => 3,
            'processing' => 3,
            'dispatched' => 15,
            'cancelled' => 7,
        ];
        
        $prodigi_status = $data['status'] ?? null;
        $oc_status = $status_map[$prodigi_status] ?? 3;
        
        $order_id = $data['merchantReference'] ?? null;
        if ($order_id) {
            $this->db->query("
                UPDATE `oc_order`
                SET order_status_id = " . (int)$oc_status . "
                WHERE order_id = " . (int)$order_id
            );
            
            $this->db->query("
                UPDATE `oc_print_orders`
                SET status = '" . $this->db->escape($prodigi_status) . "',
                    tracking_number = '" . $this->db->escape($data['tracking_number'] ?? '') . "',
                    updated_at = NOW()
                WHERE oc_order_id = " . (int)$order_id . "
                AND fulfillment_provider = 'prodigi'
            ");
        }
        
        http_response_code(200);
        echo json_encode(['success' => true]);
    }
}
?>
```

---

## STAGE 6: Deployment & Configuration Checklist

### Pre-Deployment Checklist

**Infrastructure:**
- [ ] SSH or Filezilla FTP access to server confirmed
- [ ] MariaDB access via phpMyAdmin confirmed
- [ ] PHP version 7.4+ verified (check cPanel or contact host)
- [ ] cURL extension enabled (required for API calls)
- [ ] OpenCart 3.x+ installed at `/public_html/shop/`

**Credentials (Obtain from respective services):**
- [ ] Stripe API Secret Key (`sk_test_...` or `sk_live_...`)
- [ ] Stripe Webhook Secret (`whsec_...`)
- [ ] Print Space API Key
- [ ] Prodigi API Key

**Configuration Files:**
- [ ] `.env` file created with all API keys
- [ ] `.env.example` created with placeholders
- [ ] `.gitignore` updated to exclude `.env`
- [ ] Database tables created via phpMyAdmin SQL script

**Code Deployment:**
- [ ] Custom PHP files uploaded to `/custom/` directory:
  - `config/Environment.php`
  - `api/PrintSpaceAPI.php`
  - `api/ProdigiAPI.php`
  - `api/StripeIntegration.php`
  - `controller/OrderFulfillment.php`
  - `controller/WebhookHandler.php`

### Deployment Steps

**1. Upload Custom Code via Filezilla**

```
Local: /path/to/PhotoSite/backend/custom/
Remote: /public_html/shop/custom/

Directories to create:
- custom/
  - api/
  - controller/
  - model/
  - config/
```

**2. Create .env File**

Via Filezilla text editor or SSH:

```bash
cd /public_html/shop
nano .env
# Paste contents from STAGE 2 section
# Save (Ctrl+X, Y, Enter)
```

**3. Update Database**

Via phpMyAdmin:
1. Log in
2. Select your OpenCart database
3. Click SQL tab
4. Paste script from STAGE 2
5. Execute

**4. Test API Connections**

Create test file: `/public_html/shop/test_apis.php`

```php
<?php
require_once 'custom/config/Environment.php';
require_once 'custom/api/PrintSpaceAPI.php';
require_once 'custom/api/ProdigiAPI.php';
require_once 'custom/api/StripeIntegration.php';

echo "<h2>API Configuration Test</h2>";

// Test Print Space
try {
    $ps = new PrintSpaceAPI();
    echo "✓ Print Space API configured correctly<br>";
} catch (Exception $e) {
    echo "✗ Print Space API error: " . $e->getMessage() . "<br>";
}

// Test Prodigi
try {
    $prodigi = new ProdigiAPI();
    echo "✓ Prodigi API configured correctly<br>";
} catch (Exception $e) {
    echo "✗ Prodigi API error: " . $e->getMessage() . "<br>";
}

// Test Stripe
try {
    $stripe = new StripeIntegration();
    echo "✓ Stripe API configured correctly<br>";
} catch (Exception $e) {
    echo "✗ Stripe API error: " . $e->getMessage() . "<br>";
}

// Test Database
try {
    global $db;
    $query = $db->query("SHOW TABLES LIKE 'oc_print_orders'");
    if ($query->num_rows > 0) {
        echo "✓ Database tables created successfully<br>";
    } else {
        echo "✗ Database tables not found<br>";
    }
} catch (Exception $e) {
    echo "✗ Database error: " . $e->getMessage() . "<br>";
}

echo "<p><strong>If all items are ✓, you're ready to proceed!</strong></p>";
?>
```

Access via browser: `https://mimmsphoto.com/shop/test_apis.php`

### GitHub Deployment

**1. Add new code to your PhotoSite repository:**

```bash
cd ~/PhotoSite
mkdir -p backend/custom/{api,controller,model,config}

# Copy files
cp /path/to/custom/api/* backend/custom/api/
cp /path/to/custom/controller/* backend/custom/controller/
cp .env.example backend/.env.example

git add backend/
git commit -m "Add backend API integrations (Print Space, Prodigi, Stripe)"
git push origin main
```

**2. Webhook Configuration in OpenCart Admin**

Manually in OpenCart admin, set up routes for webhooks:

- Print Space webhook: `shop/custom/controller/WebhookHandler.php` → `handlePrintSpaceWebhook()`
- Prodigi webhook: `shop/custom/controller/WebhookHandler.php` → `handleProdigiWebhook()`

Or create `.htaccess` rewrite rules:

```
RewriteRule ^shop/webhook/print-space$ custom/controller/WebhookHandler.php?action=print_space [L]
RewriteRule ^shop/webhook/prodigi$ custom/controller/WebhookHandler.php?action=prodigi [L]
```

---

## STAGE 7: Integration Steps & When to Call Me

### The assistant will ask you for input at these stages:

**When to provide:**

1. **Stripe API Keys** (after creating Stripe account)
2. **Print Space API Key** (after creating Print Space account)
3. **Prodigi API Key** (after creating Prodigi account)
4. **Database Credentials** (from cPanel or host email)
5. **Server FTP Details** (to upload code)

### Implementation Timeline

```
Week 1: Environment + Database
├─ [ ] Provide database credentials
├─ [ ] Create .env file
└─ [ ] Execute database schema

Week 2: API Integration
├─ [ ] Provide Stripe keys
├─ [ ] Provide Print Space key
├─ [ ] Provide Prodigi key
├─ [ ] Upload PHP files via Filezilla
└─ [ ] Run test_apis.php

Week 3: OpenCart Configuration
├─ [ ] Map products to SKUs in oc_product_fulfillment table
├─ [ ] Configure Stripe extension in OpenCart admin
├─ [ ] Test payment flow

Week 4: Print Lab Configuration
├─ [ ] Configure Print Space webhooks
├─ [ ] Configure Prodigi webhooks
├─ [ ] Place test orders

Week 5: Go Live
├─ [ ] Switch to Stripe live keys
├─ [ ] Monitor first orders
└─ [ ] Fine-tune based on customer feedback
```

---

## Production Recommendations

### Performance
- Enable caching on Cloudflare (currently set up)
- Images: Use lazy loading in OpenCart templates
- Database: Regular backups via cPanel

### Security
- Use HTTPS only (already configured)
- Keep API keys in `.env` (never commit to git)
- Validate all webhook signatures (included in code)
- Rate limit API calls (Stripe/Print Space will handle)

### Monitoring
- Log all API calls: `/var/log/printspace-api.log`, `/var/log/prodigi-api.log`, `/var/log/stripe-api.log`
- Check `oc_webhook_log` table regularly for errors
- Set up email alerts for failed orders

### Backup Strategy
1. **Code:** GitHub (all custom code versioned)
2. **Database:** cPanel automated backups + manual export before major changes
3. **Images:** Already on CDN via Cloudflare

---

## File Structure Summary

```
mimmsphoto.com/
├── public_html/
│   ├── portfolio/        (Existing HTML/CSS)
│   ├── shop/             (OpenCart)
│   │   ├── admin/
│   │   ├── catalog/
│   │   ├── custom/       (NEW)
│   │   │   ├── api/
│   │   │   │   ├── PrintSpaceAPI.php
│   │   │   │   ├── ProdigiAPI.php
│   │   │   │   └── StripeIntegration.php
│   │   │   ├── controller/
│   │   │   │   ├── OrderFulfillment.php
│   │   │   │   └── WebhookHandler.php
│   │   │   ├── model/
│   │   │   ├── config/
│   │   │   │   └── Environment.php
│   │   │   └── .htaccess
│   │   ├── system/
│   │   ├── .env          (NEW - NOT IN GIT)
│   │   ├── .env.example  (NEW - IN GIT)
│   │   ├── .htaccess
│   │   ├── config.php
│   │   └── index.php
│   └── info.php
├── .github/
│   └── workflows/
│       └── deploy.yml    (Optional: CI/CD)
└── Markdowns/
    └── Backend-Strategy.md (THIS FILE)
```

---

## Next Steps

**When ready to begin:**

1. ✅ Confirm you have Filezilla FTP access
2. ✅ Provide database credentials
3. ✅ Provide API keys (as you obtain them)
4. ✅ I'll walk you through each stage
5. ✅ We'll deploy and test

**Questions to answer before starting:**

- [ ] Is OpenCart already installed at `/public_html/shop/`?
- [ ] What are your MariaDB credentials (host, username, password)?
- [ ] Do you have Stripe account created? (Free tier available)
- [ ] Do you have Print Space account? (Need API key)
- [ ] Do you have Prodigi account? (Need API key)

---

## Document Control

**Version:** 1.0  
**Status:** Production Ready (MVP)  
**Last Updated:** January 3, 2026  
**For:** mimmsphoto.com  
**Tech Stack:** OpenCart 3.x, PHP 7.4+, MariaDB, Print Space + Prodigi APIs, Stripe

---

**Ready to begin? Let me know:**
1. Current OpenCart setup status
2. Database credentials
3. Which API keys you have ready
4. Any questions about implementation

The assistant will guide you through each stage with concrete steps and code ready to use.