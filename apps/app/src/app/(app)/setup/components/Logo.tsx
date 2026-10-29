import { brand } from '@trycompai/utils/brand';
import { SVGProps } from 'react';

const initial = brand.name.charAt(0).toUpperCase();

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
    <rect x={3} y={3} width={37} height={37} rx={8} stroke="currentColor" strokeWidth={3} />
    <text
      x={21.5}
      y={21.5}
      dominantBaseline="central"
      textAnchor="middle"
      fontFamily="ui-sans-serif, system-ui, sans-serif"
      fontSize={22}
      fontWeight={700}
      fill="currentColor"
    >
      {initial}
    </text>
    <text
      x={50}
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
