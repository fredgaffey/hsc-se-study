/* SEN Offline — progress sync.
   Local-first: scores are written to localStorage immediately so the app keeps
   working offline. Sync pushes them to D1 under the signed-in account; the
   server derives which bucket to use from the session cookie, so no key is
   ever held or sent by the client. */
(function (w) {
  var SCORES = 'sen_scores', STATUS = 'sen_syncstatus', WHO = 'sen_user';

  function read(k, d) { try { return JSON.parse(localStorage.getItem(k)) || d; } catch (e) { return d; } }
  function write(k, v) { try { localStorage.setItem(k, JSON.stringify(v)); } catch (e) {} }
  function status() { return read(STATUS, { at: null, ok: null, msg: 'not synced yet' }); }
  function setStatus(ok, msg) { var s = { at: new Date().toISOString(), ok: ok, msg: msg }; write(STATUS, s); return s; }

  async function me() {
    try {
      var r = await fetch('/api/auth/me', { credentials: 'same-origin' });
      if (!r.ok) return null;
      var d = await r.json();
      write(WHO, d.user || null);
      return d.user || null;
    } catch (e) { return read(WHO, null); }
  }

  async function sync() {
    if (!navigator.onLine) return setStatus(null, 'offline — will sync when back online');
    try {
      var r = await fetch('/api/sync', {
        method: 'POST', credentials: 'same-origin',
        headers: { 'content-type': 'application/json' },
        body: JSON.stringify({ scores: read(SCORES, {}) })
      });
      if (r.status === 401) return setStatus(false, 'signed out — sign in to sync');
      if (!r.ok) return setStatus(false, 'sync failed (' + r.status + ')');
      var d = await r.json();
      if (d && d.scores) {
        write(SCORES, d.scores);
        w.dispatchEvent(new CustomEvent('sen-scores-updated', { detail: d.scores }));
      }
      return setStatus(true, 'synced ' + Object.keys((d && d.scores) || {}).length + ' topics');
    } catch (e) { return setStatus(false, 'sync failed — ' + e.message); }
  }

  async function pull() {
    try {
      var r = await fetch('/api/sync', { credentials: 'same-origin' });
      if (!r.ok) return setStatus(false, 'pull failed (' + r.status + ')');
      var d = await r.json();
      write(SCORES, d.scores || {});
      w.dispatchEvent(new CustomEvent('sen-scores-updated', { detail: d.scores || {} }));
      return setStatus(true, 'pulled ' + Object.keys(d.scores || {}).length + ' topics');
    } catch (e) { return setStatus(false, 'pull failed — ' + e.message); }
  }

  async function logout() {
    try { await fetch('/api/auth/logout', { method: 'POST', credentials: 'same-origin' }); } catch (e) {}
    // a different account must not inherit this device's scores
    try { localStorage.removeItem(SCORES); localStorage.removeItem(STATUS); localStorage.removeItem(WHO); } catch (e) {}
    location.href = '/login.html';
  }

  w.SENSync = { sync: sync, pull: pull, me: me, logout: logout, status: status };

  function auto() { sync(); }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', function () { setTimeout(auto, 1200); });
  else setTimeout(auto, 1200);
  w.addEventListener('online', auto);
})(window);
