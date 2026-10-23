/// <reference types="vite/client" />

declare module "react-plotly.js";

declare module "lucide-react/dist/esm/icons/*.js" {
  import type { ComponentType, SVGProps } from "react";

  type LucideProps = SVGProps<SVGSVGElement> & {
    size?: number | string;
  };

  const Icon: ComponentType<LucideProps>;
  export default Icon;
}
