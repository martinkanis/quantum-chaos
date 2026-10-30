// Offline reading for Quantum Knowledge Base (see web/offline.py).
//
// Online everything goes to the server first and good answers are stored; offline the stored copy is used.
// Dash builds every page from callback answers, so those are stored too, keyed by what they depend on. A missing
// answer becomes 204, which Dash treats as "no update", so an unsaved page or a calculation just stays as it is.

const CACHE_NAME = "quantum-chaos-offline-v1";
const CALLBACK_PATH = "/_dash-update-component";
const MANIFEST_PATH = "/offline-manifest.json";
const INDEX_KEY = "/";
const META_KEY = "/__offline__/meta";
const CALLBACK_KEY_PREFIX = "/__offline__/callback/";
const NETWORK_FIRST_PATHS = new Set(["/_dash-layout", "/_dash-dependencies"]);
const STATIC_PREFIXES = ["/_dash-component-suites/", "/assets/", "/prednasky/"];
const SKIPPED_NAVIGATIONS = new Set(["/login"]);
const LOGOUT_PATH = "/logout";
const USER_ACTIONS = [".n_clicks", ".n_intervals", ".n_submit", ".contents"];
const REFRESH_MILLISECONDS = 12 * 60 * 60 * 1000;
const PARALLEL_DOWNLOADS = 3;
const STORE_SUFFIX = "-store";

self.addEventListener("install", () => self.skipWaiting());

self.addEventListener("activate", (event) => {
  event.waitUntil((async () => {
    const names = await caches.keys();
    await Promise.all(names.filter((name) => name !== CACHE_NAME).map((name) => caches.delete(name)));
    await self.clients.claim();
  })());
});

self.addEventListener("fetch", (event) => {
  const request = event.request;
  const url = new URL(request.url);
  if (url.origin !== self.location.origin) {
    return;
  }
  if (request.mode === "navigate") {
    if (url.pathname === LOGOUT_PATH) {
      // The stored pages are the reader's own; whoever logs out takes them away from this browser.
      event.respondWith(caches.delete(CACHE_NAME).then(() => fetch(request)));
    } else if (!SKIPPED_NAVIGATIONS.has(url.pathname)) {
      event.respondWith(navigation(request));
    }
  } else if (request.method === "POST" && url.pathname === CALLBACK_PATH) {
    event.respondWith(callback(request));
  } else if (request.method === "GET" && NETWORK_FIRST_PATHS.has(url.pathname)) {
    event.respondWith(networkFirst(request, url.pathname));
  } else if (request.method === "GET" && STATIC_PREFIXES.some((prefix) => url.pathname.startsWith(prefix))) {
    event.respondWith(staleWhileRevalidate(request));
  }
});

self.addEventListener("message", (event) => {
  if (event.data && event.data.type === "warm-up") {
    event.waitUntil(warmUp(event.source, Boolean(event.data.force)));
  }
});

// Dash answers every path with the same page, so one stored copy serves all of them.
async function navigation(request) {
  try {
    const response = await fetch(request);
    if (isStorable(response) && (response.headers.get("Content-Type") || "").includes("text/html")) {
      await put(INDEX_KEY, response.clone());
    }
    return response;
  } catch (error) {
    const cached = await match(INDEX_KEY);
    return cached || offlinePage();
  }
}

async function callback(request) {
  let body;
  try {
    body = JSON.parse(await request.clone().text());
  } catch (error) {
    return fetch(request);
  }
  const key = await callbackKey(body);
  try {
    const response = await fetch(request);
    if (response.status === 200 && isStorable(response) && !isUserAction(body)) {
      await put(key, response.clone());
    }
    return response;
  } catch (error) {
    return (await match(key)) || new Response(null, { status: 204 });
  }
}

async function networkFirst(request, key) {
  try {
    const response = await fetch(request);
    if (isStorable(response)) {
      await put(key, response.clone());
    }
    return response;
  } catch (error) {
    return (await match(key)) || Response.error();
  }
}

async function staleWhileRevalidate(request) {
  const cached = await match(request);
  const update = fetch(request).then(async (response) => {
    if (isStorable(response)) {
      await put(request, response.clone());
    }
    return response;
  });
  if (cached) {
    update.catch(() => undefined);
    return cached;
  }
  return update;
}

// Downloads in advance everything needed to read every page offline. Runs again after a deployment
// (new manifest version) or when the copy is older than REFRESH_MILLISECONDS.
async function warmUp(client, force) {
  let manifest;
  try {
    const response = await fetch(MANIFEST_PATH, { cache: "no-store", redirect: "manual" });
    if (response.status !== 200) {
      return;
    }
    manifest = await response.json();
  } catch (error) {
    return;
  }
  const meta = await readMeta();
  if (!force && meta.version === manifest.version && Date.now() - meta.savedAt < REFRESH_MILLISECONDS) {
    notify(client, { type: "offline-ready", pages: meta.pages, savedAt: meta.savedAt, fresh: false });
    return;
  }
  const tasks = [() => storeGet(INDEX_KEY, INDEX_KEY).then(storeIndexResources)];
  manifest.urls.forEach((url) => tasks.push(() => storeGet(url, url)));
  manifest.paths.forEach((path) => manifest.callbacks.forEach((template) => {
    tasks.push(() => storeCallback(withPath(template, path)));
  }));
  let done = 0;
  let failed = 0;
  const total = tasks.length;
  const queue = tasks.slice();
  const worker = async () => {
    while (queue.length) {
      const task = queue.shift();
      try {
        await task();
      } catch (error) {
        failed += 1;
      }
      done += 1;
      if (done % 10 === 0 || done === total) {
        notify(client, { type: "offline-progress", done, total });
      }
    }
  };
  await Promise.all(Array.from({ length: PARALLEL_DOWNLOADS }, worker));
  const savedAt = Date.now();
  if (failed === 0) {
    await put(META_KEY, new Response(JSON.stringify({
      version: manifest.version, savedAt, pages: manifest.paths.length,
    })));
  }
  notify(client, { type: "offline-ready", pages: manifest.paths.length, savedAt, fresh: true, failed });
}

async function storeGet(url, key) {
  const response = await fetch(url, { redirect: "manual" });
  if (!isStorable(response)) {
    throw new Error(`${url}: ${response.status}`);
  }
  await put(key, response.clone());
  return response;
}

// The page itself loads its scripts and stylesheets; stores them before the reader goes offline.
async function storeIndexResources(response) {
  const html = await response.text();
  const urls = new Set();
  for (const match of html.matchAll(/(?:src|href)="([^"]+)"/g)) {
    const url = match[1].replace(/&amp;/g, "&");
    if (STATIC_PREFIXES.some((prefix) => url.startsWith(prefix))) {
      urls.add(url);
    }
  }
  await Promise.all([...urls].map((url) => storeGet(url, url)));
}

async function storeCallback(body) {
  const response = await fetch(CALLBACK_PATH, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
    redirect: "manual",
  });
  if (response.status === 204) {
    return;
  }
  if (response.status !== 200 || !isStorable(response)) {
    throw new Error(`${body.output}: ${response.status}`);
  }
  await put(await callbackKey(body), response);
}

function withPath(template, path) {
  const body = JSON.parse(JSON.stringify(template));
  body.inputs.forEach((input) => {
    if (input.id === "url" && input.property === "pathname") {
      input.value = path;
    }
  });
  return body;
}

// What a callback answer depends on: its outputs and the values of its inputs and state. Answers driven by the
// path ignore the stores, which only record what this browser already has (see web/offline.py).
async function callbackKey(body) {
  const dependencies = [...(body.inputs || []), ...(body.state || [])].flat(Infinity);
  const pathDriven = dependencies.some((item) => item && item.id === "url" && item.property === "pathname");
  const values = dependencies
    .filter((item) => item && !(pathDriven && isStore(item)))
    .map((item) => [typeof item.id === "string" ? item.id : JSON.stringify(item.id), item.property, item.value]);
  const text = JSON.stringify([body.output, values]);
  const digest = await crypto.subtle.digest("SHA-256", new TextEncoder().encode(text));
  const hex = [...new Uint8Array(digest)].map((byte) => byte.toString(16).padStart(2, "0")).join("");
  return CALLBACK_KEY_PREFIX + hex;
}

function isStore(item) {
  return typeof item.id === "string" && item.id.endsWith(STORE_SUFFIX) && item.property === "data";
}

// Answers to clicks and timers are not worth keeping: offline nothing can recompute them anyway.
function isUserAction(body) {
  return (body.changedPropIds || []).some((prop) => USER_ACTIONS.some((suffix) => prop.endsWith(suffix)));
}

function isStorable(response) {
  return response && response.ok && response.type === "basic" && !response.redirected;
}

async function readMeta() {
  const response = await match(META_KEY);
  return response ? response.json() : {};
}

async function put(key, response) {
  const cache = await caches.open(CACHE_NAME);
  await cache.put(key, response);
}

async function match(key) {
  const cache = await caches.open(CACHE_NAME);
  return cache.match(key);
}

function notify(client, message) {
  if (client) {
    client.postMessage(message);
  }
}

function offlinePage() {
  const html = `<!DOCTYPE html><html lang="cs"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Offline – Quantum Knowledge Base</title></head>
<body style="font-family: system-ui, sans-serif; max-width: 40rem; margin: 3rem auto; padding: 0 1rem;
line-height: 1.6">
<h1>Jsi offline</h1>
<p>Stránky se v tomhle prohlížeči ještě neuložily. Otevři aplikaci jednou s připojením a počkej, až se dole objeví
„Uloženo pro čtení offline“. Potom půjdou číst i bez internetu.</p></body></html>`;
  return new Response(html, { status: 503, headers: { "Content-Type": "text/html; charset=utf-8" } });
}
