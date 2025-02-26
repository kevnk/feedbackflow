document.addEventListener('DOMContentLoaded', function() {
  const feedbackText = document.getElementById('feedback-text');
  const sendButton = document.getElementById('send-feedback');
  const statusDiv = document.getElementById('status');
  
  // Detect OS and update button text with appropriate key symbols
  function updateButtonText() {
    // Check if macOS (Darwin)
    const isMac = navigator.platform.toUpperCase().indexOf('MAC') >= 0 || 
                 navigator.userAgent.toUpperCase().indexOf('MAC') >= 0;
    
    // Use symbols for both modifier key and Enter key
    // ⌘ for Mac, ⌃ for Windows/Linux, and ↵ for Enter
    const modKey = isMac ? '&#8984;' : '&#8963;';
    
    // Update button text - using HTML entities for both symbols
    sendButton.innerHTML = `Send Feedback ${modKey}&#8629;`;
  }

  // Update button text on load
  updateButtonText();
  
  function checkFeedbackFlowAPI() {
    if (window.FeedbackFlow) {
      statusDiv.textContent = 'Feedback Flow extension is active.';
      statusDiv.className = 'status success';
      sendButton.disabled = false;
      return true;
    } else {
      statusDiv.textContent = 'Feedback Flow extension is not installed or not active.';
      statusDiv.className = 'status error';
      sendButton.disabled = true;
      return false;
    }
  }
  
  // Initial check for the API
  checkFeedbackFlowAPI();
  
  // Listen for the API readiness event
  window.addEventListener('feedbackflow-ready', function() {
    console.log('Feedback Flow API is now ready');
    checkFeedbackFlowAPI();
  });
  
  // Periodically check for the API (in case the event is missed)
  const apiCheckInterval = setInterval(function() {
    if (checkFeedbackFlowAPI()) {
      clearInterval(apiCheckInterval);
    }
  }, 1000);
  
  // Function to send feedback
  function sendFeedback() {
    const feedback = feedbackText.value.trim();
    
    if (!feedback) {
      statusDiv.textContent = 'Please enter some feedback.';
      statusDiv.className = 'status error';
      return;
    }
    
    if (window.FeedbackFlow) {
      try {
        // Send feedback using the API
        window.FeedbackFlow.sendFeedback(feedback);
        statusDiv.textContent = 'Sending feedback...';
        statusDiv.className = 'status';
      } catch (error) {
        console.error('Error sending feedback:', error);
        statusDiv.textContent = 'Error sending feedback: ' + error.message;
        statusDiv.className = 'status error';
      }
    } else {
      statusDiv.textContent = 'Feedback Flow extension is not installed or not active.';
      statusDiv.className = 'status error';
    }
  }
  
  // Send feedback when button is clicked
  sendButton.addEventListener('click', sendFeedback);
  
  // Add keyboard shortcut (Cmd/Ctrl + Enter) to send feedback
  feedbackText.addEventListener('keydown', function(event) {
    // Check if it's Cmd/Ctrl + Enter
    if ((event.metaKey || event.ctrlKey) && event.key === 'Enter') {
      event.preventDefault();
      sendFeedback();
    }
  });
  
  // Listen for responses from the extension
  window.addEventListener('message', function(event) {
    // Only accept messages from the same frame
    if (event.source !== window) return;
    
    // Check if the message is from our expected format
    if (event.data.type && event.data.type === 'FEEDBACK_FLOW_RESPONSE') {
      if (event.data.success) {
        statusDiv.textContent = 'Feedback sent successfully!';
        statusDiv.className = 'status success';
        feedbackText.value = '';
      } else {
        statusDiv.textContent = 'Error sending feedback.';
        statusDiv.className = 'status error';
      }
      
      if (event.data.warning) {
        console.warn('Warning:', event.data.warning);
      }
    }
  });
}); 