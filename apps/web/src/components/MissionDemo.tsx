"use client";

import { useState } from "react";

type TabKey = "ticket" | "diff" | "checks";

const TABS: { key: TabKey; label: string; file: string }[] = [
  { key: "ticket", label: "Ticket", file: "BYTE-103" },
  { key: "diff", label: "Diff", file: "app/health.py" },
  { key: "checks", label: "Checks", file: "pytest" },
];

const SPRINT = [
  { n: 1, title: "Set up your environment", state: "done" },
  { n: 2, title: "Clone & run the service", state: "done" },
  { n: 3, title: "Fix your first bug", state: "current" },
  { n: 4, title: "Ship it as a pull request", state: "todo" },
  { n: 5, title: "Incident: works on my machine", state: "todo" },
] as const;

const CRITERIA = [
  "GET /health returns HTTP 200",
  'Response body is exactly {"status": "ok"}',
  "No other endpoint's behavior changed",
];

function Gutter({ n }: { n: number | string }) {
  return (
    <span className="w-7 shrink-0 select-none pr-3 text-right text-ink-subtle/70">
      {n}
    </span>
  );
}

export default function MissionDemo() {
  const [tab, setTab] = useState<TabKey>("ticket");

  return (
    <section id="mission" className="relative mx-auto max-w-6xl px-6 py-20 sm:py-28">
      <p className="font-mono text-[11px] tracking-[0.18em] text-accent uppercase">
        Product proof
      </p>
      <h2 className="mt-4 max-w-2xl font-display text-3xl leading-tight font-medium tracking-[-0.02em] text-balance sm:text-[40px]">
        A lesson here is a ticket, a repository, and a check that has to pass.
      </h2>
      <p className="mt-4 max-w-xl text-[17px] leading-relaxed text-ink-muted text-pretty">
        This is mission 3 of 25 in BUILD — a real one-line bug in a real FastAPI
        service. No slides, no quiz. You read the ticket, change the code, and the
        test tells you whether you were right.
      </p>

      <div className="relative mt-10">
        <div
          className="pointer-events-none absolute -inset-x-6 -top-10 bottom-0 glow-panel"
          aria-hidden="true"
        />

        <div className="panel-shadow relative overflow-hidden rounded-2xl border border-white/10 bg-surface">
          {/* window chrome */}
          <div className="flex items-center gap-4 border-b border-white/8 bg-white/[0.02] px-4 py-3">
            <div className="flex gap-1.5" aria-hidden="true">
              <span className="size-2.5 rounded-full bg-white/12" />
              <span className="size-2.5 rounded-full bg-white/12" />
              <span className="size-2.5 rounded-full bg-white/12" />
            </div>
            <span className="hidden font-mono text-xs text-ink-subtle sm:block">
              bytebangla-api
              <span className="mx-1.5 text-ink-subtle/50">/</span>
              <span className="text-ink-muted">
                {TABS.find((t) => t.key === tab)?.file}
              </span>
            </span>
            <span className="ml-auto inline-flex items-center gap-1.5 rounded-md border border-amber/25 bg-amber/10 px-2 py-1 font-mono text-[11px] text-amber">
              <span className="size-1.5 rounded-full bg-amber" />
              BYTE-103 OPEN
            </span>
          </div>

          <div className="grid md:grid-cols-[232px_1fr]">
            {/* sprint rail */}
            <aside className="hidden border-r border-white/8 bg-white/[0.015] p-4 md:block">
              <p className="font-mono text-[10px] tracking-[0.16em] text-ink-subtle uppercase">
                Sprint 1 · Onboarding
              </p>
              <ul className="mt-4 space-y-1">
                {SPRINT.map((m) => (
                  <li
                    key={m.n}
                    className={`flex items-start gap-2.5 rounded-lg px-2.5 py-2 text-[13px] leading-snug ${
                      m.state === "current"
                        ? "bg-white/[0.06] text-ink"
                        : "text-ink-subtle"
                    }`}
                  >
                    <span className="mt-0.5 shrink-0">
                      {m.state === "done" ? (
                        <svg width="13" height="13" viewBox="0 0 14 14" fill="none">
                          <circle cx="7" cy="7" r="6.25" stroke="var(--color-accent)" strokeWidth="1.2" opacity="0.5" />
                          <path d="M4.4 7.2 6.2 9l3.5-3.6" stroke="var(--color-accent)" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" />
                        </svg>
                      ) : m.state === "current" ? (
                        <span className="mt-[3px] block size-[7px] rounded-full bg-amber" />
                      ) : (
                        <svg width="13" height="13" viewBox="0 0 14 14" fill="none">
                          <circle cx="7" cy="7" r="6.25" stroke="currentColor" strokeWidth="1.2" opacity="0.4" />
                        </svg>
                      )}
                    </span>
                    <span>{m.title}</span>
                  </li>
                ))}
              </ul>
              <div className="mt-5 border-t border-white/8 pt-4">
                <div className="flex items-center justify-between font-mono text-[11px] text-ink-subtle">
                  <span>PROGRESS</span>
                  <span className="text-ink-muted">2 / 5</span>
                </div>
                <div className="mt-2 h-1 overflow-hidden rounded-full bg-white/8">
                  <div className="h-full w-2/5 rounded-full bg-accent" />
                </div>
              </div>
            </aside>

            {/* main panel — min-w-0 so the code block scrolls inside instead of stretching the grid */}
            <div className="min-w-0">
              <div className="flex border-b border-white/8">
                {TABS.map((t) => (
                  <button
                    key={t.key}
                    onClick={() => setTab(t.key)}
                    className={`relative cursor-pointer border-r border-white/8 px-4 py-2.5 text-[13px] transition-colors ${
                      tab === t.key
                        ? "bg-white/[0.05] text-ink"
                        : "text-ink-subtle hover:bg-white/[0.02] hover:text-ink-muted"
                    }`}
                  >
                    {tab === t.key && (
                      <span className="absolute inset-x-0 top-0 h-px bg-accent" />
                    )}
                    {t.label}
                  </button>
                ))}
              </div>

              <div className="min-h-[330px] p-5 sm:p-6">
                {tab === "ticket" && (
                  <div key="ticket" className="rise">
                    <h3 className="font-display text-lg font-medium tracking-tight">
                      /health always returns &ldquo;not implemented&rdquo;
                    </h3>
                    <div className="mt-3 flex flex-wrap gap-2 font-mono text-[11px]">
                      {["Reported by QA", "Type: Debugging", "Sprint 1"].map((chip) => (
                        <span
                          key={chip}
                          className="rounded-md border border-white/10 bg-white/[0.03] px-2 py-1 text-ink-subtle"
                        >
                          {chip}
                        </span>
                      ))}
                    </div>
                    <p className="mt-5 max-w-[62ch] text-[15px] leading-relaxed text-ink-muted">
                      ByteBangla&rsquo;s uptime monitor pings{" "}
                      <code className="rounded bg-white/[0.06] px-1.5 py-0.5 font-mono text-[13px] text-ink">
                        /health
                      </code>{" "}
                      every 30 seconds and pages on-call if it doesn&rsquo;t return ok.
                      It always reports{" "}
                      <code className="rounded bg-white/[0.06] px-1.5 py-0.5 font-mono text-[13px] text-ink">
                        not implemented
                      </code>
                      , so the monitor can never detect a real outage.
                    </p>
                    <div className="mt-6 rounded-xl border border-white/8 bg-white/[0.02] p-4">
                      <p className="font-mono text-[10px] tracking-[0.16em] text-ink-subtle uppercase">
                        Acceptance criteria
                      </p>
                      <ul className="mt-3 space-y-2">
                        {CRITERIA.map((c) => (
                          <li key={c} className="flex items-start gap-2.5 text-[14px] text-ink-muted">
                            <span className="mt-[3px] size-3.5 shrink-0 rounded border border-white/20" />
                            <span className="font-mono text-[13px] leading-relaxed">{c}</span>
                          </li>
                        ))}
                      </ul>
                    </div>
                  </div>
                )}

                {tab === "diff" && (
                  <div key="diff" className="rise overflow-x-auto">
                    <pre className="font-mono text-[13px] leading-[1.75]">
                      <code className="block whitespace-pre">
                        <span className="flex">
                          <Gutter n={1} />
                          <span className="w-4 shrink-0" />
                          <span>
                            <span className="text-sky">from</span> fastapi{" "}
                            <span className="text-sky">import</span> APIRouter
                          </span>
                        </span>
                        <span className="flex">
                          <Gutter n={2} />
                          <span className="w-4 shrink-0" />
                        </span>
                        <span className="flex">
                          <Gutter n={3} />
                          <span className="w-4 shrink-0" />
                          <span>router = APIRouter()</span>
                        </span>
                        <span className="flex">
                          <Gutter n={4} />
                          <span className="w-4 shrink-0" />
                        </span>
                        <span className="flex">
                          <Gutter n={5} />
                          <span className="w-4 shrink-0" />
                          <span className="text-violet">@router.get(</span>
                          <span className="text-[#e8c07d]">&quot;/health&quot;</span>
                          <span className="text-violet">)</span>
                        </span>
                        <span className="flex">
                          <Gutter n={6} />
                          <span className="w-4 shrink-0" />
                          <span>
                            <span className="text-sky">def</span> health_check():
                          </span>
                        </span>
                        <span className="-mx-5 flex border-l-2 border-danger bg-danger/10 px-5 sm:-mx-6 sm:px-6">
                          <Gutter n={7} />
                          <span className="w-4 shrink-0 text-danger">-</span>
                          <span>
                            {"    "}
                            <span className="text-sky">return</span> {"{"}
                            <span className="text-[#e8c07d]">&quot;status&quot;</span>:{" "}
                            <span className="text-[#e8c07d]">&quot;not implemented&quot;</span>
                            {"}"}
                          </span>
                        </span>
                        <span className="-mx-5 flex border-l-2 border-accent bg-accent/10 px-5 sm:-mx-6 sm:px-6">
                          <Gutter n={7} />
                          <span className="w-4 shrink-0 text-accent">+</span>
                          <span>
                            {"    "}
                            <span className="text-sky">return</span> {"{"}
                            <span className="text-[#e8c07d]">&quot;status&quot;</span>:{" "}
                            <span className="text-[#e8c07d]">&quot;ok&quot;</span>
                            {"}"}
                          </span>
                        </span>
                      </code>
                    </pre>
                    <p className="mt-6 font-mono text-[12px] text-ink-subtle">
                      1 file changed, 1 insertion(+), 1 deletion(-)
                    </p>
                  </div>
                )}

                {tab === "checks" && (
                  <div key="checks" className="overflow-x-auto">
                    <pre className="font-mono text-[13px] leading-[1.8] whitespace-pre">
                      <code>
                        <span className="rise block" style={{ animationDelay: "0ms" }}>
                          <span className="text-accent">$</span> pytest
                          tests/test_health.py -v
                        </span>
                        <span
                          className="rise mt-3 block text-ink-subtle"
                          style={{ animationDelay: "220ms" }}
                        >
                          collected 1 item
                        </span>
                        <span
                          className="rise mt-3 block"
                          style={{ animationDelay: "460ms" }}
                        >
                          <span className="text-ink-muted">
                            tests/test_health.py::test_health_returns_ok
                          </span>{" "}
                          <span className="text-accent">PASSED</span>
                          <span className="text-ink-subtle"> [100%]</span>
                        </span>
                        <span
                          className="rise mt-3 block text-accent"
                          style={{ animationDelay: "700ms" }}
                        >
                          1 passed in 0.04s
                        </span>
                        <span
                          className="rise block text-ink-subtle"
                          style={{ animationDelay: "820ms" }}
                        >
                          $ <span className="caret">▋</span>
                        </span>
                      </code>
                    </pre>

                    <div
                      className="rise mt-6 rounded-xl border border-accent/25 bg-accent/[0.07] p-4"
                      style={{ animationDelay: "1000ms" }}
                    >
                      <div className="flex items-start gap-3">
                        <svg width="18" height="18" viewBox="0 0 18 18" fill="none" className="mt-0.5 shrink-0">
                          <circle cx="9" cy="9" r="8.25" stroke="var(--color-accent)" strokeWidth="1.3" />
                          <path d="M5.6 9.3 7.9 11.6l4.5-4.8" stroke="var(--color-accent)" strokeWidth="1.7" strokeLinecap="round" strokeLinejoin="round" />
                        </svg>
                        <div className="min-w-0">
                          <p className="text-[14px] font-medium text-ink">
                            All acceptance criteria met — mission 3 complete
                          </p>
                          <p className="mt-1 font-mono text-[12px] text-ink-muted">
                            Next up: ship it as a pull request (BYTE-104)
                          </p>
                        </div>
                      </div>
                    </div>
                  </div>
                )}
              </div>
            </div>
          </div>

          {/* window footer */}
          <div className="flex flex-wrap items-center gap-x-5 gap-y-1 border-t border-white/8 bg-white/[0.02] px-4 py-2.5 font-mono text-[11px] text-ink-subtle">
            <span>Submission: diff + commit</span>
            <span className="hidden sm:inline">Hints: 3 (progressive)</span>
            <span className="ml-auto">Evaluation: automated</span>
          </div>
        </div>
      </div>
    </section>
  );
}
