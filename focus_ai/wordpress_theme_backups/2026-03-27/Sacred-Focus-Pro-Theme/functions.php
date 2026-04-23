<?php

// Add Admin Menu Page
function focus_chatbot_admin_page() {
    add_menu_page(
        'WPiko Admin Chatbot',          // Page title
        'WPiko Chatbot',            // Menu title
        'manage_options',                // Capability
        'focus-chatbot',                  // Menu slug
        'focus_chatbot_page_callback' // Callback function
    );
}
add_action('admin_menu', 'focus_chatbot_admin_page');

// Callback Function to Display Content
function focus_chatbot_page_callback() {
    ?>
    <div class="wrap">
        <h1>WPiko Admin Chatbot</h1>
        <p>This chatbot is only visible inside the WordPress admin panel.</p>
        <div style="background:#fff; padding:20px; border:1px solid #ccc;">
            <?php echo do_shortcode('[wpiko_chatbot]'); ?>
        </div>
    </div>
    <?php
}

// Enqueue Styles and Scripts
function focus_sacred_assets() {
    wp_enqueue_style('main-style', get_stylesheet_uri());
    wp_enqueue_script('main-script', get_template_directory_uri() . '/js/main.js', array('jquery'), null, true);
}
add_action('wp_enqueue_scripts', 'focus_sacred_assets');

// SEO + Speed Headers
function focus_speed_headers() {
    header("X-XSS-Protection: 1; mode=block");
    header("X-Content-Type-Options: nosniff");
}
add_action('send_headers', 'focus_speed_headers');

// Add Favicon Support
function focus_favicon() {
    echo '<link rel="icon" href="'.get_stylesheet_directory_uri().'/favicon.ico" type="image/x-icon">';
}
add_action('wp_head', 'focus_favicon');

// Auto Sitemap
function focus_generate_sitemap() {
    if ($_SERVER['REQUEST_URI'] == '/sitemap.xml') {
        header("Content-Type: text/xml");
        echo '<?xml version="1.0" encoding="UTF-8"?>';
        echo '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">';
        $pages = get_pages();
        foreach($pages as $page){
            echo '<url><loc>'.get_page_link($page->ID).'</loc></url>';
        }
        echo '</urlset>';
        exit;
    }
}
add_action('init', 'focus_generate_sitemap');

if ( ! defined( 'ABSPATH' ) ) {
    exit; // Prevent direct access
}

?>