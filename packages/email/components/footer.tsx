import { Hr, Link, Section, Text } from '@react-email/components';
import { brand } from '@trycompai/utils/brand';

export function Footer() {
  return (
    <Section className="w-full">
      <Hr />

      <Text className="font-regular text-[14px]">
        Sent by <Link href={brand.websiteUrl}>{brand.name}</Link>.
      </Text>

      <Text className="text-xs text-[#B8B8B8]">{brand.postalAddress}</Text>
    </Section>
  );
}
