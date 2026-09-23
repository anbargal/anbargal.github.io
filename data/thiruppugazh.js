/* Loads and parses data/thiruppugazh.jsonl */
const Thiruppugazh = (() => {
  const SCRIPT_URL = document.currentScript && document.currentScript.src;
  const BASE_URL = SCRIPT_URL ? new URL(".", SCRIPT_URL).href : "data/";

  async function load() {
    const res = await fetch(new URL("thiruppugazh.jsonl", BASE_URL));
    if (!res.ok) throw new Error("HTTP " + res.status);
    const text = await res.text();
    const songs = text.trim().split("\n").filter(Boolean).map(JSON.parse);
    const byTiv = songs.slice().sort((a, b) => a.tiv - b.tiv);
    return { songs, byTiv };
  }

  return { load };
})();