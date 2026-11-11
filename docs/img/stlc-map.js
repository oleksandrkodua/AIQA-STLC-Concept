/* Flowchart: the AI-assisted QA lifecycle, drawn as a pirate treasure map.
   Seven islands in a ring, a dashed trail, a red X wherever a person decides, and a small pirate (the reviewer)
   who walks the trail and stops at every X. Illustrative: no counts, no data.
   Rebuild with tools/build_stlc_map.py after any edit. */
const tmI = '#5e5f6b';
const tmX = (x,y,s = 6) => { r0.ln([[x-s,y-s],[x+s,y+s]],'#b8503f',3.4); r0.ln([[x+s,y-s],[x-s,y+s]],'#b8503f',3.4); };
const tmCoin = (x,y,n) => { r0.part(r0.el(x,y,8.5,8.5,18),'#e2c273',.9,tmI); rim(r0.el(x,y,6,6,16),.5,'#a8873f'); TX(x,y+4.6,String(n),{size:13.5,anchor:'middle',col:'#6b5527'}); };
const tmSand = (cx,cy,rx,ry,k,dash) => { rim(oval(cx,cy+3,rx+9,ry+6),.7,'#7fa3bb',.55); r0.shadow(cx,cy+ry+3,rx*.85,4,.14);
  const b = blob(cx,cy,rx,ry,.09,k); r0.part(b,'#ead6a4',1.1,tmI); if (dash) rim(oval(cx,cy,rx+4,ry+3),.9,tmI,.7); r0.ln(r0.arc(cx,cy,rx-6,ry-4,200,300,8),'#f6ead0',1.2,.8); };

card({id:'stlcmap',name:'Flowchart',of:'the QA lifecycle with AI, as a treasure map',
  note:'Follow the dashed trail from the scroll. The pirate stops at every red X: that is where a person decides. Touch an island.',
  draw(){
  const S = [[78,100],[214,80],[352,100],[446,184],[352,244],[216,266],[80,250]];
  /* the red X, in trail order: one between every two stages, and none after island 6.
     The release decision is the X before island 6; the last X (QA Lead) closes the loop */
  const M = [[146,74],[283,96],[399,142],[414,224],[282,262],[46,172]];
  const ring = [S[0],M[0],S[1],M[1],S[2],M[2],S[3],M[3],S[4],M[4],S[5],[148,274],S[6],M[5]];
  const tr = spline(ring,true,5); tr.push(tr[0]);

  /* the parchment, with its own project layer */
  PT('the map itself is the project layer: context, knowledge and decisions that differ for every project',() => {
    const edge = (x0,y0,x1,y1,k) => { const o = []; const n = 8; for (let i = 0; i < n; i++) { const t = i/n, j = 4*Math.sin((i+k)*2.3)+3*Math.cos((i+k)*1.3); const dx = x1-x0, dy = y1-y0, l = Math.hypot(dx,dy); o.push([x0+dx*t-dy/l*j,y0+dy*t+dx/l*j]); } return o; };
    const par = [...edge(24,26,498,22,0),...edge(498,22,502,400,3),...edge(502,400,22,404,6),...edge(22,404,24,26,9)];
    const p = spline(par,true,4); r0.sol(p,'#f1e3bf'); rim(p,1.3,tmI);
    rim(spline(par.map(([x,y]) => [260+(x-260)*.975,212+(y-212)*.975]),true,4),.6,'#c9ae7a',.8);
    r0.sol(blob(120,336,60,34,.05,3),'#ead8ac',.6);
  },{lift:[0,0]});

  /* the trail */
  PT('the trail: the path one change takes. Everything on it is a draft until a person marks the X',() => {
    r0.ln(tr,'#7a5a3a',2.1,.9,'7 6');
  });

  /* 1 requirements: a scroll on a post */
  PT('1 requirements: AI reads the story and lists gaps and questions. Output is a draft',() => {
    const [cx,cy] = S[0]; tmSand(cx,cy,30,16,5);
    r0.ln([[cx,cy+6],[cx,cy-34]],'#8a6a45',3.4);
    r0.part(rrect(cx-17,cy-40,34,20,3),'#f6edd2',1,tmI);
    r0.part(r0.el(cx-17,cy-30,4.5,10,14),'#e6d3a4',.8,tmI); r0.part(r0.el(cx+17,cy-30,4.5,10,14),'#e6d3a4',.8,tmI);
    rule([[[cx-10,cy-34],[cx+10,cy-34]],[[cx-10,cy-29],[cx+6,cy-29]],[[cx-10,cy-24],[cx+9,cy-24]]],'#a89c82',.7,.9);
    tmCoin(cx-26,cy+6,1);
  },{lift:[0,-4]});

  /* 2 test design: a signpost with a checklist */
  PT('2 test design: AI drafts cases from the approved brief. A person reviews every case',() => {
    const [cx,cy] = S[1]; tmSand(cx,cy,30,16,6);
    r0.ln([[cx,cy+6],[cx,cy-38]],'#8a6a45',3.4);
    r0.part(rrect(cx-19,cy-48,38,28,3),'#c9a877',1,tmI);
    for (const k of [0,1,2]) { r0.ln([[cx-14,cy-40+k*8],[cx-11,cy-37+k*8],[cx-6,cy-43+k*8]],'#4f7a4a',1.4); rule([[[cx-2,cy-40+k*8],[cx+13,cy-40+k*8]]],'#7b6342',.8,.9); }
    tmCoin(cx-26,cy+6,2);
  },{lift:[0,-4]});

  /* 3 manual testing: a spyglass on a rock */
  PT('3 manual testing: a person runs the cases, decides pass or fail and confirms each bug',() => {
    const [cx,cy] = S[2]; tmSand(cx,cy,30,16,7);
    r0.ln([[cx-2,cy-14],[cx-12,cy+6]],'#6d5436',2.2); r0.ln([[cx+2,cy-14],[cx+12,cy+6]],'#6d5436',2.2); r0.ln([[cx,cy-14],[cx,cy+6]],'#6d5436',2.2);
    r0.ln([[cx-18,cy-12],[cx+16,cy-34]],tmI,10); r0.ln([[cx-18,cy-12],[cx+16,cy-34]],'#c9a24e',8);
    r0.ln([[cx-18,cy-12],[cx-6,cy-19.5]],'#a8803a',9); r0.ln([[cx+9,cy-29.5],[cx+16,cy-34]],'#a8803a',10);
    r0.part(r0.el(cx+17,cy-35,5.5,6.5,14),'#cfe1ea',.9,tmI);
    tmCoin(cx-30,cy+6,3);
  },{lift:[0,-4]});

  /* 4 automation: a ship's wheel on a raft, optional */
  PT('4 automation, optional: only for a case a person already confirmed. No automation project is in this repository yet',() => {
    const [cx,cy] = S[3]; tmSand(cx,cy,28,15,8,true);
    const wy = cy-22, ang = Array.from({length:8},(_,k) => k*Math.PI/4);
    for (const a of ang) { r0.ln([[cx,wy],[cx+Math.cos(a)*18,wy+Math.sin(a)*18]],'#7b5a36',2.2); r0.dot(cx+Math.cos(a)*18,wy+Math.sin(a)*18,2.4,'#c9a24e'); }
    rim(r0.el(cx,wy,13,13,24),2.2,'#8a6a45'); rim(r0.el(cx,wy,13,13,24),.6,tmI); r0.dot(cx,wy,4.2,'#c9a24e'); rim(r0.el(cx,wy,4.2,4.2,12),.7,tmI);
    r0.ln([[cx,cy+4],[cx,cy-4]],'#8a6a45',3);
    tmCoin(cx+27,cy+6,4);
  },{lift:[0,-4]});

  /* 5 CI: a lighthouse that runs without anyone */
  PT('5 CI: runs the same way every time. No AI and no skill here, so no draft to review',() => {
    const [cx,cy] = S[4]; tmSand(cx,cy,30,16,9);
    out.push(`<path d="M${cx+8} ${cy-40}L${cx+58} ${cy-52}L${cx+58} ${cy-26}Z" fill="#f3e3a0" opacity=".45"/>`);
    r0.part([[cx-10,cy+4],[cx-6.5,cy-34],[cx+6.5,cy-34],[cx+10,cy+4]],'#f2ecde',1.1,tmI);
    r0.sol([[cx-9,cy-8],[cx-8.2,cy-16],[cx+8.2,cy-16],[cx+9,cy-8]],'#9fb3c4',.9); r0.sol([[cx-7.6,cy-24],[cx-7,cy-30],[cx+7,cy-30],[cx+7.6,cy-24]],'#9fb3c4',.9);
    r0.part(rrect(cx-8,cy-45,16,11,2),'#e9d58c',1,tmI); r0.part([[cx-10,cy-45],[cx,cy-55],[cx+10,cy-45]],'#7a8794',1,tmI);
    tmCoin(cx+31,cy+6,5);
  },{lift:[0,-4]});

  /* 6 release: the treasure */
  PT('6 analysis and release: AI reads CI failures and drafts the report and risk summary. The release decision is made at the red X before it',() => {
    const [cx,cy] = S[5]; tmSand(cx,cy,32,17,10);
    r0.shadow(cx,cy+8,24,4,.16);
    r0.part([[cx-19,cy-16],[cx-16,cy-34],[cx+16,cy-34],[cx+19,cy-16]],'#a8794a',1.1,tmI);
    r0.part(rrect(cx-19,cy-16,38,22,2),'#c08c56',1.1,tmI); rule([[[cx-19,cy-8],[cx+19,cy-8]]],tmI,.8,.8);
    r0.part(rrect(cx-3.5,cy-12,7,9,1.5),'#e2c273',.8,tmI);
    for (const [dx,dy] of [[-12,-17],[-4,-19],[5,-18],[12,-16],[-8,-14],[2,-15]]) { r0.part(r0.el(cx+dx,cy+dy,4.6,3.2,12),'#e9c862',.7,'#8a6a2c'); }
    tmCoin(cx-31,cy+10,6);
  },{lift:[0,-4]});

  /* 7 feedback: a bottle that sails back */
  PT('7 feedback: every miss becomes an entry, then a change proposal. A person approves any change to rules, skills or hooks',() => {
    const [cx,cy] = S[6];
    r0.ln(bend([cx-30,cy+12],[cx-18,cy+5],[cx-6,cy+12],6),'#6f9bb5',1.4,.9); r0.ln(bend([cx-6,cy+12],[cx+6,cy+19],[cx+22,cy+12],6),'#6f9bb5',1.4,.9); r0.ln(bend([cx+8,cy+4],[cx+18,cy-1],[cx+30,cy+4],6),'#6f9bb5',1.2,.8);
    out.push(`<g transform="rotate(-24 ${cx} ${cy})">`);
    r0.part(rrect(cx-9,cy-13,18,30,7),'#cfe4ec',1.1,tmI); r0.part(rrect(cx-3.5,cy-24,7,13,2),'#cfe4ec',1,tmI);
    r0.part(rrect(cx-4,cy-29,8,6,1.5),'#b88a54',.9,tmI); r0.part(rrect(cx-3.5,cy-7,7,20,1.5),'#f6edd2',.7,tmI);
    out.push('</g>'); tmCoin(cx+28,cy-16,7);
  },{lift:[0,-4]});

  /* production: a skull rock, off the route */
  PT('production: a skull rock off the route. No access, and nothing on this map goes there',() => {
    const cx = 452, cy = 322;
    rim(oval(cx,cy+4,40,20),.8,'#7fa3bb',.5);
    r0.part(blob(cx,cy,32,17,.1,6),'#9a9aa3',1.1,tmI);
    r0.part(r0.el(cx,cy-6,12,11,18),'#f4f0e6',1,tmI); r0.part(rrect(cx-6,cy+1,12,8,2),'#f4f0e6',.9,tmI);
    r0.dot(cx-4.5,cy-7,3,'#4b4d59'); r0.dot(cx+4.5,cy-7,3,'#4b4d59'); r0.ln([[cx,cy-3],[cx-1.4,cy-1],[cx+1.4,cy-1],[cx,cy-3]],'#4b4d59',1);
    rim(oval(cx,cy,38,19),.9,tmI,.75);
    TXC(cx,cy+36,'production:\nno access',{size:13.5,col:LN});
  },{lift:[0,-3]});

  /* the compass rose: governance */
  PT('the compass: rules, policy and permissions. It sits in the middle because every leg is steered by it',() => {
    const cx = 262, cy = 166;
    rim(r0.el(cx,cy,34,34,36),1,tmI,.85); rim(r0.el(cx,cy,29,29,36),.5,'#a89c82');
    for (let k = 0; k < 16; k++) { const a = k*Math.PI/8, r2 = k%2 ? 29 : 34; r0.ln([[cx+Math.cos(a)*29,cy+Math.sin(a)*29],[cx+Math.cos(a)*r2,cy+Math.sin(a)*r2]],tmI,.6); }
    r0.part([[cx,cy-30],[cx+5,cy],[cx,cy+30],[cx-5,cy]],'#e9d9ae',1,tmI);
    r0.part([[cx-30,cy],[cx,cy-5],[cx+30,cy],[cx,cy+5]],'#d3c28f',1,tmI);
    r0.sol([[cx,cy-30],[cx+5,cy],[cx-5,cy]],'#b8503f',.9); r0.dot(cx,cy,2.4,tmI);
    TXC(cx-84,cy-2,'rules, policy,\npermissions',{size:13.5,col:LN});
  },{lift:[0,-2]});

  /* the ruler: evals */
  PT('the ruler: evals. They measure whether a skill or a hook works; the validator checks the file structure on every pull request',() => {
    const x0 = 58, y0 = 372, w = 230;
    r0.part(rrect(x0,y0,w,15,2),'#d9b878',1,tmI);
    rule(Array.from({length:12},(_,k) => [[x0+8+k*(w-16)/11,y0],[x0+8+k*(w-16)/11,y0+(k%5 === 0 ? 9 : 5.5)]]),'#7b6342',.8,.9);
    TX(x0+w+10,y0+12,'evals: the ruler',{size:13.5,col:LN});
  },{lift:[0,-2]});

  /* the decisions: a red X, a short label, a note */
  const D = [
    [0,'approves\nbrief',[146,104],'answers the questions, approves the brief'],
    [1,'reviews\nthe cases',[272,68],'reviews every case, saves it to the test management system'],
    [2,'pass or\nfail',[366,170],'decides pass or fail, confirms each bug'],
    [3,'approves\nthe PR',[460,236],'approves the candidate, reviews the pull request'],
    [4,'release\ndecision',[282,296],'triages the CI result (defect, test or environment?) and makes the release decision'],
    [5,'QA Lead\napproves',[94,176],'QA Lead approves any change to a rule, skill, hook or eval']];
  D.forEach(([i,t,[lx,ly],note]) => { PT('red X: '+note,() => { tmX(M[i][0],M[i][1]); TXC(lx,ly,t,{size:13.5,col:'#7a3a2f'}); },{lift:[0,-2]}); });

  /* island names, outside the ring */
  const NM = [['requirements',78,50],['test design',226,122],['manual testing',376,50],['automation\n(optional)',452,122],['CI, no AI',382,296],['release',200,316],['feedback',80,298]];
  for (const [n,x,y] of NM) PT(n.replace('\n',' '),() => TXC(x,y,n,{size:13.5,cap:false,col:'#5a4a30'}),{deco:true});

  /* the walk: to each red X, then a pause there. kt and kp are the timeline, shared by the pirate and the SVG captions */
  const cum = [0]; for (let i = 1; i < tr.length; i++) cum.push(cum[i-1]+Math.hypot(tr[i][0]-tr[i-1][0],tr[i][1]-tr[i-1][1]));
  const tot = cum.at(-1), idx = [M[0],M[1],M[2],M[3],M[4],S[5],M[5]].map(m => { let b = 0, bd = 1e9; tr.forEach((q,i) => { const d = Math.hypot(q[0]-m[0],q[1]-m[1]); if (d < bd) { bd = d; b = i; } }); return b; });
  const pause = .05; let tt = 0, prev = 0; const kp = [0], kt = [0];
  idx.forEach(ix => { const f = cum[ix]/tot; tt += f-prev; kp.push(f); kt.push(tt); tt += pause; kp.push(f); kt.push(tt); prev = f; });
  tt += 1-prev; kp.push(1); kt.push(tt);
  const T = kt.map(v => v/tt), DUR = 30;

  /* the pirate: the reviewer, walking the trail and waiting at every red X */
  PT('the pirate is the reviewer. He walks the trail and waits at every red X until a person has decided, and rests on the treasure',() => {
    const d = 'M'+tr.map(q => n1(q[0])+' '+n1(q[1])).join('L');
    out.push('<g><g transform="translate(0 -3) scale(1.05)">');
    r0.ln([[-2.5,-6],[-3.2,0]],tmI,2); r0.ln([[2.5,-6],[2.6,0]],'#8a6a45',2.2);
    r0.part(rrect(-5,-16,10,11,2.5),'#f3ead4',1,tmI); rule([[[-5,-13],[5,-13]],[[-5,-9.5],[5,-9.5]]],'#5e6a85',.9,.9);
    r0.ln([[5,-10],[11,-14]],'#7a8794',1.6);
    r0.part(r0.el(0,-21,5,5.2,14),'#efcfa6',1,tmI); r0.dot(2,-21.5,1,tmI); r0.ln([[-1,-22.4],[3.6,-21]],tmI,.6);
    r0.part([[-9,-23],[0,-32],[9,-23],[5,-21],[-5,-21]],'#3a3a46',1,tmI); rule([[[-6,-23.6],[6,-23.6]]],'#e2c273',1.3,1);
    out.push(`<animateMotion dur="${DUR}s" repeatCount="indefinite" calcMode="linear" keyPoints="${kp.map(n1).join(';')}" keyTimes="${T.map(v => v.toFixed(4)).join(';')}" path="${d}"/>`);
    out.push('</g></g>');
  });

  /* the status line: one text per stage, shown while the pirate walks to that stage's red X and waits there.
     In the standalone SVG (the builder sets SVGMODE) it is drawn under the map and switches by itself;
     on the page it is the note under the card, switched by a small script the builder adds (window.STLC_STAGES) */
  const CAP = [
    ['1 requirements: AI lists the gaps and questions.','A person answers them and approves the brief.'],
    ['2 test design: AI drafts the cases from the brief.','A person reviews every case and saves it to the TMS.'],
    ['3 manual testing: a person runs the cases,','decides pass or fail and confirms each bug.'],
    ['4 automation, optional: only for a case already confirmed.','A person approves it and reviews the pull request.'],
    ['5 CI: runs the same way every time, no AI.','A person triages the result and makes the release decision.'],
    ['6 analysis and release: AI reads the CI failures and drafts','the report and the risk summary for the release.'],
    ['7 feedback: every miss becomes an entry, then a proposal.','QA Lead approves any change to a rule, skill, hook or eval.']];
  /* a stage's text is shown from the moment the pirate leaves the previous stop until he leaves this stage's own stop.
     The stops are the six red X and island 6 (he rests on the treasure: stage 6 has no X after it) */
  const WIN = [[0,T[2]],[T[2],T[4]],[T[4],T[6]],[T[6],T[8]],[T[8],T[10]],[T[10],T[12]],[T[12],1]];
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
