<footer class="site-footer">
  <div class="site-footer__inner">
    <div>
      <p class="brand-kicker">Focus AI operating surface</p>
      <p class="footer-copy">&copy; <?php echo esc_html( date( 'Y' ) ); ?> Focus Negotium Inc. All rights reserved.</p>
    </div>
    <div class="footer-links">
      <a href="<?php echo esc_url( home_url( '/products.html' ) ); ?>">Offers</a>
      <a href="<?php echo esc_url( home_url( '/services.html' ) ); ?>">Services</a>
      <a href="<?php echo esc_url( home_url( '/ebooks/index.html' ) ); ?>">Books</a>
      <a href="<?php echo esc_url( home_url( '/business_os.html' ) ); ?>">Business OS</a>
    </div>
  </div>
</footer>

<button id="ai-bot" type="button" aria-expanded="false" aria-controls="ai-chatbox">AI Consult</button>
<div id="ai-chatbox" hidden>
  <p><strong>Executive Assistant</strong></p>
  <p>Use the live portal to explore offers, services, books, and the business operating system.</p>
  <p><a href="<?php echo esc_url( home_url( '/business_os.html' ) ); ?>">Open the Business OS</a></p>
</div>

<script>
const focusBotButton = document.getElementById('ai-bot');
const focusBotPanel = document.getElementById('ai-chatbox');

if (focusBotButton && focusBotPanel) {
  focusBotButton.addEventListener('click', function () {
    const expanded = focusBotButton.getAttribute('aria-expanded') === 'true';
    focusBotButton.setAttribute('aria-expanded', String(!expanded));
    focusBotPanel.hidden = expanded;
  });
}
</script>

<?php wp_footer(); ?>
</body>
</html>
