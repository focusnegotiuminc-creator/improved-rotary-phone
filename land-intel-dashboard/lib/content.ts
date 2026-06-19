export type Confidence =
  | "verified"
  | "strong"
  | "likely"
  | "possible"
  | "speculative"
  | "unknown";

export const CONFIDENCE_LABELS: Record<
  Confidence,
  { label: string; blurb: string }
> = {
  verified: {
    label: "Verified",
    blurb: "Supported by official record, map, deed, statute, or government source.",
  },
  strong: {
    label: "Strongly supported",
    blurb: "Supported by multiple reliable, independent sources.",
  },
  likely: {
    label: "Likely",
    blurb: "Supported by map evidence or standard practice; needs confirmation.",
  },
  possible: {
    label: "Possible",
    blurb: "Plausible but not yet proven with a source.",
  },
  speculative: {
    label: "Speculative",
    blurb: "Alternative, symbolic, esoteric, or unverified claim. Not fact.",
  },
  unknown: {
    label: "Unknown",
    blurb: "Not enough evidence to assess. Verification path provided.",
  },
};

export const COORDINATE = {
  latText: "39.6810292\u00b0 North latitude",
  lonText: "91.4115990\u00b0 West longitude",
  decimal: "39.6810292, -91.4115990",
  county: "Marion County",
  state: "Missouri",
  meridian: "Fifth Principal Meridian (5th P.M.)",
};

/* ----------------------------- Map legend & key ----------------------------- */
export type LegendItem = {
  name: string;
  symbol: string;
  kind: "line" | "fill" | "point" | "label";
  meaning: string;
};

export type LegendGroup = {
  group: string;
  items: LegendItem[];
};

export const MAP_LEGEND: LegendGroup[] = [
  {
    group: "Boundaries & Survey Lines",
    items: [
      { name: "Parcel line", symbol: "\u2014\u2014", kind: "line", meaning: "Edge of a single tax/ownership parcel. Defines what you own." },
      { name: "Lot line", symbol: "\u00b7\u2014\u00b7", kind: "line", meaning: "Subdivision of a parcel into platted lots." },
      { name: "Section line", symbol: "\u2014 \u2014", kind: "line", meaning: "1 sq mile (640 ac) PLSS grid line." },
      { name: "Township line", symbol: "\u2550\u2550", kind: "line", meaning: "Boundary of a 6x6 mile congressional township." },
      { name: "Range line", symbol: "\u2551\u2551", kind: "line", meaning: "North-south PLSS column boundary measured from the meridian." },
      { name: "City limits", symbol: "\u2581\u2581", kind: "line", meaning: "Edge of municipal jurisdiction; controls zoning, police power, taxes." },
      { name: "County boundary", symbol: "\u2014\u00b7\u2014", kind: "line", meaning: "Edge of county jurisdiction; recorder/assessor authority changes here." },
      { name: "Right-of-way boundary", symbol: "R/W", kind: "line", meaning: "Strip dedicated to roads/utilities; limits where you can build." },
    ],
  },
  {
    group: "Zoning (typical color conventions)",
    items: [
      { name: "Residential", symbol: "R", kind: "fill", meaning: "Yellow on most maps. Housing; limits commercial/industrial use." },
      { name: "Commercial", symbol: "C", kind: "fill", meaning: "Red/pink. Retail, office, services." },
      { name: "Industrial", symbol: "I", kind: "fill", meaning: "Gray/purple. Manufacturing, warehousing; higher nuisance tolerance." },
      { name: "Agricultural", symbol: "A", kind: "fill", meaning: "Green/tan. Farming; large minimum lot sizes." },
      { name: "Conservation", symbol: "CN", kind: "fill", meaning: "Protected land; heavy development restriction." },
      { name: "Mineral area", symbol: "M", kind: "fill", meaning: "Severed/active mineral estate; surface vs subsurface rights split." },
    ],
  },
  {
    group: "Water & Hydrology",
    items: [
      { name: "River", symbol: "\u2248", kind: "line", meaning: "Solid blue, wide. May be navigable (public) - affects ownership of bed." },
      { name: "Creek / stream", symbol: "~", kind: "line", meaning: "Thin blue. Triggers riparian rights and setbacks." },
      { name: "Intermittent stream", symbol: "-\u00b7-", kind: "line", meaning: "Dashed blue. Flows seasonally; still regulated." },
      { name: "Spring", symbol: "\u25cb\u2192", kind: "point", meaning: "Open circle w/ tail. Groundwater surfacing; karst indicator." },
      { name: "Cave / sinkhole", symbol: "\u2229", kind: "point", meaning: "Karst feature; affects septic, wells, foundations, liability." },
      { name: "Drainage path", symbol: "\u21d2", kind: "line", meaning: "Arrowed line showing water flow direction across terrain." },
      { name: "Watershed", symbol: "\u2237", kind: "fill", meaning: "Area draining to one outlet; used for stormwater rules." },
      { name: "Floodplain (100-yr)", symbol: "AE", kind: "fill", meaning: "FEMA zone. Blue/teal hatch. Insurance + build restrictions." },
      { name: "Wetland", symbol: "\u2592", kind: "fill", meaning: "Green hatch. Federally regulated; fill/drain limits." },
    ],
  },
  {
    group: "Transportation",
    items: [
      { name: "Public road", symbol: "\u2550", kind: "line", meaning: "Maintained by city/county/state; public access." },
      { name: "Private road / drive", symbol: "= =", kind: "line", meaning: "Maintained privately; access by easement." },
      { name: "Railroad (active)", symbol: "\u251c\u2500\u2524", kind: "line", meaning: "Crosstie symbol. Noise/vibration; railroad owns ROW." },
      { name: "Abandoned rail line", symbol: "x\u2014x", kind: "line", meaning: "Former corridor; may be railbanked/trail or reversion to abutters." },
      { name: "Old roadbed", symbol: "\u00b7\u00b7\u00b7", kind: "line", meaning: "Historic alignment; can carry buried easements." },
    ],
  },
  {
    group: "Utilities & Infrastructure",
    items: [
      { name: "Electric transmission", symbol: "\u2014T\u2014", kind: "line", meaning: "High-voltage line on towers; wide easement." },
      { name: "Electric distribution pole", symbol: "\u25cf", kind: "point", meaning: "Filled dot. Local power; usually a utility easement." },
      { name: "Water main", symbol: "\u2014W\u2014", kind: "line", meaning: "Public supply line in ROW/easement." },
      { name: "Water service line", symbol: "\u00b7w\u00b7", kind: "line", meaning: "Branch from main to a structure." },
      { name: "Sanitary sewer", symbol: "\u2014S\u2014", kind: "line", meaning: "Gravity/force main; manholes mark alignment." },
      { name: "Storm sewer", symbol: "\u2014SD\u2014", kind: "line", meaning: "Carries runoff; inlets and culverts." },
      { name: "Gas pipeline", symbol: "\u2014G\u2014", kind: "line", meaning: "Distribution or transmission; PHMSA-mapped if major." },
      { name: "Oil / hazardous pipeline", symbol: "\u2014P\u2014", kind: "line", meaning: "Transmission corridor; safety setbacks apply." },
      { name: "Underground tunnel/culvert", symbol: "\u2533", kind: "line", meaning: "Where public records exist; rare on assessor maps." },
    ],
  },
  {
    group: "Survey, Terrain & Records",
    items: [
      { name: "Survey marker", symbol: "\u25b3", kind: "point", meaning: "Set corner monument; controls boundary location." },
      { name: "Benchmark", symbol: "BM", kind: "point", meaning: "Known elevation reference point." },
      { name: "Contour line", symbol: "\u223f", kind: "line", meaning: "Connects equal elevation; close lines = steep ground." },
      { name: "Elevation shading", symbol: "\u2591\u2592\u2593", kind: "fill", meaning: "Hillshade; lighter/darker shows slope and aspect." },
      { name: "Soil map unit", symbol: "9B", kind: "label", meaning: "NRCS code; tells drainage, bearing, septic suitability." },
      { name: "Assessor parcel number (APN)", symbol: "##-###", kind: "label", meaning: "Unique tax ID linking to ownership + value records." },
      { name: "Land patent boundary", symbol: "\u2592\u2592", kind: "line", meaning: "Original federal grant footprint; root of title." },
    ],
  },
  {
    group: "Districts & Overlays",
    items: [
      { name: "Tax district", symbol: "TX", kind: "fill", meaning: "Determines which taxing bodies levy on the parcel." },
      { name: "School district", symbol: "SD", kind: "fill", meaning: "Affects taxes and resale value." },
      { name: "Fire district", symbol: "FD", kind: "fill", meaning: "Service area; affects insurance (ISO rating)." },
      { name: "Improvement / special assessment district", symbol: "SAD", kind: "fill", meaning: "Extra levies for infrastructure (NID/TIF/CID)." },
    ],
  },
];

/* ----------------------------- Black's Law glossary ----------------------------- */
export type GlossaryTerm = {
  term: string;
  legal: string;
  plain: string;
  land: string;
  nature: "legal" | "historical" | "symbolic" | "speculative";
};

export const GLOSSARY: GlossaryTerm[] = [
  { term: "Title", legal: "The union of all elements constituting legal ownership; the means by which an owner has just possession of property.", plain: "Proof you own it and the right to control it.", land: "Determines who may sell, mortgage, or transfer the land.", nature: "legal" },
  { term: "Land", legal: "The solid material of the earth; comprehends not only the surface but everything under and over it (ad coelum doctrine), historically up to the sky and down to the center.", plain: "The ground plus what's above and below it.", land: "Drives mineral, air, water, and subsurface rights questions.", nature: "legal" },
  { term: "Estate", legal: "The degree, quantity, nature, and extent of interest a person has in real property.", plain: "How much of an ownership interest you hold and for how long.", land: "Fee simple vs life estate vs leasehold changes value and control.", nature: "legal" },
  { term: "Fee simple", legal: "An absolute estate in perpetuity; the largest possible aggregate of rights in land.", plain: "The fullest ordinary ownership you can have.", land: "Highest market value; freely transferable and inheritable.", nature: "legal" },
  { term: "Allodial", legal: "Land held in absolute independence, without obligation of service or acknowledgment to a superior.", plain: "Ownership with no overlord - extremely rare in U.S. practice.", land: "Often invoked in fringe theories; true allodial title is essentially nonexistent in the modern U.S. system.", nature: "speculative" },
  { term: "Trust", legal: "A fiduciary relationship in which one party (trustee) holds legal title to property for the benefit of another (beneficiary).", plain: "A legal container someone manages on another's behalf.", land: "Can hold real estate for privacy, estate planning, asset protection.", nature: "legal" },
  { term: "Trustee", legal: "Person or entity holding legal title to trust property with a duty to manage it for beneficiaries.", plain: "The manager of the trust.", land: "Name may appear on recorded deeds into trust.", nature: "legal" },
  { term: "Beneficiary", legal: "One for whose benefit a trust is created; holds equitable, not legal, title.", plain: "Who actually benefits from the property.", land: "Usually kept private; not always disclosed in public records.", nature: "legal" },
  { term: "Deed", legal: "A written instrument, signed and delivered, by which title to real property is conveyed.", plain: "The document that transfers ownership.", land: "Recorded at the county recorder of deeds to give public notice.", nature: "legal" },
  { term: "Patent", legal: "The instrument by which the government conveys title to public land to a private party.", plain: "The original grant of land from the government.", land: "Root of title; foundation of the chain of ownership.", nature: "historical" },
  { term: "Grant", legal: "A transfer of real property by deed or other instrument.", plain: "An act of giving/transferring land rights.", land: "Language ('grant, bargain, and sell') implies certain warranties.", nature: "legal" },
  { term: "Easement", legal: "A right to use another's land for a specific limited purpose.", plain: "Someone else's legal right to cross or use part of your land.", land: "Reduces use and sometimes value; often where poles/lines sit.", nature: "legal" },
  { term: "Right-of-way", legal: "A type of easement granting passage over land; also the strip of land itself.", plain: "A path/strip others may legally use (roads, utilities).", land: "Limits building; may be public or utility-held.", nature: "legal" },
  { term: "Appurtenance", legal: "That which belongs to and passes with the principal property.", plain: "A right attached to the land that travels with it when sold.", land: "E.g., an access easement benefiting your parcel.", nature: "legal" },
  { term: "Hereditament", legal: "Anything capable of being inherited, whether corporeal or incorporeal, real or personal.", plain: "Inheritable property and rights.", land: "Old term still used in deeds to sweep in all attached rights.", nature: "historical" },
  { term: "Tenement", legal: "Property, especially land, held by a tenant; broadly, anything permanent that may be held.", plain: "Held land and the rights in it.", land: "Appears in 'lands, tenements, and hereditaments' deed language.", nature: "historical" },
  { term: "Real property", legal: "Land and generally whatever is erected or affixed to it.", plain: "Land and buildings.", land: "Distinct from movable personal property in taxation and transfer.", nature: "legal" },
  { term: "Riparian", legal: "Pertaining to the bank of a watercourse; rights of an owner of land abutting flowing water.", plain: "Water rights from owning land along a stream/river.", land: "Reasonable-use rights to the water; affects value and access.", nature: "legal" },
  { term: "Watercourse", legal: "A stream of water flowing in a defined channel with bed and banks.", plain: "A natural channel that carries water.", land: "Triggers setbacks, riparian rights, and drainage duties.", nature: "legal" },
  { term: "Navigable", legal: "Waters used or usable as highways for commerce; bed often held by the state in public trust.", plain: "Big enough to be a public waterway.", land: "Public may have access; you may not own the bed.", nature: "legal" },
  { term: "Jurisdiction", legal: "The authority of a government body to govern or legislate over persons and property.", plain: "Who has legal power over the land.", land: "City vs county vs state changes rules and taxes.", nature: "legal" },
  { term: "Municipality", legal: "A legally incorporated political unit (city/town) with local self-government.", plain: "A city or town government.", land: "Controls zoning, permits, and police power inside its limits.", nature: "legal" },
  { term: "Township", legal: "In the PLSS, a unit ~6 miles square; also a civil township of local government.", plain: "A survey square OR a small unit of local government - not an owner.", land: "A location descriptor and sometimes a minor governing body.", nature: "legal" },
  { term: "Record / Register", legal: "To deposit a document in the public office charged with keeping such records, giving constructive notice.", plain: "Filing a document so the public is legally on notice.", land: "Recording protects priority; over-recording can expose private info.", nature: "legal" },
  { term: "Conveyance", legal: "The transfer of title to property from one person to another by deed or instrument.", plain: "Moving ownership from one party to another.", land: "Each conveyance is a link in the chain of title.", nature: "legal" },
];

/* ----------------------------- Agents ----------------------------- */
export type Agent = {
  code: string;
  name: string;
  does: string;
};

export const AGENTS: Agent[] = [
  { code: "A", name: "Original Prompt Recovery Agent", does: "Finds prior prompt versions, fragments, chat exports, and saved context across authorized sources." },
  { code: "B", name: "Coordinate Intelligence Agent", does: "Resolves exact location, parcels, township/range/section, city limits, county lines, jurisdiction." },
  { code: "C", name: "GIS Map Agent", does: "Generates maps, layers, overlays, legends, keys, and plain-English explanations." },
  { code: "D", name: "Utility Pole & Easement Agent", does: "Researches poles, spacing, easements, right-of-way, ownership, and relocation rules." },
  { code: "E", name: "Water/Spring/Cave/Hydrology Agent", does: "Researches creeks, springs, caves, karst, groundwater, floodplains, wetlands, micro-hydro." },
  { code: "F", name: "Railroad/Factory/Industrial Value Agent", does: "Analyzes proximity, contamination, access, zoning, and value impact." },
  { code: "G", name: "Trust & Title Agent", does: "Researches trusts, public registration, deeds, title language, recording, ownership structures." },
  { code: "H", name: "Black's Law Dictionary Agent", does: "Defines land/title/legal terms and how terminology affects ownership and value." },
  { code: "I", name: "Ancient & Prehistoric Knowledge Agent", does: "Researches old maps and pre-modern land meaning; separates fact from speculation." },
  { code: "J", name: "Underground Infrastructure Agent", does: "Searches public records for tunnels, pipelines, culverts, sewer/water systems." },
  { code: "K", name: "Recoding Agent", does: "Inspects authorized code, finds weak algorithms, rewrites them, adds tests, preps deploy." },
  { code: "L", name: "Vercel Deployment Agent", does: "Turns research into a deployable app/dashboard (this app is its first output)." },
  { code: "M", name: "Drive Knowledge Agent", does: "Searches authorized Drive for files, maps, notes, prompts, and research." },
  { code: "N", name: "Asana Execution Agent", does: "Creates tasks, subtasks, milestones, timelines, and roadmaps." },
  { code: "O", name: "Notion Knowledgebase Agent", does: "Builds structured databases for parcels, maps, records, terms, and sources." },
  { code: "P", name: "Codex Implementation Agent", does: "Writes copy-paste prompts and coding instructions for implementation." },
  { code: "Q", name: "Quality Control Agent", does: "Checks outputs for missing detail, weak claims, bad citations, incomplete deliverables." },
  { code: "R", name: "Regeneration Agent", does: "Regenerates weak maps, legends, reports, and algorithms until expert quality." },
  { code: "S", name: "School & R&D Research Agent", does: "Converts findings into school/research/dev-ready documents with citations." },
];

/* ----------------------------- Records request checklist ----------------------------- */
export const RECORDS_REQUESTS: { office: string; ask: string[] }[] = [
  {
    office: "County Recorder of Deeds (Marion County)",
    ask: [
      "Full chain of title and recorded deeds for the parcel",
      "Recorded easements, rights-of-way, and memoranda of trust",
      "Any recorded plats and subdivision documents",
    ],
  },
  {
    office: "County Assessor / GIS",
    ask: [
      "Assessor parcel number (APN), maps, and current valuation",
      "Adjacent parcel ownership and boundaries",
      "GIS layers: zoning, floodplain, utilities, soils",
    ],
  },
  {
    office: "Public Works / County Engineer",
    ask: [
      "Sewer, stormwater, and water main as-builts near the parcel",
      "Culvert/tunnel records and road jurisdiction maps",
      "Right-of-way and special assessment district records",
    ],
  },
  {
    office: "Utility Companies / Rural Co-op",
    ask: [
      "Pole ownership and recorded utility easements",
      "Overhead/underground service maps for the area",
      "Relocation policy and who bears the cost",
    ],
  },
  {
    office: "State & Federal (DNR, EPA, PHMSA, USGS, FEMA)",
    ask: [
      "Environmental/brownfield/Superfund records (DNR/EPA)",
      "National Pipeline Mapping System public viewer (PHMSA)",
      "Historic topo maps (USGS) and flood maps (FEMA)",
    ],
  },
];
