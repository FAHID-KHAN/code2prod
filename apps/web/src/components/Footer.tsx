import Logo from "./Logo";

export default function Footer() {
  return (
    <footer className="border-t border-white/8">
      <div className="mx-auto max-w-6xl px-6 py-12">
        <div className="flex flex-col gap-8 sm:flex-row sm:items-start sm:justify-between">
          <div className="max-w-sm">
            <div className="flex items-center gap-2.5">
              <Logo size={22} />
              <span className="font-display text-[14px] font-medium tracking-tight">
                Code2Prod
              </span>
            </div>
            <p className="mt-4 text-[13px] leading-relaxed text-ink-subtle">
              Your first engineering experience before your first engineering job.
              Practice-first engineering education, built for learners in Bangladesh.
            </p>
          </div>

          <nav className="flex gap-12">
            <div>
              <p className="font-mono text-[10px] tracking-[0.16em] text-ink-subtle uppercase">
                Explore
              </p>
              <ul className="mt-3 space-y-2 text-[13px]">
                <li>
                  <a href="#mission" className="text-ink-muted transition-colors hover:text-ink">
                    Sample mission
                  </a>
                </li>
                <li>
                  <a href="#path" className="text-ink-muted transition-colors hover:text-ink">
                    Course path
                  </a>
                </li>
                <li>
                  <a href="#evidence" className="text-ink-muted transition-colors hover:text-ink">
                    Evidence
                  </a>
                </li>
              </ul>
            </div>
          </nav>
        </div>

        <div className="mt-10 flex flex-col gap-2 border-t border-white/8 pt-6 font-mono text-[11px] text-ink-subtle sm:flex-row sm:items-center sm:justify-between">
          <span>Code2Prod — product blueprint v0.1</span>
          <span>
            ByteBangla Technologies is a fictional company used for training.
          </span>
        </div>
      </div>
    </footer>
  );
}
