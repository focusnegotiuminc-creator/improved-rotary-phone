<?php
if ( ! defined( 'ABSPATH' ) ) {
    exit; // Prevent direct access
}
?>

<div class="wrap">
    <h1>WPiko Admin Chatbot</h1>
    <p>This chatbot is only visible inside the WordPress admin panel.</p>

    <div style="background:#fff; padding:20px; border:1px solid #ccc;">
        <?php echo do_shortcode('[wpiko_chatbot]'); ?>
    </div>
</div>