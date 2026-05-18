import { Injectable, NgZone, OnDestroy } from '@angular/core';
import Lenis from 'lenis';
import { gsap } from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';

gsap.registerPlugin(ScrollTrigger);

/**
 * Global premium smooth-scroll service.
 *
 * Lenis powers the inertial scroll, ScrollTrigger is synced to it so all
 * scrub-based timelines move with the same easing as the page itself.
 * Created lazily on the first request — pages that don't need it pay nothing.
 */
@Injectable({ providedIn: 'root' })
export class LenisService implements OnDestroy {
  private lenis: Lenis | null = null;
  private rafId: number | null = null;

  constructor(private zone: NgZone) {}

  /** Start (or restart) smooth scrolling. Safe to call multiple times. */
  start(): void {
    if (this.lenis) return;
    if (typeof window === 'undefined') return;

    this.zone.runOutsideAngular(() => {
      this.lenis = new Lenis({
        duration: 1.15,
        // cubic-bezier exponential-out feel
        easing: (t: number) => Math.min(1, 1.001 - Math.pow(2, -10 * t)),
        smoothWheel: true,
        wheelMultiplier: 1,
        touchMultiplier: 1.4,
        infinite: false
      });

      // Sync ScrollTrigger to Lenis frames
      this.lenis.on('scroll', ScrollTrigger.update);

      const raf = (time: number) => {
        this.lenis?.raf(time);
        this.rafId = requestAnimationFrame(raf);
      };
      this.rafId = requestAnimationFrame(raf);

      // GSAP ticker -> Lenis (extra safety for scrub timelines)
      gsap.ticker.lagSmoothing(0);
    });
  }

  /** Tear down. Called automatically on app shutdown. */
  stop(): void {
    if (this.rafId != null) cancelAnimationFrame(this.rafId);
    this.lenis?.destroy();
    this.lenis = null;
    this.rafId = null;
  }

  /** Programmatic scroll to a target. */
  scrollTo(target: string | number | HTMLElement, opts?: { offset?: number; duration?: number; immediate?: boolean }): void {
    this.lenis?.scrollTo(target as any, {
      offset: opts?.offset ?? 0,
      duration: opts?.duration ?? 1.2,
      immediate: opts?.immediate ?? false
    });
  }

  ngOnDestroy(): void {
    this.stop();
  }
}
