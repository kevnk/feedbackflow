// Which pages may send feedback. Shared by background.js (importScripts) and
// popup.html (<script>).
//
// Pages on local development hosts always may. Any other site needs the user to
// allow it from the popup; allowed origins live in chrome.storage.local under
// `allowedOrigins`. Without this, every site you visit could write text into
// the log your AI assistant reads.
const FEEDBACK_LOCAL_HOST = /^(localhost|127\.0\.0\.1|\[::1\])$|\.(localhost|test)$/;

// Returns 'local', 'allowed', 'blocked' or 'unsupported' (not an http(s) page).
function feedbackOriginStatus(url, allowedOrigins) {
  let parsed;
  try {
    parsed = new URL(url);
  } catch (error) {
    return 'unsupported';
  }
  if (parsed.protocol !== 'http:' && parsed.protocol !== 'https:') return 'unsupported';
  if (FEEDBACK_LOCAL_HOST.test(parsed.hostname)) return 'local';
  return (allowedOrigins || []).includes(parsed.origin) ? 'allowed' : 'blocked';
}
