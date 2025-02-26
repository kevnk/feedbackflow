document.addEventListener('DOMContentLoaded', function() {
  const feedbackText = document.getElementById('feedback-text');
  const sendButton = document.getElementById('send-feedback');
  const statusDiv = document.getElementById('status');
  
  function checkFeedbackLoopAPI() {
    if (window.FeedbackLoop) {
      statusDiv.textContent = 'FeedbackLoop extension is active.';
      statusDiv.className = 'status success';
      sendButton.disabled = false;
      return true;
    } else {
      statusDiv.textContent = 'FeedbackLoop extension is not installed or not active.';
      statusDiv.className = 'status error';
      sendButton.disabled = true;
      return false;
    }
  }
  
  // Initial check for the API
  checkFeedbackLoopAPI();
  
  // Listen for the API readiness event
  window.addEventListener('feedbackloop-ready', function() {
    console.log('FeedbackLoop API is now ready');
    checkFeedbackLoopAPI();
  });
  
  // Periodically check for the API (in case the event is missed)
  const apiCheckInterval = setInterval(function() {
    if (checkFeedbackLoopAPI()) {
      clearInterval(apiCheckInterval);
    }
  }, 1000);
  
  // Send feedback when button is clicked
  sendButton.addEventListener('click', function() {
    const feedback = feedbackText.value.trim();
    
    if (!feedback) {
      statusDiv.textContent = 'Please enter some feedback.';
      statusDiv.className = 'status error';
      return;
    }
    
    if (window.FeedbackLoop) {
      try {
        // Send feedback using the API
        window.FeedbackLoop.sendFeedback(feedback);
        statusDiv.textContent = 'Sending feedback...';
        statusDiv.className = 'status';
      } catch (error) {
        console.error('Error sending feedback:', error);
        statusDiv.textContent = 'Error sending feedback: ' + error.message;
        statusDiv.className = 'status error';
      }
    } else {
      statusDiv.textContent = 'FeedbackLoop extension is not installed or not active.';
      statusDiv.className = 'status error';
    }
  });
  
  // Listen for responses from the extension
  window.addEventListener('message', function(event) {
    // Only accept messages from the same frame
    if (event.source !== window) return;
    
    // Check if the message is from our expected format
    if (event.data.type && event.data.type === 'FEEDBACK_LOOP_RESPONSE') {
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