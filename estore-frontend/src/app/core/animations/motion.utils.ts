import { gsap } from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';

gsap.registerPlugin(ScrollTrigger);

/**
 * Reusable motion vocabulary for the cinematic landing page.
 * Every helper returns the GSAP instance(s) so callers can compose timelines.
 */

/** Split a text node into word- and line-wrapped spans for staggered reveals. */
export function splitText(el: HTMLElement): { words: HTMLSpanElement[]; lines: HTMLSpanElement[] } {
  if (el.dataset['splitDone'] === 'true') {
    return {
      words: Array.from(el.querySelectorAll<HTMLSpanElement>('.word')),
      lines: Array.from(el.querySelectorAll<HTMLSpanElement>('.line .inner'))
    };
  }
  const raw = el.textContent ?? '';
  el.textContent = '';
  const words = raw.split(/\s+/).filter(Boolean);
  const wordSpans: HTMLSpanElement[] = [];

  words.forEach((w, i) => {
    const wordWrap = document.createElement('span');
    wordWrap.className = 'line';
    wordWrap.style.display = 'inline-block';
    wordWrap.style.overflow = 'hidden';
    wordWrap.style.verticalAlign = 'top';

    const inner = document.createElement('span');
    inner.className = 'inner';
    inner.style.display = 'inline-block';
    inner.style.transform = 'translateY(110%)';
    inner.style.willChange = 'transform';
    inner.textContent = w;

    const space = document.createElement('span');
    space.textContent = i < words.length - 1 ? ' ' : '';
    space.style.display = 'inline-block';

    wordWrap.appendChild(inner);
    el.appendChild(wordWrap);
    el.appendChild(space);
    wordSpans.push(inner);
  });

  el.dataset['splitDone'] = 'true';
  return { words: wordSpans, lines: wordSpans };
}

/** Reveal text by sliding each word up from below its own clip. */
export function revealSplit(el: HTMLElement, opts: { delay?: number; stagger?: number; duration?: number; trigger?: Element | null } = {}): gsap.core.Tween {
  const { words } = splitText(el);
  return gsap.to(words, {
    y: '0%',
    duration: opts.duration ?? 1.05,
    ease: 'expo.out',
    stagger: opts.stagger ?? 0.045,
    delay: opts.delay ?? 0,
    scrollTrigger: opts.trigger
      ? { trigger: opts.trigger, start: 'top 80%', toggleActions: 'play none none reverse' }
      : undefined
  });
}

/** Soft rise-in for a single element on scroll. */
export function revealRise(el: Element, opts: { delay?: number; y?: number; duration?: number } = {}): gsap.core.Tween {
  return gsap.fromTo(
    el,
    { autoAlpha: 0, y: opts.y ?? 28 },
    {
      autoAlpha: 1,
      y: 0,
      duration: opts.duration ?? 1.1,
      ease: 'expo.out',
      delay: opts.delay ?? 0,
      scrollTrigger: { trigger: el, start: 'top 85%', toggleActions: 'play none none reverse' }
    }
  );
}

/** Staggered cascade for a NodeList / array of elements. */
export function revealStagger(els: ArrayLike<Element> | Element[], opts: { trigger?: Element; stagger?: number; y?: number } = {}): gsap.core.Tween {
  return gsap.fromTo(
    els,
    { autoAlpha: 0, y: opts.y ?? 36 },
    {
      autoAlpha: 1,
      y: 0,
      duration: 1.1,
      ease: 'expo.out',
      stagger: opts.stagger ?? 0.08,
      scrollTrigger: {
        trigger: opts.trigger ?? (els as Element[])[0],
        start: 'top 80%',
        toggleActions: 'play none none reverse'
      }
    }
  );
}

/** Animated number counter triggered when in view. */
export function animateCounter(el: HTMLElement, end: number, opts: { duration?: number; suffix?: string; prefix?: string; decimals?: number } = {}): gsap.core.Tween {
  const obj = { val: 0 };
  return gsap.to(obj, {
    val: end,
    duration: opts.duration ?? 2,
    ease: 'expo.out',
    onUpdate: () => {
      const n = opts.decimals ? obj.val.toFixed(opts.decimals) : Math.round(obj.val).toLocaleString();
      el.textContent = `${opts.prefix ?? ''}${n}${opts.suffix ?? ''}`;
    },
    scrollTrigger: { trigger: el, start: 'top 85%', toggleActions: 'play none none reset' }
  });
}

/** Magnetic hover — moves an element subtly toward the cursor. */
export function magnetize(el: HTMLElement, strength = 0.25): () => void {
  const onMove = (e: MouseEvent) => {
    const rect = el.getBoundingClientRect();
    const x = e.clientX - (rect.left + rect.width / 2);
    const y = e.clientY - (rect.top + rect.height / 2);
    gsap.to(el, { x: x * strength, y: y * strength, duration: 0.6, ease: 'power3.out' });
  };
  const onLeave = () => gsap.to(el, { x: 0, y: 0, duration: 0.8, ease: 'elastic.out(1, 0.5)' });
  el.addEventListener('mousemove', onMove);
  el.addEventListener('mouseleave', onLeave);
  return () => {
    el.removeEventListener('mousemove', onMove);
    el.removeEventListener('mouseleave', onLeave);
  };
}

/** Parallax scroll for decorative layers. */
export function parallax(el: Element, distance = 80): gsap.core.Tween {
  return gsap.to(el, {
    yPercent: distance > 0 ? -distance : Math.abs(distance),
    ease: 'none',
    scrollTrigger: { trigger: el, start: 'top bottom', end: 'bottom top', scrub: 0.6 }
  });
}
