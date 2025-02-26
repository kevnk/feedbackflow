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

// Listen for the custom event from the page
window.addEventListener('feedbackloop-send', function(event) {
  if (event.detail && event.detail.feedback) {
    // Forward the feedback to the background script
    chrome.runtime.sendMessage({
      action: 'saveFeedback',
      feedback: event.detail.feedback,
      url: window.location.href,
      title: document.title,
      timestamp: new Date().toISOString()
    }, function(response) {
      // Send a response back to the page
      window.postMessage({
        type: 'FEEDBACK_LOOP_RESPONSE',
        success: response && response.success,
        warning: response && response.warning
      }, '*');
    });
  }
});

// Inject the FeedbackLoop API script
function injectFeedbackLoopAPI() {
  // Get the URL to the feedbackloop-api.js file
  const apiScriptURL = chrome.runtime.getURL('feedbackloop-api.js');
  
  // Create a script element
  const script = document.createElement('script');
  script.src = apiScriptURL;
  script.type = 'text/javascript';
  
  // Log when the script is loaded
  script.onload = function() {
    console.log('FeedbackLoop API script loaded successfully');
  };
  
  // Log any errors
  script.onerror = function() {
    console.error('Failed to load FeedbackLoop API script');
  };
  
  // Append the script to the document
  (document.head || document.documentElement).appendChild(script);
  
  console.log('FeedbackLoop API script injection attempted:', apiScriptURL);
}

// Execute the injection as soon as possible
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', injectFeedbackLoopAPI);
} else {
  injectFeedbackLoopAPI();
} 