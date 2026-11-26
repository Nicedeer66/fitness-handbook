(function(){
  var root=document.documentElement, pages=[].slice.call(document.querySelectorAll('.page'));
  var ids=pages.map(function(p){return p.id});
  var links=[].slice.call(document.querySelectorAll('.nav a.nl'));
  var crumb=document.getElementById('crumb');
  function store(k,v){try{if(v===undefined)return localStorage.getItem(k);localStorage.setItem(k,v)}catch(e){return null}}
  function show(id,keepScroll){
    if(ids.indexOf(id)<0)id='home';
    pages.forEach(function(p){p.hidden=(p.id!==id)});
    links.forEach(function(a){a.classList.toggle('on',a.getAttribute('href')==='#'+id)});
    var cur=document.getElementById(id);
    if(crumb&&cur)crumb.textContent=cur.getAttribute('data-title')||'';
    root.classList.remove('open');
    if(!keepScroll){ if(root.classList.contains('all')&&cur){cur.scrollIntoView()} else {window.scrollTo(0,0); setTimeout(function(){window.scrollTo(0,0)},0)} }
    store('fit-handbook-page',id);
  }
  function route(first){
    var h=(location.hash||'').replace('#','');
    if(!h&&first){var last=store('fit-handbook-page'); if(last&&ids.indexOf(last)>=0){h=last}}
    show(h||'home',first&&!location.hash);
  }
  window.addEventListener('hashchange',function(){route(false)});
  route(true);
  var mb=document.getElementById('menu-btn'), sc=document.getElementById('scrim');
  if(mb)mb.addEventListener('click',function(){root.classList.toggle('open')});
  if(sc)sc.addEventListener('click',function(){root.classList.remove('open')});
  var ab=document.getElementById('all-btn');
  if(ab)ab.addEventListener('click',function(){
    var on=root.classList.toggle('all'); ab.textContent=on?'回到分章阅读':'展开全书（便于搜索）';
    if(!on)route(false);
  });
  document.addEventListener('click',function(e){
    var a=e.target.closest&&e.target.closest('sup.cite a'); if(!a)return;
    e.preventDefault();
    var li=document.getElementById(a.getAttribute('data-t')); if(!li)return;
    li.scrollIntoView({block:'center'}); li.classList.add('flash');
    setTimeout(function(){li.classList.remove('flash')},1600);
  });
})();
