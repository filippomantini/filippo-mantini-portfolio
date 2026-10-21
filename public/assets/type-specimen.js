(() => {
  const profiles = {
    CDCDisplay: { characters: "ABCDEFGHILMNOPQRSTUVZ ,.'\n", uppercase: true },
    NoFontDisplay: { characters: 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789ÀÅÉÎÕàåéî !$&(),.?£€\n', uppercase: false }
  };
  for (const section of document.querySelectorAll('[data-type-tester]')) {
    const family = section.getAttribute('data-type-font') || 'CDCDisplay';
    const profile = profiles[family];
    if (!profile) continue;
    const input = section.querySelector('textarea');
    const size = section.querySelector('input[type=range]');
    const preview = section.querySelector('[data-type-preview]');
    const status = section.querySelector('[data-type-status]');
    const it = document.documentElement.lang === 'it';
    const supported = new Set(profile.characters);
    let ready = false;
    const update = () => {
      const value = profile.uppercase ? input.value.toUpperCase() : input.value;
      const missing = [...new Set([...value].filter(c => !supported.has(c)))];
      preview.textContent = [...value].map(c => supported.has(c) ? c : '□').join('');
      preview.style.setProperty('--type-size', size.value + 'px');
      if (ready) status.textContent = missing.length
        ? (it ? 'Caratteri non disponibili: ' : 'Unavailable characters: ') + missing.join(' ')
        : profile.uppercase ? (it ? 'Anteprima in maiuscolo.' : 'Uppercase preview.')
        : (it ? 'Anteprima con i caratteri originali.' : 'Preview using the original letterforms.');
    };
    input.addEventListener('input', update);
    size.addEventListener('input', update);
    update();
    document.fonts.load('48px ' + family).then(fonts => {
      if (!fonts.length) throw new Error('font');
      ready = true;
      preview.hidden = false;
      update();
    }).catch(() => {
      status.textContent = it
        ? 'Anteprima non disponibile. Puoi vedere l’alfabeto nelle tavole del progetto.'
        : 'Preview unavailable. The original alphabet is shown in the project boards.';
    });
  }
})();
