(function(){
  const prefersDark = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;
  const theme = localStorage.getItem('theme') || (prefersDark ? 'dark' : 'dark');
  document.documentElement.dataset.theme = theme;

  function toggleTheme(){
    const t = document.documentElement.dataset.theme === 'dark' ? 'light' : 'dark';
    document.documentElement.dataset.theme = t;
    localStorage.setItem('theme', t);
  }

  const btn = document.createElement('button');
  btn.textContent = 'Changer de thème';
  btn.style.position = 'fixed';
  btn.style.bottom = '18px';
  btn.style.right = '18px';
  btn.style.padding = '10px 12px';
  btn.style.borderRadius = '10px';
  btn.style.border = '1px solid rgba(255,255,255,.15)';
  btn.style.background = 'rgba(17,24,39,.7)';
  btn.style.color = '#e5e7eb';
  btn.addEventListener('click', toggleTheme);
  document.addEventListener('DOMContentLoaded', () => document.body.appendChild(btn));
})();