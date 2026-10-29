import { cn } from '@trycompai/ui/cn';
import { brand } from '@trycompai/utils/brand';
import type { CSSProperties } from 'react';

interface BrandLogoProps {
  className?: string;
  style?: CSSProperties;
  /** Hide the wordmark and render only the square mark. */
  markOnly?: boolean;
}

/**
 * Neutral wordmark for the instance brand: a rounded square carrying the brand
 * initial, followed by the brand name. Colors follow `currentColor`.
 */
export function BrandLogo({ className, style, markOnly = false }: BrandLogoProps) {
  const initial = brand.name.charAt(0).toUpperCase();

  return (
    <span
      className={cn('inline-flex items-center gap-2 text-foreground', className)}
      style={style}
      aria-label={brand.name}
      role="img"
    >
      <span className="flex h-6 w-6 shrink-0 items-center justify-center rounded-md border-2 border-current text-xs font-bold leading-none">
        {initial}
      </span>
      {!markOnly && (
        <span className="text-sm font-semibold tracking-tight whitespace-nowrap">{brand.name}</span>
      )}
    </span>
  );
}
