/*
  Shared site JS
  ----------------
  This file contains the small scroll handler that hides the header when the
  user scrolls down twice and shows it when they scroll up twice. It matches
  the behavior previously inlined in `landing.html` but now it's shared across
  all pages.
*/
(function () {
  const header = document.getElementById('site-header');
  if (!header) return; // nothing to do if the header isn't present

  let lastY = window.scrollY || 0;
  let downCount = 0;
  let upCount = 0;
  const THRESHOLD = 2; // number of consecutive scroll events before toggle

  window.addEventListener('scroll', function () {
    const y = window.scrollY || 0;

    if (y > lastY) {
      // scrolling down
      downCount++;
      upCount = 0;
    } else if (y < lastY) {
      // scrolling up
      upCount++;
      downCount = 0;
    }

    if (downCount >= THRESHOLD) {
      header.classList.add('header-hidden');
    } else if (upCount >= THRESHOLD) {
      header.classList.remove('header-hidden');
    }

    lastY = y;
  }, { passive: true });
  
  // USER MENU: toggle a small dropdown when the "Hello {username}" item is clicked
  const userTrigger = document.getElementById('user-trigger');
  const userMenu = document.getElementById('user-menu');
  if (userTrigger && userMenu) {
    userTrigger.addEventListener('click', function (ev) {
      ev.preventDefault();
      const isOpen = userMenu.style.display === 'block';
      userMenu.style.display = isOpen ? 'none' : 'block';
    });

    // close when clicking outside
    document.addEventListener('click', function (ev) {
      if (!userMenu.contains(ev.target) && ev.target !== userTrigger) {
        userMenu.style.display = 'none';
      }
    });

    // close on Escape key
    document.addEventListener('keydown', function (ev) {
      if (ev.key === 'Escape') userMenu.style.display = 'none';
    });
  }

})();
