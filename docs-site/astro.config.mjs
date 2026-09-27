import { defineConfig } from "astro/config";
import starlight from "@astrojs/starlight";

export default defineConfig({
  site: "https://averyfreeman.github.io",
  base: "/dfrs",
  integrations: [
    starlight({
      title: "dfrs",
      description: "A platform-aware terminal filesystem usage viewer.",
      social: [
        {
          icon: "github",
          label: "GitHub",
          href: "https://github.com/averyfreeman/dfrs",
        },
      ],
      customCss: ["./src/styles/custom.css"],
      sidebar: [
        {
          label: "Use dfrs",
          items: [
            { slug: "index", label: "Overview" },
            { slug: "cli", label: "CLI reference" },
          ],
        },
        {
          label: "Maintain dfrs",
          items: [
            { slug: "architecture", label: "Architecture" },
            { slug: "development", label: "Development" },
            { slug: "release-notes", label: "Release notes" },
          ],
        },
      ],
    }),
  ],
});
