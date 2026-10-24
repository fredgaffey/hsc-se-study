/* SEN Offline — find bar.
   "/"   find on this page
   "//"  switch to global search (all lessons + questions), popup, stays on page
   Esc   close everything                                                        */
(function(){
  var bar,input,label,chip,panel,marks=[],cur=-1,timer=null,lastSlash=0,global=false,dataP=null;
  var fuzzy=true, wcache={}, wantQ=false;   // questions off by default                       // fuzzy matching is the default
  var SKIP=/^(SCRIPT|STYLE|NOSCRIPT|TEXTAREA|INPUT|SELECT)$/;

  /* ---------- paths (depth-aware) ---------- */
  function depth(){ var p=location.pathname;
    return p.indexOf('/pages/lessons/')>-1?2:(p.indexOf('/pages/')>-1?1:0); }
  function rootPre(){ return ['./','../','../../'][depth()]; }
  function pageHref(f){ return (depth()===0?'pages/':(depth()===2?'../':''))+f; }
  function esc(x){ return String(x).replace(/[&<>]/g,function(c){
    return {'&':'&amp;','<':'&lt;','>':'&gt;'}[c]; }); }

  /* ---------- in-page highlighting ---------- */
  function root(){ return document.querySelector('main')||document.body; }
  function clear(){
    marks.forEach(function(m){ var t=document.createTextNode(m.textContent),p=m.parentNode;
      if(p){ p.replaceChild(t,m); p.normalize(); } });
    marks=[]; cur=-1;
  }
  function highlight(q){
    clear();
    if(!q||q.length<2){ label.textContent=''; return; }
    var rx; try{ rx=new RegExp(q.replace(/[.*+?^${}()|[\]\\]/g,'\\$&'),'gi'); }catch(e){ return; }
    var w=document.createTreeWalker(root(),NodeFilter.SHOW_TEXT,{acceptNode:function(n){
      if(!n.nodeValue.trim()) return NodeFilter.FILTER_REJECT;
      var p=n.parentNode;
      while(p&&p!==document.body){
        if(SKIP.test(p.nodeName)||p.id==='senFindBar'||p.id==='senGlobalPanel') return NodeFilter.FILTER_REJECT;
        p=p.parentNode; }
      return NodeFilter.FILTER_ACCEPT; }});
    var nodes=[],n; while((n=w.nextNode())) nodes.push(n);
    nodes.forEach(function(node){
      var txt=node.nodeValue,m,last=0,frag=null; rx.lastIndex=0;
      while((m=rx.exec(txt))){
        frag=frag||document.createDocumentFragment();
        if(m.index>last) frag.appendChild(document.createTextNode(txt.slice(last,m.index)));
        var mk=document.createElement('mark'); mk.className='sen-find'; mk.textContent=m[0];
        frag.appendChild(mk); marks.push(mk); last=m.index+m[0].length;
        if(!m[0].length) rx.lastIndex++;
      }
      if(frag){ if(last<txt.length) frag.appendChild(document.createTextNode(txt.slice(last)));
        node.parentNode.replaceChild(frag,node); }
    });
    if(marks.length){ cur=-1; step(1); } else label.textContent='no matches';
  }
  function step(d){
    if(!marks.length) return;
    if(cur>-1&&marks[cur]) marks[cur].classList.remove('on');
    cur=(cur+d+marks.length)%marks.length;
    marks[cur].classList.add('on');
    marks[cur].scrollIntoView({block:'center',behavior:'smooth'});
    label.textContent=(cur+1)+' / '+marks.length;
  }

  /* ---------- fuzzy matching (Damerau-Levenshtein: a swap costs 1, not 2) ---------- */
  function lev(a,b){
    if(Math.abs(a.length-b.length)>3) return 9;
    var m=a.length,n=b.length,i,j,d=[];
    for(i=0;i<=m;i++){ d[i]=[i]; }
    for(j=0;j<=n;j++){ d[0][j]=j; }
    for(i=1;i<=m;i++) for(j=1;j<=n;j++){
      var c=a.charAt(i-1)===b.charAt(j-1)?0:1;
      d[i][j]=Math.min(d[i-1][j]+1,d[i][j-1]+1,d[i-1][j-1]+c);
      if(i>1&&j>1&&a.charAt(i-1)===b.charAt(j-2)&&a.charAt(i-2)===b.charAt(j-1))
        d[i][j]=Math.min(d[i][j],d[i-2][j-2]+1);
    }
    return d[m][n];
  }
  function thr(l){ return l<=3?0:(l<=5?1:(l<=8?2:3)); }
  function words(hay,key){
    if(wcache[key]) return wcache[key];
    var seen={},list=[],m,rx=/[a-z0-9]{3,}/g;
    while((m=rx.exec(hay))){ if(!seen[m[0]]){ seen[m[0]]=1; list.push(m[0]); } }
    return (wcache[key]=list);
  }
  /* returns match index, or -1 */
  function findIn(hay,t,key){
    var i=hay.indexOf(t);
    if(i>=0) return i;
    if(!fuzzy) return -1;
    var lim=thr(t.length), ws=words(hay,key), pre=t.slice(0,Math.min(4,t.length));
    for(var k=0;k<ws.length;k++){
      var w=ws[k];
      if((w.length>=t.length-1&&w.indexOf(pre)===0)||lev(t,w)<=lim) return hay.indexOf(w);
    }
    return -1;
  }

  /* ---------- global search ---------- */
  function loadData(){
    if(dataP) return dataP;
    dataP=new Promise(function(res){
      var need=[]; if(!window.PAGES) need.push('data/pages.js');
      if(!window.QB) need.push('data/questions.js');
      if(!need.length) return res();
      var left=need.length;
      need.forEach(function(u){ var s=document.createElement('script');
        s.src=rootPre()+u; s.onload=s.onerror=function(){ if(!--left) res(); };
        document.head.appendChild(s); });
    });
    return dataP;
  }
  function buildPanel(){ panel=document.createElement('div'); panel.id='senGlobalPanel';
    document.body.appendChild(panel); }
  function runGlobal(q){
    if(!panel) buildPanel();
    panel.classList.add('show');
    if(!q||q.length<2){
      panel.innerHTML='<div class="gs-note">Type at least 2 characters to search '
        +'every lesson and question · Esc to close</div>';
      label.textContent=''; return;
    }
    panel.innerHTML='<div class="gs-note">Searching…</div>';
    loadData().then(function(){
      var t=q.toLowerCase(),out=[]; wcache={};
      (window.PAGES||[]).forEach(function(p,pi){
        var hay=(p.t+' '+p.x).toLowerCase(),i=findIn(hay,t,'p'+pi); if(i<0) return;
        out.push({k:'lesson',title:p.t,crumb:p.cl+' · '+p.m,href:pageHref(p.f),
          snip:(p.t+' '+p.x).substr(Math.max(0,i-70),190),i:i}); });
      if(wantQ) (window.QB||[]).forEach(function(qq,qi){
        var body=qq.q+' '+qq.opts.map(function(o){return o.t;}).join(' ');
        var hay=body.toLowerCase(),i=findIn(hay,t,'q'+qi); if(i<0) return;
        out.push({k:'quiz',title:qq.q.slice(0,110),crumb:qq.unit+' · '+qq.quiz,
          href:pageHref('browse.html'),snip:body.substr(Math.max(0,i-70),190),i:i}); });
      out.sort(function(a,b){return a.i-b.i;});
      label.textContent=out.length+' found';
      var rx=new RegExp('('+q.replace(/[.*+?^${}()|[\]\\]/g,'\\$&')+')','ig');
      var head='<div class="gs-note">'+out.length+' matches in course notes · '+(fuzzy?'fuzzy on':'exact')+(wantQ?' · incl. questions':'')+' · Esc to close</div>';
      panel.innerHTML=head+(out.slice(0,60).map(function(r){
        return '<a class="gs-row" href="'+r.href+'">'
          +'<span class="gs-crumb">'+esc(r.crumb)+'<b class="gs-kind '+r.k+'">'+r.k+'</b></span>'
          +'<span class="gs-title">'+esc(r.title).replace(rx,'<em>$1</em>')+'</span>'
          +'<span class="gs-snip">'+esc(r.snip).replace(rx,'<em>$1</em>')+'</span></a>';
      }).join('')||'<div class="gs-note">No matches.</div>');
    });
  }

  /* ---------- mode ---------- */
  function setGlobal(on){
    global=on;
    bar.classList.toggle('global',on);
    chip.style.display=on?'inline-block':'none';
    input.placeholder=on?'Search every lesson and question…':'Find on this page — / again for global';
    if(!on&&panel) panel.classList.remove('show');
    if(on) clear();
  }

  /* ---------- ui ---------- */
  function build(){
    bar=document.createElement('div'); bar.id='senFindBar';
    bar.innerHTML='<span class="mode">GLOBAL</span>'
      +'<input type="text" placeholder="Find on this page — / again for global">'
      +'<span class="lbl"></span>'
      +'<button data-a="prev" title="Previous (Shift+Enter)">↑</button>'
      +'<button data-a="next" title="Next (Enter)">↓</button>'
      +'<button data-a="fuzz" title="Fuzzy matching (tolerates typos)">fuzzy: on</button>'
      +'<button data-a="qs" class="off" title="Include quiz questions in global search">+questions</button>'+'<button data-a="all" title="Search everything">Global</button>'
      +'<button data-a="close" title="Close (Esc)">✕</button>'
      +'<span class="hint">Enter confirm · n/N next · j/k scroll</span>';
    document.body.appendChild(bar);
    input=bar.querySelector('input'); label=bar.querySelector('.lbl'); chip=bar.querySelector('.mode');
    chip.style.display='none';
    input.addEventListener('input',function(){
      var v=input.value;
      if(!global&&v.charAt(0)==='/'){ input.value=v.slice(1); setGlobal(true); }
      clearTimeout(timer);
      timer=setTimeout(function(){
        global?runGlobal(input.value.trim()):highlight(input.value.trim()); },150);
    });
    input.addEventListener('keydown',function(e){
      if(e.key==='Escape'){ e.preventDefault(); close(); }
      else if(e.key==='Enter'){
        if(global) return;
        e.preventDefault();
        if(e.shiftKey){ step(-1); return; }
        // vim-style: Enter confirms. Highlights stay, focus leaves the field so
        // n / N / j / k drive the page immediately.
        if(marks.length){ input.blur(); }
        else step(1);
      }
      else if(e.key==='Backspace'&&global&&!input.value){ e.preventDefault(); setGlobal(false); }
    });
    bar.addEventListener('click',function(e){
      var a=e.target.getAttribute&&e.target.getAttribute('data-a'); if(!a) return;
      if(a==='next') step(1); else if(a==='prev') step(-1);
      else if(a==='close') close();
      else if(a==='qs'){
        wantQ=!wantQ;
        e.target.classList.toggle('off',!wantQ);
        if(global) runGlobal(input.value.trim());
      }
      else if(a==='fuzz'){
        fuzzy=!fuzzy;
        e.target.textContent='fuzzy: '+(fuzzy?'on':'off');
        e.target.classList.toggle('off',!fuzzy);
        if(global) runGlobal(input.value.trim());
      }
      else if(a==='all'){ setGlobal(true); input.focus(); runGlobal(input.value.trim()); }
    });
  }
  function open(){ if(!bar) build(); bar.classList.add('show'); input.focus(); input.select(); }
  function close(){ clear(); if(panel) panel.classList.remove('show');
    if(bar){ setGlobal(false); bar.classList.remove('show'); input.value=''; label.textContent=''; }
    if(document.activeElement&&document.activeElement.blur) document.activeElement.blur(); }

  /* exposed so the vim key layer can reuse the same match list */
  window.SENFind={
    step:function(d){ step(d); },
    count:function(){ return marks.length; },
    index:function(){ return cur; },
    open:open, close:close,
    barOpen:function(){ return !!(bar&&bar.classList.contains('show')); },
    focused:function(){ return document.activeElement===input; }
  };

  document.addEventListener('keydown',function(e){
    if(e.key==='Escape'){
      if((bar&&bar.classList.contains('show'))||(panel&&panel.classList.contains('show'))){
        e.preventDefault(); close(); }
      return;
    }
    if(e.key!=='/'||e.metaKey||e.ctrlKey||e.altKey) return;
    var t=e.target||{},tag=(t.tagName||'').toLowerCase(), now=Date.now();
    if(now-lastSlash<700){                       // "//" double-tap anywhere
      lastSlash=0; e.preventDefault();
      if(!bar) build();
      bar.classList.add('show'); setGlobal(true); input.focus();
      runGlobal(input.value.trim()); return;
    }
    lastSlash=now;
    if(bar&&t===input) return;
    if(tag==='input'||tag==='textarea'||tag==='select'||t.isContentEditable) return;
    e.preventDefault();
    var box=document.querySelector('input[type=search]');
    if(box){ box.focus(); box.select(); return; }
    open();
  });
})();

/* ---- account control in the app bar (every page loads this file) ---- */
(function () {
  function build(nav, username) {
    if (nav.querySelector('.sen-acct')) return;
    var wrap = document.createElement('span');
    wrap.className = 'sen-acct';

    var who = document.createElement('span');
    who.className = 'sen-who';
    who.textContent = username || 'guest';          // textContent: never parsed as HTML
    who.title = 'Signed in as ' + (username || 'guest');

    var out = document.createElement('button');
    out.type = 'button';
    out.className = 'sen-out';
    out.textContent = 'Sign out';
    out.addEventListener('click', async function () {
      if (!confirm('Sign out?\n\nScores cached on this device are cleared. They stay on the server and return when you sign back in.')) return;
      out.disabled = true; out.textContent = 'Signing out…';
      try { await fetch('/api/auth/logout', { method: 'POST', credentials: 'same-origin' }); } catch (e) {}
      try {
        localStorage.removeItem('sen_scores');
        localStorage.removeItem('sen_syncstatus');
        localStorage.removeItem('sen_user');
      } catch (e) {}
      location.href = '/login.html';
    });

    wrap.appendChild(who);
    wrap.appendChild(out);
    nav.appendChild(wrap);
  }

  async function init() {
    var nav = document.querySelector('nav.appnav');
    if (!nav) return;
    try {
      var r = await fetch('/api/auth/me', { credentials: 'same-origin' });
      if (!r.ok) return;
      var d = await r.json();
      if (d && d.user) build(nav, d.user.username);
    } catch (e) { /* offline: leave the bar alone */ }
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();
})();

/* ---- vim-style keys: j/k scroll, n/N cycle matches, gg/G jump ---- */
(function () {
  var LINE = 64, lastG = 0;

  function typing(t) {
    var tag = (t && t.tagName || '').toLowerCase();
    return tag === 'input' || tag === 'textarea' || tag === 'select' ||
           (t && t.isContentEditable);
  }
  function by(px) { window.scrollBy({ top: px, behavior: 'instant' in window ? 'instant' : 'auto' }); }

  document.addEventListener('keydown', function (e) {
    if (e.metaKey || e.ctrlKey || e.altKey) return;
    // never hijack real typing, including the find bar's own field
    if (typing(e.target)) return;
    if (window.SENFind && window.SENFind.focused && window.SENFind.focused()) return;

    var k = e.key;

    if (k === 'j') { e.preventDefault(); by(LINE); return; }
    if (k === 'k') { e.preventDefault(); by(-LINE); return; }
    if (k === 'd') { e.preventDefault(); by(window.innerHeight / 2); return; }
    if (k === 'u') { e.preventDefault(); by(-window.innerHeight / 2); return; }

    if (k === 'G') { e.preventDefault(); window.scrollTo(0, document.body.scrollHeight); return; }
    if (k === 'g') {
      var now = Date.now();
      if (now - lastG < 600) { e.preventDefault(); window.scrollTo(0, 0); lastG = 0; }
      else lastG = now;
      return;
    }

    // n / N step through the current search matches
    if (k === 'n' || k === 'N') {
      if (!window.SENFind || !window.SENFind.count()) return;
      e.preventDefault();
      window.SENFind.step(k === 'n' ? 1 : -1);
      return;
    }
  });
})();


/* ---- theme: auto -> light -> dark, remembered per device ---- */
(function () {
  var KEY = 'sen_theme', ORDER = ['auto', 'light', 'dark'];
  var ICON = { auto: '◐', light: '☀', dark: '☾' };
  var LABEL = { auto: 'Theme: follow system', light: 'Theme: light', dark: 'Theme: dark' };

  function get() { try { return localStorage.getItem(KEY) || 'auto'; } catch (e) { return 'auto'; } }
  function apply(t) {
    if (t === 'auto') delete document.documentElement.dataset.theme;
    else document.documentElement.dataset.theme = t;
    var b = document.querySelector('nav.appnav .sen-theme');
    if (b) { b.textContent = ICON[t]; b.title = LABEL[t] + ' (click to change)'; }
  }
  function set(t) { try { localStorage.setItem(KEY, t); } catch (e) {} apply(t); }

  function mount() {
    var nav = document.querySelector('nav.appnav');
    if (!nav || nav.querySelector('.sen-theme')) return;
    var b = document.createElement('button');
    b.type = 'button'; b.className = 'sen-theme';
    b.addEventListener('click', function () {
      set(ORDER[(ORDER.indexOf(get()) + 1) % ORDER.length]);
    });
    // sits next to the account control if that exists, else at the end
    var acct = nav.querySelector('.sen-acct');
    if (acct) nav.insertBefore(b, acct); else nav.appendChild(b);
    apply(get());
  }

  apply(get());                       // before paint where possible
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', mount);
  else mount();
})();
