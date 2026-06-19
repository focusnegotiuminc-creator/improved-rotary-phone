import { Section, Card, KeyValue } from "@/components/section";
import { ConfidenceBadge } from "@/components/confidence-badge";
import { MapLegend } from "@/components/map-legend";
import { Glossary } from "@/components/glossary";
import { SidebarNav, type NavItem } from "@/components/sidebar-nav";
import {
  AGENTS,
  COORDINATE,
  RECORDS_REQUESTS,
  CONFIDENCE_LABELS,
  type Confidence,
} from "@/lib/content";

const NAV: NavItem[] = [
  { id: "overview", index: "00", label: "Overview & how to read this" },
  { id: "coordinate", index: "01", label: "Coordinate location report" },
  { id: "jurisdiction", index: "02", label: "Parcel & jurisdiction" },
  { id: "township", index: "03", label: "Township 59 & ownership myths" },
  { id: "legend", index: "04", label: "Map legend & key" },
  { id: "water", index: "05", label: "Springs, caves & water rights" },
  { id: "electricity", index: "06", label: "Natural electricity (fact vs theory)" },
  { id: "poles", index: "07", label: "Utility poles & easements" },
  { id: "proximity", index: "08", label: "Railroad / industrial proximity" },
  { id: "trust", index: "09", label: "Trusts, title & recording" },
  { id: "glossary", index: "10", label: "Black's Law land glossary" },
  { id: "history", index: "11", label: "Historical & old-map research" },
  { id: "underground", index: "12", label: "Underground infrastructure" },
  { id: "records", index: "13", label: "Records request checklist" },
  { id: "agents", index: "14", label: "Master agent system" },
];

function ULabel({ level }: { level: Confidence }) {
  return <ConfidenceBadge level={level} />;
}

export default function Page() {
  return (
    <div className="min-h-screen lg:flex">
      <SidebarNav items={NAV} />

      <main className="min-w-0 flex-1">
        {/* Hero */}
        <header className="paper-grid border-b border-border bg-primary/95 px-6 py-12 text-primary-foreground md:px-10 md:py-16">
          <p className="font-mono text-xs uppercase tracking-[0.3em] text-primary-foreground/70">
            Land Intelligence Investigation
          </p>
          <h1 className="mt-3 max-w-3xl text-balance font-serif text-3xl font-semibold leading-tight md:text-5xl">
            A geo-legal dossier for one coordinate
          </h1>
          <p className="mt-4 max-w-2xl text-pretty leading-relaxed text-primary-foreground/85">
            {COORDINATE.latText}, {COORDINATE.lonText} &mdash; {COORDINATE.county},{" "}
            {COORDINATE.state}. This dashboard organizes location facts, a professional
            map legend, water and utility research, and land/title terminology into one
            structured, clearly-labeled report.
          </p>
          <div className="mt-6 flex flex-wrap gap-3 font-mono text-sm">
            <span className="rounded-md bg-primary-foreground/10 px-3 py-1.5">
              {COORDINATE.decimal}
            </span>
            <span className="rounded-md bg-primary-foreground/10 px-3 py-1.5">
              {COORDINATE.meridian}
            </span>
          </div>
        </header>

        <div className="px-6 pb-24 md:px-10">
          {/* Overview */}
          <Section
            id="overview"
            index="00"
            title="How to read this report"
            subtitle="Every claim is tagged with a confidence level so verified facts are never mixed with speculation. This is research and organized questions to bring to licensed professionals — not legal, engineering, or financial advice."
          >
            <div className="grid grid-cols-1 gap-3 sm:grid-cols-2 lg:grid-cols-3">
              {(Object.keys(CONFIDENCE_LABELS) as Confidence[]).map((k) => (
                <div
                  key={k}
                  className="flex items-start gap-3 rounded-lg border border-border bg-card p-4"
                >
                  <ConfidenceBadge level={k} withTooltip={false} />
                  <p className="text-sm leading-relaxed text-muted-foreground">
                    {CONFIDENCE_LABELS[k].blurb}
                  </p>
                </div>
              ))}
            </div>
            <div className="mt-5 rounded-lg border border-accent/40 bg-accent/5 p-4 text-sm leading-relaxed text-foreground">
              <strong className="font-semibold">Scope note.</strong> This first version
              focuses on the coordinate location report and the full map legend &amp; key,
              with structured research for the remaining sections. Exact parcel number,
              owner, and recorded easements must be confirmed at the Marion County
              Assessor and Recorder of Deeds.
            </div>
          </Section>

          {/* Coordinate */}
          <Section
            id="coordinate"
            index="01"
            title="Coordinate location report"
            subtitle="What the latitude/longitude resolves to and how to confirm the precise spot."
          >
            <div className="grid grid-cols-1 gap-5 lg:grid-cols-2">
              <Card title="Resolved location">
                <dl>
                  <KeyValue k="Latitude" v={COORDINATE.latText} />
                  <KeyValue k="Longitude" v={COORDINATE.lonText} />
                  <KeyValue k="Decimal" v={COORDINATE.decimal} />
                  <KeyValue
                    k="County / State"
                    v={
                      <span className="inline-flex items-center gap-2">
                        {COORDINATE.county}, {COORDINATE.state} <ULabel level="verified" />
                      </span>
                    }
                  />
                  <KeyValue
                    k="Nearest city"
                    v={
                      <span className="inline-flex items-center gap-2">
                        Near Hannibal / Palmyra area <ULabel level="likely" />
                      </span>
                    }
                  />
                  <KeyValue
                    k="Setting"
                    v={
                      <span className="inline-flex items-center gap-2">
                        Rural / agricultural NE Missouri <ULabel level="likely" />
                      </span>
                    }
                  />
                </dl>
              </Card>
              <Card title="How to confirm precisely">
                <ul className="flex list-inside list-decimal flex-col gap-2 text-sm leading-relaxed text-foreground">
                  <li>
                    Enter <span className="font-mono">{COORDINATE.decimal}</span> into the
                    Marion County GIS / assessor parcel viewer to read the exact parcel.
                  </li>
                  <li>Cross-check on USGS National Map and FEMA flood map service.</li>
                  <li>
                    Confirm the PLSS section/township/range via BLM GLO Records and the
                    USGS topo quad covering the point.
                  </li>
                  <li>
                    Verify city-limit status — the point may be unincorporated county
                    land rather than inside a municipality.
                  </li>
                </ul>
              </Card>
            </div>
          </Section>

          {/* Jurisdiction */}
          <Section
            id="jurisdiction"
            index="02"
            title="Parcel & jurisdiction"
            subtitle="Who governs the land, who taxes it, and which offices hold the records."
          >
            <div className="grid grid-cols-1 gap-5 md:grid-cols-2 lg:grid-cols-3">
              <Card title="Governing bodies">
                <ul className="flex flex-col gap-1.5 text-sm leading-relaxed text-foreground">
                  <li>State of Missouri (statutes, DNR, DOT)</li>
                  <li>Marion County (assessor, recorder, commission)</li>
                  <li>City/village only if inside municipal limits</li>
                  <li>Township (civil) — minor/administrative role</li>
                </ul>
              </Card>
              <Card title="Likely taxing layers">
                <ul className="flex flex-col gap-1.5 text-sm leading-relaxed text-foreground">
                  <li>County general + road &amp; bridge</li>
                  <li>School district</li>
                  <li>Fire protection district</li>
                  <li>Possible special / improvement districts</li>
                </ul>
              </Card>
              <Card title="Record holders">
                <ul className="flex flex-col gap-1.5 text-sm leading-relaxed text-foreground">
                  <li>Recorder of Deeds — title chain, easements</li>
                  <li>Assessor / GIS — parcel, value, maps</li>
                  <li>Public Works — utility as-builts</li>
                  <li>State/Federal — environmental, flood, pipelines</li>
                </ul>
              </Card>
            </div>
          </Section>

          {/* Township */}
          <Section
            id="township"
            index="03"
            title="&ldquo;Township 59&rdquo; & ownership myths"
            subtitle="Clearing up what a township is — and what it is not."
          >
            <div className="grid grid-cols-1 gap-5 lg:grid-cols-2">
              <Card title="What Township 59 North actually means">
                <p className="text-sm leading-relaxed text-foreground">
                  In the Public Land Survey System, &ldquo;Township 59 North&rdquo; is a
                  row of the survey grid measured north of a baseline, on the Fifth
                  Principal Meridian used across Missouri. Combined with a Range
                  (east/west column) and a Section number (1&ndash;36), it pinpoints a
                  one-square-mile block. It is a <em>location descriptor</em>, established
                  by federal survey.
                </p>
                <div className="mt-3">
                  <ULabel level="verified" />
                </div>
              </Card>
              <Card title="It does not by itself mean a city/county/LLC owns your land">
                <p className="text-sm leading-relaxed text-foreground">
                  A township appearing in a legal description does not transfer ownership
                  to a city, county, or company. Ownership is set by the recorded deed and
                  chain of title. Claims that &ldquo;the township owns you&rdquo; or that a
                  hidden LLC holds your land are <strong>speculative</strong> and should be
                  tested only by pulling the actual recorded deed and tax records.
                </p>
                <div className="mt-3 flex gap-2">
                  <ULabel level="speculative" />
                </div>
              </Card>
            </div>
          </Section>

          {/* Legend */}
          <Section
            id="legend"
            index="04"
            title="Map legend & key"
            subtitle="A professional legend covering boundaries, zoning, hydrology, transportation, utilities, survey, and districts — with a plain-English meaning for each."
          >
            <MapLegend />
          </Section>

          {/* Water */}
          <Section
            id="water"
            index="05"
            title="Springs, caves & water rights"
            subtitle="What it means to own land near flowing water or karst features in Missouri."
          >
            <div className="grid grid-cols-1 gap-5 lg:grid-cols-2">
              <Card title="Water rights (legally usable info)">
                <ul className="flex flex-col gap-2 text-sm leading-relaxed text-foreground">
                  <li>
                    <strong>Riparian rights:</strong> Missouri follows reasonable-use
                    riparian doctrine — owners along a watercourse may make reasonable use
                    of the water. <ULabel level="verified" />
                  </li>
                  <li>
                    <strong>Navigable waters:</strong> the bed of a navigable stream may be
                    held by the state in public trust; the public may have access.{" "}
                    <ULabel level="strong" />
                  </li>
                  <li>
                    <strong>Setbacks / floodplain / wetland:</strong> building near streams
                    triggers FEMA flood zones and possible wetland limits.{" "}
                    <ULabel level="strong" />
                  </li>
                  <li>
                    <strong>Groundwater &amp; drainage:</strong> separate rules govern wells
                    and surface runoff between neighbors. <ULabel level="likely" />
                  </li>
                </ul>
              </Card>
              <Card title="Caves & karst geology">
                <ul className="flex flex-col gap-2 text-sm leading-relaxed text-foreground">
                  <li>
                    Springs and caves are strong indicators of <strong>karst</strong>{" "}
                    (soluble limestone) common in Missouri. <ULabel level="strong" />
                  </li>
                  <li>
                    Karst affects septic suitability, well safety, sinkhole risk, and
                    foundations. <ULabel level="strong" />
                  </li>
                  <li>
                    Caves can create liability and may carry conservation protections or
                    endangered-species considerations. <ULabel level="likely" />
                  </li>
                  <li>
                    Subsurface/cave ownership can be severed from the surface estate —
                    confirm in the deed. <ULabel level="possible" />
                  </li>
                </ul>
              </Card>
            </div>
          </Section>

          {/* Electricity */}
          <Section
            id="electricity"
            index="06"
            title="Natural electricity — fact vs. theory"
            subtitle="The prompt asked about 'natural free electricity' from water and earth. Here it is, strictly separated by evidence level."
          >
            <div className="grid grid-cols-1 gap-5 lg:grid-cols-3">
              <Card title="Verified engineering">
                <ul className="flex flex-col gap-2 text-sm leading-relaxed text-foreground">
                  <li>Micro-hydro generation from sufficient flow + head is real and well understood.</li>
                  <li>Hydraulic ram pumps move water using flow energy, no electricity needed.</li>
                  <li>Geothermal heat pumps use stable ground temperature for heating/cooling.</li>
                </ul>
                <div className="mt-3"><ULabel level="verified" /></div>
              </Card>
              <Card title="Conditional / site-dependent">
                <ul className="flex flex-col gap-2 text-sm leading-relaxed text-foreground">
                  <li>Whether THIS site has usable head and flow is unknown without field measurement.</li>
                  <li>Water-rights and dam permits may be required to build any diversion.</li>
                  <li>Piezoelectric/EM effects exist but are not practical power sources at this scale.</li>
                </ul>
                <div className="mt-3"><ULabel level="possible" /></div>
              </Card>
              <Card title="Speculative / esoteric">
                <ul className="flex flex-col gap-2 text-sm leading-relaxed text-foreground">
                  <li>&ldquo;Free energy&rdquo; from earth fields, ley lines, or springs as power.</li>
                  <li>Symbolic/ancient interpretations of water and caves as energy sources.</li>
                  <li>Presented for completeness only — not established science.</li>
                </ul>
                <div className="mt-3"><ULabel level="speculative" /></div>
              </Card>
            </div>
          </Section>

          {/* Poles */}
          <Section
            id="poles"
            index="07"
            title="Utility poles & easements"
            subtitle="Why poles sit where they do, and what to verify about easements crossing the land."
          >
            <div className="grid grid-cols-1 gap-5 lg:grid-cols-2">
              <Card title="Pole placement & spacing (typical)">
                <ul className="flex flex-col gap-2 text-sm leading-relaxed text-foreground">
                  <li>Rural distribution poles commonly sit ~125&ndash;300+ ft apart, along roads/ROW. <ULabel level="likely" /></li>
                  <li>Placement follows the recorded utility easement, not the yard&apos;s aesthetics. <ULabel level="strong" /></li>
                  <li>Transmission lines need much wider easements than distribution. <ULabel level="verified" /></li>
                  <li>Relocation is usually possible but the requesting owner often pays. <ULabel level="likely" /></li>
                </ul>
              </Card>
              <Card title="Easement checklist">
                <ul className="flex list-inside list-disc flex-col gap-1.5 text-sm leading-relaxed text-foreground">
                  <li>Is there a recorded utility easement on the parcel?</li>
                  <li>Who owns each pole (electric co-op, telecom, joint use)?</li>
                  <li>What width and use does the easement grant?</li>
                  <li>Are there access/maintenance rights across the yard?</li>
                  <li>Any vegetation-management or build-restriction terms?</li>
                </ul>
              </Card>
            </div>
          </Section>

          {/* Proximity */}
          <Section
            id="proximity"
            index="08"
            title="Railroad / factory / industrial proximity"
            subtitle="How nearby infrastructure can raise or lower land value and use."
          >
            <div className="grid grid-cols-1 gap-5 md:grid-cols-2">
              <Card title="Possible negatives">
                <ul className="flex list-inside list-disc flex-col gap-1.5 text-sm leading-relaxed text-foreground">
                  <li>Noise, vibration, and air/odor from rail or factories</li>
                  <li>Contamination / brownfield history (check DNR &amp; EPA)</li>
                  <li>Wider easements and right-of-way encumbrances</li>
                  <li>Possible stigma affecting resale</li>
                </ul>
                <div className="mt-3"><ULabel level="likely" /></div>
              </Card>
              <Card title="Possible positives">
                <ul className="flex list-inside list-disc flex-col gap-1.5 text-sm leading-relaxed text-foreground">
                  <li>Industrial/commercial zoning can raise value for the right buyer</li>
                  <li>Rail spur or highway access aids logistics-dependent uses</li>
                  <li>Utilities are often already nearby and sized up</li>
                  <li>Abandoned rail corridors can become trails or revert to abutters</li>
                </ul>
                <div className="mt-3"><ULabel level="possible" /></div>
              </Card>
            </div>
          </Section>

          {/* Trust */}
          <Section
            id="trust"
            index="09"
            title="Trusts, title & public recording"
            subtitle="How real estate can be held in trust and what 'public registration of a private trust' really involves."
          >
            <div className="grid grid-cols-1 gap-5 lg:grid-cols-2">
              <Card title="How trusts hold land">
                <p className="text-sm leading-relaxed text-foreground">
                  A trustee holds <em>legal</em> title for the benefit of beneficiaries who
                  hold <em>equitable</em> title. Property is moved into a trust by recording
                  a deed to the trustee. The deed is public; the trust&apos;s internal terms
                  and beneficiaries are usually kept private (often only a memorandum of
                  trust is recorded).
                </p>
                <div className="mt-3"><ULabel level="verified" /></div>
              </Card>
              <Card title="Public vs private — cautions">
                <ul className="flex list-inside list-disc flex-col gap-1.5 text-sm leading-relaxed text-foreground">
                  <li>Recording a full private trust can expose sensitive details publicly.</li>
                  <li>&ldquo;Registering&rdquo; a trust does not create extra-legal ownership powers.</li>
                  <li>Fringe &ldquo;land patent / allodial reclaim&rdquo; theories are not recognized title methods.</li>
                  <li>Confirm any structure with a licensed Missouri real-estate attorney.</li>
                </ul>
                <div className="mt-3 flex gap-2"><ULabel level="speculative" /></div>
              </Card>
            </div>
          </Section>

          {/* Glossary */}
          <Section
            id="glossary"
            index="10"
            title="Black&apos;s Law land &amp; title glossary"
            subtitle="Key terms with a Black's Law-style definition, a plain-English meaning, and the effect on land or title. Searchable."
          >
            <Glossary />
          </Section>

          {/* History */}
          <Section
            id="history"
            index="11"
            title="Historical & old-map research plan"
            subtitle="Where to look for the deep history of this exact ground — clearly separated from speculation."
          >
            <div className="grid grid-cols-1 gap-5 lg:grid-cols-2">
              <Card title="Documented sources to pull">
                <ul className="flex list-inside list-disc flex-col gap-1.5 text-sm leading-relaxed text-foreground">
                  <li>BLM GLO original land patents &amp; survey plats</li>
                  <li>USGS historical topographic quads (topoView)</li>
                  <li>Sanborn &amp; county atlas / plat-book maps</li>
                  <li>County histories and Library of Congress map collections</li>
                  <li>State archives and indigenous/tribal land records</li>
                </ul>
                <div className="mt-3"><ULabel level="strong" /></div>
              </Card>
              <Card title="Alternative / esoteric layer">
                <p className="text-sm leading-relaxed text-foreground">
                  Pre-mainstream, symbolic, or ancient interpretations (earthworks lore, ley
                  lines, mound-builder myths) are recorded here only as
                  <strong> clearly-labeled speculation</strong> for research interest. They
                  carry no legal weight and are not presented as fact.
                </p>
                <div className="mt-3"><ULabel level="speculative" /></div>
              </Card>
            </div>
          </Section>

          {/* Underground */}
          <Section
            id="underground"
            index="12"
            title="Underground tunnels, pipelines & hidden infrastructure"
            subtitle="What can actually be found in public records — and where the line is."
          >
            <Card>
              <ul className="flex list-inside list-disc flex-col gap-2 text-sm leading-relaxed text-foreground">
                <li>
                  <strong>PHMSA National Pipeline Mapping System</strong> shows public
                  transmission pipelines by area. <ULabel level="verified" />
                </li>
                <li>
                  <strong>County Public Works as-builts</strong> document sewer, water, and
                  stormwater lines and culverts. <ULabel level="strong" />
                </li>
                <li>
                  <strong>Call-before-you-dig (811)</strong> locates buried utilities before
                  excavation. <ULabel level="verified" />
                </li>
                <li>
                  Claims of secret tunnels or undocumented networks are{" "}
                  <strong>speculative</strong> unless a public record confirms them.{" "}
                  <ULabel level="speculative" />
                </li>
              </ul>
            </Card>
          </Section>

          {/* Records */}
          <Section
            id="records"
            index="13"
            title="Records request checklist"
            subtitle="Exactly what to ask each office to confirm the facts in this report."
          >
            <div className="grid grid-cols-1 gap-5 md:grid-cols-2">
              {RECORDS_REQUESTS.map((r) => (
                <Card key={r.office} title={r.office}>
                  <ul className="flex list-inside list-disc flex-col gap-1.5 text-sm leading-relaxed text-foreground">
                    {r.ask.map((a) => (
                      <li key={a}>{a}</li>
                    ))}
                  </ul>
                </Card>
              ))}
            </div>
          </Section>

          {/* Agents */}
          <Section
            id="agents"
            index="14"
            title="Master agent system (architecture)"
            subtitle="The prompt described a multi-agent 'Master OS.' Here is a clean, buildable breakdown of each agent and its job — this dashboard is the first concrete output (Agent L)."
          >
            <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
              {AGENTS.map((a) => (
                <div
                  key={a.code}
                  className="flex flex-col gap-2 rounded-lg border border-border bg-card p-4 text-card-foreground shadow-sm"
                >
                  <div className="flex items-center gap-2">
                    <span className="inline-flex h-7 w-7 items-center justify-center rounded-md bg-primary font-mono text-xs font-semibold text-primary-foreground">
                      {a.code}
                    </span>
                    <h3 className="font-serif text-base font-semibold text-foreground">
                      {a.name}
                    </h3>
                  </div>
                  <p className="text-sm leading-relaxed text-muted-foreground">{a.does}</p>
                </div>
              ))}
            </div>
          </Section>

          <footer className="mt-12 border-t border-border pt-6 text-sm leading-relaxed text-muted-foreground">
            <p>
              <strong className="text-foreground">Disclaimer.</strong> This dashboard is
              organized research and a question framework. It is not legal, engineering,
              financial, or title advice. Confidence tags indicate evidence strength;
              verify all specifics with Marion County offices and licensed professionals
              before acting.
            </p>
          </footer>
        </div>
      </main>
    </div>
  );
}
