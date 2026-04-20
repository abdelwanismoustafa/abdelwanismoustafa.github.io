(function () {
  function initPublicationFilters() {
    var browser = document.querySelector('.pub-browser');
    if (!browser) {
      return;
    }

    var buttons = Array.prototype.slice.call(browser.querySelectorAll('.filter-chip'));
    var records = Array.prototype.slice.call(browser.querySelectorAll('.pub-record'));
    var sections = Array.prototype.slice.call(browser.querySelectorAll('.pub-section'));
    var searchInput = browser.querySelector('#pub-search');
    var emptyState = browser.querySelector('.pub-empty-state');

    var state = {
      type: 'all',
      theme: 'all',
      query: ''
    };

    function setActiveButton(group, value) {
      buttons.forEach(function (button) {
        if (button.getAttribute('data-filter-group') === group) {
          var active = button.getAttribute('data-filter-value') === value;
          button.classList.toggle('is-active', active);
          button.setAttribute('aria-pressed', active ? 'true' : 'false');
        }
      });
    }

    function applyFilters() {
      var visibleCount = 0;

      records.forEach(function (record) {
        var type = record.getAttribute('data-type') || '';
        var themes = record.getAttribute('data-themes') || '';
        var searchBlob = (record.getAttribute('data-search') || '').toLowerCase();

        var matchesType = state.type === 'all' || type === state.type;
        var matchesTheme = state.theme === 'all' || themes.split(/\s+/).indexOf(state.theme) !== -1;
        var matchesQuery = state.query === '' || searchBlob.indexOf(state.query) !== -1;

        var visible = matchesType && matchesTheme && matchesQuery;
        record.hidden = !visible;
        record.classList.toggle('is-hidden', !visible);

        if (visible) {
          visibleCount += 1;
        }
      });

      sections.forEach(function (section) {
        var hasVisibleRecord = section.querySelector('.pub-record:not([hidden])');
        section.hidden = !hasVisibleRecord;
      });

      if (emptyState) {
        emptyState.hidden = visibleCount !== 0;
      }
    }

    buttons.forEach(function (button) {
      button.setAttribute('aria-pressed', button.classList.contains('is-active') ? 'true' : 'false');
      button.addEventListener('click', function () {
        var group = button.getAttribute('data-filter-group');
        var value = button.getAttribute('data-filter-value');

        state[group] = value;
        setActiveButton(group, value);
        applyFilters();
      });
    });

    if (searchInput) {
      searchInput.addEventListener('input', function () {
        state.query = searchInput.value.trim().toLowerCase();
        applyFilters();
      });
    }

    applyFilters();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initPublicationFilters);
  } else {
    initPublicationFilters();
  }
})();
