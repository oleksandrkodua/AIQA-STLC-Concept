/* Flowchart: the improvement loop of the AI-assisted QA process, drawn as a pirate treasure map.
   Nine islands in a ring (observe, analyze, recommend, approve, act, audit, learn, evaluate, improve), one dashed trail,
   one red X where a person decides, and a small pirate (the reviewer) who walks the trail and rests at every island.
   Illustrative: no counts, no data. Rebuild with tools/build_stlc_map.py after any edit. */
const lmI = '#5e5f6b';
const lmX = (x,y,s = 6,w = 3.4) => { r0.ln([[x-s,y-s],[x+s,y+s]],'#b8503f',w); r0.ln([[x+s,y-s],[x-s,y+s]],'#b8503f',w); };
const lmCoin = (x,y,n) => { r0.part(r0.el(x,y,8.5,8.5,18),'#e2c273',.9,lmI); rim(r0.el(x,y,6,6,16),.5,'#a8873f'); TX(x,y+4.6,String(n),{size:13.5,anchor:'middle',col:'#6b5527'}); };
const lmSand = (cx,cy,rx,ry,k) => { rim(oval(cx,cy+3,rx+9,ry+6),.7,'#7fa3bb',.55); r0.shadow(cx,cy+ry+3,rx*.85,4,.14);
  const b = blob(cx,cy,rx,ry,.09,k); r0.part(b,'#ead6a4',1.1,lmI); r0.ln(r0.arc(cx,cy,rx-6,ry-4,200,300,8),'#f6ead0',1.2,.8); };

card({id:'loopmap',name:'Flowchart',of:'how the AI-assisted QA process improves itself, as a treasure map',
  note:'Follow the dashed trail from island 1. The pirate rests on every island; the red X is the one place where a person decides. Touch an island.',
  draw(){
  const S = Array.from({length:9},(_,k) => { const a = (-135+40*k)*Math.PI/180; return [Math.round(262+190*Math.cos(a)),Math.round(190+116*Math.sin(a))]; });
  const tr = spline(S,true,5); tr.push(tr[0]);

  /* the parchment, with its own project layer */
  PT('the map itself is the project layer: context, knowledge and decisions that differ for every project',() => {
    const edge = (x0,y0,x1,y1,k) => { const o = []; const n = 8; for (let i = 0; i < n; i++) { const t = i/n, j = 4*Math.sin((i+k)*2.3)+3*Math.cos((i+k)*1.3); const dx = x1-x0, dy = y1-y0, l = Math.hypot(dx,dy); o.push([x0+dx*t-dy/l*j,y0+dy*t+dx/l*j]); } return o; };
    const par = [...edge(24,26,498,22,0),...edge(498,22,502,400,3),...edge(502,400,22,404,6),...edge(22,404,24,26,9)];
    const p = spline(par,true,4); r0.sol(p,'#f1e3bf'); rim(p,1.3,lmI);
    rim(spline(par.map(([x,y]) => [260+(x-260)*.975,212+(y-212)*.975]),true,4),.6,'#c9ae7a',.8);
  },{lift:[0,0]});

  /* the trail */
  PT('the trail: a loop. The last island leads back to the first, because every new miss is a new observation',() => {
    r0.ln(tr,'#7a5a3a',2.1,.9,'7 6');
  });

  /* 1 observe: a spyglass on a rock */
  PT('1 observe: a run, a CI failure or a miss is written down as a feedback entry. Nothing is judged yet',() => {
    const [cx,cy] = S[0]; lmSand(cx,cy,30,16,5);
    r0.ln([[cx-2,cy-14],[cx-12,cy+6]],'#6d5436',2.2); r0.ln([[cx+2,cy-14],[cx+12,cy+6]],'#6d5436',2.2); r0.ln([[cx,cy-14],[cx,cy+6]],'#6d5436',2.2);
    r0.ln([[cx-18,cy-12],[cx+16,cy-34]],lmI,10); r0.ln([[cx-18,cy-12],[cx+16,cy-34]],'#c9a24e',8);
    r0.ln([[cx-18,cy-12],[cx-6,cy-19.5]],'#a8803a',9); r0.ln([[cx+9,cy-29.5],[cx+16,cy-34]],'#a8803a',10);
    r0.part(r0.el(cx+17,cy-35,5.5,6.5,14),'#cfe1ea',.9,lmI);
    lmCoin(cx-30,cy+6,1);
  },{lift:[0,-4]});

  /* 2 analyze: a magnifier over a page */
  PT('2 analyze: AI groups the entries and looks for patterns. The result is a draft, not a finding',() => {
    const [cx,cy] = S[1]; lmSand(cx,cy,30,16,6);
    r0.part(rrect(cx-16,cy-36,30,38,2),'#fbf8f1',1,lmI);
    rule([[[cx-10,cy-28],[cx+8,cy-28]],[[cx-10,cy-22],[cx+4,cy-22]],[[cx-10,cy-16],[cx+8,cy-16]],[[cx-10,cy-10],[cx+2,cy-10]]],'#a89c82',.7,.9);
    const g = r0.el(cx+10,cy-18,9,9,22); r0.ln([[cx+16,cy-11],[cx+25,cy-1]],lmI,5.5); r0.ln([[cx+16,cy-11],[cx+25,cy-1]],'#b08a63',3.6);
    r0.sol(g,'#dfeaf0',.7); rim(g,1.4,lmI);
    lmCoin(cx-30,cy+6,2);
  },{lift:[0,-4]});

  /* 3 recommend: a scroll on a post */
  PT('3 recommend: AI writes a change proposal: the exact old and new text, the reason and a candidate eval',() => {
    const [cx,cy] = S[2]; lmSand(cx,cy,30,16,7);
    r0.ln([[cx,cy+6],[cx,cy-34]],'#8a6a45',3.4);
    r0.part(rrect(cx-17,cy-40,34,20,3),'#f6edd2',1,lmI);
    r0.part(r0.el(cx-17,cy-30,4.5,10,14),'#e6d3a4',.8,lmI); r0.part(r0.el(cx+17,cy-30,4.5,10,14),'#e6d3a4',.8,lmI);
    rule([[[cx-10,cy-34],[cx+10,cy-34]],[[cx-10,cy-29],[cx+6,cy-29]],[[cx-10,cy-24],[cx+9,cy-24]]],'#a89c82',.7,.9);
    lmCoin(cx-26,cy+6,3);
  },{lift:[0,-4]});

  /* 4 approve: a stone tablet with the red X */
  PT('4 approve: QA Lead approves or rejects any change to a rule, skill, hook or eval. Nothing is applied before this',() => {
    const [cx,cy] = S[3]; lmSand(cx,cy,30,16,8);
    r0.part([[cx-17,cy+4],[cx-17,cy-34],[cx-10,cy-42],[cx+10,cy-42],[cx+17,cy-34],[cx+17,cy+4]],'#c9cdd2',1.1,lmI);
    lmX(cx,cy-22,10,4.4);
    lmCoin(cx+31,cy+6,4);
  },{lift:[0,-4]});

  /* 5 act: a hammer and a plank */
  PT('5 act: the approved change is applied, and only that change. Nothing else is touched along with it',() => {
    const [cx,cy] = S[4]; lmSand(cx,cy,30,16,9);
    r0.part(rrect(cx-24,cy-8,48,11,2),'#c9a877',1,lmI); rule([[[cx-20,cy-3],[cx+6,cy-3]]],'#8a6a45',.7,.8); r0.dot(cx+14,cy-2.5,1.8,'#6c7178');
    r0.ln([[cx+6,cy-9],[cx-6,cy-40]],'#8a6a45',3.6);
    r0.part([[cx-14,cy-42],[cx+6,cy-48],[cx+11,cy-38],[cx-9,cy-32]],'#8d949b',1.1,lmI);
    lmCoin(cx+31,cy+6,5);
  },{lift:[0,-4]});

  /* 6 audit: a lighthouse */
  PT('6 audit: hooks, the validator and the run journal leave a trail, so a person can check what changed and why',() => {
    const [cx,cy] = S[5]; lmSand(cx,cy,30,16,10);
    out.push(`<path d="M${cx+8} ${cy-40}L${cx+58} ${cy-52}L${cx+58} ${cy-26}Z" fill="#f3e3a0" opacity=".45"/>`);
    r0.part([[cx-10,cy+4],[cx-6.5,cy-34],[cx+6.5,cy-34],[cx+10,cy+4]],'#f2ecde',1.1,lmI);
    r0.sol([[cx-9,cy-8],[cx-8.2,cy-16],[cx+8.2,cy-16],[cx+9,cy-8]],'#9fb3c4',.9); r0.sol([[cx-7.6,cy-24],[cx-7,cy-30],[cx+7,cy-30],[cx+7.6,cy-24]],'#9fb3c4',.9);
    r0.part(rrect(cx-8,cy-45,16,11,2),'#e9d58c',1,lmI); r0.part([[cx-10,cy-45],[cx,cy-55],[cx+10,cy-45]],'#7a8794',1,lmI);
    lmCoin(cx+31,cy+6,6);
  },{lift:[0,-4]});

  /* 7 learn: an open book on a stand */
  PT('7 learn: lessons enter the knowledge base through intake. One source is one opinion until it is confirmed',() => {
    const [cx,cy] = S[6]; lmSand(cx,cy,30,16,11);
    r0.ln([[cx,cy+6],[cx,cy-12]],'#8a6a45',3.4);
    r0.part([[cx-25,cy-14],[cx,cy-9],[cx,cy-31],[cx-25,cy-36]],'#f6edd2',1.1,lmI);
    r0.part([[cx,cy-9],[cx+25,cy-14],[cx+25,cy-36],[cx,cy-31]],'#f1e6c6',1.1,lmI);
    rule([[[cx-20,cy-28],[cx-5,cy-25]],[[cx-20,cy-23],[cx-8,cy-20.5]],[[cx+5,cy-25],[cx+20,cy-28]],[[cx+8,cy-20.5],[cx+20,cy-23]]],'#a89c82',.7,.9);
    lmCoin(cx-31,cy+6,7);
  },{lift:[0,-4]});

  /* 8 evaluate: balance scales */
  PT('8 evaluate: evals measure whether a skill or a hook works. A check that was not run is NOT RUN, never PASS',() => {
    const [cx,cy] = S[7]; lmSand(cx,cy,30,16,12);
    r0.ln([[cx,cy+6],[cx,cy-40]],'#8a6a45',3.2);
    r0.ln([[cx-24,cy-38],[cx+24,cy-38]],lmI,2.6);
    for (const sx of [-24,24]) { r0.ln([[cx+sx,cy-38],[cx+sx-9,cy-22]],lmI,.9); r0.ln([[cx+sx,cy-38],[cx+sx+9,cy-22]],lmI,.9); r0.part(r0.el(cx+sx,cy-21,11,3.6,16),'#d9b878',.9,lmI); }
    r0.part(r0.el(cx-24,cy-26,4,3,10),'#e2c273',.7,'#8a6a2c');
    lmCoin(cx-30,cy+6,8);
  },{lift:[0,-4]});

  /* 9 improve: the treasure chest */
  PT('9 improve: the next version of the rule, skill or hook starts from this result. New misses go back to step 1',() => {
    const [cx,cy] = S[8]; lmSand(cx,cy,32,17,13);
    r0.shadow(cx,cy+8,24,4,.16);
    r0.part([[cx-19,cy-16],[cx-16,cy-34],[cx+16,cy-34],[cx+19,cy-16]],'#a8794a',1.1,lmI);
    r0.part(rrect(cx-19,cy-16,38,22,2),'#c08c56',1.1,lmI); rule([[[cx-19,cy-8],[cx+19,cy-8]]],lmI,.8,.8);
    r0.part(rrect(cx-3.5,cy-12,7,9,1.5),'#e2c273',.8,lmI);
    for (const [dx,dy] of [[-12,-17],[-4,-19],[5,-18],[12,-16],[-8,-14],[2,-15]]) { r0.part(r0.el(cx+dx,cy+dy,4.6,3.2,12),'#e9c862',.7,'#8a6a2c'); }
    lmCoin(cx-31,cy+10,9);
  },{lift:[0,-4]});

  /* production: a skull rock, off the route */
  PT('production: a skull rock off the route. No access, and nothing on this map goes there',() => {
    const cx = 462, cy = 336;
    rim(oval(cx,cy+4,40,20),.8,'#7fa3bb',.5);
    r0.part(blob(cx,cy,32,17,.1,6),'#9a9aa3',1.1,lmI);
    r0.part(r0.el(cx,cy-6,12,11,18),'#f4f0e6',1,lmI); r0.part(rrect(cx-6,cy+1,12,8,2),'#f4f0e6',.9,lmI);
    r0.dot(cx-4.5,cy-7,3,'#4b4d59'); r0.dot(cx+4.5,cy-7,3,'#4b4d59'); r0.ln([[cx,cy-3],[cx-1.4,cy-1],[cx+1.4,cy-1],[cx,cy-3]],'#4b4d59',1);
    rim(oval(cx,cy,38,19),.9,lmI,.75);
    TXC(cx,cy+36,'production:\nno access',{size:13.5,col:LN});
  },{lift:[0,-3]});

  /* the compass rose: governance */
  PT('the compass: rules, policy and permissions. It sits in the middle because every step is steered by it',() => {
    const cx = 262, cy = 190;
    rim(r0.el(cx,cy,34,34,36),1,lmI,.85); rim(r0.el(cx,cy,29,29,36),.5,'#a89c82');
    for (let k = 0; k < 16; k++) { const a = k*Math.PI/8, r2 = k%2 ? 29 : 34; r0.ln([[cx+Math.cos(a)*29,cy+Math.sin(a)*29],[cx+Math.cos(a)*r2,cy+Math.sin(a)*r2]],lmI,.6); }
    r0.part([[cx,cy-30],[cx+5,cy],[cx,cy+30],[cx-5,cy]],'#e9d9ae',1,lmI);
    r0.part([[cx-30,cy],[cx,cy-5],[cx+30,cy],[cx,cy+5]],'#d3c28f',1,lmI);
    r0.sol([[cx,cy-30],[cx+5,cy],[cx-5,cy]],'#b8503f',.9); r0.dot(cx,cy,2.4,lmI);
    TXC(cx,cy+52,'rules, policy,\npermissions',{size:13.5,col:LN});
  },{lift:[0,-2]});

  /* island names, under the islands */
  const NM = ['observe','analyze','recommend','approve\nQA Lead','act','audit','learn','evaluate','improve'];
  /* most names sit under their island; two sit inside the ring, where the neighbouring island's props would cover them */
  const NP = k => k === 3 ? [S[k][0]-68,S[k][1]-2] : k === 8 ? [S[k][0]+70,S[k][1]-2] : [S[k][0],S[k][1]+36];
  NM.forEach((n,k) => PT(n.replace('\n',' '),() => TXC(...NP(k),n,{size:13.5,cap:false,col:k === 3 ? '#7a3a2f' : '#5a4a30'}),{deco:true}));

  /* the walk: a rest on every island, a longer one on the approve island. kt and kp are the timeline, shared by the pirate and the SVG captions */
  const cum = [0]; for (let i = 1; i < tr.length; i++) cum.push(cum[i-1]+Math.hypot(tr[i][0]-tr[i-1][0],tr[i][1]-tr[i-1][1]));
  const tot = cum.at(-1), idx = S.map(m => { let b = 0, bd = 1e9; tr.forEach((q,i) => { const d = Math.hypot(q[0]-m[0],q[1]-m[1]); if (d < bd) { bd = d; b = i; } }); return b; });
  let tt = 0, prev = 0; const kp = [0], kt = [0];
  idx.forEach((ix,k) => { const f = cum[ix]/tot; tt += f-prev; kp.push(f); kt.push(tt); tt += k === 3 ? .07 : .035; kp.push(f); kt.push(tt); prev = f; });
  tt += 1-prev; kp.push(1); kt.push(tt);
  const T = kt.map(v => v/tt), DUR = 40;

  /* the pirate: the reviewer, walking the trail and resting on every island */
  PT('the pirate is the reviewer. He walks the trail, rests on every island, and waits longest at the red X until a person has decided',() => {
    const d = 'M'+tr.map(q => n1(q[0])+' '+n1(q[1])).join('L');
    out.push('<g><g transform="translate(0 -3) scale(1.05)">');
    r0.ln([[-2.5,-6],[-3.2,0]],lmI,2); r0.ln([[2.5,-6],[2.6,0]],'#8a6a45',2.2);
    r0.part(rrect(-5,-16,10,11,2.5),'#f3ead4',1,lmI); rule([[[-5,-13],[5,-13]],[[-5,-9.5],[5,-9.5]]],'#5e6a85',.9,.9);
    r0.ln([[5,-10],[11,-14]],'#7a8794',1.6);
    r0.part(r0.el(0,-21,5,5.2,14),'#efcfa6',1,lmI); r0.dot(2,-21.5,1,lmI); r0.ln([[-1,-22.4],[3.6,-21]],lmI,.6);
    r0.part([[-9,-23],[0,-32],[9,-23],[5,-21],[-5,-21]],'#3a3a46',1,lmI); rule([[[-6,-23.6],[6,-23.6]]],'#e2c273',1.3,1);
    out.push(`<animateMotion dur="${DUR}s" repeatCount="indefinite" calcMode="linear" keyPoints="${kp.map(n1).join(';')}" keyTimes="${T.map(v => v.toFixed(4)).join(';')}" path="${d}"/>`);
    out.push('</g></g>');
  });

  /* the status line: one text per step, shown from the moment the pirate leaves the previous island until he leaves this one.
     In the standalone SVG (the builder sets SVGMODE) it is drawn under the map and switches by itself;
     on the page it is the note under the card, switched by a small script the builder adds (window.STLC_STAGES) */
  const CAP = [
    ['1 observe: a run, a CI failure or a miss is written down','as a feedback entry. Nothing is judged yet.'],
    ['2 analyze: AI groups the entries and looks for patterns.','The result is a draft, not a finding.'],
    ['3 recommend: AI writes a change proposal: the exact old and','new text, the reason and a candidate eval.'],
    ['4 approve: a person decides. QA Lead approves or rejects','any change to a rule, skill, hook or eval.'],
    ['5 act: the approved change is applied, and only that one.','Nothing else is touched along with it.'],
    ['6 audit: hooks, the validator and the run journal leave a trail,','so a person can check what changed and why.'],
    ['7 learn: lessons enter the knowledge base through intake.','One source is one opinion until it is confirmed.'],
    ['8 evaluate: evals measure whether a skill or a hook works.','A check that was not run is NOT RUN, never PASS.'],
    ['9 improve: the next version starts from this result.','New misses go back to step 1.']];
  const WIN = CAP.map((_,k) => [k === 0 ? 0 : T[2*k], k === CAP.length-1 ? 1 : T[2*k+2]]);
  if (typeof SVGMODE !== 'undefined') {
    rule([[[40,428],[480,428]]],'#c9ae7a',.8,.9);
    CAP.forEach((c,k) => {
      const [a,b] = WIN[k];
      const kT = a === 0 ? ['0',b.toFixed(4)] : b === 1 ? ['0',a.toFixed(4)] : ['0',a.toFixed(4),b.toFixed(4)];
      const vs = a === 0 ? '1;0' : b === 1 ? '0;1' : '0;1;0';
      out.push(`<g opacity="${k === 0 ? 1 : 0}"><animate attributeName="opacity" dur="${DUR}s" repeatCount="indefinite" calcMode="discrete" keyTimes="${kT.join(';')}" values="${vs}"/>`);
      TXC(260,452,c.join('\n'),{size:14.5,col:'#4a3d28'}); out.push('</g>');
    });
  } else globalThis.STLC_STAGES = {dur:DUR, win:WIN, text:CAP.map(c => c.join(' '))};
}});
