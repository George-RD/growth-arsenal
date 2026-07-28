(() => {
  const rig = document.querySelector('[data-rig]');
  const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  if (rig) {
    const tabs = [...rig.querySelectorAll('[data-rig-tab]')];
    const panels = [...rig.querySelectorAll('[data-rig-panel]')];
    const progress = rig.querySelector('[data-rig-progress]');
    const count = rig.querySelector('[data-rig-count]');
    const previous = rig.querySelector('[data-rig-prev]');
    const next = rig.querySelector('[data-rig-next]');
    let current = 0;
    let timer = null;

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
        if (active && animate) {
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

    const start = () => {
      if (reducedMotion || timer) return;
      timer = window.setInterval(() => show(current + 1), 5200);
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

    rig.addEventListener('mouseenter', stop);
    rig.addEventListener('mouseleave', start);
    rig.addEventListener('focusin', stop);
    rig.addEventListener('focusout', (event) => {
      if (!rig.contains(event.relatedTarget)) start();
    });

    show(0, false, false);
    start();
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
