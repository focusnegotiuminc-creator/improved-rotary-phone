const books = [
  {
    title: "Focus Architecture for Creators",
    pages: 186,
    price: "$19",
    summary:
      "A full system for deep work, creative output batching, and weekly planning designed for solopreneurs.",
    outcomes: [
      "Install a 5-block daily focus protocol",
      "Design interruption-proof workspaces",
      "Run a weekly review that compounds output"
    ]
  },
  {
    title: "The Profitable eBook Machine",
    pages: 204,
    price: "$24",
    summary:
      "Covers product ideation, reader research, drafting, editing, launch mechanics, and post-launch upsell systems.",
    outcomes: [
      "Validate demand before writing",
      "Assemble conversion-oriented table of contents",
      "Build repeatable publishing pipelines"
    ]
  },
  {
    title: "Authority SEO for Digital Products",
    pages: 172,
    price: "$21",
    summary:
      "Teaches semantic SEO strategy, internal linking architecture, and buyer-intent content development.",
    outcomes: [
      "Create 90-day content clusters",
      "Rank for high-intent long-tail keywords",
      "Capture leads with educational pages"
    ]
  },
  {
    title: "Email Conversion Copybook",
    pages: 158,
    price: "$18",
    summary:
      "Frameworks for welcome sequences, nurture flows, launch campaigns, and lifecycle monetization.",
    outcomes: [
      "Write trust-first onboarding sequences",
      "Engineer urgency without hype",
      "Improve click-through and reply rates"
    ]
  },
  {
    title: "Offer Design and Pricing Psychology",
    pages: 196,
    price: "$23",
    summary:
      "Combines behavioral economics with practical bundle strategy to increase average order value.",
    outcomes: [
      "Craft clear value ladders",
      "Package bonuses that reduce risk",
      "Price based on transformation value"
    ]
  },
  {
    title: "Automation Playbooks for Lean Teams",
    pages: 214,
    price: "$26",
    summary:
      "Operational SOPs for AI-assisted content, CRM workflows, analytics alerts, and campaign scheduling.",
    outcomes: [
      "Automate recurring marketing tasks",
      "Create prompt libraries for consistency",
      "Track KPI exceptions automatically"
    ]
  },
  {
    title: "Storytelling Ads that Sell",
    pages: 168,
    price: "$20",
    summary:
      "Practical ad scripting models for social channels, retargeting, and product education funnels.",
    outcomes: [
      "Convert case studies into ad hooks",
      "Build multi-angle ad testing sets",
      "Scale winning messaging responsibly"
    ]
  },
  {
    title: "Retention and Community Growth",
    pages: 182,
    price: "$22",
    summary:
      "Shows how to increase LTV via onboarding communities, customer rituals, and referral loops.",
    outcomes: [
      "Design loyalty touchpoints",
      "Reduce refund risk with activation",
      "Launch referral incentives with clarity"
    ]
  }
];

const prompts = {
  seo: `Role: Elite SEO strategist + conversion copywriter.\nTask: Build one 2,000-word authority article targeting [PRIMARY KEYWORD] for [IDEAL CUSTOMER].\nRequirements:\n1) Include search intent map and semantic keyword cluster.\n2) Create an opening hook tied to a painful business bottleneck.\n3) Add H2/H3 structure with skimmable tactical steps.\n4) Insert a soft CTA for [EBOOK TITLE] and one lead-magnet CTA.\n5) End with FAQ section for rich-snippet intent.\nOutput: title options, meta title, meta description, slug, full draft, internal link suggestions, and social caption variants.`,
  email: `Role: Direct-response email strategist.\nTask: Produce a 7-day launch sequence for [OFFER] to [AUDIENCE].\nRequirements:\n- Day-by-day objective, subject line, and preview text.\n- Psychological trigger map (authority, proof, future pace, urgency).\n- Include objection handling and risk reversal on days 4-6.\n- Add segmentation logic for clickers vs non-clickers.\nOutput: 7 complete emails plus automation rules and KPI targets for open/click/conversion rates.`,
  ads: `Role: Paid social performance team (creative director + media buyer + copy lead).\nTask: Generate 12 ad concepts to sell [EBOOK/BUNDLE].\nRequirements:\n- 4 pain-driven hooks, 4 aspiration hooks, 4 authority hooks.\n- For each concept include: headline, primary text, visual direction, CTA, and test hypothesis.\n- Add one short UGC script and one 30-second founder script.\nOutput: ad matrix table + recommended test budget split + optimization schedule for 14 days.`,
  funnel: `Role: Funnel optimization consultant.\nTask: Audit and improve the conversion path from traffic to checkout for [PRODUCT].\nRequirements:\n1) Identify likely drop-off points across landing page, checkout, and email follow-up.\n2) Provide 10 A/B tests prioritized by impact/effort.\n3) Rewrite value proposition and offer stack with clearer outcomes.\n4) Propose one order bump and one upsell aligned to buyer journey.\nOutput: prioritized optimization roadmap, revised copy blocks, and weekly reporting template.`
};

const grid = document.getElementById("book-grid");
const year = document.getElementById("year");
const promptType = document.getElementById("promptType");
const generatePrompt = document.getElementById("generatePrompt");
const promptOutput = document.getElementById("promptOutput");

function renderBooks() {
  grid.innerHTML = books
    .map(
      (book) => `
      <article class="book-card">
        <div class="book-meta"><span>${book.pages} pages</span><span>${book.price}</span></div>
        <h3>${book.title}</h3>
        <p>${book.summary}</p>
        <ul>${book.outcomes.map((outcome) => `<li>${outcome}</li>`).join("")}</ul>
      </article>
    `
    )
    .join("");
}

function initPromptEngine() {
  generatePrompt.addEventListener("click", () => {
    promptOutput.textContent = prompts[promptType.value];
  });
}

renderBooks();
initPromptEngine();
year.textContent = new Date().getFullYear();
