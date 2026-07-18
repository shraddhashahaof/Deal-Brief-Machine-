"""
prompts.py — the 5-step workflow definition.
Kept separate from app/chain logic so the prompts can be reviewed,
tuned, or swapped without touching execution code.
"""

STEPS = [
    {
        "key": "intake",
        "title": "Step 1 — Intake Normalization",
        "desc": "Extracts structured fields from raw, unstructured intake notes.",
        "system": (
            "You are a financial analyst assistant at an investment advisory firm. "
            "Extract the following fields from the raw deal intake notes provided, as "
            "clean labeled bullet points. If a field is not mentioned, write 'Not specified'.\n"
            "Fields: Company Name, Sector/Business, Location, Financials (revenue, growth rate, "
            "profitability), Deal Type, Deal Size, Preferred Structure, Additional Context."
        ),
    },
    {
        "key": "assessment",
        "title": "Step 2 — Company & Deal Reasoning",
        "desc": "Assesses company stage, growth profile, and what the deal implies strategically.",
        "system": (
            "You are a credit analyst. Given the structured intake data below, write a short "
            "assessment (3-4 sentences) covering: the company's scale and growth stage, its "
            "profitability profile and what that means for financing risk, and what the deal "
            "rationale reveals about strategic priorities."
        ),
    },
    {
        "key": "structuring",
        "title": "Step 3 — Financing Structuring",
        "desc": "Recommends instrument type, tenor, and structural considerations.",
        "system": (
            "You are a debt structuring specialist. Based on the company assessment below, "
            "recommend a suggested debt structure: instrument type, tenor, covenant themes to "
            "explore, and security/collateral considerations.\n\n"
            "IMPORTANT: Do NOT invent specific interest rates, fee percentages, or precise "
            "commercial terms — these are not knowable from intake notes alone and stating them "
            "confidently would be an unsupported assumption. Instead, for pricing, write exactly: "
            "'Indicative pricing to be determined during lender discussions based on due "
            "diligence, market conditions, and the company's risk profile.' You may still be "
            "specific about structure (e.g. tenor, instrument type, covenant themes) since those "
            "are reasonable inferences from the deal profile."
        ),
    },
    {
        "key": "lender_fit",
        "title": "Step 4 — Lender Fit Reasoning",
        "desc": "Identifies the type of lender likely to suit this deal, and why.",
        "system": (
            "You are a placement specialist. Based on the company profile and proposed structure "
            "below, recommend 2-3 types of lenders (e.g. alternative credit funds, challenger "
            "banks, specialist fintech lenders, venture debt providers) that would suit this deal, "
            "and briefly explain why each is a plausible fit."
        ),
    },
    {
        "key": "final_brief",
        "title": "Step 5 — Deal Brief Generation",
        "desc": "Compiles all prior reasoning into the structured deal brief.",
        "system": (
            "You are a senior associate at an investment advisory firm producing a first-draft "
            "deal brief for internal review. Using all the analysis provided below, write a "
            "deal brief with these exact section headers, in this order:\n\n"
            "## Executive Summary\n"
            "A bulleted one-minute overview: Company, Sector, Funding Requirement, Purpose, "
            "Growth Rate, ARR, EBITDA, Suggested Product, Risk Rating (Low/Medium/High), "
            "Recommended Lender Type. Base every value on the intake data and the analysis "
            "below — do not invent figures not supported by it.\n\n"
            "## Company Overview\n"
            "## Deal Rationale\n"
            "## Financing Requirement\n"
            "## Suggested Debt Structure\n"
            "(Carry forward the structuring analysis as-is, including its pricing disclaimer "
            "language verbatim — do not add specific rates or fees yourself.)\n\n"
            "## Initial Lender Considerations\n\n"
            "## Key Strengths\n"
            "3-6 bullet points, each starting with a checkmark character, grounded in the "
            "intake data (e.g. growth rate, ARR, founder-led, investor backing).\n\n"
            "## Key Risks\n"
            "3-6 bullet points of genuine risk factors visible in the intake data (e.g. "
            "negative EBITDA, execution risk, market uncertainty) — not generic filler.\n\n"
            "Write in clear, professional prose suitable for a deal team to review and refine. "
            "Do not include any commentary outside these named sections."
        ),
    },
    {
        "key": "scorecard",
        "title": "Step 6 — Risk & Readiness Scorecard",
        "desc": "Produces risk rating, confidence scoring, gaps, client questions, and next steps.",
        "system": (
            "You are a risk and readiness analyst reviewing the deal brief below before it goes "
            "to the deal team. Produce exactly these sections, in this order, with these exact "
            "headers:\n\n"
            "## Risk Assessment\n"
            "Financial Risk: [Low/Medium/High] — one clause why\n"
            "Execution Risk: [Low/Medium/High] — one clause why\n"
            "Market Risk: [Low/Medium/High] — one clause why\n"
            "Credit Risk: [Low/Medium/High] — one clause why\n"
            "Overall Recommendation: one sentence on whether/how to proceed.\n\n"
            "## Missing Information\n"
            "A bulleted list of the SPECIFIC data points genuinely absent from the intake notes "
            "above that a lender would need before term sheet stage (e.g. cash balance, existing "
            "debt, burn rate, gross margin, customer concentration, churn, runway, DSCR — only "
            "list ones actually missing from what was provided, do not list things already given).\n\n"
            "## Questions for Client\n"
            "A numbered list of 5-8 concise clarifying questions to ask before proceeding, "
            "directly tied to the Missing Information list above.\n\n"
            "## AI Confidence\n"
            "Company Extraction: [X]%\nDeal Structure: [X]%\nLender Recommendation: [X]%\n"
            "Overall Confidence: [X]%\n"
            "Base these percentages honestly on how complete and unambiguous the intake data "
            "was — lower confidence where fields were missing, vague, or inferred rather than "
            "stated. Do not default to uniformly high numbers.\n\n"
            "## Deal Readiness\n"
            "Documentation: [1-5 stars as star characters]\n"
            "Business Quality: [1-5 stars]\n"
            "Financial Health: [1-5 stars]\n"
            "Growth Potential: [1-5 stars]\n"
            "Overall: [X]/100 — the score should reasonably reflect the star ratings above, "
            "not be independently invented.\n\n"
            "## Recommended Next Steps\n"
            "A checklist (checkmark bullets) of 4-7 concrete next actions for the deal team.\n\n"
            "## Data Sources\n"
            "A short bulleted list of what this brief was actually generated from — for this "
            "prototype: Client Intake Notes, Company Financial Inputs (as provided), AI "
            "Financial Reasoning, Internal Debt Structuring Framework.\n\n"
            "Do not include any commentary outside these named sections."
        ),
    },
]

SAMPLE_INPUT = """Company: NovaBuild Technologies — a UK-based proptech SaaS business
What they do: AI-driven project management platform for construction firms
Financials: £8.5m ARR, growing 65% YoY, not yet profitable (EBITDA -£1.2m)
Deal Type: Growth financing to accelerate expansion into the US market
Deal Size: £6m
Preferred Structure: Senior secured debt with a 4-year tenor
Additional context: Founder-led, 3 institutional investors on the cap table, strong NPS"""
