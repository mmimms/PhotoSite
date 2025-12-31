<?php
// Where to send the messages
$to      = "you@example.com";          // TODO: change to your real inbox
$subject = "New message from website contact form";

// Simple sanitization helper
function clean_input($value) {
    return trim(strip_tags($value));
}

if ($_SERVER["REQUEST_METHOD"] === "POST") {

    // Honeypot check: if filled, treat as spam and exit quietly
    $honeypot = $_POST["website"] ?? "";
    if ($honeypot !== "") {
        http_response_code(200);
        exit;
    }

    // Get fields from the form
    $name    = clean_input($_POST["name"] ?? "");
    $email   = clean_input($_POST["email"] ?? "");
    $message = trim($_POST["message"] ?? "");

    $errors = [];

    // Required fields
    if ($name === "") {
        $errors[] = "Name is required.";
    }

    if ($email === "" || !filter_var($email, FILTER_VALIDATE_EMAIL)) {
        $errors[] = "A valid email address is required.";
    }

    if ($message === "") {
        $errors[] = "Message is required.";
    }

    if (!empty($errors)) {
        http_response_code(400);
        echo implode(" ", $errors);
        exit;
    }

    // Build email body
    $body  = "Name: {$name}\n";
    $body .= "Email: {$email}\n\n";
    $body .= "Message:\n{$message}\n";

    // Headers
    $fromEmail = "no-reply@yourdomain.com";   // use an address on your domain
    $headers  = "From: {$name} <{$fromEmail}>\r\n";
    $headers .= "Reply-To: {$email}\r\n";
    $headers .= "Content-Type: text/plain; charset=UTF-8\r\n";

    // Send email
    $sent = mail($to, $subject, $body, $headers); // PHP mail() call[web:323][web:326][web:332]

    if ($sent) {
        echo "Thank you, your message has been sent.";
    } else {
        http_response_code(500);
        echo "Sorry, there was a problem sending your message.";
    }
} else {
    http_response_code(405);
    echo "Method not allowed.";
}