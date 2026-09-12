const STACK = [
  "Git",
  "Linux",
  "Python",
  "FastAPI",
  "PostgreSQL",
  "Docker",
  "CI/CD",
  "Kubernetes",
  "Prometheus",
];

export default function Hero() {
  return (
    <section id="top" className="relative overflow-hidden">
      <div className="pointer-events-none absolute inset-0 bg-grid" aria-hidden="true" />
      <div className="pointer-events-none absolute inset-x-0 top-0 h-[520px] glow-top" aria-hidden="true" />

      <div className="relative mx-auto max-w-6xl px-6 pt-20 pb-14 sm:pt-28 sm:pb-20">
        <div className="inline-flex items-center gap-2.5 rounded-full border border-white/10 bg-white/[0.03] px-3.5 py-1.5 text-[13px] text-ink-muted">
          <span className="relative flex size-1.5">
            <span className="halo absolute inline-flex size-1.5 rounded-full bg-accent" />
            <span className="relative inline-flex size-1.5 rounded-full bg-accent" />
          </span>
          Founding cohort forming — the full BUILD backlog is public
        </div>

        <h1 className="mt-7 max-w-3xl font-display text-[42px] leading-[1.04] font-medium tracking-[-0.03em] text-balance sm:text-6xl">
          Stop watching.
          <br />
          <span className="bg-gradient-to-r from-accent to-[#a5f3c8] bg-clip-text text-transparent">
            Start engineering.
          </span>
        </h1>

        <p className="mt-6 max-w-xl text-[17px] leading-relaxed text-ink-muted text-pretty">
          Your first engineering job should not be your first experience doing real
          engineering work. Code2Prod drops you inside a simulated software company
          where you pick up tickets, ship code, and get paged when production breaks.
        </p>

        <div className="mt-9 flex flex-wrap items-center gap-3">
          <a
            href="#mission"
            className="rounded-xl bg-accent px-5 py-3 text-[15px] font-medium text-accent-ink transition-opacity hover:opacity-90"
          >
            See a real mission
          </a>
          <a
            href="#path"
            className="rounded-xl border border-white/12 bg-white/[0.03] px-5 py-3 text-[15px] font-medium text-ink transition-colors hover:border-white/25 hover:bg-white/[0.06]"
          >
            How the path works
          </a>
        </div>

        <div className="mt-14">
          <p className="font-mono text-[11px] tracking-[0.18em] text-ink-subtle uppercase">
            The tools you actually touch
          </p>
          <div className="mt-4 flex flex-wrap gap-x-6 gap-y-3">
            {STACK.map((tool) => (
              <span key={tool} className="font-mono text-sm text-ink-subtle">
                {tool}
              </span>
            ))}
          </div>
        </div>
      </div>
    </section>
  );
}
