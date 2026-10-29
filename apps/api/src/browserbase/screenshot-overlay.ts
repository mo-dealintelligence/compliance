// apps/api/src/browserbase/screenshot-overlay.ts
import { brand } from '@trycompai/utils/brand';
import sharp from 'sharp';

export const OVERLAY_HEIGHT_PX = 88;
const OVERLAY_BG = '#0A0A0A';
const OVERLAY_SURFACE = '#111113';
const OVERLAY_BORDER = '#1F1F23';
const OVERLAY_TEXT = '#FAFAFA';
const OVERLAY_MUTED = '#8B8B92';
const OVERLAY_ACCENT = '#22C55E';
const BRAND_PILLAR_WIDTH = 168;
const MAX_INSTRUCTION_CHARS = 120;
const MAX_URL_CHARS = 140;

const BRAND_INITIAL = brand.name.charAt(0).toUpperCase();

export interface RenderOverlayInput {
  buffer: Buffer;
  instruction: string;
  sourceUrl: string;
  capturedAt: Date;
}

/**
 * Composite an audit metadata banner onto the bottom of a screenshot.
 * The banner adds OVERLAY_HEIGHT_PX to the total image height.
 * Failure-mode contract: throws on malformed input; callers should handle
 * and fall back to the raw image.
 */
export async function renderOverlay(
  input: RenderOverlayInput,
): Promise<Buffer> {
  const { buffer, instruction, sourceUrl, capturedAt } = input;

  const sourceMeta = await sharp(buffer).metadata();
  const width = sourceMeta.width;
  const height = sourceMeta.height;
  if (!width) {
    throw new Error('renderOverlay: source image has no width');
  }
  if (!height) {
    throw new Error('renderOverlay: source image has no height');
  }

  const instructionText = truncate(instruction, MAX_INSTRUCTION_CHARS);
  const sourceUrlText = truncate(sourceUrl, MAX_URL_CHARS);
  const timestampText = formatUtc(capturedAt);

  const bannerSvg = buildBannerSvg({
    width,
    height: OVERLAY_HEIGHT_PX,
    instruction: instructionText,
    sourceUrl: sourceUrlText,
    timestamp: timestampText,
  });

  const bannerBuffer = await sharp(Buffer.from(bannerSvg)).png().toBuffer();

  const extended = await sharp(buffer)
    .extend({
      bottom: OVERLAY_HEIGHT_PX,
      background: OVERLAY_BG,
    })
    .composite([
      {
        input: bannerBuffer,
        top: height,
        left: 0,
      },
    ])
    .jpeg({ quality: 85 })
    .toBuffer();

  return extended;
}

function truncate(value: string, max: number): string {
  if (value.length <= max) return value;
  return value.slice(0, max - 1) + '…';
}

function formatUtc(date: Date): string {
  const pad = (n: number) => String(n).padStart(2, '0');
  const y = date.getUTCFullYear();
  const m = pad(date.getUTCMonth() + 1);
  const d = pad(date.getUTCDate());
  const hh = pad(date.getUTCHours());
  const mm = pad(date.getUTCMinutes());
  const ss = pad(date.getUTCSeconds());
  return `${y}-${m}-${d} ${hh}:${mm}:${ss} UTC`;
}

function escapeXml(value: string): string {
  // Strip XML 1.0 illegal control chars (keep tab 0x09, LF 0x0A, CR 0x0D)
  const stripped = value.replace(/[\x00-\x08\x0B\x0C\x0E-\x1F]/g, '');
  return stripped
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&apos;');
}

interface BannerArgs {
  width: number;
  height: number;
  instruction: string;
  sourceUrl: string;
  timestamp: string;
}

function buildBannerSvg(args: BannerArgs): string {
  const { width, height, instruction, sourceUrl, timestamp } = args;
  const rowFontSize = 12;
  const labelFontSize = 9;
  // Explicit Linux-safe font stack. The production container only ships
  // DejaVu Sans (via fonts-dejavu-core); Apple/Segoe/Roboto aren't available
  // so librsvg would render .notdef glyphs ("□ □ □") on servers.
  const fontFamily = '"DejaVu Sans", sans-serif';

  const w = Math.floor(width);
  const h = Math.floor(height);
  const pillarW = Math.min(BRAND_PILLAR_WIDTH, Math.floor(w / 3));
  const infoX = pillarW + 20;
  const accentStripeH = 2;
  const logoSize = 28;
  const logoX = 18;
  const logoY = Math.floor((h - accentStripeH - logoSize) / 2);
  const brandTextX = logoX + logoSize + 12;
  const brandTextY = logoY + 14;
  const brandTaglineY = logoY + 27;

  return `<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="${w}" height="${h}" viewBox="0 0 ${w} ${h}">
  <rect x="0" y="0" width="${w}" height="${h}" fill="${OVERLAY_BG}"/>
  <rect x="0" y="0" width="${pillarW}" height="${h - accentStripeH}" fill="${OVERLAY_SURFACE}"/>
  <rect x="${pillarW}" y="0" width="1" height="${h - accentStripeH}" fill="${OVERLAY_BORDER}"/>
  <rect x="0" y="${h - accentStripeH}" width="${w}" height="${accentStripeH}" fill="${OVERLAY_ACCENT}"/>
  <g transform="translate(${logoX} ${logoY}) scale(${logoSize / 56})">
    <rect x="3" y="3" width="50" height="50" rx="11" fill="none" stroke="${OVERLAY_TEXT}" stroke-width="4"/>
    <text x="28" y="29" font-family='${fontFamily}' font-size="30" font-weight="700" text-anchor="middle" dominant-baseline="central" fill="${OVERLAY_TEXT}">${BRAND_INITIAL}</text>
  </g>
  <g font-family='${fontFamily}' fill="${OVERLAY_TEXT}">
    <text x="${brandTextX}" y="${brandTextY}" font-size="13" font-weight="700" letter-spacing="-0.2">${escapeXml(brand.name)}</text>
    <text x="${brandTextX}" y="${brandTaglineY}" font-size="${labelFontSize}" font-weight="500" fill="${OVERLAY_MUTED}" letter-spacing="0.8">AUDIT TRAIL</text>
  </g>
  <g font-family='${fontFamily}' fill="${OVERLAY_TEXT}">
    <text x="${infoX}" y="22" font-size="${rowFontSize}" font-weight="600">
      <tspan fill="${OVERLAY_MUTED}" font-size="${labelFontSize}" letter-spacing="0.6">REQUIREMENT  </tspan>
      <tspan letter-spacing="0">${escapeXml(instruction)}</tspan>
    </text>
    <text x="${infoX}" y="46" font-size="${rowFontSize}">
      <tspan fill="${OVERLAY_MUTED}" font-size="${labelFontSize}" letter-spacing="0.6">CAPTURED  </tspan>
      <tspan letter-spacing="0">${escapeXml(timestamp)}</tspan>
    </text>
    <text x="${infoX}" y="70" font-size="${rowFontSize}">
      <tspan fill="${OVERLAY_MUTED}" font-size="${labelFontSize}" letter-spacing="0.6">SOURCE  </tspan>
      <tspan letter-spacing="0">${escapeXml(sourceUrl)}</tspan>
    </text>
  </g>
</svg>`;
}
