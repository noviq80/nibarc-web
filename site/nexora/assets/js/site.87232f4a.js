(function () {
  var t = document.querySelector('.nav-toggle');
  var n = document.querySelector('.nav');
  if (t && n) {
    t.addEventListener('click', function () {
      var open = n.classList.toggle('open');
      t.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
  }
  // Mark the current page in the nav.
  var here = location.pathname.replace(/\/index\.html$/, '/').replace(/\.html$/, '');
  document.querySelectorAll('.nav a').forEach(function (a) {
    var href = a.getAttribute('href').replace(/\.html$/, '');
    if (href === here || (here === '/' && href === '/')) a.setAttribute('aria-current', 'page');
  });
})();
