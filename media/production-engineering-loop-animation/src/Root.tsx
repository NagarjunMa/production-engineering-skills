import React from 'react';
import {Composition} from 'remotion';
import {z} from 'zod';
import {ProductionEngineeringLoop} from './ProductionEngineeringLoop';
import {HowTheLoopWorks} from './HowTheLoopWorks';
import {SocialLoop} from './SocialLoop';

export const animationSchema = z.object({
  title: z.string(),
  subtitle: z.string(),
  installCommand: z.string(),
});

export type AnimationProps = z.infer<typeof animationSchema>;

const defaultProps: AnimationProps = {
  title: 'Make quality the default in every AI coding session',
  subtitle: 'Use one skill across the work you already do',
  installCommand: 'npx skills add NagarjunMa/production-engineering-skills',
};

export const Root: React.FC = () => (
  <>
    <Composition
      id="ProductionEngineeringLoop"
      component={ProductionEngineeringLoop}
      durationInFrames={450}
      fps={30}
      width={1080}
      height={1080}
      schema={animationSchema}
      defaultProps={defaultProps}
      calculateMetadata={({props}) => ({
        durationInFrames: 450,
        fps: 30,
        width: 1080,
        height: 1080,
        props,
      })}
    />
    <Composition
      id="HowTheLoopWorks"
      component={HowTheLoopWorks}
      durationInFrames={780}
      fps={30}
      width={1080}
      height={1080}
      schema={animationSchema}
      defaultProps={{
        title: 'How the engineering loop works',
        subtitle: 'Enough structure to improve the work—without slowing it down',
        installCommand: 'npx skills add NagarjunMa/production-engineering-skills',
      }}
      calculateMetadata={({props}) => ({
        durationInFrames: 780,
        fps: 30,
        width: 1080,
        height: 1080,
        props,
      })}
    />
    <Composition
      id="SocialLoop"
      component={SocialLoop}
      durationInFrames={510}
      fps={30}
      width={1080}
      height={1080}
      schema={animationSchema}
      defaultProps={{
        title: 'Better AI coding, task after task.',
        subtitle: 'Understand, build, verify, and learn',
        installCommand: 'npx skills add NagarjunMa/production-engineering-skills',
      }}
      calculateMetadata={({props}) => ({
        durationInFrames: 510,
        fps: 30,
        width: 1080,
        height: 1080,
        props,
      })}
    />
  </>
);
