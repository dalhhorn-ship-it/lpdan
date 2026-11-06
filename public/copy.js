/* Progressive enhancement: copy buttons. Without JS (or without clipboard) they stay hidden. */
(function () {
  if (!navigator.clipboard) return;
  document.documentElement.classList.add('js');
  var status = document.createElement('div');
  status.className = 'sr';
  status.setAttribute('role', 'status');
  status.setAttribute('aria-live', 'polite');
  document.body.appendChild(status);
  document.addEventListener('click', function (e) {
    var b = e.target.closest('.copy');
    if (!b) return;
    var txt = b.getAttribute('data-copy');
    if (!txt) return;
    clearTimeout(b._t);
    navigator.clipboard.writeText(txt).then(function () {
      b.textContent = 'copied';
      b.classList.add('done');
      status.textContent = 'Copied';
      b._t = setTimeout(function () {
        b.textContent = 'copy';
        b.classList.remove('done');
        status.textContent = '';
      }, 1600);
    }, function () { status.textContent = 'Copy failed'; });
  });
})();
