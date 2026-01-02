<?php
// Where to send the messages
$to      = "mark.o.mimms@gmail.com";          // TODO: change to your real inbox
$subject = "New message from website contact form";

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

    // Build email body
    $body  = "Name: {$name}\n";
    $body .= "Email: {$email}\n";
    $body .= "Subject: {$subject}\n\n";
    $body .= "Message:\n{$message}\n";

    // Headers
    $fromEmail = "no-reply@mimmsphoto.com";   // use an address on your domain
    $headers  = "From: {$name} <{$fromEmail}>\r\n";
    $headers .= "Reply-To: {$email}\r\n";
    $headers .= "Content-Type: text/plain; charset=UTF-8\r\n";

    // Send email
    $sent = mail($to, "Website Contact: {$subject}", $body, $headers); // PHP mail() call

    if ($sent) {
        http_response_code(200);
        echo json_encode(['success' => true, 'message' => 'Thank you! Your message has been sent successfully.']);
    } else {
        http_response_code(500);
        echo json_encode(['success' => false, 'message' => 'Sorry, there was a problem sending your message. Please try again later.']);
    }
} else {
    http_response_code(405);
    echo json_encode(['success' => false, 'message' => 'Method not allowed.']);
}
