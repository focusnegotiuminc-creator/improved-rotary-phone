export const stacks = [
  {
    id: "website_delivery_stack",
    label: "Website Delivery Stack",
    objective: "Plan, draft, verify, and publish customer-facing website work.",
    engines: ["research", "writing", "marketing", "publish", "automation"],
  },
  {
    id: "real_estate_development_stack",
    label: "Real Estate Development Stack",
    objective: "Build decision-ready development, construction, and property-operation packets.",
    engines: ["research", "geometry", "construction", "compliance", "writing", "automation"],
  },
  {
    id: "media_release_stack",
    label: "Media Release Stack",
    objective: "Package release campaigns, visual assets, and catalog handoffs.",
    engines: ["research", "writing", "ai_twin", "marketing", "publish", "automation"],
  },
  {
    id: "client_intake_stack",
    label: "Client Intake Stack",
    objective: "Normalize client requests into scoped service, routing, and follow-up actions.",
    engines: ["research", "claims", "writing", "automation"],
  },
  {
    id: "sacred_geometry_book_stack",
    label: "Sacred Geometry Book Stack",
    objective: "Research, verify, outline, draft, diagram, audit, and assemble nonfiction books with source discipline.",
    engines: ["research", "claims", "writing", "geometry", "construction", "compliance", "publish", "automation"],
  },
  {
    id: "productivity_command_stack",
    label: "Productivity Command Stack",
    objective: "Prioritize tasks, organize knowledge, and build operator-ready plans across business systems.",
    engines: ["research", "frequency", "writing", "automation"],
  }
];

export const toolBridges = [
  {
    id: "github_workspace",
    label: "GitHub Bridge",
    role: "Repos, branches, pull requests, and publish handoffs.",
    analogs: ["GitHub"],
  },
  {
    id: "creative_studio",
    label: "Creative Studio Bridge",
    role: "Campaign art, PDFs, visual studies, and design prompts.",
    analogs: ["Adobe CC", "Canva", "Figma"],
  },
  {
    id: "automation_router",
    label: "Automation Router",
    role: "Workflow continuation across approved webhooks and connectors.",
    analogs: ["Make", "Zapier"],
  },
  {
    id: "artifact_archive",
    label: "Artifact Archive",
    role: "Structured storage for runs, bundles, and delivery outputs.",
    analogs: ["Drive", "GitHub", "Airtable"],
  },
  {
    id: "task_hub",
    label: "Task Hub",
    role: "Priority planning, work queues, and operator command overlays.",
    analogs: ["Notion", "ClickUp", "Trello"],
  },
  {
    id: "stripe_catalog",
    label: "Offer Catalog",
    role: "Service offers, pricing ladders, and checkout routing.",
    analogs: ["Stripe"],
  }
];

export const templates = [
  {
    id: "private-run-brief.md",
    label: "Private Run Brief",
    content: `# Focus Private Run Brief

## Mission
- Define the task clearly

## Desired outputs
- List the deliverables

## Constraints
- Protect public quality
- Preserve rollback safety
- Keep internal systems private

## Source context
- URLs
- files
- notes
`
  },
  {
    id: "website-sprint.md",
    label: "Website Sprint Template",
    content: `# Website Sprint

## Scope
- page or route:
- primary objective:

## Checklist
1. Audit live content
2. Update copy and assets
3. Verify desktop
4. Verify mobile
5. Verify apex and www if applicable
6. Publish and document rollback
`
  },
  {
    id: "sacred-geometry-book-agent.md",
    label: "Sacred Geometry Book Agent",
    content: `SYSTEM ROLE
You are an autonomous research, verification, and publishing agent.

GOAL
Build a source-disciplined book workflow for sacred geometry, architecture, engineering, and construction.

REQUIREMENTS
- Never fabricate sources
- Mark uncertain claims as REQUIRES FURTHER VERIFICATION
- Build research database, verified claims, outline, diagrams, bibliography, manuscript plan
`
  }
];
