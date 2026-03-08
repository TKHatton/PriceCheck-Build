# PriceCheck -- The Price Gaslighting Detector

> See the real price. Stop getting played.

**Live landing page:** [your-netlify-url]
**Demo video:** [your-video-link]
**Extension download:** [zip file link or Chrome Web Store]

## What It Does

PriceCheck is a Chrome browser extension that exposes pricing manipulation
tactics on any product page. Click the extension icon while browsing and
get a Gaslighting Score from 0 to 100 plus a breakdown of every tactic
being used against you.

No URL copying. No tab switching. Works on the page you are already on.

## Detection Categories

1. Fake Discounts -- phantom original prices, was/now manipulation
2. Hidden Fees -- charges withheld until checkout
3. Drip Pricing -- mandatory extras added sequentially
4. Dark Patterns -- fake urgency, pre-checked add-ons
5. Subscription Traps -- free trials that auto-convert
6. Shrinkflation -- same price, smaller quantity
7. Fraudulent Storefronts -- scam sites (silent detection layer)

## Architecture

Three components from one GitHub repository:

  /extension    Chrome extension (React + Vite)
  /backend      FastAPI + LangGraph agent (Render)
  /landing      Marketing landing page (Netlify)

### LangGraph Pipeline

  START
    -> input_router (conditional: page / image / manual)
    -> content_node OR ocr_node OR manual_node
    -> trust_node (URLScan + WHOIS)
    -> trust_gate (scam exit if trust_score < 30)
    -> analyze_node (Claude claude-sonnet-4-6)
    -> score_node (weighted Python algorithm)
    -> output_node
  END

### Stack

  Chrome Extension:  React, Vite, Tailwind CSS, Framer Motion
  Backend:           FastAPI, LangGraph, Python
  AI:                Claude claude-sonnet-4-6 (Anthropic API)
  Domain Trust:      URLScan.io, WHOIS API
  Landing Page:      Netlify
  Backend Host:      Render

## Running Locally

### Backend
  cd backend
  pip install -r requirements.txt
  cp .env.example .env
  uvicorn app.main:app --reload --port 8000

### Extension
  cd extension
  npm install
  npm run build
  Load /extension/dist in chrome://extensions (Developer Mode, Load unpacked)

### Landing Page
  cd landing
  npm install && npm run dev

## Environment Variables

  ANTHROPIC_API_KEY     Required
  URLSCAN_API_KEY       Required for domain trust
  WHOIS_API_KEY         Optional (trust check degrades gracefully without it)
  FRONTEND_URL          Netlify production URL (for CORS)

## Built With

Claude Code (claude-opus-4-6) -- AI-assisted development
Solo build -- 48-hour hackathon, March 2026
