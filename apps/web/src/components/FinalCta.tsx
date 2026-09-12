export default function FinalCta() {
  return (
    <section id="start" className="relative overflow-hidden border-t border-white/8">
      <div
        className="pointer-events-none absolute inset-x-0 bottom-0 h-[420px] glow-top rotate-180"
        aria-hidden="true"
      />
      <div className="relative mx-auto max-w-3xl px-6 py-24 text-center sm:py-32">
        <h2 className="font-display text-3xl leading-tight font-medium tracking-[-0.02em] text-balance sm:text-[44px]">
          It starts with one ticket.
        </h2>
        <p className="mx-auto mt-5 max-w-lg text-[17px] leading-relaxed text-ink-muted text-pretty">
          Foundations opens with the founding cohort. Until then, everything is
          readable: the full mission backlog, the acceptance criteria, and the starter
          repository you&rsquo;d be working in.
        </p>

        <div className="mt-9 flex flex-wrap justify-center gap-3">
          <a
            href="#mission"
            className="rounded-xl bg-accent px-5 py-3 text-[15px] font-medium text-accent-ink transition-opacity hover:opacity-90"
          >
            Work through the sample mission
          </a>
          <a
            href="#path"
            className="rounded-xl border border-white/12 bg-white/[0.03] px-5 py-3 text-[15px] font-medium text-ink transition-colors hover:border-white/25 hover:bg-white/[0.06]"
          >
            See all five stages
          </a>
        </div>

        <p className="mt-8 font-mono text-[12px] text-ink-subtle">
          25 missions · 2 incidents · 1 capstone — all published before launch
        </p>
      </div>
    </section>
  );
}
