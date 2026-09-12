export default function Evidence() {
  return (
    <section
      id="evidence"
      className="border-y border-white/8 bg-white/[0.015]"
    >
      <div className="mx-auto max-w-6xl px-6 py-20 sm:py-28">
        <p className="font-mono text-[11px] tracking-[0.18em] text-accent uppercase">
          What you leave with
        </p>
        <h2 className="mt-4 max-w-2xl font-display text-3xl leading-tight font-medium tracking-[-0.02em] text-balance sm:text-[40px]">
          Evidence, not a certificate.
        </h2>
        <p className="mt-4 max-w-xl text-[17px] leading-relaxed text-ink-muted text-pretty">
          A certificate says you finished something. These say you did the work — and
          they&rsquo;re what you actually talk about in an interview.
        </p>

        <div className="mt-12 grid gap-4 md:grid-cols-3">
          {/* pull request artifact */}
          <article className="rounded-2xl border border-white/10 bg-surface p-5">
            <div className="flex items-center gap-2">
              <span className="inline-flex items-center gap-1.5 rounded-md border border-violet/25 bg-violet/10 px-2 py-1 font-mono text-[10px] text-violet">
                MERGED
              </span>
              <span className="font-mono text-[11px] text-ink-subtle">#42</span>
            </div>
            <h3 className="mt-4 font-display text-[15px] leading-snug font-medium">
              Fix /health to return ok status (BYTE-103)
            </h3>
            <p className="mt-2 font-mono text-[11px] text-ink-subtle">
              fix/health-check-status → main
            </p>
            <div className="mt-5 space-y-2 border-t border-white/8 pt-4 font-mono text-[11px]">
              <p className="flex items-center gap-2 text-ink-muted">
                <span className="text-accent">✓</span> 1 review approved
              </p>
              <p className="flex items-center gap-2 text-ink-muted">
                <span className="text-accent">✓</span> checks passed
              </p>
              <p className="text-ink-subtle">
                <span className="text-accent">+1</span>{" "}
                <span className="text-danger">−1</span> · 1 file
              </p>
            </div>
          </article>

          {/* test suite artifact */}
          <article className="rounded-2xl border border-white/10 bg-surface p-5">
            <div className="flex items-center gap-2">
              <span className="inline-flex items-center gap-1.5 rounded-md border border-accent/25 bg-accent/10 px-2 py-1 font-mono text-[10px] text-accent">
                PASSING
              </span>
              <span className="font-mono text-[11px] text-ink-subtle">pytest</span>
            </div>
            <h3 className="mt-4 font-display text-[15px] leading-snug font-medium">
              A test suite you wrote yourself
            </h3>
            <p className="mt-2 font-mono text-[11px] text-ink-subtle">
              tests/test_users.py
            </p>
            <div className="mt-5 space-y-1.5 border-t border-white/8 pt-4 font-mono text-[11px] text-ink-muted">
              <p>
                test_create_user <span className="text-accent">PASSED</span>
              </p>
              <p>
                test_rejects_bad_email <span className="text-accent">PASSED</span>
              </p>
              <p>
                test_pagination_limit <span className="text-accent">PASSED</span>
              </p>
              <p className="pt-1 text-ink-subtle">12 passed in 0.31s</p>
            </div>
          </article>

          {/* postmortem artifact */}
          <article className="rounded-2xl border border-white/10 bg-surface p-5">
            <div className="flex items-center gap-2">
              <span className="inline-flex items-center gap-1.5 rounded-md border border-amber/25 bg-amber/10 px-2 py-1 font-mono text-[10px] text-amber">
                RESOLVED
              </span>
              <span className="font-mono text-[11px] text-ink-subtle">INC-07</span>
            </div>
            <h3 className="mt-4 font-display text-[15px] leading-snug font-medium">
              An incident write-up with a real root cause
            </h3>
            <p className="mt-2 font-mono text-[11px] text-ink-subtle">
              postmortems/inc-07.md
            </p>
            <div className="mt-5 space-y-2.5 border-t border-white/8 pt-4 font-mono text-[11px]">
              <p className="text-ink-subtle">
                <span className="text-ink-muted">Impact</span> · 14 min, staging
              </p>
              <p className="text-ink-subtle">
                <span className="text-ink-muted">Root cause</span> · missing env var
                after rollout
              </p>
              <p className="text-ink-subtle">
                <span className="text-ink-muted">Prevention</span> · startup config
                validation
              </p>
            </div>
          </article>
        </div>

        <p className="mt-8 max-w-2xl font-mono text-[12px] leading-relaxed text-ink-subtle">
          Representative artifacts showing the kind of work missions produce. Real
          learner repositories and write-ups get published here — with permission —
          once the founding cohort finishes.
        </p>
      </div>
    </section>
  );
}
