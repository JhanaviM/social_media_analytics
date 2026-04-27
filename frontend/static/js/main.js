/* ═══════════════════════════════════════════════
   SMA Platform — Global JS Utilities
   ═══════════════════════════════════════════════ */

// ── Loading Overlay ──────────────────────────────────────
function showLoading(text = 'Running analysis...') {
  const overlay = document.getElementById('loadingOverlay');
  const txt = document.getElementById('loadingText');
  if (overlay) {
    overlay.classList.remove('d-none');
    if (txt) txt.textContent = text;
  }
}

function hideLoading() {
  const overlay = document.getElementById('loadingOverlay');
  if (overlay) overlay.classList.add('d-none');
}

// ── Run a single module ──────────────────────────────────
// Called by each tab's "Run Analysis" button
async function runModule(moduleName, caseId) {
  showLoading(`Running ${moduleName} analysis... please wait`);

  try {
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), 60000); // 60 sec

    const resp = await fetch(`/api/${moduleName}/${caseId}`, {
      method: 'POST',
      signal: controller.signal
    });
    clearTimeout(timeoutId);

    if (!resp.ok) {
      const text = await resp.text();
      alert(`Server error (${resp.status}): ` + text.slice(0, 200));
      return;
    }

    const data = await resp.json();
    if (data.error) {
      alert('Module error: ' + data.error);
      return;
    }

    // Success — reload page to show results
    window.location.reload();

  } catch (e) {
    if (e.name === 'AbortError') {
      alert(`${moduleName} timed out after 60 seconds. The server may still be processing — try refreshing the page.`);
    } else {
      alert('Request failed: ' + e.message);
    }
  } finally {
    hideLoading();
  }
}

// ── Run all 12 modules at once ───────────────────────────
// Has a 90 second timeout. If it times out, user can
// still run each tab individually with the Run Analysis button.
async function runAllModules(caseId) {
  showLoading('Running all 12 modules... please wait up to 60 seconds');

  try {
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), 90000); // 90 sec

    const resp = await fetch(`/api/run-all/${caseId}`, {
      method: 'POST',
      signal: controller.signal
    });
    clearTimeout(timeoutId);

    if (!resp.ok) {
      const text = await resp.text();
      alert(`Server error (${resp.status}): ` + text.slice(0, 200));
      return;
    }

    const data = await resp.json();

    if (data.error) {
      alert('Error: ' + data.error);
      return;
    }

    // Log any modules that had issues (non-blocking)
    if (data.modules) {
      const failed = Object.entries(data.modules)
        .filter(([, v]) => v !== 'ok')
        .map(([k, v]) => `${k}: ${v}`);
      if (failed.length > 0) {
        console.warn('Some modules had issues:', failed);
      }
    }

    // Reload to display all results
    window.location.reload();

  } catch (e) {
    if (e.name === 'AbortError') {
      alert(
        'Request timed out after 90 seconds.\n\n' +
        'The server may still be working. Try refreshing the page in 30 seconds.\n\n' +
        'Or use the "Run Analysis" button on each individual tab — that always works.'
      );
    } else {
      alert('Request failed: ' + e.message);
    }
  } finally {
    hideLoading();
  }
}

// ── Collect data via Apify ───────────────────────────────
async function collectData(caseId) {
  showLoading('Collecting data from Apify... this may take 30-60 seconds');

  try {
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), 120000); // 2 min for Apify

    const resp = await fetch(`/api/collect/${caseId}`, {
      method: 'POST',
      signal: controller.signal
    });
    clearTimeout(timeoutId);

    if (!resp.ok) {
      const text = await resp.text();
      alert(`Server error: ` + text.slice(0, 200));
      return;
    }

    const data = await resp.json();
    if (data.error) {
      alert('Collection error: ' + data.error);
      return;
    }

    alert(`Successfully collected ${data.count} posts!`);
    window.location.reload();

  } catch (e) {
    if (e.name === 'AbortError') {
      alert('Apify collection timed out. Try again or use Load Sample Data instead.');
    } else {
      alert('Request failed: ' + e.message);
    }
  } finally {
    hideLoading();
  }
}

// ── Auto-dismiss flash alerts after 4 seconds ────────────
document.addEventListener('DOMContentLoaded', () => {
  setTimeout(() => {
    document.querySelectorAll('.alert').forEach(el => {
      try {
        const bsAlert = bootstrap.Alert.getOrCreateInstance(el);
        if (bsAlert) bsAlert.close();
      } catch (_) {}
    });
  }, 4000);
});
