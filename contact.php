<?php
// Load environment variables from .env file
function load_env_file($filepath = '.env') {
    if (!file_exists($filepath)) {
        return false;
    }
    $lines = file($filepath, FILE_IGNORE_NEW_LINES | FILE_SKIP_EMPTY_LINES);
    foreach ($lines as $line) {
        if (strpos(trim($line), '#') === 0) {
            continue; // Skip comments
        }
        if (strpos($line, '=') !== false) {
            list($key, $value) = explode('=', $line, 2);
            $key = trim($key);
            $value = trim($value);
            putenv("$key=$value");
        }
    }
    return true;
}

// Load environment variables
load_env_file();

// Get configuration from environment variables
$recaptcha_secret = getenv('RECAPTCHA_SECRET_KEY');
$recaptcha_threshold = (float) getenv('RECAPTCHA_THRESHOLD') ?: 0.5;
$contact_email = getenv('CONTACT_EMAIL');
$from_email = getenv('CONTACT_FROM_EMAIL');

// Validate required configuration
if (!$recaptcha_secret || !$contact_email || !$from_email) {
    http_response_code(500);
    echo json_encode([
        'success' => false,
        'message' => 'Server configuration error. Please contact the administrator.'
    ]);
    exit;
}

// Simple sanitization helper
function clean_input($value) {
    return trim(strip_tags($value));
}

// Set JSON response header
header('Content-Type: application/json');

if ($_SERVER["REQUEST_METHOD"] === "POST") {

    // Honeypot check: if filled, treat as spam and exit quietly
    $honeypot = $_POST["website"] ?? "";
    if ($honeypot !== "") {
        http_response_code(200);
        echo json_encode(['success' => true]);
        exit;
    }

    // Get reCAPTCHA token from form
    $recaptcha_token = $_POST["recaptcha_token"] ?? "";
    
    if (empty($recaptcha_token)) {
        http_response_code(400);
        echo json_encode([
            'success' => false,
            'message' => 'reCAPTCHA token missing. Please try again.'
        ]);
        exit;
    }

    // Verify reCAPTCHA token with Google
    $recaptcha_verified = verify_recaptcha($recaptcha_token, $recaptcha_secret, $recaptcha_threshold);
    
    if (!$recaptcha_verified['valid']) {
        http_response_code(400);
        echo json_encode([
            'success' => false,
            'message' => 'reCAPTCHA verification failed. You may be a bot. Please try again.'
        ]);
        exit;
    }

    // Get fields from the form
    $name    = clean_input($_POST["name"] ?? "");
    $email   = clean_input($_POST["email"] ?? "");
    $subject = clean_input($_POST["subject"] ?? "");
    $message = trim($_POST["message"] ?? "");

    $errors = [];

    // Required fields
    if ($name === "") {
        $errors[] = "Name is required.";
    }

    if ($email === "" || !filter_var($email, FILTER_VALIDATE_EMAIL)) {
        $errors[] = "A valid email address is required.";
    }

    if ($subject === "") {
        $errors[] = "Subject is required.";
    }

    if ($message === "") {
        $errors[] = "Message is required.";
    }

    if (!empty($errors)) {
        http_response_code(400);
        echo json_encode(['success' => false, 'message' => implode(' ', $errors)]);
        exit;
    }

    // Build email body with reCAPTCHA score info (for admin reference)
    $body  = "Name: {$name}\n";
    $body .= "Email: {$email}\n";
    $body .= "Subject: {$subject}\n";
    $body .= "reCAPTCHA Score: {$recaptcha_verified['score']}\n\n";
    $body .= "Message:\n{$message}\n";

    // Headers
    $headers  = "From: {$name} <{$from_email}>\r\n";
    $headers .= "Reply-To: {$email}\r\n";
    $headers .= "Content-Type: text/plain; charset=UTF-8\r\n";

    // Send email
    $sent = mail($contact_email, "Website Contact: {$subject}", $body, $headers);

    if ($sent) {
        http_response_code(200);
        echo json_encode([
            'success' => true,
            'message' => 'Thank you! Your message has been sent successfully.'
        ]);
    } else {
        http_response_code(500);
        echo json_encode([
            'success' => false,
            'message' => 'Sorry, there was a problem sending your message. Please try again later.'
        ]);
    }
} else {
    http_response_code(405);
    echo json_encode(['success' => false, 'message' => 'Method not allowed.']);
}

/**
 * Verify reCAPTCHA v3 token with Google's API
 * 
 * @param string $token The reCAPTCHA token from the client
 * @param string $secret The reCAPTCHA secret key from environment
 * @param float $threshold Minimum score required (0.0 - 1.0)
 * @return array Array with 'valid' (bool) and 'score' (float) keys
 */
function verify_recaptcha($token, $secret, $threshold = 0.5) {
    $url = 'https://www.google.com/recaptcha/api/siteverify';
    
    $data = [
        'secret' => $secret,
        'response' => $token
    ];

    // Use cURL or file_get_contents depending on server setup
    if (function_exists('curl_init')) {
        // Use cURL (preferred for better control)
        $ch = curl_init();
        curl_setopt($ch, CURLOPT_URL, $url);
        curl_setopt($ch, CURLOPT_POST, 1);
        curl_setopt($ch, CURLOPT_POSTFIELDS, http_build_query($data));
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
        curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, true);
        curl_setopt($ch, CURLOPT_TIMEOUT, 5);
        
        $response = curl_exec($ch);
        $http_code = curl_getinfo($ch, CURLINFO_HTTP_CODE);
        curl_close($ch);
        
        if ($http_code !== 200 || !$response) {
            return ['valid' => false, 'score' => 0.0];
        }
    } else {
        // Fallback to file_get_contents with stream context
        $options = [
            'http' => [
                'header' => 'Content-Type: application/x-www-form-urlencoded\r\n',
                'method' => 'POST',
                'content' => http_build_query($data),
                'timeout' => 5
            ]
        ];
        $context = stream_context_create($options);
        $response = @file_get_contents($url, false, $context);
        
        if ($response === false) {
            return ['valid' => false, 'score' => 0.0];
        }
    }

    // Parse Google's response
    $result = json_decode($response, true);
    
    if (!isset($result['success']) || !$result['success']) {
        return ['valid' => false, 'score' => 0.0];
    }

    // Check score threshold
    $score = isset($result['score']) ? (float) $result['score'] : 0.0;
    
    return [
        'valid' => ($score >= $threshold),
        'score' => $score
    ];
}
