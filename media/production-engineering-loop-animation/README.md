# Production Engineering Loop animation

A 17-second, 1080×1080 Remotion infographic for LinkedIn, X, and Reddit. It presents the surface-level Understand → Build → Verify → Learn loop and ends with the interactive installation command.

## Render

```sh
npm install
npm run render:social
```

The published MP4 is written to `out/production-engineering-loop-social.mp4`. Its final held frame is `out/social-final.png`.

The project retains two earlier compositions for iteration and comparison. Render them locally with `npm run render` and `npm run render:explainer`; their generated outputs are intentionally excluded from version control.

All motion is derived from the Remotion frame. The scene does not use timers, random values, remote fonts, or external media.
