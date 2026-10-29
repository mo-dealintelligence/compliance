import { Img, Section } from '@react-email/components';
import { brand } from '@trycompai/utils/brand';

export function Logo() {
  return (
    <Section className="mt-[32px]">
      <Img
        src={brand.logoUrl}
        width="45"
        height="45"
        alt={brand.name}
        className="mx-auto my-0 block"
      />
    </Section>
  );
}
