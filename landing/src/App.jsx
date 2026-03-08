import React from 'react';

function App() {
  return (
    <div className="min-h-screen bg-paper">
      {/* Section 1: Hero */}
      <section className="bg-paper py-20 px-6 md:py-32">
        <div className="max-w-4xl mx-auto text-center">
          <h1 className="font-display text-5xl md:text-7xl font-extrabold text-ink uppercase tracking-tight leading-tight mb-6">
            YOU THINK YOU ARE GETTING A DEAL
          </h1>
          <p className="font-display text-3xl md:text-5xl font-bold text-red-alarm mb-12">
            PriceCheck finds out the truth.
          </p>

          {/* CTAs */}
          <div className="flex flex-col sm:flex-row gap-4 justify-center items-center">
            <a
              href="https://github.com/TKHatton/PriceCheck-Build/releases/tag/v1.0"
              target="_blank"
              rel="noopener noreferrer"
              className="bg-red-alarm text-white font-display text-xl font-bold px-8 py-4 rounded-lg hover:bg-opacity-90 transition-all duration-150 w-full sm:w-auto text-center"
            >
              Install Extension
            </a>
            <a
              href="#how-it-works"
              className="bg-transparent border-2 border-ink text-ink font-display text-xl font-bold px-8 py-4 rounded-lg hover:bg-ink hover:text-white transition-all duration-150 w-full sm:w-auto text-center"
            >
              See How It Works
            </a>
          </div>
        </div>
      </section>

      {/* Section 2: Trust Bar */}
      <section className="bg-white border-y border-rule py-6 px-6">
        <div className="max-w-5xl mx-auto">
          <div className="font-mono text-sm text-ink-light text-center">
            <span className="inline-block mx-3 my-2">Works on any product page</span>
            <span className="hidden sm:inline text-ink-light">•</span>
            <span className="inline-block mx-3 my-2">6 manipulation categories</span>
            <span className="hidden sm:inline text-ink-light">•</span>
            <span className="inline-block mx-3 my-2">Fake site detection</span>
            <span className="hidden sm:inline text-ink-light">•</span>
            <span className="inline-block mx-3 my-2">Gaslighting Score 0-100</span>
          </div>
        </div>
      </section>

      {/* Section 3: Demo Result */}
      <section className="py-20 px-6">
        <div className="max-w-4xl mx-auto">
          <p className="font-mono text-xs uppercase text-ink-light tracking-wider text-center mb-6">
            Example Analysis
          </p>

          <div className="grid md:grid-cols-2 gap-6">
            {/* Left: What They Show */}
            <div className="bg-white border border-rule rounded-lg p-6">
              <h3 className="font-mono text-xs uppercase text-ink-light tracking-wider mb-4">
                WHAT THEY SHOW
              </h3>
              <p className="font-body text-ink text-lg font-medium mb-3">
                DreamCloud Luxury Mattress
              </p>
              <p className="font-display text-4xl font-bold text-ink mb-2">
                $499
              </p>
              <p className="font-body text-sm text-ink-mid">
                Was $1,599 - Save $1,100!
              </p>
            </div>

            {/* Right: What Is Really Happening */}
            <div className="bg-red-tint border border-red-mid rounded-lg p-6">
              <h3 className="font-mono text-xs uppercase text-ink-light tracking-wider mb-4">
                WHAT IS REALLY HAPPENING
              </h3>
              <p className="font-display text-4xl font-bold text-red-alarm mb-4">
                $1,127
              </p>
              <div className="space-y-2 text-sm font-body text-ink-mid">
                <p>• Fake discount: $1,599 never charged</p>
                <p>• Mandatory $199 white glove delivery</p>
                <p>• $429 premium mattress protector added at checkout</p>
              </div>
            </div>
          </div>

          {/* Score Badge */}
          <div className="flex justify-center mt-8">
            <div
              className="inline-block p-6 bg-white rounded-lg"
              style={{
                border: '2px solid #D42B2B',
                boxShadow: '4px 4px 0 #D42B2B'
              }}
            >
              <div className="flex items-baseline justify-center">
                <span className="font-display text-6xl font-bold text-red-alarm">
                  74
                </span>
                <span className="font-display text-3xl font-bold text-ink-light ml-1">
                  /100
                </span>
              </div>
              <div className="mt-4 text-center">
                <span className="font-mono text-sm uppercase text-ink tracking-wider">
                  Full Gaslighting
                </span>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Section 4: How It Works */}
      <section id="how-it-works" className="bg-white py-20 px-6">
        <div className="max-w-5xl mx-auto">
          <h2 className="font-display text-4xl md:text-5xl font-bold text-ink text-center mb-16">
            How It Works
          </h2>

          <div className="grid md:grid-cols-3 gap-8">
            {/* Step 1 */}
            <div className="text-center">
              <div className="w-16 h-16 bg-red-alarm rounded-full flex items-center justify-center mx-auto mb-4">
                <span className="font-display text-3xl font-bold text-white">1</span>
              </div>
              <h3 className="font-display text-xl font-bold text-ink mb-2">
                Install the extension
              </h3>
            </div>

            {/* Step 2 */}
            <div className="text-center">
              <div className="w-16 h-16 bg-red-alarm rounded-full flex items-center justify-center mx-auto mb-4">
                <span className="font-display text-3xl font-bold text-white">2</span>
              </div>
              <h3 className="font-display text-xl font-bold text-ink mb-2">
                Visit any product page
              </h3>
            </div>

            {/* Step 3 */}
            <div className="text-center">
              <div className="w-16 h-16 bg-red-alarm rounded-full flex items-center justify-center mx-auto mb-4">
                <span className="font-display text-3xl font-bold text-white">3</span>
              </div>
              <h3 className="font-display text-xl font-bold text-ink mb-2">
                Click the icon
              </h3>
            </div>
          </div>
        </div>
      </section>

      {/* Section 5: Install in 3 Steps */}
      <section className="py-20 px-6">
        <div className="max-w-5xl mx-auto">
          <h2 className="font-display text-4xl md:text-5xl font-bold text-ink text-center mb-16">
            Install in 3 Steps
          </h2>

          <div className="grid md:grid-cols-3 gap-8">
            {/* Step 1 */}
            <div className="text-center">
              <div className="w-16 h-16 bg-red-alarm rounded-full flex items-center justify-center mx-auto mb-4">
                <span className="font-display text-3xl font-bold text-white">1</span>
              </div>
              <h3 className="font-display text-xl font-bold text-ink mb-2">
                Download
              </h3>
              <p className="font-body text-sm text-ink-mid">
                Click Install Extension above to download the zip from GitHub
              </p>
            </div>

            {/* Step 2 */}
            <div className="text-center">
              <div className="w-16 h-16 bg-red-alarm rounded-full flex items-center justify-center mx-auto mb-4">
                <span className="font-display text-3xl font-bold text-white">2</span>
              </div>
              <h3 className="font-display text-xl font-bold text-ink mb-2">
                Unzip
              </h3>
              <p className="font-body text-sm text-ink-mid">
                Extract the downloaded zip file to any folder on your computer
              </p>
            </div>

            {/* Step 3 */}
            <div className="text-center">
              <div className="w-16 h-16 bg-red-alarm rounded-full flex items-center justify-center mx-auto mb-4">
                <span className="font-display text-3xl font-bold text-white">3</span>
              </div>
              <h3 className="font-display text-xl font-bold text-ink mb-2">
                Load in Chrome
              </h3>
              <p className="font-body text-sm text-ink-mid">
                Open chrome://extensions, enable Developer Mode, click Load Unpacked, select the dist folder
              </p>
            </div>
          </div>

          <p className="font-body text-sm text-ink-light text-center mt-8">
            Works on any Chromium browser: Chrome, Edge, Brave, Arc. Mobile browsers do not support extensions.
          </p>
        </div>
      </section>

      {/* Section 6: Tactic Cards */}
      <section className="py-20 px-6">
        <div className="max-w-6xl mx-auto">
          <h2 className="font-display text-4xl md:text-5xl font-bold text-ink text-center mb-16">
            What PriceCheck Detects
          </h2>

          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
            {/* Fake Discounts */}
            <div className="bg-white border-l-4 border-red-alarm rounded-lg p-6">
              <h3 className="font-display text-xl font-bold text-red-alarm uppercase mb-3">
                Fake Discounts
              </h3>
              <p className="font-body text-sm text-ink-mid">
                Inflated original prices, was/now manipulation, perpetual sales that never end.
              </p>
            </div>

            {/* Hidden Fees */}
            <div className="bg-white border-l-4 border-red-alarm rounded-lg p-6">
              <h3 className="font-display text-xl font-bold text-red-alarm uppercase mb-3">
                Hidden Fees
              </h3>
              <p className="font-body text-sm text-ink-mid">
                Mandatory charges withheld until checkout: resort fees, service fees, convenience fees.
              </p>
            </div>

            {/* Drip Pricing */}
            <div className="bg-white border-l-4 border-red-alarm rounded-lg p-6">
              <h3 className="font-display text-xl font-bold text-red-alarm uppercase mb-3">
                Drip Pricing
              </h3>
              <p className="font-body text-sm text-ink-mid">
                Base price shown upfront, mandatory extras added one by one through the purchase flow.
              </p>
            </div>

            {/* Dark Patterns */}
            <div className="bg-white border-l-4 border-red-alarm rounded-lg p-6">
              <h3 className="font-display text-xl font-bold text-red-alarm uppercase mb-3">
                Dark Patterns
              </h3>
              <p className="font-body text-sm text-ink-mid">
                Fake urgency timers, pre-checked add-ons, manipulative social proof claims.
              </p>
            </div>

            {/* Subscription Traps */}
            <div className="bg-white border-l-4 border-red-alarm rounded-lg p-6">
              <h3 className="font-display text-xl font-bold text-red-alarm uppercase mb-3">
                Subscription Traps
              </h3>
              <p className="font-body text-sm text-ink-mid">
                Free trials that auto-convert to paid, hard-to-cancel recurring charges.
              </p>
            </div>

            {/* Shrinkflation */}
            <div className="bg-white border-l-4 border-red-alarm rounded-lg p-6">
              <h3 className="font-display text-xl font-bold text-red-alarm uppercase mb-3">
                Shrinkflation
              </h3>
              <p className="font-body text-sm text-ink-mid">
                Same price, smaller quantity. Price-per-unit calculation exposes the real increase.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Section 7: Bottom CTA */}
      <section className="bg-red-alarm py-20 px-6">
        <div className="max-w-3xl mx-auto text-center">
          <p className="font-display text-3xl md:text-4xl font-bold text-white mb-8">
            Stop getting played.
          </p>
          <a
            href="https://github.com/TKHatton/PriceCheck-Build/releases/tag/v1.0"
            target="_blank"
            rel="noopener noreferrer"
            className="inline-block bg-white text-red-alarm font-display text-xl font-bold px-10 py-5 rounded-lg hover:bg-opacity-90 transition-all duration-150"
          >
            Install Extension
          </a>
        </div>
      </section>
    </div>
  );
}

export default App;
