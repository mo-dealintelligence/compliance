import { brand } from '@trycompai/utils/brand';
import { SVGProps } from 'react';

export const Logo = (props: SVGProps<SVGSVGElement>) => (
  <svg
    width={178}
    height={43}
    viewBox="0 0 178 43"
    fill="none"
    xmlns="http://www.w3.org/2000/svg"
    role="img"
    aria-label={brand.name}
    {...props}
  >
    <title>{brand.name}</title>
    <g transform="translate(3 5) scale(1.03)">
      <rect width={32} height={32} rx={6} fill="#0a0a09" />
      <g transform="translate(2.5 0)">
        <circle cx={5} cy={13} r={2} fill="#ff7a3d" />
        <circle cx={5} cy={19} r={2} fill="#ff7a3d" />
        <path d="M8 8 H16 a8 8 0 0 1 0 16 H8 Z" fill="#ff7a3d" />
        <path d="M12 12 H16 a4 4 0 0 1 0 8 H12 Z" fill="#0a0a09" />
      </g>
    </g>
    <text
      x={46}
      y={21.5}
      dominantBaseline="central"
      fontFamily="ui-sans-serif, system-ui, sans-serif"
      fontSize={20}
      fontWeight={600}
      fill="currentColor"
    >
      {brand.name}
    </text>
  </svg>
);
