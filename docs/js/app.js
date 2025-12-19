(function(){
  const statusEl = document.getElementById('status');
  const downloadBtn = document.getElementById('download-btn');
  const checkBtn = document.getElementById('check-btn');
  const releasesLink = document.getElementById('releases-link');

  // Candidate installer locations (checked in order)
  const candidates = [
    '/NoiseStudio_Installer.exe',
    '/dist/NoiseStudio.exe',
    '/dist/NoiseStudio_Installer.exe',
    '/NoiseStudio.exe',
    'https://github.com/blobbyofficial/noise-studio/releases/latest'
  ];

  let resolvedUrl = null;

  async function checkUrl(url){
    try{
      // Try HEAD first to be polite
      let res = await fetch(url, {method:'HEAD'});
      if(res && res.ok) return url;
      // Some servers don't support HEAD — try GET but don't download fully
      res = await fetch(url, {method:'GET'});
      if(res && res.ok) return url;
    }catch(e){
      // ignore
    }
    return null;
  }

  async function findInstaller(){
    statusEl.textContent = 'Checking for installer...';
    for(const url of candidates){
      const ok = await checkUrl(url);
      if(ok){
        resolvedUrl = ok;
        statusEl.innerHTML = `Installer available: <code>${ok}</code>`;
        releasesLink.href = ok.includes('github.com') ? ok : (ok.startsWith('/') ? ok : ok);
        return ok;
      }
    }
    resolvedUrl = candidates[candidates.length-1];
    statusEl.innerHTML = `Installer not found on this host. <a href="${resolvedUrl}" target="_blank">Open Releases page</a>`;
    releasesLink.href = resolvedUrl;
    return null;
  }

  async function doDownload(){
    if(!resolvedUrl){
      await findInstaller();
    }
    if(!resolvedUrl) return;

    // If resolvedUrl is a GitHub releases page, open it in new tab
    if(resolvedUrl.includes('github.com') && !resolvedUrl.endsWith('.exe')){
      window.open(resolvedUrl, '_blank');
      return;
    }

    try{
      statusEl.textContent = 'Starting download...';
      const res = await fetch(resolvedUrl);
      if(!res.ok){
        statusEl.textContent = 'Download failed — opening releases page';
        window.open('https://github.com/blobbyofficial/noise-studio/releases/latest','_blank');
        return;
      }
      const blob = await res.blob();
      const a = document.createElement('a');
      const url = window.URL.createObjectURL(blob);
      a.href = url;
      a.download = resolvedUrl.split('/').pop();
      document.body.appendChild(a);
      a.click();
      a.remove();
      window.URL.revokeObjectURL(url);
      statusEl.textContent = 'Download started. Check your Downloads folder.';
    }catch(e){
      statusEl.textContent = 'Download failed; opening Releases page';
      window.open('https://github.com/blobbyofficial/noise-studio/releases/latest','_blank');
    }
  }

  downloadBtn.addEventListener('click', (e)=>{ e.preventDefault(); doDownload(); });
  checkBtn.addEventListener('click', (e)=>{ e.preventDefault(); findInstaller(); });

  // Run initial check
  findInstaller();
})();