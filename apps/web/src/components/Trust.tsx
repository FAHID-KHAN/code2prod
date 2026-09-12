const PROMISES = [
  {
    title: "The free course is genuinely useful on its own",
    body: "Foundations isn't a trailer for the paid courses. It stands alone, and you never hit a paywall mid-lesson.",
  },
  {
    title: "The whole BUILD backlog is public before you pay",
    body: "All 25 missions are written down in this repository under docs/curriculum. Read every one of them first.",
  },
  {
    title: "No job guarantees, no salary claims",
    body: "This is simulated practice and verifiable evidence. It's honest preparation — you still have to earn the job.",
  },
  {
    title: "Early learners are collaborators, not customers",
    body: "A small founding cohort goes first, at low or no cost, so friction gets found and fixed before anyone pays full price.",
  },
];

export default function Trust() {
  return (
    <section className="mx-auto max-w-6xl px-6 py-20 sm:py-28">
      <div className="grid gap-12 lg:grid-cols-[1fr_1.2fr] lg:gap-16">
        <div>
          <p className="font-mono text-[11px] tracking-[0.18em] text-accent uppercase">
            Straight answers
          </p>
          <h2 className="mt-4 font-display text-3xl leading-tight font-medium tracking-[-0.02em] text-balance sm:text-[40px]">
            A new education brand can&rsquo;t just claim it&rsquo;s good.
          </h2>
          <p className="mt-5 max-w-md text-[17px] leading-relaxed text-ink-muted text-pretty">
            So here&rsquo;s exactly where things stand, including the parts that
            aren&rsquo;t finished yet. You can check every one of these before you
            spend anything.
          </p>
        </div>

        <ul className="space-y-px overflow-hidden rounded-2xl border border-white/10">
          {PROMISES.map((p, i) => (
            <li
              key={p.title}
              className="flex gap-4 bg-surface p-5 transition-colors hover:bg-surface-2 sm:p-6"
            >
              <span className="mt-0.5 font-mono text-[11px] text-accent">
                0{i + 1}
              </span>
              <div>
                <h3 className="text-[15px] font-medium text-ink">{p.title}</h3>
                <p className="mt-1.5 text-[14px] leading-relaxed text-ink-muted">
                  {p.body}
                </p>
              </div>
            </li>
          ))}
        </ul>
      </div>
    </section>
  );
}
