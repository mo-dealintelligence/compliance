import { cn } from '@trycompai/ui/cn';
import { brand } from '@trycompai/utils/brand';
import type { CSSProperties } from 'react';

interface BrandLogoProps {
  className?: string;
  style?: CSSProperties;
  /** Hide the wordmark and render only the square mark. */
  markOnly?: boolean;
}

/** Deal Intelligence mark (matches dealintelligence.io favicon) + wordmark. */
export function BrandMark({ size = 24, className }: { size?: number; className?: string }) {
  return (
    <svg
      width={size}
      height={size}
      viewBox="0 0 32 32"
      xmlns="http://www.w3.org/2000/svg"
      className={className}
      aria-hidden="true"
    >
      <rect width={32} height={32} rx={6} fill="#0a0a09" />
      <g transform="translate(2.5 0)">
        <circle cx={5} cy={13} r={2} fill="#ff7a3d" />
        <circle cx={5} cy={19} r={2} fill="#ff7a3d" />
        <path d="M8 8 H16 a8 8 0 0 1 0 16 H8 Z" fill="#ff7a3d" />
        <path d="M12 12 H16 a4 4 0 0 1 0 8 H12 Z" fill="#0a0a09" />
      </g>
    </svg>
  );
}

export function BrandLogo({ className, style, markOnly = false }: BrandLogoProps) {
  return (
    <span
      className={cn('inline-flex items-center gap-2 text-foreground', className)}
      style={style}
      aria-label={brand.name}
      role="img"
    >
      <BrandMark size={24} className="shrink-0 rounded-md" />
      {!markOnly && (
        <span className="text-sm font-semibold tracking-tight whitespace-nowrap">{brand.name}</span>
      )}
    </span>
  );
}
