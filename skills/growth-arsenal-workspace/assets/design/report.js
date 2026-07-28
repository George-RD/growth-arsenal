(() => {
  const printButton = document.querySelector('[data-print]');
  printButton?.addEventListener('click', () => window.print());
})();
