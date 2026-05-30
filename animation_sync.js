// Add ticker animation
const style = document.createElement('style');
style.textContent = `
  .ticker-content {
    animation: scrollText 20s linear infinite;
  }
  
  @keyframes scrollText {
    0% { transform: translateX(100vw); }
    100% { transform: translateX(-100vw); }
  }
`;
document.head.appendChild(style);

// Server sync for OBS
const isOBS = new URLSearchParams(window.location.search).get('obs') === '1';
if (isOBS) {
  console.log('[OBS] Fetching server config every 2s');
  setInterval(() => {
    fetch('/api/config')
      .then(r => r.json())
      .then(config => {
        if (config && Object.keys(config).length > 0) {
          Object.keys(config).forEach(key => {
            const el = document.getElementById(key);
            if (el) {
              if (el.type === 'checkbox') el.checked = config[key];
              else el.value = config[key];
              el.dispatchEvent(new Event('change'));
            }
          });
        }
      })
      .catch(() => {});
  }, 2000);
}

console.log('[Ready] Frame ready - OBS:', isOBS);
