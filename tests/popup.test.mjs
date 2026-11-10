// Runs chrome-extension/popup.js against a fake DOM and a fake `chrome` to check
// the per-site "send feedback" toggle.  node --test tests/*.test.mjs
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import vm from 'node:vm';

const dir = new URL('../chrome-extension/', import.meta.url);

async function openPopup(tabUrl, stored = {}) {
  const storage = { ...stored };
  const elements = {};
  const el = id => (elements[id] ??= {
    hidden: id === 'site-access', checked: false, disabled: false, textContent: '', value: '', listeners: {},
    addEventListener(type, fn) { this.listeners[type] = fn; },
  });
  let ready;
  const context = vm.createContext({
    URL, console, setTimeout,
    navigator: { platform: 'MacIntel', userAgent: 'Mac' },
    confirm: () => false,
    document: { getElementById: el, addEventListener: (type, fn) => { ready = fn; } },
    chrome: {
      runtime: { sendMessage() {} },
      tabs: { query: async () => [{ url: tabUrl, title: 'Tab' }] },
      storage: { local: {
        get: (keys, done) => done(Object.fromEntries([].concat(keys).filter(k => k in storage).map(k => [k, storage[k]]))),
        set: (values, done) => { Object.assign(storage, structuredClone(values)); if (done) done(); },
      } },
    },
  });
  for (const file of ['origins.js', 'popup.js']) vm.runInContext(readFileSync(new URL(file, dir), 'utf8'), context);
  ready();
  await new Promise(r => setTimeout(r, 0));
  return { toggle: el('allow-site'), row: el('site-access'), text: el('site-access-text'), storage };
}

test('a local development site shows as always on', async () => {
  const { toggle, row, text } = await openPopup('http://localhost:3000/page');
  assert.equal(row.hidden, false);
  assert.equal(toggle.checked, true);
  assert.equal(toggle.disabled, true);
  assert.match(text.textContent, /http:\/\/localhost:3000 can send feedback/);
});

test('another site starts off, and turning it on saves its origin', async () => {
  const { toggle, text, storage } = await openPopup('https://staging.example.com/cart', { allowedOrigins: ['https://a.example'] });
  assert.equal(toggle.checked, false);
  assert.equal(toggle.disabled, false);
  assert.match(text.textContent, /Let pages on https:\/\/staging\.example\.com send feedback/);

  toggle.checked = true;
  toggle.listeners.change();
  assert.deepEqual(storage.allowedOrigins, ['https://a.example', 'https://staging.example.com']);

  toggle.checked = false;
  toggle.listeners.change();
  assert.deepEqual(storage.allowedOrigins, ['https://a.example']);
});

test('an allowed site shows as on', async () => {
  const { toggle } = await openPopup('https://a.example/x', { allowedOrigins: ['https://a.example'] });
  assert.equal(toggle.checked, true);
});

test('browser pages hide the toggle', async () => {
  const { row } = await openPopup('chrome://extensions/');
  assert.equal(row.hidden, true);
});
