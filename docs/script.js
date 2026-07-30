(() => {
  const reducedMotionQuery = window.matchMedia('(prefers-reduced-motion: reduce)');
  let reducedMotion = reducedMotionQuery.matches;
  reducedMotionQuery.addEventListener?.('change', (event) => {
    reducedMotion = event.matches;
  });
  const pageIsVisible = () => document.visibilityState === 'visible';

  const rig = document.querySelector('[data-rig]');
  if (rig) {
    const tabs = [...rig.querySelectorAll('[data-rig-tab]')];
    const panels = [...rig.querySelectorAll('[data-rig-panel]')];
    const progress = rig.querySelector('[data-rig-progress]');
    const count = rig.querySelector('[data-rig-count]');
    const previous = rig.querySelector('[data-rig-prev]');
    const next = rig.querySelector('[data-rig-next]');
    let current = 0;
    let timer = null;
    let rigVisible = !('IntersectionObserver' in window);
    let pointerPaused = false;
    let focusPaused = false;

    const show = (index, focusTab = false, animate = true) => {
      current = (index + tabs.length) % tabs.length;

      tabs.forEach((tab, tabIndex) => {
        const active = tabIndex === current;
        tab.setAttribute('aria-selected', String(active));
        tab.tabIndex = active ? 0 : -1;
        if (active && focusTab) tab.focus();
      });

      panels.forEach((panel, panelIndex) => {
        panel.classList.remove('rig-enter');
        const active = panelIndex === current;
        panel.hidden = !active;
        panel.classList.toggle('is-active', active);
        if (active && animate && !reducedMotion) {
          void panel.offsetWidth;
          panel.classList.add('rig-enter');
        }
      });

      progress.style.width = `${((current + 1) / tabs.length) * 100}%`;
      count.textContent = `${String(current + 1).padStart(2, '0')} / ${String(tabs.length).padStart(2, '0')}`;
    };

    const stop = () => {
      if (timer) window.clearInterval(timer);
      timer = null;
    };

    const canAutoplay = () => (
      !reducedMotion
      && rigVisible
      && pageIsVisible()
      && !pointerPaused
      && !focusPaused
    );

    const start = () => {
      if (!canAutoplay() || timer) return;
      timer = window.setInterval(() => show(current + 1), 6500);
    };

    tabs.forEach((tab, index) => {
      tab.addEventListener('click', () => {
        stop();
        show(index);
      });
      tab.addEventListener('keydown', (event) => {
        if (event.key === 'ArrowRight') {
          event.preventDefault();
          stop();
          show(current + 1, true);
        }
        if (event.key === 'ArrowLeft') {
          event.preventDefault();
          stop();
          show(current - 1, true);
        }
      });
    });

    previous?.addEventListener('click', () => {
      stop();
      show(current - 1);
    });
    next?.addEventListener('click', () => {
      stop();
      show(current + 1);
    });

    rig.addEventListener('mouseenter', () => {
      pointerPaused = true;
      stop();
    });
    rig.addEventListener('mouseleave', () => {
      pointerPaused = false;
      start();
    });
    rig.addEventListener('focusin', () => {
      focusPaused = true;
      stop();
    });
    rig.addEventListener('focusout', (event) => {
      if (!rig.contains(event.relatedTarget)) {
        focusPaused = false;
        start();
      }
    });

    if ('IntersectionObserver' in window) {
      const rigObserver = new IntersectionObserver(([entry]) => {
        rigVisible = entry.isIntersecting && entry.intersectionRatio >= 0.25;
        if (rigVisible) start();
        else stop();
      }, { threshold: [0, 0.25, 0.6] });
      rigObserver.observe(rig);
    }

    document.addEventListener('visibilitychange', () => {
      if (pageIsVisible()) start();
      else stop();
    });

    reducedMotionQuery.addEventListener?.('change', () => {
      if (reducedMotion) stop();
      else start();
    });

    show(0, false, false);
    start();
  }

  const sequence = document.querySelector('.sequence');
  if (sequence) {
    let sequenceVisible = !('IntersectionObserver' in window);
    let sequencePlayed = false;
    let sequenceTimer = null;

    const resetSequence = (allowReplay = false) => {
      if (sequenceTimer) window.clearTimeout(sequenceTimer);
      sequenceTimer = null;
      sequence.classList.remove('is-tracing');
      if (allowReplay) sequencePlayed = false;
    };

    const playSequence = () => {
      if (reducedMotion || sequencePlayed || !sequenceVisible || !pageIsVisible()) return;
      sequencePlayed = true;
      sequence.classList.remove('is-tracing');
      void sequence.offsetWidth;
      sequence.classList.add('is-tracing');
      sequenceTimer = window.setTimeout(() => {
        sequence.classList.remove('is-tracing');
        sequence.classList.add('has-traced');
        sequenceTimer = null;
      }, 3800);
    };

    if ('IntersectionObserver' in window) {
      const sequenceObserver = new IntersectionObserver(([entry]) => {
        sequenceVisible = entry.isIntersecting && entry.intersectionRatio >= 0.35;
        if (sequenceVisible) playSequence();
        else if (sequence.classList.contains('is-tracing')) resetSequence(true);
      }, { threshold: [0, 0.35, 0.7] });
      sequenceObserver.observe(sequence);
    } else {
      playSequence();
    }

    document.addEventListener('visibilitychange', () => {
      if (!pageIsVisible() && sequence.classList.contains('is-tracing')) {
        resetSequence(true);
      } else if (pageIsVisible()) {
        playSequence();
      }
    });

    reducedMotionQuery.addEventListener?.('change', () => {
      if (reducedMotion) resetSequence(true);
      else playSequence();
    });
  }

  const install = document.querySelector('[data-install]');
  if (install) {
    const tabs = [...install.querySelectorAll('[data-install-tab]')];
    const panels = [...install.querySelectorAll('[data-install-panel]')];

    const showInstall = (name, focusTab = false) => {
      tabs.forEach((tab) => {
        const active = tab.dataset.installTab === name;
        tab.setAttribute('aria-selected', String(active));
        tab.tabIndex = active ? 0 : -1;
        if (active && focusTab) tab.focus();
      });
      panels.forEach((panel) => {
        panel.hidden = panel.dataset.installPanel !== name;
      });
    };

    tabs.forEach((tab, index) => {
      tab.addEventListener('click', () => showInstall(tab.dataset.installTab));
      tab.addEventListener('keydown', (event) => {
        if (event.key !== 'ArrowRight' && event.key !== 'ArrowLeft') return;
        event.preventDefault();
        const offset = event.key === 'ArrowRight' ? 1 : -1;
        const nextIndex = (index + offset + tabs.length) % tabs.length;
        showInstall(tabs[nextIndex].dataset.installTab, true);
      });
    });
  }

  document.querySelectorAll('[data-copy]').forEach((button) => {
    button.addEventListener('click', async () => {
      const target = document.querySelector(button.dataset.copy);
      if (!target) return;
      const text = target.textContent.trim();
      const original = button.textContent;

      try {
        await navigator.clipboard.writeText(text);
        button.textContent = 'Copied';
      } catch {
        const selection = window.getSelection();
        const range = document.createRange();
        range.selectNodeContents(target);
        selection.removeAllRanges();
        selection.addRange(range);
        button.textContent = 'Select + copy';
      }

      window.setTimeout(() => {
        button.textContent = original;
      }, 1800);
    });
  });
})();
