(() => {
const $=id=>document.getElementById(id);
const STORE='catMasteryProgressV2', IMPORT='catMasteryImportedV1';
const state={view:'dashboard',selectedDate:new Date(),calDate:new Date(),test:null,timer:null,seconds:1200,answers:{},startedAt:null};
const sections=['VARC','DILR','QA'];

const WEIGHTAGE_DATA = {
  CAT: {
    "2022": {
      VARC: {"Reading Comprehension":48,"Parajumbles":10,"Para Completion":6,"Parasummary":9},
      DILR: {"Reasoning based DI":28,"Routes and Networks":5,"Scatter Graphs":5,"Bar Graphs":5,"Table based DI":5},
      QA: {"Interest":3,"Sequence & Series":3,"Equations":4,"Averages and Mixtures":9,"Number Systems":12,"Time, Speed & Distance":5,"Functions":4,"Ratio, Proportion & Variation":6,"Geometry":7,"Percentages":1,"Permutations and Combinations":2,"Time & Work":3,"Logarithm and Surds":1,"Maxima-Minima":3,"Profit, Loss & Discount":2,"Mensuration":2,"Inequalities":1,"Set Theory":1}
    },
    "2021": {
      VARC: {"Reading Comprehension":47,"Parasummary":9,"Odd one out/Misfit Sentence":5,"Parajumbles":11},
      DILR: {"Ordering and Sequencing":6,"Bar Graphs":8,"Reasoning based DI":19,"Table based DI":21,"Games and Tournaments":4},
      QA: {"Number Systems":9,"Time, Speed & Distance":4,"Inequalities":2,"Percentages":6,"Sequence & Series":3,"Equations":5,"Logarithm and Surds":3,"Permutations and Combinations":3,"Averages and Mixtures":5,"Profit, Loss & Discount":4,"Mensuration":5,"Ratio, Proportion & Variation":1,"Geometry":4,"Functions":2,"Interest":2,"Time & Work":5,"Coordinate Geometry":1}
    },
    "2020": {
      VARC: {"Reading Comprehension":57,"Parajumbles":8,"Parasummary":8,"Odd one out/Misfit Sentence":7},
      DILR: {"Table based DI":28,"Logical Deductions and Connections":6,"Reasoning based DI":13,"Ordering and Sequencing":6,"Games and Tournaments":6,"Venn Diagrams":4},
      QA: {"Time, Speed & Distance":10,"Time & Work":2,"Functions":2,"Interest":3,"Geometry":4,"Number Systems":17,"Mensuration":6,"Ratio, Proportion & Variation":4,"Logarithm and Surds":5,"Averages and Mixtures":5,"Profit, Loss & Discount":3,"Equations":8,"Sequence & Series":1,"Percentages":4,"Inequalities":1,"Set Theory":1,"Surds and Indices":1,"Coordinate Geometry":3}
    }
  }
};

const SOURCE_LIBRARY = [
  {year:2016,coverage:"Question paper with answer key",type:"Reconstructed / archive",status:"Indexed",file:"CAT_2024_-_Past_10_Year_Question_Paper_2016.pdf"},
  {year:2017,coverage:"Slot-wise CAT questions",type:"PYQ archive",status:"Indexed",file:"CAT_2024_-_Past_10_Year_Question_Paper_2017.pdf"},
  {year:2019,coverage:"Slot-wise CAT questions",type:"PYQ archive",status:"Indexed",file:"CAT_2024_-_Past_10_Year_Question_Paper_2019.pdf"},
  {year:2020,coverage:"VARC / DILR / QA, slot-wise",type:"PYQ archive",status:"Indexed",file:"CAT_2024_-_Past_10_Year_Question_Paper_2020_WTJQ1JR.pdf"},
  {year:2021,coverage:"Slot-wise CAT questions",type:"PYQ archive",status:"Indexed",file:"CAT_2024_-_Past_10_Year_Question_Paper_2021.pdf"},
  {year:2022,coverage:"Question papers with solutions",type:"PYQ with solutions",status:"Indexed",file:"CAT_2022_-_Question_Paper_with_solutions.pdf"},
  {year:2023,coverage:"All slots referenced",type:"Official-question compilation",status:"Indexed",file:"CAT 2023 Official Question Paper with Solutions (Slot 1, 2 and 3).pdf"},
  {year:2024,coverage:"All three slots",type:"Official-question compilation",status:"Indexed",file:"CAT 2024 Official Question Paper with Solutions (Slot 1, 2 and 3).pdf"},
  {year:2025,coverage:"All three slots · VARC / DILR / QA",type:"Official-question compilation",status:"Indexed",file:"CAT 2025 Official Question Paper with Solutions (Slot 1, 2 and 3).pdf"},
  {year:"Practice",coverage:"20 DILR sets · 100 questions",type:"Careers360 practice",status:"Catalogued",file:"CAT 2026 DILR Practice Questions with Solution...pdf"},
  {year:"Practice",coverage:"Chapter-wise QA MCQs",type:"Careers360 practice",status:"Catalogued",file:"CAT 2026 Quantitative Aptitude Questions with Answers PDF...pdf"},
  {year:"Weightage",coverage:"2020–2022 year-wise chapter counts",type:"Careers360 analysis",status:"Loaded",file:"Mastering CAT Exam_ VARC, DILR, and Quant MCQs & Weightages...pdf"}
];

function normalizeTopicName(t){
  const map={
    "Averages":"Averages and Mixtures","Mixtures":"Averages and Mixtures","Ratio":"Ratio, Proportion & Variation",
    "Profit and Loss":"Profit, Loss & Discount","Profit & Loss":"Profit, Loss & Discount","Time Speed Distance":"Time, Speed & Distance",
    "Time and Work":"Time & Work","Logarithms":"Logarithm and Surds","Number Systems":"Number Systems",
    "Geometry":"Geometry","Percentages":"Percentages","Compound Interest":"Interest","Simple Interest":"Interest",
    "Sequencing":"Ordering and Sequencing","Arrangement":"Ordering and Sequencing","Tables":"Table based DI",
    "Main idea":"Reading Comprehension","Inference":"Reading Comprehension","Detail":"Reading Comprehension",
    "Author tone":"Reading Comprehension","Vocabulary in context":"Reading Comprehension"
  };
  return map[t] || t;
}

function getWeightRows(exam,section,year){
  if(exam!=="CAT") return [];
  const years=year==="all"?["2020","2021","2022"]:[year];
  const agg={};
  years.forEach(y=>{
    const d=WEIGHTAGE_DATA.CAT[y]?.[section]||{};
    Object.entries(d).forEach(([topic,n])=>agg[topic]=(agg[topic]||0)+n);
  });
  return Object.entries(agg).map(([topic,count])=>({topic,count,years:years.length}));
}

function topicUserStat(topic){
  const target=normalizeTopicName(topic);
  let attempted=0,correct=0;
  progress.attempts.forEach(a=>a.details.forEach(d=>{
    if(normalizeTopicName(d.topic)===target && d.answer!==null && d.answer!==undefined){
      attempted++; if(d.correct) correct++;
    }
  }));
  return {attempted,correct,acc:attempted?Math.round(100*correct/attempted):null};
}

function priorityScore(row,maxCount){
  const u=topicUserStat(row.topic);
  const freq=maxCount?row.count/maxCount:0;
  const weakness=u.acc===null?0.45:(100-u.acc)/100;
  return Math.round(100*(0.65*freq+0.35*weakness));
}
function priorityLabel(score){return score>=70?"High":score>=45?"Medium":"Low"}

function renderIntelligence(){
  const exam=$('intelExam').value, sec=$('intelSection').value, year=$('intelYear').value, sort=$('intelSort').value;
  let rows=getWeightRows(exam,sec,year);
  if(exam!=="CAT"){
    $('intelNotice').innerHTML=`<b>${exam} dataset not loaded yet.</b> The page is ready for it, but the PDFs you uploaded support CAT. Add ${exam} source material and it can use the same structure.`;
  } else {
    $('intelNotice').innerHTML=`<b>Source basis:</b> uploaded CAT year-wise chapter-weightage material for 2020–2022. Counts are shown as reported in that source; they are not silently normalised to a single slot.`;
  }
  const max=Math.max(1,...rows.map(r=>r.count));
  rows=rows.map(r=>({...r,user:topicUserStat(r.topic),priority:priorityScore(r,max)}));
  if(sort==="frequency") rows.sort((a,b)=>b.count-a.count);
  if(sort==="priority") rows.sort((a,b)=>b.priority-a.priority);
  if(sort==="accuracy") rows.sort((a,b)=>(a.user.acc??101)-(b.user.acc??101));

  $('intelTopics').textContent=rows.length;
  $('intelQuestions').textContent=rows.reduce((s,r)=>s+r.count,0);
  const attempted=rows.filter(r=>r.user.acc!==null).sort((a,b)=>a.user.acc-b.user.acc);
  $('intelWeakest').textContent=attempted[0]?.topic||'—';
  $('intelWeakestMeta').textContent=attempted[0]?`${attempted[0].user.acc}% accuracy · ${attempted[0].user.attempted} attempted`:'No attempts yet';
  const top=[...rows].sort((a,b)=>b.priority-a.priority)[0];
  $('intelPriority').textContent=top?.topic||'—';

  $('intelTable').innerHTML=rows.length?`<div class="weightage-row head"><div>TOPIC</div><div>QUESTIONS</div><div>YOUR ACC.</div><div>PRIORITY</div><div>ACTION</div></div>`+
    rows.map(r=>`<div class="weightage-row">
      <div class="weightage-topic"><b>${r.topic}</b><small>${year==="all"?"2020–2022 combined":year}</small><div class="freqbar"><span style="width:${Math.round(100*r.count/max)}%"></span></div></div>
      <div><b>${r.count}</b></div>
      <div>${r.user.acc===null?'<span class="pill">No data</span>':`<b>${r.user.acc}%</b><small style="display:block;color:#888">${r.user.attempted} q</small>`}</div>
      <div class="priority-${priorityLabel(r.priority).toLowerCase()}">${priorityLabel(r.priority)}<small style="display:block;color:#888">${r.priority}/100</small></div>
      <div><button class="btn ghost" onclick="window.CAT.practiceTopic('${sec}','${r.topic.replaceAll("'","\\'")}')">Practice</button></div>
    </div>`).join(''):'No data loaded for this filter.';
  drawWeightageChart(rows.slice(0,12));
  renderSourceLibrary();
}

function drawWeightageChart(rows){
  const c=$('weightageCanvas'),ctx=c.getContext('2d'),W=c.width,H=c.height;
  ctx.clearRect(0,0,W,H); if(!rows.length){ctx.fillStyle='#777';ctx.fillText('No data loaded',30,40);return}
  const max=Math.max(...rows.map(r=>r.count)), left=160, barH=18, gap=10;
  ctx.font='11px sans-serif';
  rows.forEach((r,i)=>{
    const y=20+i*(barH+gap);
    ctx.fillStyle='#555';ctx.fillText(r.topic.slice(0,22),10,y+13);
    ctx.fillStyle='#eeeae5';ctx.fillRect(left,y,W-left-45,barH);
    ctx.fillStyle='#e64b33';ctx.fillRect(left,y,(W-left-45)*(r.count/max),barH);
    ctx.fillStyle='#222';ctx.fillText(String(r.count),W-35,y+13);
  });
}
function renderSourceLibrary(){
  $('sourceLibraryTable').innerHTML=`<table class="table"><thead><tr><th>YEAR</th><th>COVERAGE</th><th>TYPE</th><th>STATUS</th></tr></thead><tbody>`+
  SOURCE_LIBRARY.map(x=>`<tr><td><b>${x.year}</b></td><td>${x.coverage}</td><td>${x.type}</td><td><span class="library-status ${x.status==="Loaded"?"ready":"indexed"}">${x.status}</span></td></tr>`).join('')+
  `</tbody></table>`;
}

const progress=load(STORE,{attempts:[]});
let imported=load(IMPORT,[]);
const bank=()=>[...(window.PYQ_BANK||[]),...(window.STARTER_BANK||[]),...(window.PRACTICE_BANK||[]),...imported];

function load(k,f){try{return JSON.parse(localStorage.getItem(k))||f}catch(e){return f}}
function save(){localStorage.setItem(STORE,JSON.stringify(progress))}
function saveImported(){localStorage.setItem(IMPORT,JSON.stringify(imported))}
function pad(n){return String(n).padStart(2,'0')}
function iso(d){return `${d.getFullYear()}-${pad(d.getMonth()+1)}-${pad(d.getDate())}`}
function pretty(d){return d.toLocaleDateString('en-IN',{weekday:'long',day:'numeric',month:'long',year:'numeric'})}
function seeded(str){let h=2166136261;for(let i=0;i<str.length;i++){h^=str.charCodeAt(i);h=Math.imul(h,16777619)}return h>>>0}
function normAnswer(v){return String(v??'').trim().toLowerCase().replace(/[,₹\s]/g,'');}
function isCorrectAnswer(q,ans){if(ans===undefined||ans===null||String(ans).trim()==='')return false;if(q.type==='TITA')return normAnswer(ans)===normAnswer(q.answerText??q.answer);return ans===q.answer}
function scoreQuestion(q,ans){if(ans===undefined||ans===null||String(ans).trim()==='')return 0;if(isCorrectAnswer(q,ans))return 3;return q.type==='TITA'?0:-1}
function attemptFor(date,section){return progress.attempts.filter(a=>a.date===date&&a.section===section).sort((a,b)=>b.ts-a.ts)[0]}
function sectionPool(s){return bank().filter(q=>q.section===s)}

function dailyQuestions(date,section){
 const pool=sectionPool(section); if(!pool.length)return [];
 const seed=seeded(date+section); let arr=[...pool].sort((a,b)=>seeded(a.id+seed)-seeded(b.id+seed));
 if(section==='VARC'||section==='DILR'){
   const anchor=arr[0];
   let same=anchor.sourceType==='PYQ'?pool.filter(q=>q.sourceType==='PYQ'&&q.year===anchor.year&&q.slot===anchor.slot&&(anchor.stimulus?q.stimulus===anchor.stimulus:true)):pool.filter(q=>q.title===anchor.title);
   if(same.length<4&&anchor.sourceType==='PYQ') same=pool.filter(q=>q.sourceType==='PYQ'&&q.year===anchor.year&&q.slot===anchor.slot);
   return same.slice(0,5);
 }
 return arr.slice(0,5);
}
function sourceMix(qs){let m={PYQ:0,RECONSTRUCTED:0,ORIGINAL:0,EXTERNAL:0};qs.forEach(q=>m[q.sourceType]=(m[q.sourceType]||0)+1);return Object.entries(m).filter(x=>x[1]).map(([k,v])=>`${v} ${k}`).join(' · ')}

function nav(view){
 document.querySelectorAll('.view').forEach(v=>v.classList.remove('active'));
 $('view-'+view).classList.add('active'); state.view=view;
 document.querySelectorAll('.nav-item').forEach(x=>x.classList.toggle('active',x.dataset.view===view));
 if(view==='dashboard')renderDashboard();
 if(view==='daily')renderDaily();
 if(view==='topics')renderTopics();
 if(view==='random')renderRandom();
 if(view==='geometry')renderGeometry();
 if(view==='papers')renderPapers();
 if(view==='intelligence')renderIntelligence();
 if(view==='analytics')renderAnalytics();
 if(view==='errors')renderErrors();
 if(view==='history')renderHistory();
 if(view==='weightage')renderWeightage();
 if(view==='sources')renderSources();
 window.scrollTo(0,0);
}
document.querySelectorAll('[data-view]').forEach(b=>b.onclick=()=>nav(b.dataset.view));
document.querySelectorAll('[data-go]').forEach(b=>b.onclick=()=>nav(b.dataset.go));

function metrics(){
 const A=progress.attempts; let correct=0,answered=0;
 A.forEach(a=>{correct+=a.correct;answered+=a.answered});
 let streak=0,d=new Date();
 while(progress.attempts.some(a=>a.date===iso(d))){streak++;d.setDate(d.getDate()-1)}
 return {tests:A.length,answered,accuracy:answered?Math.round(100*correct/answered):0,streak};
}
function renderDashboard(){
 const m=metrics(); $('mStreak').textContent=m.streak;$('mTests').textContent=m.tests;$('mAnswered').textContent=m.answered;$('mAccuracy').textContent=m.accuracy+'%';
 $('dashDate').textContent=pretty(new Date());
 const date=iso(new Date()); const done=sections.filter(s=>attemptFor(date,s)).length,pct=Math.round(done/3*100);
 $('completionPct').textContent=pct+'%';$('completionRing').style.background=`conic-gradient(var(--red) ${pct}%,#3a3a3a ${pct}%)`;
 $('todaySectionCards').innerHTML=sections.map(s=>sectionCard(date,s)).join('');
 drawTrend($('trendCanvas'),progress.attempts.slice(-30));
 renderFocus();
}
function sectionCard(date,s){
 const qs=dailyQuestions(date,s),a=attemptFor(date,s);
 return `<div class="section-card"><span class="badge">${qs[0]?.sourceType||'BANK'}</span><h4>${s}</h4><p>${qs[0]?.title||'No questions loaded'}<br>${sourceMix(qs)}</p><div class="row"><span class="pill ${a?'good':''}">${a?`Score ${a.score}/${a.maxScore}`:'Not attempted'}</span><button class="btn ${a?'ghost':'primary'}" onclick="window.CAT.startDaily('${date}','${s}')">${a?'Attempt again':'Start'}</button></div></div>`
}
function renderFocus(){
 const stats=topicStats(); const items=Object.values(stats).filter(x=>x.attempted>=2).sort((a,b)=>a.acc-b.acc).slice(0,5);
 $('focusList').innerHTML=items.length?items.map(x=>`<div class="focus-item"><strong>${x.topic}</strong><span>${x.acc}% · ${x.attempted} attempted</span></div>`).join(''):`<div class="muted">Complete a few tests and your weakest topics will appear here.</div>`;
}

function renderDaily(){
 $('dailyDate').textContent=pretty(state.selectedDate); const date=iso(state.selectedDate);
 $('dailyCards').innerHTML=`<div class="panel-title"><div><h3>${pretty(state.selectedDate)}</h3><p>Daily allocation</p></div></div>`+sections.map(s=>{
  const qs=dailyQuestions(date,s),a=attemptFor(date,s);
  return `<div class="daily-row"><div class="daily-icon">${a?'✓':s[0]}</div><div><h4>${s} · ${qs[0]?.title||'No questions'}</h4><p>5 questions · 20 min · ${sourceMix(qs)}</p></div><button class="btn ${a?'ghost':'primary'}" onclick="window.CAT.startDaily('${date}','${s}')">${a?'Attempt again':'Start test'}</button></div>`
 }).join('');
 renderCalendar();
}
function renderCalendar(){
 let d=state.calDate,y=d.getFullYear(),m=d.getMonth();$('calMonth').textContent=new Date(y,m,1).toLocaleDateString('en-IN',{month:'long',year:'numeric'});
 let html=['M','T','W','T','F','S','S'].map(x=>`<div class="cal-dow">${x}</div>`).join(''); let first=new Date(y,m,1),offset=(first.getDay()+6)%7;
 for(let i=0;i<offset;i++)html+='<div></div>';
 let last=new Date(y,m+1,0).getDate();
 for(let n=1;n<=last;n++){let x=new Date(y,m,n),ds=iso(x),done=sections.filter(s=>attemptFor(ds,s)).length;
  html+=`<button class="cal-day ${ds===iso(new Date())?'today':''} ${ds===iso(state.selectedDate)?'selected':''} ${done===3?'done':''}" onclick="window.CAT.selectDate('${ds}')">${n}<small>${done?done+'/3':''}</small></button>`
 } $('calendar').innerHTML=html;
}
$('calPrev').onclick=()=>{state.calDate=new Date(state.calDate.getFullYear(),state.calDate.getMonth()-1,1);renderCalendar()}
$('calNext').onclick=()=>{state.calDate=new Date(state.calDate.getFullYear(),state.calDate.getMonth()+1,1);renderCalendar()}

function renderTopics(){
 const sec=$('topicSection').value||'QA'; const topics=[...new Set(sectionPool(sec).map(q=>q.topic))].sort();
 $('topicName').innerHTML=topics.map(t=>`<option>${t}</option>`).join('');
 const st=topicStats();$('topicSummary').innerHTML=topics.map(t=>{let x=st[t];return `<div class="focus-item"><strong>${t}</strong><span>${x?x.acc+'% accuracy · '+x.attempted+' attempted':'No attempts yet'}</span></div>`}).join('');
}
$('topicSection').onchange=renderTopics;
$('topicStart').onclick=()=>{let sec=$('topicSection').value,topic=$('topicName').value,diff=$('topicDifficulty').value;let qs=sectionPool(sec).filter(q=>q.topic===topic&&(diff==='all'||q.difficulty===diff)).slice(0,5);if(!qs.length)return alert('No questions in this filter yet. Import more questions.');startTest({date:iso(new Date()),section:sec,questions:qs,mode:'topic',label:`${sec} · ${topic}`})}


const GEOMETRY_LESSONS=[
 {t:'1. Lines & basic angle language',k:'Point, line, ray, angle; acute/right/obtuse/straight/reflex/full angles.',f:['Straight line = 180°','Around a point = 360°']},
 {t:'2. Angle pairs',k:'Complementary, supplementary and vertically opposite angles.',f:['Complementary sum = 90°','Supplementary sum = 180°','Vertically opposite angles are equal']},
 {t:'3. Parallel lines & transversals',k:'Corresponding, alternate and co-interior angle relationships.',f:['Alternate interior angles are equal','Co-interior angles sum to 180°']},
 {t:'4. Triangle fundamentals',k:'Angle sum, exterior angle, side feasibility and area.',f:['A+B+C=180°','Exterior angle = sum of two remote interior angles','Area = 1/2 bh']},
 {t:'5. Right triangles',k:'Pythagoras, common triples and inradius shortcut.',f:['a²+b²=c²','r=(a+b−c)/2']},
 {t:'6. Angle bisectors & cevians',k:'Internal/external bisectors and proportional division of the opposite side.',f:['BD/DC = AB/AC for an internal angle bisector']},
 {t:'7. Medians & centroid',k:'A median joins a vertex to the opposite midpoint; all three medians meet at the centroid.',f:['Centroid divides each median 2:1 from the vertex']},
 {t:'8. Altitudes & orthocenter',k:'Altitudes are perpendiculars from vertices; their concurrency point is the orthocenter.',f:['Acute triangle: orthocenter inside','Right triangle: at right-angle vertex']},
 {t:'9. Perpendicular bisectors & circumcenter',k:'Perpendicular bisectors meet at the circumcenter, equidistant from vertices.',f:['Right triangle circumcenter = midpoint of hypotenuse']},
 {t:'10. Incenter & incircle',k:'Angle bisectors meet at the incenter, equidistant from all sides.',f:['Area = r×semiperimeter']},
 {t:'11. Similarity & proportionality',k:'Use equal angles / proportional sides to establish similarity and transfer ratios.',f:['Similar triangles: corresponding sides proportional','Areas scale as square of side ratio']},
 {t:'12. Thales & midpoint theorem',k:'A line parallel to one side of a triangle creates proportional segments.',f:['Midpoint connector is parallel to third side and half its length']},
 {t:'13. Quadrilaterals',k:'Core properties of square, rectangle, parallelogram, rhombus and trapezium.',f:['Quadrilateral interior-angle sum = 360°']},
 {t:'14. Parallelograms & rhombi',k:'Opposite sides/angles and diagonal behaviour.',f:['Parallelogram diagonals bisect each other','Rhombus diagonals are perpendicular bisectors']},
 {t:'15. Trapezium',k:'Parallel-side structure, mid-segment and isosceles trapezium properties.',f:['Mid-segment = half the sum of parallel sides']},
 {t:'16. Circle fundamentals',k:'Radius, diameter, chord, secant and tangent.',f:['Diameter is the longest chord','Perpendicular from centre to chord bisects chord']},
 {t:'17. Angles in circles',k:'Same-segment angles, cyclic quadrilaterals and alternate-segment theorem.',f:['Opposite angles of cyclic quadrilateral sum to 180°']},
 {t:'18. Tangents & common tangents',k:'Radius-tangent perpendicularity and equal tangent lengths from an external point.',f:['Radius ⟂ tangent at contact','Tangents from same external point are equal']}
];
function shuffled(a){let x=[...a];for(let i=x.length-1;i>0;i--){let j=Math.floor(Math.random()*(i+1));[x[i],x[j]]=[x[j],x[i]]}return x}
function renderRandom(){
 const all=bank(), pyq=all.filter(q=>q.sourceType==='PYQ').length, pr=all.filter(q=>q.sourceType!=='PYQ').length;
 $('bankBreakdown').innerHTML=`<div><strong>${all.length}</strong><span>Total questions</span></div><div><strong>${pyq}</strong><span>Real CAT PYQ</span></div><div><strong>${pr}</strong><span>Practice / original</span></div><div><strong>${all.filter(q=>q.section==='QA').length}</strong><span>QA</span></div><div><strong>${all.filter(q=>q.section==='DILR').length}</strong><span>DILR</span></div><div><strong>${all.filter(q=>q.section==='VARC').length}</strong><span>VARC</span></div>`;
 const c=Number($('randomCount').value),sec=$('randomSection').value,src=$('randomSource').value;let pool=all.filter(q=>(sec==='ALL'||q.section===sec)&&(src==='ALL'||(src==='PYQ'?q.sourceType==='PYQ':q.sourceType!=='PYQ')));
 $('randomSummary').textContent=`${pool.length} questions available for this filter. ${Math.min(c,pool.length)} will be selected without duplicates.`;
}
function startRandom(){const c=Number($('randomCount').value),sec=$('randomSection').value,src=$('randomSource').value,tv=$('randomTime').value;let pool=bank().filter(q=>(sec==='ALL'||q.section===sec)&&(src==='ALL'||(src==='PYQ'?q.sourceType==='PYQ':q.sourceType!=='PYQ')));if(pool.length<c)return alert(`Only ${pool.length} questions match this filter. Reduce test size or broaden filters.`);let qs=shuffled(pool).slice(0,c);let seconds=tv==='auto'?Math.round(c*100):Number(tv)*60;startTest({date:iso(new Date()),section:sec==='ALL'?'MIXED':sec,questions:qs,mode:'random',label:`Random Test · ${c} questions`,seconds});}
function renderGeometry(){const done=load('catGeometryDoneV1',[]);$('geometryProgress').textContent=Math.round(100*done.length/GEOMETRY_LESSONS.length)+'%';$('geometryModules').innerHTML=GEOMETRY_LESSONS.map((m,i)=>`<article class="lesson-card ${done.includes(i)?'done':''}"><div class="lesson-top"><span class="pill">Module ${i+1}</span><button class="icon-btn" onclick="window.CAT.toggleGeometry(${i})">${done.includes(i)?'✓':'Mark done'}</button></div><h3>${m.t}</h3><p>${m.k}</p><div class="formula-box">${m.f.map(x=>`<span>${x}</span>`).join('')}</div></article>`).join('');}
function toggleGeometry(i){let done=load('catGeometryDoneV1',[]);if(done.includes(i))done=done.filter(x=>x!==i);else done.push(i);localStorage.setItem('catGeometryDoneV1',JSON.stringify(done));renderGeometry();}

function paperQuestions(year,slot,section){return (window.PYQ_BANK||[]).filter(q=>q.year===Number(year)&&q.slot===Number(slot)&&q.section===section)}
function paperCoverage(year){const qs=(window.PYQ_BANK||[]).filter(q=>q.year===year);return {count:qs.length,slots:[...new Set(qs.map(q=>q.slot))].sort(),sections:[...new Set(qs.map(q=>q.section))]}}
function renderPapers(){
 const years=Array.from({length:10},(_,i)=>2016+i); const current=$('paperYear')?.value||String(years.find(y=>paperCoverage(y).count)||2022);
 $('paperYear').innerHTML=years.map(y=>`<option value="${y}" ${String(y)===current?'selected':''}>CAT ${y}</option>`).join('');
 const y=Number($('paperYear').value), cov=paperCoverage(y), slots=cov.slots.length?cov.slots:[1];
 const curSlot=Number($('paperSlot').value||slots[0]); $('paperSlot').innerHTML=slots.map(x=>`<option value="${x}" ${x===curSlot?'selected':''}>Slot ${x}</option>`).join('');
 const sec=$('paperSection').value, slot=Number($('paperSlot').value), qs=paperQuestions(y,slot,sec);
 const sectionCounts=['VARC','DILR','QA'].map(x=>`${x}: ${paperQuestions(y,slot,x).length}`).join(' · ');
 $('paperSelectionSummary').innerHTML=qs.length?`<div class="source-card"><b>CAT ${y} · Slot ${slot} · ${sec}</b><span>${qs.length} scored questions extracted from your uploaded answer-bearing PDF. ${sectionCounts}</span></div>`:`<div class="notice"><b>No scored question bank extracted for CAT ${y} · Slot ${slot} · ${sec}.</b> The source may be missing, link-only, question-only, or lack a machine-readable answer key.</div>`;
 const status={2016:['partial','Source uploaded; answer key not extractable'],2017:['ready','Scored PYQs loaded'],2018:['missing','No full standalone paper supplied'],2019:['ready','Scored PYQs loaded'],2020:['ready','Scored PYQs loaded'],2021:['ready','Scored PYQs loaded'],2022:['ready','Scored PYQs + detailed solutions'],2023:['partial','Uploaded PDF mainly links/index'],2024:['partial','Uploaded PDF mainly links/index'],2025:['partial','Full questions; answers not consistently embedded']};
 $('paperYears').innerHTML=years.map(y=>{const c=paperCoverage(y),st=status[y]||['missing','Not loaded'];return `<div class="year-card ${st[0]}"><strong>${y}</strong><span>${st[1]}</span><small>${c.count?c.count+' scored questions in site':'Not yet score-ready'}</small></div>`}).join('');
}
function startSelectedPaper(){const y=Number($('paperYear').value),slot=Number($('paperSlot').value),section=$('paperSection').value,size=$('paperSize').value;let qs=paperQuestions(y,slot,section);if(!qs.length){alert('This year/slot/section is not score-ready from the uploaded source yet.');return;}if(size!=='full')qs=qs.slice(0,Number(size));const seconds=size==='full'?(y<=2019?3600:2400):1200;startTest({date:`CAT ${y}`,section,questions:qs,mode:'paper',label:`CAT ${y} · Slot ${slot} · ${section}`,seconds});}
if($('paperYear'))$('paperYear').onchange=()=>{renderPapers()};if($('paperSlot'))$('paperSlot').onchange=renderPapers;if($('paperSection'))$('paperSection').onchange=renderPapers;if($('paperStart'))$('paperStart').onclick=startSelectedPaper;

function topicStats(){
 let out={}; progress.attempts.forEach(a=>a.details.forEach(d=>{let t=d.topic||(d.section+' general');if(!out[t])out[t]={topic:t,attempted:0,correct:0};if(d.answer!==null&&d.answer!==undefined){out[t].attempted++;if(d.correct)out[t].correct++}}));
 Object.values(out).forEach(x=>x.acc=x.attempted?Math.round(100*x.correct/x.attempted):0);return out;
}
function secAcc(sec){let d=progress.attempts.filter(a=>a.section===sec),c=d.reduce((s,a)=>s+a.correct,0),n=d.reduce((s,a)=>s+a.answered,0);return n?Math.round(100*c/n):0}
function renderAnalytics(){
 const A=progress.attempts, last=A.slice(-10),prev=A.slice(-20,-10);let acc=x=>{let c=x.reduce((s,a)=>s+a.correct,0),n=x.reduce((s,a)=>s+a.answered,0);return n?Math.round(100*c/n):0};
 let l=acc(last),p=acc(prev);$('aLast10').textContent=l+'%';$('aVsPrev').textContent=prev.length?`${l-p>=0?'+':''}${l-p} pts vs previous 10`:'No baseline yet';
 $('aVarc').textContent=secAcc('VARC')+'%';$('aDilr').textContent=secAcc('DILR')+'%';$('aQa').textContent=secAcc('QA')+'%';
 drawTrend($('analyticsCanvas'),A.slice(-40));
 let stats=Object.values(topicStats()).sort((a,b)=>a.acc-b.acc);
 $('topicReport').innerHTML=stats.length?stats.map(x=>`<div class="topic-line"><div><b>${x.topic}</b><div class="bar"><span style="width:${x.acc}%"></span></div><small>${x.attempted} attempted</small></div><strong>${x.acc}%</strong></div>`).join(''):'Complete tests to build your report.';
}
function drawTrend(canvas,arr){
 const ctx=canvas.getContext('2d'),W=canvas.width,H=canvas.height;ctx.clearRect(0,0,W,H);ctx.strokeStyle='#ded9d2';ctx.lineWidth=1;
 for(let i=0;i<=4;i++){let y=20+i*(H-45)/4;ctx.beginPath();ctx.moveTo(35,y);ctx.lineTo(W-10,y);ctx.stroke()}
 if(!arr.length){ctx.fillStyle='#777';ctx.fillText('No attempts yet',40,60);return}
 let vals=arr.map(a=>a.answered?100*a.correct/a.answered:0), step=(W-55)/Math.max(vals.length-1,1);ctx.strokeStyle='#e64b33';ctx.lineWidth=3;ctx.beginPath();
 vals.forEach((v,i)=>{let x=35+i*step,y=20+(100-v)*(H-45)/100;i?ctx.lineTo(x,y):ctx.moveTo(x,y)});ctx.stroke();
 ctx.fillStyle='#e64b33';vals.forEach((v,i)=>{let x=35+i*step,y=20+(100-v)*(H-45)/100;ctx.beginPath();ctx.arc(x,y,3.5,0,Math.PI*2);ctx.fill()});
 ctx.fillStyle='#777';ctx.font='11px sans-serif';ctx.fillText('100%',2,25);ctx.fillText('0%',12,H-20)
}

function renderErrors(){
 let rows=[];progress.attempts.slice().reverse().forEach(a=>a.details.forEach(d=>{if(!d.correct)rows.push({...d,date:a.date,section:a.section})}));
 $('errorTable').innerHTML=rows.length?`<table class="table"><thead><tr><th>Date</th><th>Section</th><th>Topic</th><th>Question</th><th>Result</th></tr></thead><tbody>${rows.slice(0,100).map(r=>`<tr><td>${r.date}</td><td>${r.section}</td><td>${r.topic}</td><td>${r.question}</td><td><span class="pill bad">${r.answer==null?'Skipped':'Wrong'}</span></td></tr>`).join('')}</tbody></table>`:'No errors yet.';
}
function renderHistory(){
 let A=progress.attempts.slice().reverse();$('historyTable').innerHTML=A.length?`<table class="table"><thead><tr><th>Date</th><th>Section</th><th>Score</th><th>Accuracy</th><th>Time</th><th>Source</th></tr></thead><tbody>${A.map(a=>`<tr><td>${a.date}</td><td>${a.section}</td><td>${a.score}/${a.maxScore}</td><td>${a.answered?Math.round(100*a.correct/a.answered):0}%</td><td>${Math.round(a.timeSec/60)} min</td><td>${a.sourceMix}</td></tr>`).join('')}</tbody></table>`:'No attempts yet.';
}

function normalTopic(s){return (s||'').toLowerCase().replace(/&/g,'and').replace(/[^a-z0-9]+/g,' ').trim()}
function topicQuestions(section,topic){
 const t=normalTopic(topic); return bank().filter(q=>q.section===section&&(normalTopic(q.topic)===t||normalTopic(q.title).includes(t)||t.includes(normalTopic(q.topic))));
}
function weightRows(){
 const exam=$('examSelect')?.value||'CAT', sec=$('weightSection')?.value||'ALL', yr=$('weightYear')?.value||'ALL', search=($('weightSearch')?.value||'').toLowerCase();
 let rows=(window.EXAM_WEIGHTAGE?.[exam]||[]).filter(r=>(sec==='ALL'||r.section===sec)&&(yr==='ALL'||String(r.year)===yr)&&(!search||r.topic.toLowerCase().includes(search)));
 if(yr==='ALL'){
   const map={}; rows.forEach(r=>{const k=r.section+'|'+r.topic;if(!map[k])map[k]={section:r.section,topic:r.topic,count:0,years:0,year:'2020–2022'};map[k].count+=r.count;map[k].years++});
   rows=Object.values(map).map(r=>({...r,avg:Math.round(r.count/r.years*10)/10}));
 } else rows=rows.map(r=>({...r,avg:r.count}));
 return rows.sort((a,b)=>b.avg-a.avg||a.topic.localeCompare(b.topic));
}
function renderWeightage(){
 const exam=$('examSelect').value, rows=weightRows();
 $('examDataNotice').innerHTML=exam==='CAT'?`<b>CAT data loaded:</b> 2020–2022 chapter/question counts from your uploaded Careers360 weightage PDF. Select a row to see practice questions.`:`<b>${exam}:</b> no verified weightage source has been loaded yet. Add a source before using this exam for planning.`;
 $('weightSubtitle').textContent=$('weightYear').value==='ALL'?'Average question count across available 2020–2022 source data.':'Question count in selected source year.';
 if(!rows.length){$('weightageTable').innerHTML='<div class="empty-state">No sourced data for this filter yet.</div>';$('priorityList').innerHTML='';$('weightQuestionHub').innerHTML='<div class="empty-state">Select CAT or import more sourced data.</div>';return}
 const max=Math.max(...rows.map(r=>r.avg));
 $('weightageTable').innerHTML=`<table class="table weight-table"><thead><tr><th>Section</th><th>Topic / question type</th><th>${$('weightYear').value==='ALL'?'Avg. count':'Questions'}</th><th>Relative weight</th><th>Practice</th></tr></thead><tbody>${rows.map((r,i)=>`<tr class="weight-row" data-section="${r.section}" data-topic="${r.topic.replace(/"/g,'&quot;')}"><td><span class="pill">${r.section}</span></td><td><b>${r.topic}</b><small>${r.year}</small></td><td><strong>${r.avg}</strong></td><td><div class="weight-bar"><span style="width:${Math.round(100*r.avg/max)}%"></span></div></td><td><button class="btn ghost mini-practice" data-section="${r.section}" data-topic="${r.topic.replace(/"/g,'&quot;')}">Questions</button></td></tr>`).join('')}</tbody></table>`;
 $('priorityList').innerHTML=rows.slice(0,8).map((r,i)=>`<div class="focus-item"><strong>${i+1}. ${r.topic}</strong><span>${r.section} · ${r.avg} ${$('weightYear').value==='ALL'?'avg':'questions'}</span></div>`).join('');
 document.querySelectorAll('.mini-practice,.weight-row').forEach(el=>el.onclick=e=>{if(e.target.closest('.mini-practice')||el.classList.contains('weight-row'))showWeightQuestions(el.dataset.section||el.closest('.weight-row')?.dataset.section,el.dataset.topic||el.closest('.weight-row')?.dataset.topic)});
 showWeightQuestions(rows[0].section,rows[0].topic);
}
function showWeightQuestions(section,topic){
 const qs=topicQuestions(section,topic);
 let stats=topicStats()[topic], perf=stats?`${stats.acc}% accuracy from ${stats.attempted} attempts`:'No attempts yet';
 $('weightQuestionHub').innerHTML=`<div class="hub-head"><div><span class="pill">${section}</span><h3>${topic}</h3><p>${perf}</p></div>${qs.length?`<button class="btn primary" id="hubStart">Start ${Math.min(5,qs.length)} questions</button>`:''}</div>${qs.length?`<div class="question-chip-list">${qs.slice(0,12).map(q=>`<div class="question-chip"><span class="pill ${q.sourceType==='PYQ'?'good':''}">${q.sourceType}</span><b>${q.title}</b><small>${q.difficulty} · ${q.sourceLabel}</small></div>`).join('')}`:`<div class="empty-state">No tagged question in your current bank for this exact topic yet. When you import PYQs/practice questions with topic = “${topic}”, they will appear here automatically.</div>`}`;
 if(qs.length)$('hubStart').onclick=()=>startTest({date:iso(new Date()),section,questions:qs.slice(0,5),mode:'weightage',label:`${section} · ${topic}`});
}
['examSelect','weightSection','weightYear'].forEach(id=>{const el=$(id);if(el)el.onchange=renderWeightage});
if($('weightSearch'))$('weightSearch').oninput=renderWeightage;

function renderSources(){
 $('schemaPreview').textContent=JSON.stringify({
"id":"Q-CAT-2024-S1-001","section":"QA","type":"MCQ","topic":"Arithmetic","difficulty":"Medium","sourceType":"PYQ","sourceLabel":"CAT 2024 Slot 1","sourceUrl":"https://source.example","year":2024,"slot":1,"title":"Question title","stimulus":"","question":"Question text","options":["A","B","C","D"],"answer":0,"explanation":"Your explanation","howToThink":"Tactical approach"},null,2);
 $('importStatus').textContent=`Starter bank: ${window.STARTER_BANK.length} questions · Imported: ${imported.length} questions · Total: ${bank().length}`;
}
$('bankImport').onchange=e=>{let f=e.target.files[0];if(!f)return;let r=new FileReader();r.onload=()=>{try{let x=JSON.parse(r.result);if(!Array.isArray(x))throw new Error('JSON must be an array');let need=['id','section','question','answer'];for(let q of x)for(let k of need)if(q[k]===undefined)throw new Error(`Missing ${k}`);imported=x;saveImported();renderSources();alert(`Imported ${x.length} questions.`)}catch(err){alert('Import failed: '+err.message)}};r.readAsText(f)}
$('clearImported').onclick=()=>{if(confirm('Clear imported question bank from this browser?')){imported=[];saveImported();renderSources()}}

function startTest(t){
 clearInterval(state.timer);state.test=t;state.answers={};state.seconds=t.seconds||1200;state.startedAt=Date.now();
 $('testMeta').textContent=`${t.section} · ${t.date}`;$('testName').textContent=t.label||`${t.section} Daily Test`;
 $('testSourceLine').textContent=sourceMix(t.questions);$('stimulus').innerHTML='';
 $('questionArea').innerHTML=t.questions.map((q,i)=>{const showStim=q.stimulus&&(i===0||q.stimulus!==t.questions[i-1]?.stimulus);const answerUI=(q.options&&q.options.length)?q.options.map((o,j)=>`<div class="option" data-q="${i}" data-o="${j}" onclick="window.CAT.pick(${i},${j},this)">${String.fromCharCode(65+j)}. ${o}</div>`).join(''):`<input class="tita-input" data-tita="${i}" placeholder="Type your answer" oninput="window.CAT.pickTita(${i},this.value)">`;return `<div class="question-card">${showStim?`<div class="stimulus"><p>${q.stimulus}</p></div>`:''}<div class="qmeta">QUESTION ${i+1} OF ${t.questions.length} · ${q.type} · ${q.sourceLabel||q.topic}</div><h3>${q.question}</h3>${answerUI}<div class="q-source">${q.sourceLabel||''}</div></div>`}).join('');
 updateProgress();nav('test');renderTimer();state.timer=setInterval(()=>{state.seconds--;renderTimer();if(state.seconds<=0){clearInterval(state.timer);submitTest()}},1000);
}
function renderTimer(){let m=Math.floor(state.seconds/60),s=state.seconds%60;$('timer').textContent=`${pad(m)}:${pad(s)}`}
function updateProgress(){if(!state.test)return;$('testProgress').style.width=(100*Object.keys(state.answers).length/state.test.questions.length)+'%'}
function pick(i,j,el){state.answers[i]=j;document.querySelectorAll(`[data-q="${i}"]`).forEach(x=>x.classList.remove('selected'));el.classList.add('selected');updateProgress()}
function pickTita(i,v){if(String(v).trim()==='')delete state.answers[i];else state.answers[i]=v;updateProgress()}
function submitTest(){
 if(!state.test)return;clearInterval(state.timer);let t=state.test,correct=0,answered=0,wrong=0,score=0;
 let details=t.questions.map((q,i)=>{let ans=state.answers[i],ok=isCorrectAnswer(q,ans);if(ans!==undefined&&ans!==null&&String(ans).trim()!==''){answered++;if(ok)correct++;else wrong++}score+=scoreQuestion(q,ans);const userText=q.type==='TITA'?(ans===undefined?null:ans):(ans===undefined?null:q.options[ans]);const correctText=q.type==='TITA'?(q.answerText??q.answer):(q.options[q.answer]??q.answerText??q.answer);return{id:q.id,section:q.section,topic:q.topic,question:q.question,answer:ans===undefined?null:ans,answerText:userText,correctAnswer:q.answer,correctText,correct:ok,explanation:q.explanation,howToThink:q.howToThink,sourceLabel:q.sourceLabel,difficulty:q.difficulty}});
 let a={id:Date.now(),ts:Date.now(),date:t.date,section:t.section,mode:t.mode||'daily',score,maxScore:t.questions.length*3,correct,wrong,skipped:t.questions.length-answered,answered,timeSec:Math.min(t.seconds||1200,Math.round((Date.now()-state.startedAt)/1000)),sourceMix:sourceMix(t.questions),details};
 progress.attempts.push(a);save();renderResult(a);nav('result');
}
function renderResult(a){
 $('resultTitle').textContent=`${a.section} · ${a.date}`;$('resultSubtitle').textContent=`${a.details.length} questions · ${a.sourceMix}`;
 $('scoreValue').textContent=a.score;$('scoreMax').textContent=`/ ${a.maxScore} marks`;$('scoreBar').style.width=Math.max(0,100*a.score/a.maxScore)+'%';$('scorePct').textContent=`${Math.round(100*a.score/a.maxScore)}% of maximum marks`;
 $('rCorrect').textContent=a.correct;$('rWrong').textContent=a.wrong;$('rSkipped').textContent=a.skipped;$('rAccuracy').textContent=(a.answered?Math.round(100*a.correct/a.answered):0)+'%';$('rTime').textContent=Math.round(a.timeSec/60)+' min';
 let prev=progress.attempts.filter(x=>x.section===a.section&&x.id!==a.id).slice(-10),avg=prev.length?prev.reduce((s,x)=>s+x.score,0)/prev.length:null;$('rVsAvg').textContent=avg===null?'—':`${a.score-avg>=0?'+':''}${(a.score-avg).toFixed(1)}`;
 $('reviewArea').innerHTML=a.details.map((d,i)=>`<div class="review-card"><span class="pill ${d.correct?'good':'bad'}">${d.correct?'Correct':d.answer==null?'Skipped':'Wrong'}</span><h4>Q${i+1}. ${d.question}</h4><div class="review-answer">Your answer: <span class="${d.correct?'correct-option':'wrong-option'}">${d.answerText||'Skipped'}</span></div><div class="review-answer">Correct answer: <span class="correct-option">${d.correctText}</span></div><div class="review-explain"><b>Explanation</b><br>${d.explanation}</div><div class="review-explain thinking"><b>How to think</b><br>${d.howToThink}</div><div class="review-answer">Source: ${d.sourceLabel}</div></div>`).join('');
}
$('testSubmit').onclick=submitTest;$('testExit').onclick=()=>{clearInterval(state.timer);nav('daily')};$('printResult').onclick=()=>window.print();$('retryTest').onclick=()=>{if(state.test)startTest(state.test)};
$('exportBtn').onclick=()=>{let blob=new Blob([JSON.stringify(progress,null,2)],{type:'application/json'}),a=document.createElement('a');a.href=URL.createObjectURL(blob);a.download='cat-mastery-progress.json';a.click();URL.revokeObjectURL(a.href)}
$('progressImport').onchange=e=>{let f=e.target.files[0];if(!f)return;let r=new FileReader();r.onload=()=>{try{let x=JSON.parse(r.result);if(!Array.isArray(x.attempts))throw new Error('Invalid progress file');progress.attempts=x.attempts;save();renderDashboard();alert('Progress imported.')}catch(err){alert(err.message)}};r.readAsText(f)}

if($('randomStart'))$('randomStart').onclick=startRandom;['randomCount','randomSection','randomSource'].forEach(id=>{const el=$(id);if(el)el.onchange=renderRandom});if($('geometryPractice'))$('geometryPractice').onclick=()=>{let qs=shuffled(bank().filter(q=>q.section==='QA'&&normalTopic(q.topic).includes('geometry'))).slice(0,25);startTest({date:iso(new Date()),section:'QA',questions:qs,mode:'geometry',label:'Geometry Practice · 25 questions',seconds:2500});};

['intelExam','intelSection','intelYear','intelSort'].forEach(id=>{const el=$(id); if(el) el.onchange=renderIntelligence;});

window.CAT={toggleGeometry,pickTita,startSelectedPaper,startDaily:(date,section)=>startTest({date,section,questions:dailyQuestions(date,section),mode:'daily',label:`Daily ${section}`}),
practiceTopic:(section,topic)=>{let qs=sectionPool(section).filter(q=>normalizeTopicName(q.topic)===normalizeTopicName(topic)).slice(0,5);if(!qs.length){alert('No publishable questions for this topic are bundled yet. Import a question bank or use Topic Practice after adding questions.');return;}startTest({date:iso(new Date()),section,questions:qs,mode:'topic',label:`${section} · ${topic}`})},
pick,selectDate:ds=>{let [y,m,d]=ds.split('-').map(Number);state.selectedDate=new Date(y,m-1,d);renderDaily()}};
$('todayLabel').textContent=' · '+pretty(new Date()); state.selectedDate=new Date();state.calDate=new Date(); renderDashboard(); renderTopics();
})();