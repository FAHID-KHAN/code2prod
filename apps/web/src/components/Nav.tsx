"use client";

import { useEffect, useState } from "react";
import Logo from "./Logo";

const LINKS = [
  { href: "#mission", label: "See a mission" },
  { href: "#path", label: "Course path" },
  { href: "#evidence", label: "Evidence" },
];

export default function Nav() {
  const [scrolled, setScrolled] = useState(false);

  useEffect(() => {
    const onScroll = () => setScrolled(window.scrollY > 8);
    onScroll();
    window.addEventListener("scroll", onScroll, { passive: true });
    return () => window.removeEventListener("scroll", onScroll);
  }, []);

  return (
    <header
      className={`sticky top-0 z-50 transition-colors duration-300 ${
        scrolled
          ? "border-b border-white/8 bg-canvas/80 backdrop-blur-xl"
          : "border-b border-transparent"
      }`}
    >
      <div className="mx-auto flex max-w-6xl items-center justify-between px-6 py-4">
        <a href="#top" className="flex items-center gap-2.5">
          <Logo />
          <span className="font-display text-[15px] font-medium tracking-tight">
            Code2Prod
          </span>
        </a>

        <nav className="flex items-center gap-1 sm:gap-2">
          {LINKS.map((link) => (
            <a
              key={link.href}
              href={link.href}
              className="hidden rounded-lg px-3 py-2 text-sm text-ink-muted transition-colors hover:text-ink sm:block"
            >
              {link.label}
            </a>
          ))}
          <a
            href="#start"
            className="rounded-lg bg-accent px-3.5 py-2 text-sm font-medium text-accent-ink transition-opacity hover:opacity-90"
          >
            Start free
          </a>
        </nav>
      </div>
    </header>
  );
}
