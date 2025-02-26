// Listen for messages from the extension
chrome.runtime.onMessage.addListener(function(request, sender, sendResponse) {
  if (request.action === "getFeedback") {
    // This could be used to get feedback directly from the page
    sendResponse({ success: true });
  }
});

// Listen for custom events from the webpage
window.addEventListener('message', function(event) {
  // Only accept messages from the same frame
  if (event.source !== window) return;

  // Check if the message is from our expected format
  if (event.data.type && event.data.type === 'FEEDBACK_LOOP') {
    // Send the feedback to the background script
    chrome.runtime.sendMessage({
      action: 'saveFeedback',
      feedback: event.data.feedback,
      url: window.location.href,
      title: document.title,
      timestamp: new Date().toISOString()
    }, function(response) {
      // Optionally send a response back to the page
      window.postMessage({
        type: 'FEEDBACK_LOOP_RESPONSE',
        success: response && response.success,
        warning: response && response.warning
      }, '*');
    });
  }
});

// Inject a small API into the page to allow direct feedback submission
const script = document.createElement('script');
script.textContent = `
  window.FeedbackLoop = {
    sendFeedback: function(feedback) {
      window.postMessage({
        type: 'FEEDBACK_LOOP',
        feedback: feedback
      }, '*');
      return true;
    }
  };
`;
(document.head || document.documentElement).appendChild(script);
script.remove(); 