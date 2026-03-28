<!DOCTYPE html>
<html <?php language_attributes(); ?>>
<head>
<meta charset="<?php bloginfo( 'charset' ); ?>">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="description" content="Focus AI operating portal for Focus Negotium Inc, Royal Lee Construction Solutions LLC, and Focus Records LLC.">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Organization",
  "name": "Focus Negotium Inc",
  "url": "<?php echo esc_url( home_url() ); ?>"
}
</script>
<?php wp_head(); ?>
</head>

<body <?php body_class(); ?>>
<?php wp_body_open(); ?>
<div class="sacred-bg"></div>

<header class="site-header">
  <div class="site-header__inner">
    <div class="brand-lockup">
      <p class="brand-kicker">Focus AI portal</p>
      <a class="brand-title" href="<?php echo esc_url( home_url( '/' ) ); ?>"><?php bloginfo( 'name' ); ?></a>
    </div>
    <nav class="site-nav" aria-label="Primary">
      <a href="<?php echo esc_url( home_url( '/' ) ); ?>">Home</a>
      <a href="<?php echo esc_url( home_url( '/products.html' ) ); ?>">Products</a>
      <a href="<?php echo esc_url( home_url( '/services.html' ) ); ?>">Services</a>
      <a href="<?php echo esc_url( home_url( '/ebooks/index.html' ) ); ?>">Books</a>
      <a href="<?php echo esc_url( home_url( '/business_os.html' ) ); ?>">Business OS</a>
      <a href="<?php echo esc_url( home_url( '/booking.html' ) ); ?>">Booking</a>
    </nav>
  </div>
</header>
