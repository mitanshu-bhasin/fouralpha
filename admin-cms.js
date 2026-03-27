import { app as e, db as t } from "./firebase-config.js";
import {
  getAuth as s,
  onAuthStateChanged as a,
} from "https://www.gstatic.com/firebasejs/11.4.0/firebase-auth.js";
import {
  doc as n,
  getDoc as r,
  setDoc as i,
  collection as o,
  getDocs as d,
  query,
  orderBy,
  updateDoc,
} from "https://www.gstatic.com/firebasejs/11.4.0/firebase-firestore.js";
const l = s(e),
  c = document.getElementById("access-denied"),
  p = document.getElementById("admin-panel"),
  u = document.getElementById("auth-status"),
  b = document.querySelectorAll(".cms-tab-btn"),
  m = document.getElementById("fields-container"),
  g = document.getElementById("cms-form"),
  x = document.getElementById("toast"),
  f = document.getElementById("save-btn"),
  y = document.getElementById("cms-editor-container"),
  h = document.getElementById("users-container"),
  w = document.getElementById("users-table-body"),
  v = document.getElementById("refresh-users-btn"),
  qC = document.getElementById("queries-container"),
  qL = document.getElementById("queries-list"),
  qR = document.getElementById("refresh-queries-btn");
let L = "home";

const fileMap = {
  home: "index.html",
  "about-deepak": "about-deepak.html",
  "policy-governance": "policy-governance.html",
  contact: "contact.html",
  "four-alpha-model": "four-alpha-model.html",
  "math-of-life": "math-of-life.html",
  "alpha-self": "alpha-self.html",
  champions: "champions.html",
  "white-belt": "white-belt/index.html",
  "yellow-belt": "yellow-belt/index.html",
  "green-belt": "green-belt/index.html",
  "black-belt": "black-belt/index.html",
  global: "index.html",
};

async function B(e) {
  m.innerHTML =
    '<div class="text-center text-gray-500 py-10 font-serif italic text-sm">Scraping fields from page structure...</div>';
  try {
    const sNode = n(t, "cms_content", e);
    const sData = await r(sNode);
    const dbVals = sData.exists() ? sData.data() : {};
    const htmlFile = fileMap[e] || "index.html";
    const res = await fetch(htmlFile);
    const htmlText = await res.text();
    const parser = new DOMParser();
    const doc = parser.parseFromString(htmlText, "text/html");
    const nodes = doc.querySelectorAll("[data-cms-id]");
    const fields = [];
    nodes.forEach((n) => {
      const id = n.getAttribute("data-cms-id");
      if ("global" === e && !id.includes("footer")) return;
      if ("global" !== e && id.includes("footer")) return;
      if (
        n.tagName.toLowerCase() === "title" ||
        n.tagName.toLowerCase() === "meta"
      )
        return;
      let label = id.replace(/-/g, " ").toUpperCase();
      let type = "textarea";
      if (n.tagName.toLowerCase() === "h1" || n.tagName.toLowerCase() === "h2")
        type = "text";
      if (!fields.find((f) => f.id === id))
        fields.push({
          id,
          label,
          type: type,
          defaultVal:
            n.tagName.toLowerCase() === "meta"
              ? n.getAttribute("content")
              : n.innerHTML.trim(),
        });
    });
    m.innerHTML = "";
    if (fields.length === 0) {
      m.innerHTML =
        '<div class="text-gray-500 font-serif italic text-sm py-4">No data-cms-id fields found in source HTML.</div>';
      return;
    }
    fields.forEach((fld) => {
      const val = dbVals[fld.id] || fld.defaultVal || "";
      const tag =
        fld.type === "textarea"
          ? `<textarea name="${fld.id}" rows="4" class="w-full bg-white/5 border border-white/20 rounded-md p-3 text-white font-serif focus:border-gold focus:outline-none focus:ring-1 focus:ring-gold transition-colors">${val}</textarea>`
          : `<input type="text" name="${fld.id}" value="${val}" class="w-full bg-white/5 border border-white/20 rounded-md p-3 text-white font-serif focus:border-gold focus:outline-none focus:ring-1 focus:ring-gold transition-colors">`;
      m.insertAdjacentHTML(
        "beforeend",
        `\n<div class="space-y-2">\n<label class="block text-xs font-black tracking-widest text-gold uppercase">${fld.label}</label>\n<div class="text-[10px] text-gray-500 mb-1 font-mono">ID: ${fld.id}</div>\n${tag}\n</div>\n`,
      );
    });
  } catch (err) {
    m.innerHTML = `<div class="text-red-500 font-bold text-center py-10">Error parsing source HTML: ${err.message}</div>`;
  }
}

async function Q() {
  qL.innerHTML =
    '<div class="text-center text-gray-500 italic py-8"><i class="fas fa-satellite-dish fa-spin mr-2"></i> Querying communications database...</div>';
  try {
    const q = query(o(t, "contacts"), orderBy("timestamp", "desc"));
    const sn = await d(q);
    if (sn.empty) {
      qL.innerHTML =
        '<div class="text-center text-gray-500 italic py-8">No transmissions intercepted.</div>';
      return;
    }
    let h = "";
    sn.forEach((doc) => {
      const dt = doc.data();
      const dtTmStr = dt.timestamp
        ? dt.timestamp.toDate().toLocaleString()
        : "Unknown Space-Time";
      const clStatus =
        dt.status === "read"
          ? "border-white/10 opacity-70"
          : "border-gold/50 shadow-[0_0_15px_rgba(255,184,0,0.1)]";
      h +=
        `<div class="bg-white/5 border ${clStatus} rounded-xl p-6 relative">` +
        (dt.status !== "read"
          ? `<span class="absolute top-4 right-4 bg-gold text-cosmic-dark text-[10px] uppercase font-bold px-2 py-1 rounded">New</span>`
          : "") +
        `<div class="flex justify-between items-start mb-4"><div><h3 class="text-lg font-bold text-white">${dt.name || "Unknown"}</h3><a href="mailto:${dt.email}" class="text-sm text-gold hover:text-white transition-colors">${dt.email || "No Email"}</a><div class="text-[10px] text-gray-500 font-mono mt-1">${dtTmStr}</div></div>` +
        (dt.status !== "read"
          ? `<button onclick="window.markRead('${doc.id}')" class="text-xs text-gray-400 hover:text-white underline uppercase tracking-widest">Mark Read</button>`
          : "") +
        `</div><div class="bg-black/30 p-4 rounded text-sm text-gray-300 font-serif leading-relaxed whitespace-pre-wrap">${dt.message || ""}</div></div>`;
    });
    qL.innerHTML = h;
  } catch (err) {
    console.error(err);
    qL.innerHTML = `<div class="text-red-500 font-bold text-center py-8">Error: ${err.message}</div>`;
  }
}
window.markRead = async function (docId) {
  try {
    await updateDoc(n(t, "contacts", docId), { status: "read" });
    Q();
  } catch (e) {
    alert(e.message);
  }
};

async function T() {
  w.innerHTML =
    '<tr><td colspan="4" class="px-6 py-8 text-center text-gray-500 italic"><i class="fas fa-satellite-dish fa-spin mr-2"></i> Querying user databanks...</td></tr>';
  try {
    const e = await d(o(t, "users"));
    if (e.empty)
      return void (w.innerHTML =
        '<tr><td colspan="4" class="px-6 py-8 text-center text-gray-500 italic">No user records found.</td></tr>');
    let s = "";
    (e.forEach((e) => {
      const t = e.data(),
        a = t.email || "Email Not Synced",
        n = t.status || "active",
        r = e.id,
        i = t.dob ? `DOB: ${t.dob}` : "DOB: Not Provided",
        o = t.certifications || {},
        d = Object.keys(o).length;
      let l = "";
      0 === d
        ? (l =
            '<span class="text-gray-600 text-xs italic">None generated</span>')
        : (o.whiteBelt &&
            (l +=
              '<span title="White Belt" class="inline-block w-3 h-3 rounded-full bg-white border border-gray-400 mr-1"></span>'),
          o.yellowBelt &&
            (l +=
              '<span title="Yellow Belt" class="inline-block w-3 h-3 rounded-full bg-yellow-400 border border-yellow-600 mr-1"></span>'),
          o.greenBelt &&
            (l +=
              '<span title="Green Belt" class="inline-block w-3 h-3 rounded-full bg-green-500 border border-green-700 mr-1"></span>'),
          o.blackBelt &&
            (l +=
              '<span title="Black Belt" class="inline-block w-3 h-3 rounded-full bg-black border border-gray-700 mr-1 shadow-[0_0_5px_rgba(255,255,255,0.2)]"></span>'),
          o.masterBlackBelt &&
            (l +=
              '<span title="Master Black Belt" class="inline-block w-3 h-3 rounded-full bg-purple-600 border border-purple-800 mr-1 text-[8px] flex items-center justify-center text-white"><i class="fas fa-crown"></i></span>'));
      const c = "suspended" === n;
      s += `\n<tr class="hover:bg-white/[0.05] transition-colors border-white/5">\n<td class="px-6 py-4">\n<div class="font-bold text-white truncate max-w-[150px] lg:max-w-[250px]" title="${t.name || "Legacy Operative"}">${(t.name || "Legacy Operative").replace(/</g, "&lt;").replace(/>/g, "&gt;")}</div>\n<div class="text-xs text-gray-400 mt-1 truncate max-w-[150px] lg:max-w-[250px]" title="${a}">${a.replace(/</g, "&lt;").replace(/>/g, "&gt;")}</div>\n<div class="text-[10px] text-gray-500 font-mono mt-1">${i}</div>\n<div class="text-[9px] text-gray-600 font-mono mt-1 truncate max-w-[150px] lg:max-w-[250px]" title="${r}">UID: ${r}</div>\n</td>\n<td class="px-6 py-4 text-center">\n<div class="flex items-center justify-center">${l}</div>\n<div class="text-[10px] text-gray-500 mt-1 uppercase tracking-wider">${d} total</div>\n</td>\n<td class="px-6 py-4 text-center">\n${c ? '<span class="px-2 py-1 bg-red-500/10 text-red-400 border border-red-500/30 rounded text-xs font-bold tracking-widest uppercase">Suspended</span>' : '<span class="px-2 py-1 bg-green-500/10 text-green-400 border border-green-500/30 rounded text-xs font-bold tracking-widest uppercase">Active</span>'}\n</td>\n<td class="px-6 py-4 text-center">\n<button onclick="window.toggleUserStatus('${r}', '${n}')" class="text-xs font-bold uppercase tracking-widest px-3 py-1 rounded transition-colors focus:ring-2 focus:ring-offset-2 focus:ring-offset-cosmic-dark ${c ? "bg-white/10 text-white hover:bg-white hover:text-black focus:ring-white" : "bg-red-500/20 text-red-500 hover:bg-red-500 hover:text-white focus:ring-red-500"}">\n${c ? "Reactivate" : "Suspend"}\n</button>\n</td>\n</tr>\n`;
    }),
      (w.innerHTML = s));
  } catch (e) {
    (console.error("Error fetching users:", e),
      (w.innerHTML = `<tr><td colspan="4" class="px-6 py-8 text-center text-red-500 font-bold">Failed to load data: ${e.message}</td></tr>`));
  }
}
a(l, (e) => {
  e && "info@fouralpha.org" === e.email
    ? (c.classList.add("hidden"),
      p.classList.remove("hidden"),
      (u.innerHTML = `<span class="text-green-500"><i class="fas fa-signal"></i> SECURE CONNECTION</span> | ${e.email}`),
      B(L))
    : (c.classList.remove("hidden"),
      p.classList.add("hidden"),
      (u.innerHTML =
        '<span class="text-red-500"><i class="fas fa-times-circle"></i> CONNECTION REFUSED</span>'));
});
b.forEach((e) => {
  e.addEventListener("click", (e) => {
    (document.querySelectorAll(".cms-tab-btn").forEach((e) => {
      (e.classList.remove("bg-gold/10", "text-gold", "border-gold"),
        e.classList.add("bg-white/5", "text-gray-400", "border-transparent"));
    }),
      e.currentTarget.classList.remove(
        "bg-white/5",
        "text-gray-400",
        "border-transparent",
      ),
      e.currentTarget.classList.add("bg-gold/10", "text-gold", "border-gold"));
    const t = e.currentTarget.getAttribute("data-target");
    "users" === t
      ? (y.classList.add("hidden"),
        qC.classList.add("hidden"),
        h.classList.remove("hidden"),
        T())
      : "queries" === t
        ? (y.classList.add("hidden"),
          h.classList.add("hidden"),
          qC.classList.remove("hidden"),
          Q())
        : (h.classList.add("hidden"),
          qC.classList.add("hidden"),
          y.classList.remove("hidden"),
          (L = t),
          B(L));
  });
});
const mainTog = document.getElementById("main_toggle");
async function checkMainTog() {
  if (!mainTog) return;
  try {
    const md = await r(n(t, "system_config", "maintenance"));
    if (md.exists() && md.data().active) {
      mainTog.classList.replace("text-gray-400", "text-red-500");
      mainTog.innerHTML =
        'Maintenance: ACTIVE <i class="fas fa-power-off text-xs"></i>';
    } else {
      mainTog.classList.replace("text-red-500", "text-gray-400");
      mainTog.innerHTML =
        'Maintenance: OFF <i class="fas fa-power-off text-xs"></i>';
    }
  } catch (e) {
    console.error(e);
  }
}
if (mainTog) {
  checkMainTog();
  mainTog.addEventListener("click", async () => {
    try {
      const md = await r(n(t, "system_config", "maintenance"));
      const cur = md.exists() ? md.data().active : false;
      const nxt = !cur;
      if (
        confirm(
          nxt
            ? "Engage Maintenance Mode? Rest of site will go offline."
            : "Disable Maintenance Mode? Rest of site will come online.",
        )
      ) {
        await i(
          n(t, "system_config", "maintenance"),
          { active: nxt },
          { merge: true },
        );
        checkMainTog();
        const mId = document.getElementById("toast");
        mId.innerHTML = `<i class="fas fa-check-circle"></i> <span>Maintenance ${nxt ? "ON" : "OFF"}</span>`;
        mId.classList.remove("hidden");
        setTimeout(() => mId.classList.add("hidden"), 3e3);
      }
    } catch (e) {
      alert(e.message);
    }
  });
}
g.addEventListener("submit", async (e) => {
  (e.preventDefault(),
    (f.innerHTML = 'Deploying... <i class="fas fa-spinner fa-spin ml-2"></i>'),
    (f.disabled = !0));
  const s = new FormData(g),
    a = {};
  for (const [e, t] of s.entries())
    if (t.trim()) a[e] = t.replace(/\r\n/g, "\n").replace(/\n/g, "<br>");
  try {
    const e = n(t, "cms_content", L);
    (await i(e, a, { merge: !0 }),
      x.classList.remove("hidden"),
      setTimeout(() => x.classList.add("hidden"), 3e3));
  } catch (e) {
    alert("Failed to save: " + e.message);
  } finally {
    ((f.innerHTML = 'Deploy Changes <i class="fas fa-upload ml-2"></i>'),
      (f.disabled = !1));
  }
});
if (v) v.addEventListener("click", T);
if (qR) qR.addEventListener("click", Q);
window.toggleUserStatus = async function (e, s) {
  const a = "suspended" === s ? "active" : "suspended";
  if (
    confirm(
      "suspended" === a
        ? "Are you SURE you want to suspend this user? They will not be able to log in to the dashboard."
        : "Reactivate this user?",
    )
  )
    try {
      const s = n(t, "users", e);
      await i(s, { status: a }, { merge: !0 });
      const r = document.getElementById("toast");
      ((r.innerHTML = `<i class="fas fa-check-circle"></i> <span>User status updated to ${a.toUpperCase()}</span>`),
        r.classList.remove("hidden"),
        setTimeout(() => r.classList.add("hidden"), 3e3),
        T());
    } catch (e) {
      alert("Action failed: " + e.message);
    }
};
