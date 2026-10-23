/// <reference types="vite/client" />

declare module "react-plotly.js";

declare module "lucide-react" {
  import type { ComponentType, SVGProps } from "react";

  export type LucideProps = SVGProps<SVGSVGElement> & {
    size?: number | string;
  };

  export const ArrowUpRight: ComponentType<LucideProps>;
  export const BadgeCheck: ComponentType<LucideProps>;
  export const CircleAlert: ComponentType<LucideProps>;
  export const FlaskConical: ComponentType<LucideProps>;
  export const RefreshCw: ComponentType<LucideProps>;
}
