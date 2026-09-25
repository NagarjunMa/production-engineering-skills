import React from 'react';
import {
  AbsoluteFill,
  Easing,
  interpolate,
  spring,
  useCurrentFrame,
  useVideoConfig,
} from 'remotion';
import type {AnimationProps} from './Root';

const COLORS = {
  background: '#07111F',
  panel: '#0D1B2C',
  ink: '#F8FAFC',
  muted: '#9BAEC3',
  blue: '#60A5FA',
  violet: '#A78BFA',
  teal: '#5EEAD4',
  amber: '#FBBF24',
  grid: 'rgba(125, 211, 252, 0.065)',
  border: 'rgba(148, 163, 184, 0.18)',
};

const FONT = 'Inter, ui-sans-serif, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif';
const clamp = {extrapolateLeft: 'clamp' as const, extrapolateRight: 'clamp' as const};

const fade = (frame: number, start: number, duration = 14) =>
  interpolate(frame, [start, start + duration], [0, 1], {
    ...clamp,
    easing: Easing.out(Easing.cubic),
  });

const fadeOut = (frame: number, start: number, duration = 14) =>
  interpolate(frame, [start, start + duration], [1, 0], {
    ...clamp,
    easing: Easing.in(Easing.cubic),
  });

type IconName = 'search' | 'code' | 'test' | 'memory' | 'arrow';

const Icon: React.FC<{name: IconName; color: string; size?: number}> = ({name, color, size = 52}) => {
  const paths: Record<IconName, React.ReactNode> = {
    search: <><circle cx="10.5" cy="10.5" r="6.5" /><path d="m15.5 15.5 5 5" /></>,
    code: <><path d="m8 7-5 5 5 5M16 7l5 5-5 5M14 4l-4 16" /></>,
    test: <><path d="M9 3h6M10 3v5l-5 9a2.5 2.5 0 0 0 2.2 4h9.6A2.5 2.5 0 0 0 19 17l-5-9V3" /><path d="M8 15h8" /></>,
    memory: <><rect x="5" y="5" width="14" height="14" rx="3" /><path d="M9 2v3M15 2v3M9 19v3M15 19v3M2 9h3M2 15h3M19 9h3M19 15h3" /></>,
    arrow: <><path d="M5 12h14" /><path d="m14 7 5 5-5 5" /></>,
  };

  return (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke={color} strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round">
      {paths[name]}
    </svg>
  );
};

type Stage = {
  name: string;
  color: string;
  icon: IconName;
  statement: string;
  from: string;
  to: string;
};

const STAGES: Stage[] = [
  {
    name: 'Understand',
    color: COLORS.blue,
    icon: 'search',
    statement: 'Reads the goal, relevant code, and constraints.',
    from: 'Problem',
    to: 'Clear change contract',
  },
  {
    name: 'Build',
    color: COLORS.violet,
    icon: 'code',
    statement: 'Follows the project’s architecture, standards, and purposeful patterns.',
    from: 'Change contract',
    to: 'Cohesive implementation',
  },
  {
    name: 'Verify',
    color: COLORS.teal,
    icon: 'test',
    statement: 'Tests acceptance criteria and meaningful failure paths.',
    from: 'Implementation',
    to: 'Evidence-backed result',
  },
  {
    name: 'Learn',
    color: COLORS.amber,
    icon: 'memory',
    statement: 'Turns verified work into reusable project context.',
    from: 'Verified evidence',
    to: 'Better next starting point',
  },
];

const StageRail: React.FC<{active?: number; complete?: boolean}> = ({active, complete = false}) => (
  <div style={{display: 'flex', alignItems: 'center', justifyContent: 'center', gap: 12}}>
    {STAGES.map((stage, index) => {
      const highlighted = complete || active === index;
      return (
        <React.Fragment key={stage.name}>
          <div style={{display: 'flex', alignItems: 'center', gap: 9, color: highlighted ? stage.color : COLORS.muted, fontSize: 17, fontWeight: 780}}>
            <div style={{width: 12, height: 12, borderRadius: 99, background: highlighted ? stage.color : 'rgba(148,163,184,0.25)', boxShadow: highlighted ? `0 0 20px ${stage.color}88` : 'none'}} />
            {stage.name}
          </div>
          {index < STAGES.length - 1 ? <div style={{width: 24, height: 1, background: COLORS.border}} /> : null}
        </React.Fragment>
      );
    })}
  </div>
);

const Intro: React.FC = () => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const titleIn = spring({frame, fps, config: {damping: 17, stiffness: 125, mass: 0.8}});
  const out = fadeOut(frame, 34, 11);

  return (
    <div style={{position: 'absolute', inset: 0, display: 'grid', placeItems: 'center', opacity: out}}>
      <div style={{textAlign: 'center'}}>
        <div style={{fontSize: 66, lineHeight: 1.04, fontWeight: 870, letterSpacing: -2.8, maxWidth: 880, opacity: titleIn, transform: `translateY(${(1 - titleIn) * 26}px)`}}>
          Better AI coding,<br />task after task.
        </div>
        <div style={{marginTop: 42, opacity: fade(frame, 12, 16)}}>
          <StageRail complete />
        </div>
      </div>
    </div>
  );
};

const StageScene: React.FC<{stage: Stage; index: number; start: number; end: number}> = ({stage, index, start, end}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const enter = fade(frame, start, 14);
  const leave = fadeOut(frame, end - 12, 12);
  const iconIn = spring({frame: frame - start - 4, fps, config: {damping: 12, stiffness: 165, mass: 0.7}});
  const transformIn = spring({frame: frame - start - 20, fps, config: {damping: 16, stiffness: 145, mass: 0.75}});

  return (
    <div style={{position: 'absolute', inset: 0, padding: '74px 76px', opacity: enter * leave}}>
      <StageRail active={index} />
      <div style={{marginTop: 104, textAlign: 'center'}}>
        <div style={{width: 156, height: 156, margin: '0 auto', borderRadius: 48, display: 'grid', placeItems: 'center', background: `${stage.color}16`, border: `1px solid ${stage.color}55`, boxShadow: `0 0 72px ${stage.color}20`, transform: `scale(${iconIn})`}}>
          <Icon name={stage.icon} color={stage.color} size={78} />
        </div>
        <div style={{marginTop: 30, color: stage.color, fontSize: 21, fontWeight: 850, letterSpacing: 3.2, textTransform: 'uppercase'}}>{stage.name}</div>
        <div style={{margin: '18px auto 0', maxWidth: 790, fontSize: 43, lineHeight: 1.16, fontWeight: 820, letterSpacing: -1.1}}>{stage.statement}</div>
      </div>
      <div style={{display: 'grid', gridTemplateColumns: '1fr 76px 1fr', alignItems: 'center', gap: 14, marginTop: 72, opacity: transformIn, transform: `translateY(${(1 - transformIn) * 20}px)`}}>
        <div style={{padding: '24px 20px', textAlign: 'center', borderRadius: 20, background: COLORS.panel, border: `1px solid ${COLORS.border}`, color: COLORS.muted, fontSize: 22, fontWeight: 700}}>{stage.from}</div>
        <div style={{display: 'grid', placeItems: 'center'}}><Icon name="arrow" color={stage.color} size={48} /></div>
        <div style={{padding: '24px 20px', textAlign: 'center', borderRadius: 20, background: `${stage.color}12`, border: `1px solid ${stage.color}55`, color: stage.color, fontSize: 22, fontWeight: 790}}>{stage.to}</div>
      </div>
    </div>
  );
};

const Final: React.FC<{installCommand: string}> = ({installCommand}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const start = 405;
  const titleIn = spring({frame: frame - start, fps, config: {damping: 16, stiffness: 120, mass: 0.8}});

  return (
    <div style={{position: 'absolute', inset: 0, padding: '72px 76px 58px', textAlign: 'center', opacity: fade(frame, start, 16)}}>
      <StageRail complete />
      <div style={{position: 'relative', width: 630, height: 330, margin: '76px auto 0'}}>
        <div style={{position: 'absolute', inset: 28, borderRadius: 170, border: '2px solid rgba(94,234,212,0.22)', boxShadow: '0 0 80px rgba(94,234,212,0.08)'}} />
        {STAGES.map((stage, index) => {
          const positions = [
            {left: 0, top: 111},
            {left: 210, top: 0},
            {left: 420, top: 111},
            {left: 210, top: 222},
          ];
          const cardIn = spring({frame: frame - start - index * 6, fps, config: {damping: 14, stiffness: 150, mass: 0.7}});
          return (
            <div key={stage.name} style={{position: 'absolute', ...positions[index], width: 210, height: 108, borderRadius: 24, display: 'flex', alignItems: 'center', justifyContent: 'center', gap: 13, background: COLORS.panel, border: `1px solid ${stage.color}50`, color: stage.color, fontSize: 20, fontWeight: 810, opacity: cardIn, transform: `scale(${0.86 + cardIn * 0.14})`}}>
              <Icon name={stage.icon} color={stage.color} size={35} />
              {stage.name}
            </div>
          );
        })}
      </div>
      <div style={{marginTop: 54, fontSize: 43, lineHeight: 1.12, fontWeight: 850, letterSpacing: -1.3, opacity: titleIn, transform: `translateY(${(1 - titleIn) * 20}px)`}}>
        Every verified task gives<br />the next task a better start.
      </div>
      <div style={{marginTop: 24, color: COLORS.muted, fontSize: 22, opacity: fade(frame, start + 35, 18)}}>Production Engineering Loop</div>
      <div style={{display: 'inline-block', marginTop: 22, padding: '13px 18px', borderRadius: 13, border: '1px solid rgba(96,165,250,0.3)', background: 'rgba(96,165,250,0.08)', color: COLORS.blue, fontFamily: 'ui-monospace, SFMono-Regular, Menlo, monospace', fontSize: 16, opacity: fade(frame, start + 50, 18)}}>{installCommand}</div>
    </div>
  );
};

export const SocialLoop: React.FC<AnimationProps> = ({installCommand}) => {
  const frame = useCurrentFrame();
  const ranges = [
    [45, 135],
    [135, 225],
    [225, 315],
    [315, 405],
  ] as const;
  const glow = interpolate(frame, [0, 255, 509], [0.12, 0.42, 0.12], clamp);

  return (
    <AbsoluteFill style={{background: COLORS.background, color: COLORS.ink, fontFamily: FONT, overflow: 'hidden'}}>
      <div style={{position: 'absolute', inset: 0, backgroundImage: `linear-gradient(${COLORS.grid} 1px, transparent 1px), linear-gradient(90deg, ${COLORS.grid} 1px, transparent 1px)`, backgroundSize: '54px 54px', maskImage: 'linear-gradient(to bottom, black, transparent 92%)'}} />
      <div style={{position: 'absolute', width: 720, height: 720, borderRadius: '50%', left: 180, top: 210, background: `radial-gradient(circle, rgba(96,165,250,${0.035 + glow * 0.035}) 0%, transparent 70%)`}} />
      <Intro />
      {STAGES.map((stage, index) => <StageScene key={stage.name} stage={stage} index={index} start={ranges[index][0]} end={ranges[index][1]} />)}
      <Final installCommand={installCommand} />
    </AbsoluteFill>
  );
};
