() => {
  const out=[];
  document.querySelectorAll('.journeys,.stories,.model,.claims,.steps,.three,.grid-2,.grid-3,.grid-4,.figures,.spine,.thread,.deliv').forEach(g=>{
    const kids=[...g.children].filter(k=>k.offsetParent!==null && !k.classList.contains('face-wide'));
    const rows={};
    kids.forEach(k=>{
      const r=k.getBoundingClientRect();
      const leaves=[...k.querySelectorAll('*')].filter(e=>e.getClientRects().length && (e.children.length===0||e.tagName==='IMG'||e.tagName==='SVG'));
      const bottom=leaves.length?Math.max(...leaves.map(e=>e.getBoundingClientRect().bottom)):r.bottom;
      const key=Math.round(r.top);(rows[key]=rows[key]||[]).push({h:Math.round(bottom-r.top),t:(k.querySelector('h3,h4,b,.what,.fig')||k).innerText.replace(/\s+/g,' ').slice(0,26)});
    });
    Object.values(rows).forEach(row=>{ if(row.length<2) return; const hs=row.map(x=>x.h); const d=Math.max(...hs)-Math.min(...hs);
      if(d>20) out.push({sel:g.className.split(' ').slice(0,2).join('.'), diff:d, items:row.map(x=>x.h+' '+x.t)}); });
  });
  return out;
}
