export default function Logo({ size = 26 }: { size?: number }) {
  return (
    <svg
      width={size}
      height={size}
      viewBox="0 0 26 26"
      fill="none"
      aria-hidden="true"
      className="shrink-0"
    >
      <rect
        x="0.6"
        y="0.6"
        width="24.8"
        height="24.8"
        rx="7.4"
        fill="#11141c"
        stroke="rgba(255,255,255,0.14)"
        strokeWidth="1.2"
      />
      <path
        d="M8.2 9.4 11.9 13 8.2 16.6"
        stroke="var(--color-accent)"
        strokeWidth="1.9"
        strokeLinecap="round"
        strokeLinejoin="round"
      />
      <path
        d="M13.9 17.2h4.3"
        stroke="var(--color-accent)"
        strokeWidth="1.9"
        strokeLinecap="round"
      />
    </svg>
  );
}
