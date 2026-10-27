# Production Engineering Loop animation

A 17-second, 1080×1080 Remotion infographic for LinkedIn, X, and Reddit. It presents the surface-level Understand → Build → Verify → Learn loop and ends with the interactive installation command.

## Render

```sh
npm ci --ignore-scripts
npm run render:social
```

The published MP4 is written to `out/production-engineering-loop-social.mp4`. Its final held frame is `out/social-final.png`.

The project retains two earlier compositions for iteration and comparison. Render them locally with `npm run render` and `npm run render:explainer`; their generated outputs are intentionally excluded from version control.

All motion is derived from the Remotion frame. The scene does not use timers, random values, remote fonts, or external media.

## Dependency verification

CI runs `npm audit` and TypeScript checks for this optional project. On 2026-10-26,
the locked dependency tree audited clean and `SocialLoop` frame 450 rendered.
Zod is pinned and overridden to 4.6.7 to fix GHSA-mrhx-c7xc-m3w5, including
Remotion's transitive copies. Remotion 4.0.527 still prints a version warning
because its expected pin is 4.5.4. The schema/type check and smoke render passed;
that does not establish every optional Remotion feature works with the override.
Recheck and remove the override when upstream supports a patched pin. These
dependencies are not installed with the skill.
