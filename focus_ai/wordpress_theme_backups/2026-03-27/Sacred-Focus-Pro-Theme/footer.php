<footer class="container">
<p>© <?php echo date("Y"); ?> Focus Negotium Inc. All Rights Reserved.</p>
</footer>

<div id="ai-bot">AI Consult</div>
<div id="ai-chatbox">
<p><strong>Executive Assistant</strong></p>
<p>How can we assist your development today?</p>
</div>

<script>
document.getElementById("ai-bot").onclick=function(){
var box=document.getElementById("ai-chatbox");
box.style.display = box.style.display==="block" ? "none":"block";
}
</script>

<?php wp_footer(); ?>
</body>
</html>