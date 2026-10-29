import { Button, Section } from '@react-email/components';
import { brand } from '@trycompai/utils/brand';

export function GetStarted() {
  return (
    <Section className="mt-[50px] mb-[50px] text-center">
      <Button
        className="text-primary border border-solid border-[#121212] bg-transparent px-6 py-3 text-center text-[14px] font-medium text-[#121212] no-underline"
        href={brand.websiteUrl}
      >
        Get started
      </Button>
    </Section>
  );
}
