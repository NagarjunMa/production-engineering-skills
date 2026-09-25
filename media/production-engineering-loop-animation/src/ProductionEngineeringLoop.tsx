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
  panelRaised: '#13253A',
  ink: '#F7FAFC',
  muted: '#9BAEC3',
  grid: 'rgba(125, 211, 252, 0.07)',
  accent: '#5EEAD4',
  accentBlue: '#60A5FA',
  accentWarm: '#FB7185',
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

const rise = (progress: number, distance = 22) => `translateY(${(1 - progress) * distance}px)`;

const Icon: React.FC<{name: 'spark' | 'layers' | 'eye' | 'check' | 'memory'; color?: string}> = ({
  name,
  color = COLORS.accent,
}) => {
  const paths = {
    spark: <path d="M12 2 14.6 9.4 22 12l-7.4 2.6L12 22l-2.6-7.4L2 12l7.4-2.6L12 2Z" />,
    layers: <><path d="m12 3 9 5-9 5-9-5 9-5Z" /><path d="m3 12 9 5 9-5" /><path d="m3 16 9 5 9-5" /></>,
    eye: <><path d="M2.5 12s3.5-6 9.5-6 9.5 6 9.5 6-3.5 6-9.5 6-9.5-6-9.5-6Z" /><circle cx="12" cy="12" r="2.7" /></>,
    check: <path d="m4 12 5 5L20 6" />,
    memory: <><rect x="5" y="5" width="14" height="14" rx="3" /><path d="M9 2v3M15 2v3M9 19v3M15 19v3M2 9h3M2 15h3M19 9h3M19 15h3" /></>,
  };

  return (
    <svg width="42" height="42" viewBox="0 0 24 24" fill="none" stroke={color} strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round">
      {paths[name]}
    </svg>
  );
};

const CodeCard: React.FC<{
  title: string;
  x: number;
  y: number;
  rotate: number;
  delay: number;
  width: number;
  tone: 'warm' | 'cool';
}> = ({title, x, y, rotate, delay, width, tone}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const enter = spring({frame: frame - delay, fps, config: {damping: 13, stiffness: 140, mass: 0.7}});
  const leave = fadeOut(frame, 105, 22);
  const color = tone === 'warm' ? COLORS.accentWarm : COLORS.accentBlue;
  const drift = interpolate(frame, [delay, 105], [0, tone === 'warm' ? -7 : 7], clamp);

  return (
    <div
      style={{
        position: 'absolute',
        left: x,
        top: y,
        width,
        height: 92,
        padding: '18px 20px',
        borderRadius: 18,
        border: `1px solid ${COLORS.border}`,
        background: 'rgba(13, 27, 44, 0.94)',
        boxShadow: '0 20px 45px rgba(0,0,0,0.22)',
        opacity: enter * leave,
        transform: `translateY(${(1 - enter) * 26 + drift}px) rotate(${rotate * enter}deg) scale(${0.92 + enter * 0.08})`,
      }}
    >
      <div style={{fontSize: 21, fontWeight: 760, color: COLORS.ink, marginBottom: 14}}>{title}</div>
      {[0.72, 0.48].map((factor, i) => (
        <div
          key={factor}
          style={{
            height: 7,
            width: `${factor * 100}%`,
            borderRadius: 8,
            marginBottom: 10,
            background: i === 0 ? color : 'rgba(155, 174, 195, 0.28)',
          }}
        />
      ))}
      <div style={{position: 'absolute', right: 14, top: 14, width: 9, height: 9, borderRadius: 99, background: color, boxShadow: `0 0 18px ${color}`}} />
    </div>
  );
};

const FlowStep: React.FC<{
  label: string;
  icon: 'layers' | 'spark' | 'eye' | 'memory';
  index: number;
  start: number;
}> = ({label, icon, index, start}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const localStart = start + index * 34;
  const pop = spring({frame: frame - localStart, fps, config: {damping: 10, stiffness: 180, mass: 0.55}});
  const textIn = fade(frame, localStart + 8, 18);
  const glow = interpolate(frame, [localStart, localStart + 22, localStart + 46], [0, 1, 0.35], clamp);

  return (
    <div style={{width: 174, display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 13}}>
      <div
        style={{
          width: 92,
          height: 92,
          borderRadius: 28,
          display: 'grid',
          placeItems: 'center',
          background: COLORS.panelRaised,
          border: `1px solid rgba(94, 234, 212, ${0.2 + glow * 0.55})`,
          boxShadow: `0 0 ${36 * glow}px rgba(94, 234, 212, ${0.25 * glow})`,
          transform: `scale(${pop})`,
        }}
      >
        <Icon name={icon} />
      </div>
      <div style={{fontSize: 24, fontWeight: 700, color: COLORS.ink, opacity: textIn, transform: rise(textIn, 10)}}>{label}</div>
    </div>
  );
};

const Connector: React.FC<{index: number; start: number}> = ({index, start}) => {
  const frame = useCurrentFrame();
  const localStart = start + index * 34 + 20;
  const draw = interpolate(frame, [localStart, localStart + 20], [0, 1], clamp);
  return (
    <svg width="62" height="44" viewBox="0 0 62 44" style={{marginTop: 25, overflow: 'visible'}}>
      <path d="M4 22 H54" stroke="rgba(94,234,212,0.6)" strokeWidth="3" strokeLinecap="round" strokeDasharray="50" strokeDashoffset={50 * (1 - draw)} />
      <path d="m48 15 9 7-9 7" fill="none" stroke="rgba(94,234,212,0.8)" strokeWidth="3" strokeLinecap="round" strokeLinejoin="round" opacity={fade(frame, localStart + 14, 6)} />
    </svg>
  );
};

const ResultPill: React.FC<{label: string; delay: number}> = ({label, delay}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const enter = spring({frame: frame - delay, fps, config: {damping: 15, stiffness: 160, mass: 0.65}});
  return (
    <div style={{display: 'flex', alignItems: 'center', gap: 14, opacity: enter, transform: rise(enter, 16)}}>
      <div style={{width: 34, height: 34, borderRadius: 12, display: 'grid', placeItems: 'center', background: 'rgba(94,234,212,0.13)', border: '1px solid rgba(94,234,212,0.28)'}}>
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke={COLORS.accent} strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round"><path d="m5 12 4 4L19 6" /></svg>
      </div>
      <div style={{fontSize: 25, fontWeight: 650, color: COLORS.ink}}>{label}</div>
    </div>
  );
};

export const ProductionEngineeringLoop: React.FC<AnimationProps> = ({title, subtitle, installCommand}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const titleIn = spring({frame, fps, config: {damping: 18, stiffness: 120, mass: 0.8}});
  const subtitleIn = fade(frame, 14, 22);
  const chaosLabelIn = fade(frame, 34, 18) * fadeOut(frame, 105, 20);
  const flowIn = fade(frame, 118, 20);
  const resultIn = spring({frame: frame - 270, fps, config: {damping: 16, stiffness: 130, mass: 0.8}});
  const brandIn = fade(frame, 326, 24);
  const pulse = interpolate(frame, [330, 390, 449], [0.2, 0.5, 0.2], clamp);
  const steps = [
    {label: 'Understand', icon: 'layers' as const},
    {label: 'Build', icon: 'spark' as const},
    {label: 'Verify', icon: 'eye' as const},
    {label: 'Learn', icon: 'memory' as const},
  ];

  return (
    <AbsoluteFill style={{background: COLORS.background, color: COLORS.ink, fontFamily: FONT, overflow: 'hidden'}}>
      <div
        style={{
          position: 'absolute',
          inset: 0,
          backgroundImage: `linear-gradient(${COLORS.grid} 1px, transparent 1px), linear-gradient(90deg, ${COLORS.grid} 1px, transparent 1px)`,
          backgroundSize: '54px 54px',
          maskImage: 'linear-gradient(to bottom, black, transparent 88%)',
        }}
      />
      <div style={{position: 'absolute', width: 620, height: 620, borderRadius: '50%', left: 230, top: 260, background: `radial-gradient(circle, rgba(94,234,212,${0.08 + pulse * 0.04}) 0%, transparent 68%)`}} />

      <div style={{position: 'absolute', top: 64, left: 76, right: 76, textAlign: 'center'}}>
        <div style={{fontSize: 54, fontWeight: 820, letterSpacing: -2.2, lineHeight: 1.05, opacity: titleIn, transform: rise(titleIn, 24)}}>{title}</div>
        <div style={{marginTop: 15, fontSize: 24, color: COLORS.muted, opacity: subtitleIn, transform: rise(subtitleIn, 12)}}>{subtitle}</div>
      </div>

      <div style={{position: 'absolute', top: 275, left: 90, right: 90, height: 150}}>
        <div style={{position: 'absolute', top: -25, left: 0, right: 0, textAlign: 'center', fontSize: 18, fontWeight: 700, letterSpacing: 2.4, textTransform: 'uppercase', color: COLORS.accentWarm, opacity: chaosLabelIn}}>Your day-to-day AI coding work</div>
        <CodeCard title="Fix a bug" x={80} y={28} rotate={-5} delay={38} width={265} tone="cool" />
        <CodeCard title="Build a feature" x={316} y={17} rotate={3} delay={48} width={280} tone="warm" />
        <CodeCard title="Review changes" x={565} y={30} rotate={-2} delay={58} width={245} tone="cool" />
      </div>

      <div style={{position: 'absolute', top: 348, left: 70, right: 70, opacity: flowIn}}>
        <div style={{textAlign: 'center', marginBottom: 28, fontSize: 18, fontWeight: 700, letterSpacing: 2.4, textTransform: 'uppercase', color: COLORS.accent}}>One repeatable engineering habit</div>
        <div style={{display: 'flex', alignItems: 'flex-start', justifyContent: 'center'}}>
          {steps.map((step, index) => (
            <React.Fragment key={step.label}>
              <FlowStep {...step} index={index} start={134} />
              {index < steps.length - 1 ? <Connector index={index} start={134} /> : null}
            </React.Fragment>
          ))}
        </div>
      </div>

      <div
        style={{
          position: 'absolute',
          left: 115,
          right: 115,
          top: 646,
          height: 232,
          padding: '32px 42px',
          borderRadius: 30,
          background: 'linear-gradient(135deg, rgba(19,37,58,0.98), rgba(10,30,43,0.98))',
          border: '1px solid rgba(94,234,212,0.22)',
          boxShadow: '0 28px 80px rgba(0,0,0,0.28)',
          opacity: resultIn,
          transform: `${rise(resultIn, 35)} scale(${0.97 + resultIn * 0.03})`,
        }}
      >
        <div style={{fontSize: 24, fontWeight: 800, color: COLORS.accent, marginBottom: 24}}>Every task leaves the codebase stronger</div>
        <div style={{display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '18px 28px'}}>
          <ResultPill label="Cleaner changes" delay={282} />
          <ResultPill label="Fewer missed edges" delay={294} />
          <ResultPill label="Review-ready evidence" delay={306} />
          <ResultPill label="Context for the next task" delay={318} />
        </div>
      </div>

      <div style={{position: 'absolute', left: 80, right: 80, bottom: 62, display: 'flex', justifyContent: 'space-between', alignItems: 'flex-end', opacity: brandIn}}>
        <div>
          <div style={{fontSize: 29, fontWeight: 820, letterSpacing: -0.6}}>Production Engineering Loop</div>
          <div style={{marginTop: 7, fontSize: 18, color: COLORS.muted}}>Install once. Use it on your next meaningful change.</div>
        </div>
        <div style={{fontSize: 14, fontFamily: 'ui-monospace, SFMono-Regular, Menlo, monospace', color: COLORS.accentBlue, textAlign: 'right', maxWidth: 455, padding: '10px 14px', borderRadius: 12, border: '1px solid rgba(96,165,250,0.25)', background: 'rgba(96,165,250,0.07)'}}>{installCommand}</div>
      </div>
    </AbsoluteFill>
  );
};
