var fuse;
var showButton = document.getElementById("search-button");
var showButtonMobile = document.getElementById("search-button-mobile");
var hideButton = document.getElementById("close-search-button");
var wrapper = document.getElementById("search-wrapper");
var modal = document.getElementById("search-modal");
var input = document.getElementById("search-query");
var output = document.getElementById("search-results");
var first = null;
var last = null;
var searchVisible = false;
var indexed = false;
var indexing = false;
var hasResults = false;
var pendingTerm = "";

var messages = {
  idle: "Escribí al menos 2 letras para buscar.",
  loading: "Preparando búsqueda…",
  noResults: "No encontramos resultados.",
  error: "No se pudo cargar la búsqueda."
};

if (showButton) showButton.addEventListener("click", displaySearch);
if (showButtonMobile) showButtonMobile.addEventListener("click", displaySearch);
if (hideButton) hideButton.addEventListener("click", hideSearch);
if (wrapper) wrapper.addEventListener("click", hideSearch);
if (modal) {
  modal.addEventListener("click", function (event) {
    event.stopPropagation();
    event.stopImmediatePropagation();
    return false;
  });
}

document.addEventListener("keydown", function (event) {
  if (!wrapper || !input || !output) return;

  if (event.key === "/") {
    var active = document.activeElement;
    var tag = active && active.tagName;
    var isInputField = tag === "INPUT" || tag === "TEXTAREA" || (active && active.isContentEditable);

    if (!searchVisible && !isInputField) {
      event.preventDefault();
      displaySearch();
    }
  }

  if (event.key === "Escape") hideSearch();

  if (event.key === "ArrowDown") {
    if (searchVisible && hasResults) {
      event.preventDefault();
      if (document.activeElement === input) {
        first.focus();
      } else if (document.activeElement === last) {
        last.focus();
      } else if (document.activeElement.parentElement && document.activeElement.parentElement.nextSibling) {
        document.activeElement.parentElement.nextSibling.firstElementChild.focus();
      }
    }
  }

  if (event.key === "ArrowUp") {
    if (searchVisible && hasResults) {
      event.preventDefault();
      if (document.activeElement === input || document.activeElement === first) {
        input.focus();
      } else if (document.activeElement.parentElement && document.activeElement.parentElement.previousSibling) {
        document.activeElement.parentElement.previousSibling.firstElementChild.focus();
      }
    }
  }

  if (event.key === "Enter") {
    if (searchVisible && hasResults) {
      event.preventDefault();
      if (document.activeElement === input) first.focus();
      else document.activeElement.click();
    }
  }
});

if (input) {
  input.onkeyup = function () {
    executeQuery(this.value);
  };
}

function displaySearch() {
  if (!wrapper || !input || !output) return;
  if (!indexed && !indexing) buildIndex();
  if (!searchVisible) {
    document.body.style.overflow = "hidden";
    wrapper.style.visibility = "visible";
    input.focus();
    searchVisible = true;
    if (!input.value) renderMessage(indexed ? messages.idle : messages.loading);
  }
}

function hideSearch() {
  if (!wrapper || !input || !output) return;
  if (searchVisible) {
    document.body.style.overflow = "visible";
    wrapper.style.visibility = "hidden";
    input.value = "";
    output.innerHTML = "";
    hasResults = false;
    if (document.activeElement) document.activeElement.blur();
    searchVisible = false;
  }
}

function renderMessage(message) {
  output.innerHTML = '<li class="px-3 py-4 text-sm text-neutral-500 dark:text-neutral-400">' + message + '</li>';
  hasResults = false;
}

function escapeHTML(value) {
  return String(value || "")
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#039;");
}

function truncate(value, length) {
  value = String(value || "").replace(/\s+/g, " ").trim();
  if (value.length <= length) return value;
  return value.slice(0, length).replace(/\s+\S*$/, "") + "…";
}

function fetchJSON(path, callback, errorCallback) {
  var httpRequest = new XMLHttpRequest();
  httpRequest.onreadystatechange = function () {
    if (httpRequest.readyState === 4) {
      if (httpRequest.status === 200) {
        var data = JSON.parse(httpRequest.responseText);
        if (callback) callback(data);
      } else if (errorCallback) {
        errorCallback();
      }
    }
  };
  httpRequest.open("GET", path);
  httpRequest.send();
}

function buildIndex() {
  indexing = true;
  var baseURL = wrapper.getAttribute("data-url");
  baseURL = baseURL.replace(/\/?$/, "/");
  fetchJSON(baseURL + "index.json", function (data) {
    var options = {
      shouldSort: true,
      ignoreLocation: true,
      ignoreDiacritics: true,
      threshold: 0.28,
      minMatchCharLength: 2,
      includeMatches: false,
      keys: [
        { name: "title", weight: 0.9 },
        { name: "section", weight: 0.25 },
        { name: "summary", weight: 0.65 },
        { name: "content", weight: 0.35 }
      ]
    };
    fuse = new Fuse(data, options);
    indexed = true;
    indexing = false;
    if (searchVisible) executeQuery(pendingTerm || input.value);
  }, function () {
    indexing = false;
    renderMessage(messages.error);
  });
}

function executeQuery(term) {
  if (!output) return;
  term = String(term || "").trim();
  pendingTerm = term;

  if (term.length < 2) {
    renderMessage(indexed ? messages.idle : messages.loading);
    return;
  }

  if (!indexed || !fuse) {
    renderMessage(messages.loading);
    if (!indexing) buildIndex();
    return;
  }

  var results = fuse.search(term, { limit: 20 });
  var resultsHTML = "";

  if (results.length > 0) {
    results.forEach(function (value) {
      var item = value.item;
      var summary = truncate(item.summary || item.content || "", 180);
      var title = item.externalUrl
        ? escapeHTML(item.title) + '<span class="text-xs ml-2 align-center cursor-default text-neutral-400 dark:text-neutral-500">' + escapeHTML(item.externalUrl) + '</span>'
        : escapeHTML(item.title);
      var linkconfig = item.externalUrl
        ? 'target="_blank" rel="noopener" href="' + escapeHTML(item.externalUrl) + '"'
        : 'href="' + escapeHTML(item.permalink) + '"';

      resultsHTML +=
        '<li class="mb-2">' +
          '<a class="flex items-center px-3 py-2 rounded-md appearance-none bg-neutral-100 dark:bg-neutral-700 focus:bg-primary-100 hover:bg-primary-100 dark:hover:bg-primary-900 dark:focus:bg-primary-900 focus:outline-dotted focus:outline-transparent focus:outline-2" ' + linkconfig + ' tabindex="0">' +
            '<div class="grow">' +
              '<div class="-mb-1 text-lg font-bold">' + title + '</div>' +
              '<div class="text-sm text-neutral-500 dark:text-neutral-400">' + escapeHTML(item.section || "") + '<span class="px-2 text-primary-500">&middot;</span>' + escapeHTML(item.date || "") + '</div>' +
              (summary ? '<div class="text-sm italic">' + escapeHTML(summary) + '</div>' : '') +
            '</div>' +
            '<div class="ml-2 ltr:block rtl:hidden text-neutral-500">&rarr;</div>' +
            '<div class="mr-2 ltr:hidden rtl:block text-neutral-500">&larr;</div>' +
          '</a>' +
        '</li>';
    });
    hasResults = true;
  } else {
    renderMessage(messages.noResults);
    return;
  }

  output.innerHTML = resultsHTML;
  first = output.firstChild ? output.firstChild.firstElementChild : null;
  last = output.lastChild ? output.lastChild.firstElementChild : null;
}
