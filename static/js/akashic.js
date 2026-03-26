const canvas = document.getElementById("geometry-canvas");

function initSacredGeometry() {
  if (!canvas) return;

  const ctx = canvas.getContext("2d");
  if (!ctx) return;

  const rings = [];
  const ringCount = 7;

  function resize() {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
    rings.length = 0;
    const base = Math.min(canvas.width, canvas.height) * 0.08;
    for (let i = 0; i < ringCount; i += 1) {
      rings.push({
        radius: base + i * base * 0.72,
        speed: 0.0005 + i * 0.00014,
        offset: Math.random() * Math.PI * 2,
      });
    }
  }

  function draw(time) {
    const w = canvas.width;
    const h = canvas.height;
    const cx = w * 0.5;
    const cy = h * 0.5;

    ctx.clearRect(0, 0, w, h);
    ctx.save();
    ctx.translate(cx, cy);

    rings.forEach((ring, index) => {
      const angle = time * ring.speed + ring.offset;
      const alpha = 0.11 + index * 0.012;
      const stroke = index % 2 === 0 ? `rgba(26, 160, 145, ${alpha})` : `rgba(224, 171, 71, ${alpha})`;

      ctx.strokeStyle = stroke;
      ctx.lineWidth = 1.1;
      ctx.beginPath();
      ctx.arc(0, 0, ring.radius, 0, Math.PI * 2);
      ctx.stroke();

      const nodes = 6 + (index % 3);
      for (let i = 0; i < nodes; i += 1) {
        const a = angle + (Math.PI * 2 * i) / nodes;
        const x = Math.cos(a) * ring.radius;
        const y = Math.sin(a) * ring.radius;
        ctx.beginPath();
        ctx.arc(x, y, 1.8, 0, Math.PI * 2);
        ctx.fillStyle = `rgba(244, 232, 199, ${0.3 + index * 0.03})`;
        ctx.fill();
      }
    });

    ctx.restore();
    requestAnimationFrame(draw);
  }

  window.addEventListener("resize", resize);
  resize();
  requestAnimationFrame(draw);
}

function pretty(data) {
  return typeof data === "string" ? data : JSON.stringify(data, null, 2);
}

async function postJson(url, body) {
  const response = await fetch(url, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });
  return response.json();
}

function bindFullMode() {
  const form = document.getElementById("full-mode-form");
  const output = document.getElementById("full-mode-output");
  const launchBtn = document.getElementById("launch-all-btn");
  const deployBtn = document.getElementById("deploy-apps-btn");

  if (!form || !output) return;

  form.addEventListener("submit", async (event) => {
    event.preventDefault();
    output.textContent = "Running standard full mode...";
    const task = form.querySelector("textarea[name='task']").value;
    try {
      const data = await postJson(form.dataset.endpoint, { task });
      output.textContent = pretty(data);
    } catch (error) {
      output.textContent = `Request failed: ${error}`;
    }
  });

  if (launchBtn) {
    launchBtn.addEventListener("click", async () => {
      output.textContent = "Launching each engine app...";
      try {
        const data = await postJson("/api/launch-all", {});
        output.textContent = pretty(data);
      } catch (error) {
        output.textContent = `Launch failed: ${error}`;
      }
    });
  }

  if (deployBtn) {
    deployBtn.addEventListener("click", async () => {
      output.textContent = "Deploying engine apps to Replit hook layer...";
      try {
        const data = await postJson("/api/replit/deploy", {});
        output.textContent = pretty(data);
      } catch (error) {
        output.textContent = `Deploy failed: ${error}`;
      }
    });
  }
}

function bindEnginePage() {
  const form = document.getElementById("engine-run-form");
  const output = document.getElementById("engine-output");
  const dispatchBtn = document.getElementById("dispatch-btn");
  if (!form || !output) return;

  form.addEventListener("submit", async (event) => {
    event.preventDefault();
    output.textContent = "Running engine...";
    const task = form.querySelector("textarea[name='task']").value;
    try {
      const data = await postJson(form.dataset.endpoint, { task });
      output.textContent = pretty(data);
    } catch (error) {
      output.textContent = `Engine request failed: ${error}`;
    }
  });

  if (dispatchBtn) {
    dispatchBtn.addEventListener("click", async () => {
      output.textContent = "Running through dispatcher...";
      const task = form.querySelector("textarea[name='task']").value;
      try {
        const data = await postJson("/api/run", { task });
        output.textContent = pretty(data);
      } catch (error) {
        output.textContent = `Dispatch failed: ${error}`;
      }
    });
  }
}

initSacredGeometry();
bindFullMode();
bindEnginePage();
