const STAGES = [
  {
    name: "Foundations",
    role: "Engineering trainee",
    outcome:
      "See how a real company ships: teams, lifecycle, environments, what breaks and who gets paged.",
    stack: ["Git", "APIs", "CI/CD", "Incidents"],
    price: "Free",
    free: true,
  },
  {
    name: "BUILD",
    role: "Junior software engineer",
    outcome:
      "Build and test the ByteBangla backend from your first bug to a feature shipped end-to-end.",
    stack: ["Linux", "Python", "FastAPI", "PostgreSQL", "pytest"],
    price: "৳599–799",
    free: false,
  },
  {
    name: "SHIP",
    role: "Junior DevOps engineer",
    outcome:
      "Take it from “works on my machine” to a repeatable pipeline that deploys to staging.",
    stack: ["Docker", "Compose", "CI/CD", "Registry"],
    price: "৳799–899",
    free: false,
  },
  {
    name: "OPERATE",
    role: "Junior platform engineer",
    outcome:
      "Run it properly: orchestration, GitOps workflows, and the dashboards you watch it through.",
    stack: ["Kubernetes", "Helm", "ArgoCD", "Prometheus"],
    price: "৳899–999",
    free: false,
  },
  {
    name: "PRODUCTION",
    role: "Production / SRE trainee",
    outcome:
      "Get paged. Dig through imperfect evidence, find root cause, fix it, and stop it recurring.",
    stack: ["Logs", "Metrics", "Rollback", "Postmortems"],
    price: "৳899–999",
    free: false,
  },
];

export default function CoursePath() {
  return (
    <section id="path" className="mx-auto max-w-6xl px-6 py-20 sm:py-28">
      <p className="font-mono text-[11px] tracking-[0.18em] text-accent uppercase">
        The path
      </p>
      <h2 className="mt-4 max-w-2xl font-display text-3xl leading-tight font-medium tracking-[-0.02em] text-balance sm:text-[40px]">
        One company. One codebase. Five stages of responsibility.
      </h2>
      <p className="mt-4 max-w-xl text-[17px] leading-relaxed text-ink-muted text-pretty">
        Every course happens inside ByteBangla Technologies, and the system never
        resets. The service you build in BUILD is the one you containerize in SHIP,
        orchestrate in OPERATE, and get paged for in PRODUCTION.
      </p>

      <div className="mt-12 overflow-x-auto pb-2">
        <ol className="grid min-w-[860px] grid-cols-5 gap-4">
          {STAGES.map((stage, i) => (
            <li key={stage.name} className="relative flex flex-col">
              {/* connector rail */}
              <div className="mb-5 flex items-center" aria-hidden="true">
                <div
                  className={`h-px flex-1 ${i === 0 ? "bg-transparent" : "bg-white/12"}`}
                />
                <span
                  className={`relative mx-2 flex size-2.5 shrink-0 items-center justify-center rounded-full ${
                    stage.free ? "bg-accent" : "bg-white/20"
                  }`}
                >
                  {stage.free && (
                    <span className="halo absolute size-2.5 rounded-full bg-accent" />
                  )}
                </span>
                <div
                  className={`h-px flex-1 ${
                    i === STAGES.length - 1 ? "bg-transparent" : "bg-white/12"
                  }`}
                />
              </div>

              <div
                className={`flex flex-1 flex-col rounded-2xl border p-5 transition-colors ${
                  stage.free
                    ? "border-accent/30 bg-accent/[0.05] hover:border-accent/50"
                    : "border-white/10 bg-surface hover:border-white/20"
                }`}
              >
                <div className="flex items-baseline justify-between gap-2">
                  <span className="font-mono text-[11px] text-ink-subtle">
                    0{i + 1}
                  </span>
                  <span
                    className={`font-mono text-[11px] ${
                      stage.free ? "text-accent" : "text-ink-muted"
                    }`}
                  >
                    {stage.price}
                  </span>
                </div>

                <h3 className="mt-3 font-display text-lg font-medium tracking-tight">
                  {stage.name}
                </h3>
                <p className="mt-1 text-[12px] text-ink-subtle">{stage.role}</p>

                <p className="mt-4 flex-1 text-[13px] leading-relaxed text-ink-muted">
                  {stage.outcome}
                </p>

                <div className="mt-5 flex flex-wrap gap-1.5">
                  {stage.stack.map((tool) => (
                    <span
                      key={tool}
                      className="rounded-md border border-white/8 bg-white/[0.04] px-1.5 py-0.5 font-mono text-[10px] text-ink-subtle"
                    >
                      {tool}
                    </span>
                  ))}
                </div>
              </div>
            </li>
          ))}
        </ol>
      </div>

      <p className="mt-6 font-mono text-[12px] text-ink-subtle">
        No standalone course is priced above roughly ৳1,000. Price is about access,
        not positioning.
      </p>
    </section>
  );
}
