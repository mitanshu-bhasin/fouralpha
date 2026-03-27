// updates.js — Shared Updates/Blog Engine (ES Module)
import { db } from "./firebase-config.js";
import {
    collection, getDocs, query, orderBy, limit, where, doc, getDoc
} from "https://www.gstatic.com/firebasejs/11.4.0/firebase-firestore.js";

const UPDATES_COL = "updates";

// ─── Fetch helpers ───
async function fetchUpdates(max) {
    const q = max
        ? query(collection(db, UPDATES_COL), where("published", "==", true), orderBy("date", "desc"), limit(max))
        : query(collection(db, UPDATES_COL), where("published", "==", true), orderBy("date", "desc"));
    const snap = await getDocs(q);
    const list = [];
    snap.forEach(d => list.push({ id: d.id, ...d.data() }));
    return list;
}

function fmtDate(ts) {
    if (!ts) return "";
    const d = ts.toDate ? ts.toDate() : new Date(ts);
    return d.toLocaleDateString("en-US", { year: "numeric", month: "short", day: "numeric" });
}

function escHtml(s) {
    const d = document.createElement("div");
    d.textContent = s;
    return d.innerHTML;
}

// ─── Card HTML Builder ───
function buildCard(u) {
    const thumb = u.thumbnail || "https://www.transparenttextures.com/patterns/stardust.png";
    const dateStr = fmtDate(u.date);
    const slug = u.slug || u.id;
    return `
  <article class="group bg-white/[0.04] border border-white/10 rounded-2xl overflow-hidden hover:border-gold/40 hover:shadow-[0_0_25px_rgba(255,184,0,0.12)] transition-all duration-500">
    <div class="relative h-48 overflow-hidden">
      <img src="${escHtml(thumb)}" alt="${escHtml(u.title || '')}" class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-700" loading="lazy">
      <div class="absolute inset-0 bg-gradient-to-t from-cosmic-dark/90 via-cosmic-dark/30 to-transparent"></div>
      <span class="absolute bottom-3 left-4 text-[10px] font-bold tracking-widest uppercase text-gold bg-gold/10 border border-gold/20 px-2 py-1 rounded">${escHtml(dateStr)}</span>
    </div>
    <div class="p-6">
      <h3 class="text-lg font-black text-white uppercase tracking-wider mb-3 line-clamp-2 group-hover:text-gold transition-colors">${escHtml(u.title || 'Untitled')}</h3>
      <p class="text-sm text-gray-400 leading-relaxed line-clamp-3 font-serif mb-6">${escHtml(u.excerpt || '')}</p>
      <div class="flex items-center gap-3">
        <a href="updates.html#${encodeURIComponent(slug)}" class="flex-1 text-center bg-gold/10 text-gold border border-gold/30 px-4 py-2.5 rounded-md font-bold text-xs hover:bg-gold hover:text-cosmic-dark transition-all uppercase tracking-widest">
          Read More <i class="fas fa-arrow-right ml-1 text-[10px]"></i>
        </a>
        <button onclick="window._shareUpdate('${escHtml(u.title || '')}','${encodeURIComponent(slug)}')" class="w-10 h-10 rounded-md bg-white/5 border border-white/10 flex items-center justify-center text-gray-400 hover:text-gold hover:border-gold/30 transition-all" title="Share">
          <i class="fas fa-share-alt text-sm"></i>
        </button>
      </div>
    </div>
  </article>`;
}

// ─── Full update detail view ───
function buildDetail(u) {
    const dateStr = fmtDate(u.date);
    const thumb = u.thumbnail || "";
    return `
  <article class="bg-white/[0.04] border border-white/10 rounded-2xl overflow-hidden p-8 md:p-12">
    <button onclick="window._closeDetail()" class="mb-6 text-gold hover:text-white text-sm font-bold uppercase tracking-widest transition-colors"><i class="fas fa-arrow-left mr-2"></i>Back to All Updates</button>
    ${thumb ? `<img src="${escHtml(thumb)}" alt="${escHtml(u.title || '')}" class="w-full max-h-[400px] object-cover rounded-xl mb-8" loading="lazy">` : ''}
    <span class="text-[10px] font-bold tracking-widest uppercase text-gold bg-gold/10 border border-gold/20 px-2 py-1 rounded">${escHtml(dateStr)}</span>
    <h1 class="text-3xl md:text-4xl font-black text-white uppercase tracking-wider mt-4 mb-6">${escHtml(u.title || 'Untitled')}</h1>
    <div class="prose prose-invert max-w-none text-gray-300 font-serif leading-relaxed">${u.content || u.excerpt || ''}</div>
    <div class="mt-8 pt-6 border-t border-white/10 flex gap-3">
      <button onclick="window._shareUpdate('${escHtml(u.title || '')}','${u.slug || u.id}')" class="bg-gold/10 text-gold border border-gold/30 px-6 py-2.5 rounded-md font-bold text-xs hover:bg-gold hover:text-cosmic-dark transition-all uppercase tracking-widest">
        <i class="fas fa-share-alt mr-2"></i>Share
      </button>
    </div>
  </article>`;
}

// ─── Share Utility ───
window._shareUpdate = function (title, slug) {
    const url = window.location.origin + "/updates.html#" + slug;
    if (navigator.share) {
        navigator.share({ title: title + " | Four Alpha", url }).catch(() => { });
    } else {
        navigator.clipboard.writeText(url).then(() => {
            const t = document.createElement("div");
            t.className = "fixed bottom-6 right-6 bg-green-500/10 border border-green-500/50 text-green-400 px-4 py-3 rounded-md text-sm font-bold tracking-widest uppercase z-50";
            t.innerHTML = '<i class="fas fa-check-circle mr-2"></i>Link Copied!';
            document.body.appendChild(t);
            setTimeout(() => t.remove(), 2500);
        });
    }
};

// ─── Render 3 cards on index.html ───
export async function renderHomeUpdates(containerId) {
    const container = document.getElementById(containerId);
    const section = document.getElementById("latest-updates-section");
    if (!container) return;
    try {
        const updates = await fetchUpdates(3);
        if (updates.length === 0) {
            if (section) section.style.display = "none";
            return;
        }
        container.innerHTML = updates.map(u => buildCard(u)).join("");
    } catch (err) {
        console.error("Error loading home updates:", err);
        if (section) section.style.display = "none";
    }
}

// ─── Render all updates on updates.html ───
let allUpdatesCache = [];
let currentPage = 0;
const PER_PAGE = 6;

export async function renderAllUpdates(containerId) {
    const container = document.getElementById(containerId);
    const loadMoreContainer = document.getElementById("load-more-container");
    const loadMoreBtn = document.getElementById("load-more-btn");
    if (!container) return;

    try {
        if (allUpdatesCache.length === 0) {
            container.innerHTML = '<div class="text-center py-16"><i class="fas fa-satellite-dish fa-spin text-gold text-2xl"></i><p class="text-gray-400 mt-4 text-sm font-bold uppercase tracking-widest">Loading Transmissions...</p></div>';
            allUpdatesCache = await fetchUpdates(null);
        }

        if (allUpdatesCache.length === 0) {
            container.innerHTML = '<div class="text-center py-16"><i class="fas fa-satellite-dish text-3xl text-white/10 mb-4"></i><p class="text-gray-500 font-serif italic">No dispatches have been transmitted yet.</p></div>';
            if (loadMoreContainer) loadMoreContainer.classList.add("hidden");
            return;
        }

        // Check if we should show a specific update via hash
        const hash = decodeURIComponent(window.location.hash.slice(1));
        if (hash) {
            const target = allUpdatesCache.find(u => (u.slug || u.id) === hash);
            if (target) {
                container.innerHTML = buildDetail(target);
                // Dynamic SEO
                document.title = (target.title || "Update") + " | Four Alpha AED Lab";
                const metaDesc = document.querySelector('meta[name="description"]');
                if (metaDesc) metaDesc.setAttribute("content", target.excerpt || target.title || "");
                const ogTitle = document.querySelector('meta[property="og:title"]');
                if (ogTitle) ogTitle.setAttribute("content", (target.title || "Update") + " | Four Alpha AED Lab");
                const ogDesc = document.querySelector('meta[property="og:description"]');
                if (ogDesc) ogDesc.setAttribute("content", target.excerpt || target.title || "");
                const ogUrl = document.querySelector('meta[property="og:url"]');
                if (ogUrl) ogUrl.setAttribute("content", window.location.href);
                if (target.thumbnail) {
                    const ogImg = document.querySelector('meta[property="og:image"]');
                    if (ogImg) ogImg.setAttribute("content", target.thumbnail);
                }
                if (loadMoreContainer) loadMoreContainer.classList.add("hidden");
                window.scrollTo({ top: 0 });
                return;
            }
        }

        // Paginated list view
        const end = (currentPage + 1) * PER_PAGE;
        const visible = allUpdatesCache.slice(0, end);
        container.innerHTML = '<div class="grid md:grid-cols-2 lg:grid-cols-3 gap-8">' + visible.map(u => buildCard(u)).join("") + '</div>';

        if (end < allUpdatesCache.length) {
            if (loadMoreContainer) loadMoreContainer.classList.remove("hidden");
        } else {
            if (loadMoreContainer) loadMoreContainer.classList.add("hidden");
        }
    } catch (err) {
        console.error("Error loading updates:", err);
        container.innerHTML = '<div class="text-center py-8 text-red-500/60 text-sm font-bold">Failed to load transmissions.</div>';
    }
}

window._closeDetail = function () {
    history.replaceState(null, "", window.location.pathname);
    currentPage = 0;
    renderAllUpdates("all-updates-container");
    // Reset SEO to default
    document.title = "All Updates | Four Alpha AED Lab";
    const metaDesc = document.querySelector('meta[name="description"]');
    if (metaDesc) metaDesc.setAttribute("content", "Track the latest strategic deployments, research data, and certification cohort announcements from Four Alpha AED Lab.");
};

// ─── Search filter ───
export function initSearch(inputId, containerId) {
    const input = document.getElementById(inputId);
    if (!input) return;
    input.addEventListener("input", () => {
        const term = input.value.toLowerCase().trim();
        const container = document.getElementById(containerId);
        if (!container) return;
        if (!term) {
            currentPage = 0;
            renderAllUpdates(containerId);
            return;
        }
        const filtered = allUpdatesCache.filter(u =>
            (u.title || "").toLowerCase().includes(term) ||
            (u.excerpt || "").toLowerCase().includes(term) ||
            (u.content || "").toLowerCase().includes(term)
        );
        if (filtered.length === 0) {
            container.innerHTML = '<div class="text-center py-12"><i class="fas fa-search text-2xl text-white/10 mb-3"></i><p class="text-gray-500 font-serif italic text-sm">No transmissions match your query.</p></div>';
        } else {
            container.innerHTML = '<div class="grid md:grid-cols-2 lg:grid-cols-3 gap-8">' + filtered.map(u => buildCard(u)).join("") + '</div>';
        }
        const loadMoreContainer = document.getElementById("load-more-container");
        if (loadMoreContainer) loadMoreContainer.classList.add("hidden");
    });
}

// ─── Load More handler ───
export function initLoadMore(containerId) {
    const btn = document.getElementById("load-more-btn");
    if (!btn) return;
    btn.addEventListener("click", () => {
        currentPage++;
        renderAllUpdates(containerId);
    });
}

// ─── Hash change listener for detail view ───
export function initHashNav(containerId) {
    window.addEventListener("hashchange", () => {
        currentPage = 0;
        renderAllUpdates(containerId);
    });
}
