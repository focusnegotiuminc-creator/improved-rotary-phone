<?php get_header(); ?>
<div class="container">
<h2>Executive Contact</h2>
<form method="post">
<input type="text" name="name" placeholder="Full Name" required><br><br>
<input type="email" name="email" placeholder="Email" required><br><br>
<textarea name="message" placeholder="Your Inquiry" required></textarea><br><br>
<button class="btn" type="submit">Submit</button>
</form>
</div>
<?php get_footer(); ?>