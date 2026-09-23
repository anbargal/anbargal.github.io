/* Shared helpers used by multiple pages */
const BhajanLists = (() => {
  const STORAGE_KEY = "bhajan_lists";

  function get() {
    try {
      return JSON.parse(localStorage.getItem(STORAGE_KEY) || "[]");
    } catch (e) {
      return [];
    }
  }

  function save(lists) {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(lists));
  }

  function clear() {
    localStorage.removeItem(STORAGE_KEY);
  }

  // Canonical catalog-page URL, root-relative. With no argument it derives the
  // query from the current page (index load); pass a query string to build one.
  function catalogUrl(search) {
    const q = search === undefined ? window.location.search.replace(/^\?/, "") : search;
    return q ? "/?" + q : "/";
  }

  function recordVisit(url, name) {
    const lists = get();
    const existing = lists.findIndex(l => l.url === url);
    if (existing >= 0) {
      lists[existing].count = (lists[existing].count || 1) + 1;
    } else {
      lists.push({ name: name || "Untitled List", url, count: 1, date: Date.now() });
    }
    save(lists);
    return lists;
  }

  return { get, save, clear, catalogUrl, recordVisit };
})();