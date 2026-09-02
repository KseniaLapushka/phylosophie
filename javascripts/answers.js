// Автосохранение ответов на домашние задания в localStorage браузера.
// Работает только локально, в этом браузере/устройстве — сервера и базы
// данных у сайта нет, это просто статические файлы на GitHub Pages.

function initAnswerFields() {
  var page = window.location.pathname;

  document.querySelectorAll(".answer-box").forEach(function (el) {
    if (el.dataset.answerInit) return;
    el.dataset.answerInit = "1";

    var key = "phylosophie:answer:" + page + ":" + el.dataset.key;
    var saved = localStorage.getItem(key);
    if (saved) el.value = saved;

    var status = el.parentElement.querySelector(".save-status");
    var timer;
    el.addEventListener("input", function () {
      if (status) status.textContent = "сохраняю…";
      clearTimeout(timer);
      timer = setTimeout(function () {
        localStorage.setItem(key, el.value);
        if (status) status.textContent = "сохранено";
      }, 400);
    });
  });

  document.querySelectorAll(".hw-check input[type=checkbox]").forEach(function (cb) {
    if (cb.dataset.checkInit) return;
    cb.dataset.checkInit = "1";

    var item = cb.closest(".hw-item");
    var key = "phylosophie:check:" + page + ":" + (item ? item.dataset.key : "");
    var saved = localStorage.getItem(key);
    if (saved === "1") cb.checked = true;

    cb.addEventListener("change", function () {
      localStorage.setItem(key, cb.checked ? "1" : "0");
    });
  });
}

// Заголовок "Конспекты по философии" в шапке должен вести на главную —
// мы прячем стандартный логотип Material (.md-logo), но у него уже есть
// правильная ссылка на корень сайта. Просто переносим клик на заголовок.
function initTitleLink() {
  var title = document.querySelector(".md-header__title");
  var logo = document.querySelector(".md-header__button.md-logo");
  if (!title || !logo || title.dataset.linked) return;
  title.dataset.linked = "1";
  title.style.cursor = "pointer";
  title.addEventListener("click", function () {
    window.location.href = logo.getAttribute("href");
  });
}

// Material использует "instant navigation" (переход между страницами без
// полной перезагрузки) — document$ это специальный поток Material,
// который срабатывает при каждом переходе, а не только при первой загрузке.
if (window.document$) {
  document$.subscribe(initAnswerFields);
  document$.subscribe(initTitleLink);
} else {
  document.addEventListener("DOMContentLoaded", initAnswerFields);
  document.addEventListener("DOMContentLoaded", initTitleLink);
}
