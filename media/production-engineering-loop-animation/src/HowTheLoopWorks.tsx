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

const C = {
  bg: '#07111F',
  panel: '#0D1B2C',
  panel2: '#13253A',
  ink: '#F7FAFC',
  muted: '#9BAEC3',
  teal: '#5EEAD4',
  blue: '#60A5FA',
  violet: '#A78BFA',
  amber: '#FBBF24',
  grid: 'rgba(125, 211, 252, 0.07)',
  border: 'rgba(148, 163, 184, 0.18)',
};

const FONT = 'Inter, ui-sans-serif, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif';
const clamp = {extrapolateLeft: 'clamp' as const, extrapolateRight: 'clamp' as const};
const fade = (frame: number, start: number, duration = 18) =>
  interpolate(frame, [start, start + duration], [0, 1], {
    ...clamp,
    easing: Easing.out(Easing.cubic),
  });
const fadeOut = (frame: number, start: number, duration = 18) =>
  interpolate(frame, [start, start + duration], [1, 0], {
    ...clamp,
    easing: Easing.in(Easing.cubic),
  });
const rise = (p: number, px = 20) => `translateY(${(1 - p) * px}px)`;

type IconName = 'search' | 'code' | 'shield' | 'check' | 'test' | 'review' | 'map' | 'memory' | 'repeat';

const Icon: React.FC<{name: IconName; color: string; size?: number}> = ({name, color, size = 42}) => {
  const paths: Record<IconName, React.ReactNode> = {
    search: <><circle cx="10.5" cy="10.5" r="6.5" /><path d="m15.5 15.5 5 5" /></>,
    code: <><path d="m8 7-5 5 5 5M16 7l5 5-5 5M14 4l-4 16" /></>,
    shield: <><path d="M12 3 20 6v5c0 5-3.4 8.2-8 10-4.6-1.8-8-5-8-10V6l8-3Z" /><path d="m8.5 12 2.2 2.2 4.8-5" /></>,
    check: <path d="m4 12 5 5L20 6" />,
    test: <><path d="M9 3h6M10 3v5l-5 9a2.5 2.5 0 0 0 2.2 4h9.6A2.5 2.5 0 0 0 19 17l-5-9V3" /><path d="M8 15h8" /></>,
    review: <><path d="M4 5h16v12H8l-4 4V5Z" /><path d="m8 11 2.2 2.2L16 8" /></>,
    map: <><path d="m3 6 6-3 6 3 6-3v15l-6 3-6-3-6 3V6Z" /><path d="M9 3v15M15 6v15" /></>,
    memory: <><rect x="5" y="5" width="14" height="14" rx="3" /><path d="M9 2v3M15 2v3M9 19v3M15 19v3M2 9h3M2 15h3M19 9h3M19 15h3" /></>,
    repeat: <><path d="M20 7h-9a6 6 0 0 0-6 6v1" /><path d="m16 3 4 4-4 4M4 17h9a6 6 0 0 0 6-6v-1" /><path d="m8 21-4-4 4-4" /></>,
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
  headline: string;
  summary: string;
  actions: Array<{icon: IconName; title: string; detail: string}>;
  output: string;
};

const STAGES: Stage[] = [
  {
    name: 'Understand',
    color: C.blue,
    icon: 'search',
    headline: 'Start from intent and evidence',
    summary: 'The agent learns what must change before deciding how to change it.',
    actions: [
      {icon: 'search', title: 'Read the goal', detail: 'Clarify the outcome, constraints, and failure cases.'},
      {icon: 'code', title: 'Inspect relevant code', detail: 'Trace current behavior, callers, and shared contracts.'},
      {icon: 'map', title: 'Bound the change', detail: 'Identify affected areas and what must remain unchanged.'},
    ],
    output: 'Output: a clear change contract',
  },
  {
    name: 'Build',
    color: C.violet,
    icon: 'code',
    headline: 'Fit the codebase—not just the prompt',
    summary: 'Implementation follows the project’s sound conventions and keeps ownership clear.',
    actions: [
      {icon: 'shield', title: 'Follow existing standards', detail: 'Respect architecture, boundaries, and repository rules.'},
      {icon: 'code', title: 'Use patterns with purpose', detail: 'Apply design patterns only when they solve today’s problem.'},
      {icon: 'check', title: 'Keep the change cohesive', detail: 'Avoid duplicated rules and unnecessary abstractions.'},
    ],
    output: 'Output: the smallest coherent implementation',
  },
  {
    name: 'Verify',
    color: C.teal,
    icon: 'test',
    headline: 'Turn acceptance criteria into evidence',
    summary: 'A confident answer is replaced by checks that can expose a plausible wrong implementation.',
    actions: [
      {icon: 'check', title: 'Test acceptance criteria', detail: 'Prove the observable behavior the task requires.'},
      {icon: 'test', title: 'Exercise failure paths', detail: 'Cover boundaries, negative cases, and regressions.'},
      {icon: 'review', title: 'Review the whole change', detail: 'Check compatibility, security, scope, and maintainability.'},
    ],
    output: 'Output: verified results and visible remaining risk',
  },
  {
    name: 'Learn',
    color: C.amber,
    icon: 'memory',
    headline: 'Make the next task start smarter',
    summary: 'Only verified knowledge is retained, and current source remains the authority.',
    actions: [
      {icon: 'map', title: 'Refresh the project map', detail: 'Record current paths, responsibilities, and decisions.'},
      {icon: 'memory', title: 'Keep regression evidence', detail: 'Preserve checks for defects that must not return.'},
      {icon: 'repeat', title: 'Reuse proven context', detail: 'Carry applicable lessons into the next task.'},
    ],
    output: 'Output: reusable context grounded in evidence',
  },
];

const ProgressRail: React.FC<{active: number; final?: boolean}> = ({active, final = false}) => (
  <div style={{display: 'flex', justifyContent: 'center', gap: 12}}>
    {STAGES.map((stage, index) => {
      const selected = final || index === active;
      const completed = final || index < active;
      return (
        <div key={stage.name} style={{display: 'flex', alignItems: 'center', gap: 10}}>
          <div style={{display: 'flex', alignItems: 'center', gap: 9, padding: '9px 14px', borderRadius: 99, background: selected ? `${stage.color}18` : 'rgba(148,163,184,0.06)', border: `1px solid ${selected ? `${stage.color}55` : C.border}`}}>
            <div style={{width: 23, height: 23, borderRadius: 99, display: 'grid', placeItems: 'center', background: completed ? stage.color : 'rgba(148,163,184,0.16)', color: completed ? C.bg : C.muted, fontSize: 13, fontWeight: 850}}>{index + 1}</div>
            <span style={{fontSize: 16, fontWeight: 740, color: selected ? C.ink : C.muted}}>{stage.name}</span>
          </div>
          {index < STAGES.length - 1 ? <div style={{width: 18, height: 1, background: C.border}} /> : null}
        </div>
      );
    })}
  </div>
);

const Intro: React.FC<AnimationProps> = ({title, subtitle}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const titleIn = spring({frame, fps, config: {damping: 18, stiffness: 125, mass: 0.8}});
  const subIn = fade(frame, 14, 22);
  const railIn = fade(frame, 30, 24);
  const out = fadeOut(frame, 60, 15);
  return (
    <div style={{position: 'absolute', inset: 0, display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', opacity: out}}>
      <div style={{fontSize: 64, lineHeight: 1.05, fontWeight: 850, letterSpacing: -2.5, textAlign: 'center', maxWidth: 860, opacity: titleIn, transform: rise(titleIn, 26)}}>{title}</div>
      <div style={{fontSize: 25, color: C.muted, marginTop: 20, textAlign: 'center', opacity: subIn, transform: rise(subIn, 12)}}>{subtitle}</div>
      <div style={{marginTop: 58, opacity: railIn, transform: rise(railIn, 16)}}><ProgressRail active={0} final /></div>
    </div>
  );
};

const StageScene: React.FC<{stage: Stage; index: number; start: number; end: number}> = ({stage, index, start, end}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const enter = fade(frame, start, 18);
  const leave = fadeOut(frame, end - 18, 18);
  const iconPop = spring({frame: frame - start - 8, fps, config: {damping: 11, stiffness: 175, mass: 0.6}});
  return (
    <div style={{position: 'absolute', inset: 0, padding: '62px 76px 64px', opacity: enter * leave}}>
      <ProgressRail active={index} />
      <div style={{display: 'grid', gridTemplateColumns: '290px 1fr', gap: 54, alignItems: 'center', marginTop: 72}}>
        <div style={{display: 'flex', flexDirection: 'column', alignItems: 'center'}}>
          <div style={{width: 176, height: 176, borderRadius: 52, display: 'grid', placeItems: 'center', background: `${stage.color}16`, border: `1px solid ${stage.color}55`, boxShadow: `0 0 70px ${stage.color}20`, transform: `scale(${iconPop})`}}>
            <Icon name={stage.icon} color={stage.color} size={86} />
          </div>
          <div style={{marginTop: 26, fontSize: 21, fontWeight: 800, color: stage.color, letterSpacing: 2.6, textTransform: 'uppercase'}}>{index + 1} · {stage.name}</div>
        </div>
        <div>
          <div style={{fontSize: 44, lineHeight: 1.08, letterSpacing: -1.2, fontWeight: 840, maxWidth: 600}}>{stage.headline}</div>
          <div style={{fontSize: 22, lineHeight: 1.45, color: C.muted, marginTop: 14, maxWidth: 600}}>{stage.summary}</div>
        </div>
      </div>
      <div style={{display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: 18, marginTop: 54}}>
        {stage.actions.map((action, actionIndex) => {
          const itemStart = start + 28 + actionIndex * 12;
          const itemIn = spring({frame: frame - itemStart, fps, config: {damping: 15, stiffness: 150, mass: 0.7}});
          return (
            <div key={action.title} style={{height: 212, padding: '25px 23px', borderRadius: 24, background: 'rgba(13,27,44,0.94)', border: `1px solid ${actionIndex === 0 ? `${stage.color}48` : C.border}`, opacity: itemIn, transform: rise(itemIn, 22)}}>
              <div style={{width: 48, height: 48, borderRadius: 15, display: 'grid', placeItems: 'center', background: `${stage.color}14`}}><Icon name={action.icon} color={stage.color} size={29} /></div>
              <div style={{fontSize: 22, fontWeight: 790, marginTop: 18}}>{action.title}</div>
              <div style={{fontSize: 17, lineHeight: 1.42, color: C.muted, marginTop: 9}}>{action.detail}</div>
            </div>
          );
        })}
      </div>
      <div style={{marginTop: 26, padding: '16px 22px', borderRadius: 16, background: `${stage.color}10`, border: `1px solid ${stage.color}35`, color: stage.color, fontSize: 20, fontWeight: 760, textAlign: 'center', opacity: fade(frame, start + 62, 18)}}>{stage.output}</div>
    </div>
  );
};

const FinalOverview: React.FC<{installCommand: string}> = ({installCommand}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const start = 615;
  const titleIn = spring({frame: frame - start, fps, config: {damping: 17, stiffness: 125, mass: 0.8}});
  return (
    <div style={{position: 'absolute', inset: 0, padding: '70px 72px 58px', opacity: fade(frame, start, 20)}}>
      <div style={{textAlign: 'center', fontSize: 48, fontWeight: 850, letterSpacing: -1.6, opacity: titleIn, transform: rise(titleIn, 22)}}>A loop that improves the work—and the next task</div>
      <div style={{marginTop: 22}}><ProgressRail active={3} final /></div>
      <div style={{display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: 18, marginTop: 54}}>
        {STAGES.map((stage, index) => {
          const cardIn = spring({frame: frame - start - 22 - index * 10, fps, config: {damping: 15, stiffness: 150, mass: 0.7}});
          const taglines = ['Goal + relevant context', 'Standards + purposeful patterns', 'Criteria + executable evidence', 'Verified memory + regression checks'];
          return (
            <div key={stage.name} style={{height: 164, padding: '25px 28px', borderRadius: 25, background: 'rgba(13,27,44,0.96)', border: `1px solid ${stage.color}40`, display: 'flex', alignItems: 'center', gap: 22, opacity: cardIn, transform: rise(cardIn, 18)}}>
              <div style={{width: 72, height: 72, flex: '0 0 auto', borderRadius: 22, display: 'grid', placeItems: 'center', background: `${stage.color}14`}}><Icon name={stage.icon} color={stage.color} size={39} /></div>
              <div>
                <div style={{fontSize: 25, fontWeight: 820, color: stage.color}}>{stage.name}</div>
                <div style={{fontSize: 18, lineHeight: 1.4, color: C.muted, marginTop: 7}}>{taglines[index]}</div>
              </div>
            </div>
          );
        })}
      </div>
      <div style={{marginTop: 48, textAlign: 'center', opacity: fade(frame, start + 74, 20)}}>
        <div style={{fontSize: 31, fontWeight: 820}}>Start your next meaningful task with Production Engineering Loop</div>
        <div style={{display: 'inline-block', marginTop: 18, padding: '13px 18px', borderRadius: 13, border: '1px solid rgba(96,165,250,0.3)', background: 'rgba(96,165,250,0.08)', color: C.blue, fontFamily: 'ui-monospace, SFMono-Regular, Menlo, monospace', fontSize: 16}}>{installCommand}</div>
      </div>
    </div>
  );
};

export const HowTheLoopWorks: React.FC<AnimationProps> = (props) => {
  const frame = useCurrentFrame();
  const pulse = interpolate(frame, [0, 390, 779], [0.15, 0.45, 0.15], clamp);
  const ranges = [
    [75, 210],
    [210, 345],
    [345, 480],
    [480, 615],
  ] as const;
  return (
    <AbsoluteFill style={{background: C.bg, color: C.ink, fontFamily: FONT, overflow: 'hidden'}}>
      <div style={{position: 'absolute', inset: 0, backgroundImage: `linear-gradient(${C.grid} 1px, transparent 1px), linear-gradient(90deg, ${C.grid} 1px, transparent 1px)`, backgroundSize: '54px 54px', maskImage: 'linear-gradient(to bottom, black, transparent 90%)'}} />
      <div style={{position: 'absolute', width: 680, height: 680, borderRadius: '50%', left: 200, top: 250, background: `radial-gradient(circle, rgba(94,234,212,${0.05 + pulse * 0.035}) 0%, transparent 70%)`}} />
      <Intro {...props} />
      {STAGES.map((stage, index) => <StageScene key={stage.name} stage={stage} index={index} start={ranges[index][0]} end={ranges[index][1]} />)}
      <FinalOverview installCommand={props.installCommand} />
    </AbsoluteFill>
  );
};
