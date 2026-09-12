const ROWS = [
  ["Watch a video", "Build the thing"],
  ["Chapter", "Sprint"],
  ["Lesson", "Mission / ticket"],
  ["Quiz", "Investigation"],
  ["Wrong answer", "Failing test"],
  ["Grade", "Engineering feedback"],
  ["Certificate", "Evidence you can show"],
];

export default function Philosophy() {
  return (
    <section className="border-y border-white/8 bg-white/[0.015]">
      <div className="mx-auto max-w-6xl px-6 py-20 sm:py-28">
        <div className="grid gap-12 lg:grid-cols-[1fr_1.1fr] lg:gap-16">
          <div>
            <p className="font-mono text-[11px] tracking-[0.18em] text-accent uppercase">
              Learning model
            </p>
            <h2 className="mt-4 font-display text-3xl leading-tight font-medium tracking-[-0.02em] text-balance sm:text-[40px]">
              We don&rsquo;t sell hours of content. We give you engineering work.
            </h2>
            <p className="mt-5 max-w-md text-[17px] leading-relaxed text-ink-muted text-pretty">
              You can learn Python, Git, Docker and SQL separately and still not know
              how a change travels from your laptop to production — or what engineers
              actually do when it fails at 2am.
            </p>
            <p className="mt-4 max-w-md text-[17px] leading-relaxed text-ink-muted text-pretty">
              So nothing here is taught because it&rsquo;s popular. PostgreSQL arrives
              when the app loses data. Docker arrives when &ldquo;works on my
              machine&rdquo; stops being funny. Kubernetes only shows up once
              there&rsquo;s enough running to be worth orchestrating.
            </p>
          </div>

          <div className="rounded-2xl border border-white/10 bg-surface p-2">
            <div className="grid grid-cols-[1fr_auto_1fr] items-center gap-x-3 px-4 py-3 font-mono text-[10px] tracking-[0.16em] uppercase">
              <span className="text-ink-subtle">Traditional EdTech</span>
              <span />
              <span className="text-accent">Code2Prod</span>
            </div>
            <div className="space-y-px">
              {ROWS.map(([before, after]) => (
                <div
                  key={before}
                  className="grid grid-cols-[1fr_auto_1fr] items-center gap-x-3 rounded-lg px-4 py-3 transition-colors hover:bg-white/[0.03]"
                >
                  <span className="text-[14px] text-ink-subtle line-through decoration-ink-subtle/40">
                    {before}
                  </span>
                  <svg
                    width="14"
                    height="14"
                    viewBox="0 0 14 14"
                    fill="none"
                    aria-hidden="true"
                    className="shrink-0"
                  >
                    <path
                      d="M2.5 7h8M7.5 3.8 10.8 7l-3.3 3.2"
                      stroke="var(--color-accent)"
                      strokeWidth="1.4"
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      opacity="0.7"
                    />
                  </svg>
                  <span className="text-[14px] font-medium text-ink">{after}</span>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
