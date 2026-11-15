(() => {
  document.querySelectorAll('[data-language-dropdown]').forEach(dropdown => {
    const button = dropdown.querySelector('.language-toggle');
    const options = dropdown.querySelector('.language-options');
    const links = [...options.querySelectorAll('a')];
    const isOpen = () => button.getAttribute('aria-expanded') === 'true';
    const close = (restoreFocus = false) => {
      button.setAttribute('aria-expanded', 'false');
      options.hidden = true;
      if (restoreFocus) button.focus();
    };
    const open = (focus = false) => {
      button.setAttribute('aria-expanded', 'true');
      options.hidden = false;
      if (focus) (options.querySelector('[aria-current]') || links[0]).focus();
    };
    button.addEventListener('click', () => isOpen() ? close() : open());
    button.addEventListener('keydown', event => {
      if (event.key === 'ArrowDown' || event.key === 'ArrowUp') {
        event.preventDefault();
        open(true);
      }
    });
    dropdown.addEventListener('keydown', event => {
      if (event.key === 'Escape' && isOpen()) {
        event.preventDefault();
        close(true);
      }
      if (event.target.closest('.language-options') && ['ArrowDown', 'ArrowUp', 'Home', 'End'].includes(event.key)) {
        event.preventDefault();
        const current = links.indexOf(document.activeElement);
        let next = event.key === 'ArrowUp' ? (current - 1 + links.length) % links.length : (current + 1) % links.length;
        if (event.key === 'Home') next = 0;
        if (event.key === 'End') next = links.length - 1;
        links[next].focus();
      }
    });
    document.addEventListener('click', event => { if (!dropdown.contains(event.target)) close(); });
    dropdown.addEventListener('focusout', () => {
      setTimeout(() => { if (!dropdown.contains(document.activeElement)) close(); }, 0);
    });
    links.forEach(link => link.addEventListener('click', () => close()));
  });
})();
