// Taalknop NL/EN + mobiel menu - geen frameworks, geen onderhoud
(function(){
  var saved = localStorage.getItem('lang');
  if(saved === 'en'){ document.body.classList.add('en'); document.documentElement.lang='en'; }
  var btn = document.getElementById('langbtn');
  function label(){ btn.textContent = document.body.classList.contains('en') ? 'NL' : 'EN'; }
  if(btn){
    label();
    btn.addEventListener('click', function(){
      document.body.classList.toggle('en');
      var en = document.body.classList.contains('en');
      document.documentElement.lang = en ? 'en' : 'nl';
      localStorage.setItem('lang', en ? 'en' : 'nl');
      label();
    });
  }
  var nav = document.querySelector('.nav');
  var mb = document.getElementById('menubtn');
  if(mb && nav){
    mb.addEventListener('click', function(){
      nav.classList.toggle('open');
      mb.textContent = nav.classList.contains('open') ? '✕' : '☰';
    });
    nav.querySelectorAll('a:not(.logo)').forEach(function(a){
      a.addEventListener('click', function(){
        nav.classList.remove('open');
        mb.textContent = '☰';
      });
    });
  }
})();
