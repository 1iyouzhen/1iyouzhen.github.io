(() => {
  const script = document.currentScript;
  const manifestUrl = script && script.dataset.deploymentUrl;
  const revision = document.querySelector('meta[name="blog-revision"]')?.content;
  const builtAt = Date.parse(document.querySelector('meta[name="blog-built-at"]')?.content || '');
  const button = document.getElementById('check-site-update');
  const status = document.getElementById('site-update-status');
  if (!manifestUrl || !revision || !button || !status) return;
  let checking = false;
  let lastCheck = 0;
  const revisionPattern = /^[a-f0-9]{40}$/;
  const setStatus = text => { status.textContent = text; };

  // The versioned URL bypasses a previously cached HTML response. Keep the
  // query until navigation so a manual reload continues to use this release.
  function loadRelease(nextRevision, force = false) {
    const url = new URL(location.href);
    url.searchParams.set('_release', nextRevision);
    if (force) url.searchParams.set('_refresh', Date.now().toString());
    location.replace(url.href);
  }

  async function checkForUpdate(manual = false) {
    if (checking || document.visibilityState === 'hidden') return;
    if (!manual && (revision === 'local' || Date.now() - lastCheck < 30000)) return;
    checking = true;
    lastCheck = Date.now();
    if (manual) { button.disabled = true; setStatus('正在检查…'); }
    try {
      const url = new URL(manifestUrl, location.origin);
      url.searchParams.set('_check', Date.now().toString());
      const response = await fetch(url.href, {cache: 'no-store', credentials: 'same-origin', signal: AbortSignal.timeout(10000)});
      if (!response.ok) throw new Error('Version check failed');
      const release = await response.json();
      if (!revisionPattern.test(release.revision)) {
        if (manual) setStatus('本地预览不检查线上版本');
        return;
      }
      const newer = release.revision !== revision && Date.parse(release.builtAt) >= builtAt;
      if (newer) {
        const active = document.activeElement;
        const typing = active && (active.matches('input, textarea, [contenteditable="true"]'));
        const selecting = String(window.getSelection() || '').length > 0;
        if (!manual && (typing || selecting)) { setStatus('有新版本，点击“检查更新”加载'); return; }
        const currentUrl = new URL(location.href);
        if (!manual && currentUrl.searchParams.get('_release') === release.revision) {
          setStatus('新版本正在同步，可稍后点击“检查更新”');
          return;
        }
        setStatus('发现新版本，正在更新…');
        loadRelease(release.revision, manual);
      } else if (manual) {
        // Also refresh the current HTML and search index when the release
        // manifest has reached the edge before another page has propagated.
        setStatus('正在重新加载最新页面…');
        loadRelease(release.revision, true);
      }
    } catch (error) {
      if (manual) setStatus('暂时无法检查，请稍后再试');
    } finally {
      checking = false;
      button.disabled = false;
    }
  }
  button.addEventListener('click', () => checkForUpdate(true));
  document.addEventListener('visibilitychange', () => { if (!document.hidden) checkForUpdate(); });
  window.addEventListener('pageshow', () => checkForUpdate());
  setTimeout(() => checkForUpdate(), 1000);
  setInterval(() => checkForUpdate(), 60000);
})();
