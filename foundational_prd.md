# Part 1: Product Overview

1.1 What PriceCheck Does

**PriceCheck** is a Chrome browser extension that exposes pricing manipulation tactics used by retailers. When a user is on any product page, they click the PriceCheck icon in their browser toolbar. The extension reads the page they are already on, sends the content to an AI analysis backend, and returns a Gaslighting Score from 0 to 100 along with a breakdown of every manipulation tactic detected.

No URL copying. No tab switching. The extension works on the page the user is already looking at.

1.2 The Two-Surface Product

**PriceCheck** is two things that work together.
•	The Chrome extension is the core product. This is what users install and use daily.

•	The landing page is the marketing surface. This is what judges see, what the demo video links to, and what explains the product to someone encountering it for the first time.
The landing page does not replace the extension. It sells it.

1.3 The One-Line Pitch

"You think you are getting a deal. PriceCheck shows you the truth."

1.4 Why an Extension Wins Over a Web App

Dimension	Web App	Chrome Extension
User flow	Copy URL, open app, paste, submit	Click icon on page you are already on
Demo moment	Paste a URL and wait	Click icon on live Amazon listing and watch it analyze
Scraping	Playwright needed (complex, brittle)	Content script reads DOM natively (fast, reliable)
Credibility	Feels like a demo	Feels like real software
Competition angle	Another web tool	Consumer protection utility -- familiar category

1.5 Why This Wins

•	Universal relatability -- every judge has been price-manipulated. The emotional connection is instant.
•	Novel framing -- price comparison tools exist. A tool that explains HOW you are being tricked does not.
•	Extension format -- clicking an icon on a real product page is a more compelling demo than pasting a URL.
•	Technical depth -- LangGraph agent + content script + Claude API + domain trust layer shows full-stack complexity.
•	Domain trust layer -- no other price tool also detects whether the site itself is fraudulent.
•	Real product potential -- this is a browser extension people would actually install and use.
 
# Part 2: Detection Categories

PriceCheck detects 7 categories. The first 6 apply to legitimate retailers. The 7th is a silent layer that runs automatically on every analysis.

Category	What It Detects	Example

*Fake Discounts*	Inflated original prices, was/now manipulation, perpetual sales that never end	Was $299, Now $149 -- but $299 was never charged to any customer

*Hidden Fees*	Mandatory charges withheld until checkout: resort fees, service fees, convenience fees	Hotel $99/night becomes $159 with mandatory fees added at checkout

*Drip Pricing*	Base price shown upfront, mandatory extras added one by one through the purchase flow	Concert ticket $45 base becomes $74 after 4 sequential fee additions

*Dark Patterns*	Fake urgency timers, pre-checked add-ons, manipulative social proof claims	Countdown timer that resets on every single page visit

*Subscription Traps*	Free trials that auto-convert to paid, hard-to-cancel recurring charges	Free 7-day trial auto-enrolls at $49/month with cancellation buried 4 screens deep

*Shrinkflation*	Same price, smaller quantity -- price-per-unit calculation exposes the real increase	Cereal bag reduced from 18oz to 14.5oz at the same shelf price

*Fraudulent Storefronts*	Scam sites impersonating real retailers to steal payment information	nike-outlet-clearance.shop registered 12 days ago, 70% below retail, Gmail contact

2.1 The Gaslighting Score
Each analysis produces a weighted score from 0 to 100 based on the number and severity of manipulation tactics detected.

Score	Label	Meaning

0 to 20	Honest Pricing	What you see is what you pay. No meaningful manipulation detected.

21 to 45	Mildly Misleading	Some common tactics present. Typical for most large retailers.

46 to 70	Actively Deceptive	Multiple tactics layered. Real price significantly higher than shown.

71 to 100	Full Gaslighting	Aggressive, layered manipulation. Real cost far exceeds advertised price.

2.2 Domain Trust Layer

This runs silently on every submission. The user sees nothing unless a flag is raised. Three possible outcomes:

•	PASS (trust score 70+): no notice shown. Analysis proceeds and displays normally.
•	WARN (trust score 30 to 69): amber notice at top of popup: unable to fully verify this retailer, proceed with caution. Analysis still runs.
•	FAIL (trust score below 30): hard red screen replaces the normal results. No score shown. Lists specific signals that triggered the failure.

Trust signals evaluated: domain age via WHOIS API, brand name in page title vs actual domain URL, price plausibility vs market rate, contact information legitimacy (Gmail address on a claimed major retailer is a hard flag), quality and authenticity of legal copy.

Important: SSL presence is checked but not weighted positively. Scam sites have SSL. The padlock does not mean safety.
 
# Part 3: Technical Architecture

3.1 System Overview

Three components. The Chrome extension handles UI and page reading. The FastAPI backend runs the LangGraph agent. The landing page is a separate static site.

Component	Technology	Hosted On

Chrome Extension UI	React + Vite (built to extension popup)	Chrome -- loaded as unpacked or zip

Extension Content Script	Vanilla JavaScript	Injected into active browser tab
Backend API	FastAPI (Python)	Render
Agent Framework	LangGraph	Render (within FastAPI)
AI Analysis	Claude claude-sonnet-4-6	Anthropic API
Image OCR	Claude Vision (same API)	Anthropic API
Domain Trust	URLScan.io + WHOIS API	External APIs
Landing Page	React + Vite or plain HTML	Netlify
Price History (stretch)	SerpAPI	External API

3.2 How the Extension Reads Pages

This is the key architectural difference from a web app. There is no Playwright. No server-side scraping. The extension reads the page natively.

When the user clicks the PriceCheck icon, Chrome runs the content script inside the active tab. The content script has direct access to the page DOM. It extracts the page title, all visible text, any elements containing price patterns (dollar signs, percent signs, was/now language, countdown timers), and the current URL. It packages this into a structured object and sends it to the extension popup via Chrome message passing. The popup sends it to the FastAPI backend. The backend runs the LangGraph pipeline. The popup displays the results.

This approach is faster than Playwright, more reliable (no scraping timeouts, no JS rendering issues), and requires no headless browser infrastructure on the server.

3.3 Repository Structure
pricecheck/
  /extension                   Chrome extension (primary product)
    /public
      icon16.png               Extension icon sizes (required by Chrome)
      icon32.png
      icon48.png
      icon128.png
      manifest.json            Extension configuration (see Part 4)
    /src
      /components
        ScoreDisplay.jsx        Gaslighting Score badge with count-up animation
        TacticCard.jsx          Individual red-flag card
        SplitScreen.jsx         Marketed vs real price comparison
        TrustBadge.jsx          Domain legitimacy indicator (3 states)
        LoadingNarrative.jsx    Step-by-step loading animation
      /pages
        Popup.jsx               Main popup view (root component)
        ResultsView.jsx         Full analysis results
        ScamView.jsx            Hard red scam warning screen
      content_script.js         Injected into active tab to read DOM
      popup.html                Entry HTML for the popup
      popup.jsx                 React root mount
    vite.config.js              Configured for extension output
    tailwind.config.js
  /backend                     FastAPI + LangGraph
    /app
      main.py                  FastAPI app, CORS, routes
      /graph
        graph.py               LangGraph StateGraph definition
        state.py               PriceCheckState TypedDict
        nodes.py               All node functions
        edges.py               Conditional edge router functions
      /services
        trust.py               URLScan + WHOIS trust checks
        claude.py              Claude API wrapper
      /models
        schemas.py             Pydantic request/response models
      /prompts
        analysis.py            Claude system prompt
    requirements.txt
  /landing                     Marketing landing page
    index.html                 Can be plain HTML or React
    (mirrors the 6-section structure from Part 5)
  README.md
  DEMO_URLS.md                 5 pre-tested URLs with expected results
  .env.example

3.4 Data Flow End to End

Step	What Happens
1. User on product page	User navigates to any retail product page in Chrome
2. User clicks icon	Chrome opens the extension popup (popup.html / Popup.jsx renders)
3. Popup requests page data	Popup sends message to content_script.js via chrome.tabs.sendMessage
4. Content script extracts	content_script.js reads DOM, finds prices, titles, page text, returns structured object
5. Popup calls backend	Popup POSTs extracted page data to FastAPI /analyze endpoint on Render
6. LangGraph runs	Backend routes through agent: trust check, Claude analysis, scoring
7. Backend responds	FastAPI returns AnalyzeResponse JSON with score, tactics, trust state
8. Popup renders results	React components animate in: trust badge, split screen, tactic cards, score
 
# Part 4: Extension Structure

4.1 manifest.json
The manifest is the configuration file that tells Chrome what the extension is, what it can do, and which files do what. Every field is required.

MANIFEST.JSON -- COMPLETE
{
  "manifest_version": 3,
  "name": "PriceCheck",
  "version": "1.0",
  "description": "See the real price. Stop getting played.",
  "permissions": ["activeTab", "scripting", "storage"],
  "host_permissions": ["<all_urls>"],
  "action": {
    "default_popup": "popup.html",
    "default_icon": {
      "16": "icon16.png",
      "32": "icon32.png",
      "48": "icon48.png",
      "128": "icon128.png"
    }
  },
  "content_scripts": [{
    "matches": ["<all_urls>"],
    "js": ["content_script.js"],
    "run_at": "document_idle"
  }],
  "icons": {
    "16": "icon16.png",
    "48": "icon48.png",
    "128": "icon128.png"
  }
}

Permissions explanation:
•	activeTab -- allows reading the currently active tab URL and injecting scripts on demand.
•	scripting -- allows programmatic injection of the content script.
•	storage -- allows caching recent analysis results so re-opening the popup does not re-run the API call.
•	host_permissions all_urls -- allows the content script to run on any website.

4.2 content_script.js
This file runs inside the active tab. It has full access to the page DOM. It does not have access to the extension popup directly -- it communicates via Chrome message passing.

CONTENT_SCRIPT.JS -- LOGIC
// Listens for a message from the popup requesting page data
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action !== 'extractPageData') return;

  const data = {
    url: window.location.href,
    title: document.title,
    // All visible text -- the main input for Claude analysis
    bodyText: document.body.innerText.slice(0, 15000),
    // Targeted price element extraction
    priceElements: extractPriceElements(),
    // Meta description for additional context
    metaDescription: getMeta('description'),
  };

  sendResponse(data);
});

function extractPriceElements() {
  // Finds elements containing price patterns
  // Looks for: $ symbols, was/now patterns, % off, countdown timers
  // Returns array of {text, selector} objects
}

function getMeta(name) {
  const el = document.querySelector(`meta[name='${name}']`);
  return el ? el.getAttribute('content') : '';
}

4.3 Vite Configuration for Extension Output
A standard Vite React app builds to a single HTML file with bundled JS. An extension needs specific output: popup.html, popup.js, and content_script.js as separate files. The Vite config handles this.

VITE.CONFIG.JS -- KEY SETTINGS
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import { resolve } from 'path';

export default defineConfig({
  plugins: [react()],
  build: {
    outDir: 'dist',
    rollupOptions: {
      input: {
        popup: resolve(__dirname, 'src/popup.html'),
        content_script: resolve(__dirname, 'src/content_script.js'),
      },
      output: {
        entryFileNames: '[name].js',
      }
    }
  }
});

4.4 Popup UI Dimensions
Chrome extension popups have size constraints. Design within these boundaries.
•	Width: 400px fixed. Set in CSS on the root element.
•	Height: up to 600px. Content should scroll gracefully if results are long.
•	The popup closes if the user clicks outside it. Results should be readable without interaction.
•	Font sizes, spacing, and component sizes from the design system all apply -- just within the 400px constraint.
 
# Part 5: LangGraph Architecture
LangGraph builds the analysis pipeline as a stateful directed graph. Each step is a node. Conditional edges route based on what is found at each step. The pipeline can short-circuit early if a site is fraudulent, skip straight to results if trust passes, and handle different input types through the same consistent state object.

5.1 State Object
All nodes read from and write to a shared PriceCheckState TypedDict. Defined in state.py.

PRICECHECKSTATE -- STATE.PY
class PriceCheckState(TypedDict):
    # Input -- from content script via popup
    input_type: str           # 'page' | 'image' | 'manual'
    page_url: str             # current tab URL
    page_title: str           # document.title
    body_text: str            # document.body.innerText (truncated 15k chars)
    price_elements: list      # targeted price DOM extracts
    raw_image: bytes | None   # if screenshot path used
    manual_text: str | None   # if manual entry path used

    # After trust check
    trust_score: int          # 0 to 100
    trust_signals: list[str]  # human-readable flag descriptions
    trust_gate_pass: bool

    # After Claude analysis
    tactics: list[dict]       # {name, severity, evidence, explanation}
    marketed_price: float | None
    real_price: float | None
    price_delta: float | None
    real_cost_note: str | None

    # After scoring
    gaslighting_score: int    # 0 to 100
    severity_label: str

    # Flags
    is_scam: bool
    error: str | None

5.2 Node Definitions
Node	Type	Behavior
input_router	Conditional Entry	Reads input_type from state. Routes to content_node (page), ocr_node (image), or manual_node (text).
content_node	Pass-through	Receives pre-extracted page data from content script. Formats body_text and price_elements into raw_content for analysis. No scraping needed.
ocr_node	Tool -- Claude Vision	Sends raw_image bytes to Claude API with extraction prompt. Returns pricing text. Writes to raw_content equivalent fields.
manual_node	Pass-through	Copies manual_text into the content fields. Skips all extraction.
trust_node	Tool -- URLScan + WHOIS	Checks domain age, brand vs URL mismatch, price plausibility, contact legitimacy. Writes trust_score (0-100) and trust_signals list.
trust_gate	Conditional Edge	If trust_score < 30: sets is_scam=True, routes directly to output_node. If trust_score >= 30: routes to analyze_node.
analyze_node	Core -- Claude API	Sends formatted page content to claude-sonnet-4-6. Returns structured JSON: tactics array, marketed_price, real_price, price_delta, real_cost_note.
score_node	Logic -- Pure Python	Applies category weights to tactic severities. Sums and normalizes to 0-100. Sets gaslighting_score and severity_label. No API call.
output_node	Terminal	Serializes full state to AnalyzeResponse Pydantic schema. FastAPI returns JSON to extension popup.

5.3 Edge Map
From Node	To Node -- Condition
START	input_router (always)
input_router	content_node (input_type == 'page')
input_router	ocr_node (input_type == 'image')
input_router	manual_node (input_type == 'manual')
content_node	trust_node (always)
ocr_node	trust_node (always)
manual_node	trust_node (always)
trust_node	trust_gate (always)
trust_gate	output_node (trust_score < 30 -- scam exit)
trust_gate	analyze_node (trust_score >= 30)
analyze_node	score_node (always)
score_node	output_node (always)
output_node	END (always)

5.4 Claude API Prompt Strategy
The system prompt in analyze_node is the core intelligence. These are the required elements:

•	Role: consumer protection analyst specializing in pricing psychology and retail dark patterns.
•	Task: analyze the provided page content and identify every pricing manipulation tactic present.
•	Output: return ONLY valid JSON. No preamble. No explanation. No markdown fences. Raw JSON only.
•	Evidence requirement: for every tactic flagged, cite the specific text from the page that supports it. Do not speculate.
•	Tone of explanations: plain English a non-expert understands. One sentence per tactic.
•	Constraint: if no manipulation is detected for a category, do not include it. Only flag what is present.

EXPECTED JSON RESPONSE SCHEMA
{
  "tactics": [
    {
      "name": "FAKE_DISCOUNT",
      "severity": 8,
      "evidence": "Was $299 shown crossed out -- no historical price data supports this figure",
      "explanation": "The original price shown has likely never been charged to any customer."
    }
  ],
  "marketed_price": 149.00,
  "real_price": 149.00,
  "price_delta": 0,
  "real_cost_note": "Price is accurate. Manipulation here is psychological, not financial."
}

5.5 Scoring Algorithm
Score node applies category weights to each detected tactic severity. Pure Python, no API call.

Category	Weight	Rationale
HIDDEN_FEES	1.3	Direct financial harm -- user pays more than shown
DRIP_PRICING	1.2	Systematic sequential deception through checkout
FAKE_DISCOUNT	1.2	Exploits anchoring bias, very common
SUBSCRIPTION_TRAP	1.1	Long-term recurring financial harm
DARK_PATTERNS	0.9	Psychological manipulation, variable severity
SHRINKFLATION	0.8	Real harm but harder to detect from single page
FRAUDULENT_STOREFRONT	Override	Sets score to minimum 95 regardless of other tactics
Formula: sum(severity * weight) for each tactic, normalize to 0-100 scale. Cap at 100.
 
# Part 6: UI Structure
6.1 Extension Popup -- View States
The popup has 4 distinct view states. Each maps to a React component.

State	Renders When	What Shows
Idle	Popup opens, no analysis yet	PriceCheck logo, Analyze This Page button, brief tagline
Loading	API call in progress	Staggered loading narrative: 4 lines appearing sequentially
Results	Analysis complete, trust passed	Trust badge, split screen, tactic cards, Gaslighting Score
Scam	trust_score below 30	Hard red warning, trust signals listed, no score shown

6.2 Loading Narrative Sequence
The loading state is not a spinner. It is a narrative that builds while the user waits. Each line appears with 700ms stagger using Framer Motion.

1.	Reading this page...
2.	Checking domain trust...
3.	Analyzing pricing tactics...
4.	Calculating your Gaslighting Score...

This does two things: makes the 8 to 12 second wait feel purposeful, and visually communicates the technical depth of what is happening to any judge watching the demo.

6.3 Results View -- Reveal Sequence
Results do not all appear at once. The reveal is a performance. Each beat is intentional.

•	Beat 1: Trust badge animates in. Green badge fades after 2 seconds if site is clean. Amber notice persists if flagged.
•	Beat 2: Split screen appears. Left pane populates with the retailer view. Right pane starts empty.
•	Beat 3: Tactic flag cards animate into the right pane one by one, 80ms stagger each.
•	Beat 4: Gaslighting Score badge drops in last. Number counts up from 0 over 1200ms. Color shifts from neutral to amber to red based on final value. Severity label fades in below the number.
•	Beat 5: Real price calculation line appears below score: You were about to pay $X. Real cost: $Y.

6.4 Landing Page Sections
The landing page is a separate static site on Netlify. It has 6 sections. It sells the extension to people who have not installed it yet.

Section	Content and Purpose
01 -- Hero	Headline: YOU THINK YOU ARE GETTING A DEAL. Subhead explains the extension in one sentence. Two CTAs: Install Extension (primary red) and See How It Works (outline). Above the fold.
02 -- Trust Bar	One line. Four stats separated by dots: works on any product page, 6 manipulation categories, fake site detection, Gaslighting Score 0-100.
03 -- Demo Result	Pre-loaded static example showing a full analysis result. Left pane shows retailer view. Right pane shows what PriceCheck found. Score badge visible. Label: Example Analysis.
04 -- How It Works	Three steps: Install the extension. Visit any product page. Click the icon. Short, no paragraphs.
05 -- Tactic Cards	Six cards, one per manipulation category. Makes the product feel substantive and expert. Judges will read this section.
06 -- Bottom CTA	Repeat install button. Tagline: Stop getting played. Nothing else.

COPY RULE
No em dashes anywhere in UI copy, landing page, or any user-facing text.
Use commas, colons, or rewrite the sentence instead.
Run this check before every commit: grep -r "\u2014" extension/src/ landing/
 
# Part 7: Design System

All tokens are defined here. Copy the Tailwind config block into both the extension and landing projects. No design decisions during build.

7.1 Color Palette
Token	Hex Value	Usage
red-alarm	#D42B2B	Score badge, tactic flag borders, CTA buttons, all danger signals
red-tint	#FDF1F1	Tactic flag card backgrounds, right pane of split screen
red-mid	#F5C5C5	Tactic flag borders at lower opacity
amber	#C47C00	Mid-severity warnings, domain trust warn state
amber-tint	#FDF6E8	Amber state backgrounds
trust	#1A7A4A	Honest pricing score, legitimacy confirmed badge
trust-tint	#EDF7F2	Trust confirmed background
ink	#1C1B18	All body text, nav rule, primary borders
ink-mid	#4A4845	Secondary text, descriptions
ink-light	#8C8880	Labels, metadata, muted copy
paper	#FAF9F6	Page background -- warm off-white
white	#FFFFFF	Card surfaces, input fields
rule	#E2E0DA	All dividers and structural borders

7.2 Typography
Role	Font	Usage
Display	Barlow Condensed 700/800	Headlines, score numbers, section titles, all button text
Body	Libre Franklin 300/400/500/600	All readable content, descriptions, tactic explanations
Mono	JetBrains Mono 400/500	Labels, evidence text, score ranges, API data display

GOOGLE FONTS IMPORT -- ADD TO INDEX.HTML HEAD
https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@700;800
  &family=Libre+Franklin:wght@300;400;500;600
  &family=JetBrains+Mono:wght@400;500&display=swap

7.3 Tailwind Config
TAILWIND.CONFIG.JS -- EXTEND BLOCK -- PASTE INTO BOTH PROJECTS
colors: {
  'red-alarm':   '#D42B2B',
  'red-tint':    '#FDF1F1',
  'red-mid':     '#F5C5C5',
  'amber':       '#C47C00',
  'amber-tint':  '#FDF6E8',
  'trust':       '#1A7A4A',
  'trust-tint':  '#EDF7F2',
  'ink':         '#1C1B18',
  'ink-mid':     '#4A4845',
  'ink-light':   '#8C8880',
  'paper':       '#FAF9F6',
  'rule':        '#E2E0DA',
},
fontFamily: {
  'display': ["'Barlow Condensed'", 'sans-serif'],
  'body':    ["'Libre Franklin'", 'sans-serif'],
  'mono':    ["'JetBrains Mono'", 'monospace'],
},

7.4 Motion Tokens
Token	Value	Used For
ease-reveal	cubic-bezier(0.16, 1, 0.3, 1)	Score badge entrance, component reveals
ease-snap	cubic-bezier(0.34, 1.56, 0.64, 1)	Tactic flag icons snapping in -- slight spring
duration-hover	150ms	Button and card hover transitions
duration-card	500ms	Tactic card entrance animations
duration-score	1200ms	Score number count-up -- the key demo moment
stagger-delay	80ms per item	Tactic flags reveal one by one, not all at once
 
