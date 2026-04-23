<!DOCTYPE html>
<html <?php language_attributes(); ?>>
<head>
<meta charset="<?php bloginfo('charset'); ?>">
<meta name="viewport" content="width=device-width, initial-scale=1.0">

<title><?php bloginfo('name'); ?></title>

<meta name="description" content="Focus Negotium Inc | Sacred Holding Corporation | Construction | Music | Private Trust Structuring">

<!-- Google Analytics -->
<script async src="https://www.googletagmanager.com/gtag/js?id=GA_MEASUREMENT_ID"></script>
<script>
window.dataLayer = window.dataLayer || [];
function gtag(){dataLayer.push(arguments);}
gtag('js', new Date());
gtag('config', 'GA_MEASUREMENT_ID');
</script>

<!-- Structured Schema -->
<script type="application/ld+json">
{
 "@context": "https://schema.org",
 "@type": "Organization",
 "name": "Focus Negotium Inc",
 "url": "<?php echo home_url(); ?>"
}
</script>

<?php wp_head(); ?>
</head>

<body>
<div class="sacred-bg"></div>

<header class="container">
<h1>FOCUS NEGOTIUM INC</h1>
<nav>
<a href="/">Home</a>
<a href="/royal-lee">Royal Lee</a>
<a href="/focus-records">Focus Records</a>
<a href="/trust">Trust Structuring</a>
<a href="/books">Books</a>
<a href="/contact">Executive Contact</a>
</nav>
</header>