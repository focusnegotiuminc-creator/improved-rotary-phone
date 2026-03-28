<?php

if ( ! defined( 'ABSPATH' ) ) {
    exit;
}

function focus_sacred_setup() {
    add_theme_support( 'title-tag' );
    add_theme_support( 'custom-logo' );
    add_theme_support( 'post-thumbnails' );
}
add_action( 'after_setup_theme', 'focus_sacred_setup' );

function focus_chatbot_admin_page() {
    add_menu_page(
        'WPiko Admin Chatbot',
        'WPiko Chatbot',
        'manage_options',
        'focus-chatbot',
        'focus_chatbot_page_callback'
    );
}
add_action( 'admin_menu', 'focus_chatbot_admin_page' );

function focus_chatbot_page_callback() {
    ?>
    <div class="wrap">
        <h1>WPiko Admin Chatbot</h1>
        <p>This chatbot is only visible inside the WordPress admin panel.</p>
        <div style="background:#fff; padding:20px; border:1px solid #ccc;">
            <?php echo do_shortcode( '[wpiko_chatbot]' ); ?>
        </div>
    </div>
    <?php
}

function focus_sacred_assets() {
    wp_enqueue_style(
        'focus-sacred-fonts',
        'https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@500;600;700&family=Space+Grotesk:wght@400;500;700&display=swap',
        array(),
        null
    );
    wp_enqueue_style(
        'focus-sacred-style',
        get_stylesheet_uri(),
        array( 'focus-sacred-fonts' ),
        wp_get_theme()->get( 'Version' )
    );
}
add_action( 'wp_enqueue_scripts', 'focus_sacred_assets' );

function focus_speed_headers() {
    header( 'X-XSS-Protection: 1; mode=block' );
    header( 'X-Content-Type-Options: nosniff' );
}
add_action( 'send_headers', 'focus_speed_headers' );

function focus_favicon() {
    echo '<link rel="icon" href="' . esc_url( get_stylesheet_directory_uri() . '/favicon.ico' ) . '" type="image/x-icon">';
}
add_action( 'wp_head', 'focus_favicon' );

function focus_generate_sitemap() {
    if ( '/sitemap.xml' !== $_SERVER['REQUEST_URI'] ) {
        return;
    }

    header( 'Content-Type: text/xml' );
    echo '<?xml version="1.0" encoding="UTF-8"?>';
    echo '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">';
    foreach ( get_pages() as $page ) {
        echo '<url><loc>' . esc_url( get_page_link( $page->ID ) ) . '</loc></url>';
    }
    echo '</urlset>';
    exit;
}
add_action( 'init', 'focus_generate_sitemap' );
