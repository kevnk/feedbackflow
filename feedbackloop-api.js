// Define the FeedbackLoop API in the global scope
window.FeedbackLoop = {
  // Verbosity flag - set to false to enable detailed logging
  verbose: false,
  
  // Log function that only logs when verbose mode is enabled
  log: function(message, type = 'log') {
    if (this.verbose) {
      if (type === 'error') {
        console.error(message);
      } else if (type === 'warn') {
        console.warn(message);
      } else {
        console.log(message);
      }
    }
  },
  
  // Enable verbose logging
  enableVerbose: function() {
    this.verbose = true;
    this.log('Verbose logging enabled for FeedbackLoop');
    return true;
  },
  
  // Disable verbose logging
  disableVerbose: function() {
    this.log('Verbose logging disabled for FeedbackLoop');
    this.verbose = false;
    return true;
  },
  
  sendFeedback: function(feedback) {
    try {
      // Use a custom event to communicate with the content script
      const customEvent = new CustomEvent('feedbackloop-send', { 
        detail: { feedback: feedback } 
      });
      window.dispatchEvent(customEvent);
      
      // Set up a listener for the response
      const responseHandler = function(event) {
        if (event.data && event.data.type === 'FEEDBACK_LOOP_RESPONSE') {
          if (event.data.success) {
            window.FeedbackLoop.log('Feedback sent successfully');
            if (event.data.warning) {
              window.FeedbackLoop.log('Warning: ' + event.data.warning, 'warn');
            }
          } else if (event.data.error) {
            // Always show errors, even in non-verbose mode
            console.error('Error sending feedback:', event.data.error);
          }
          // Remove the listener after receiving a response
          window.removeEventListener('message', responseHandler);
        }
      };
      
      // Add the response listener
      window.addEventListener('message', responseHandler);
      
      this.log('Feedback submitted. Waiting for confirmation...');
      return true;
    } catch (error) {
      // Always show errors, even in non-verbose mode
      console.error('Failed to send feedback:', error.message);
      console.log('If you\'re seeing "Extension context invalidated", try refreshing the page and try again.');
      return false;
    }
  }
};

// Listen for verbose mode toggle messages from the content script
window.addEventListener('message', function(event) {
  // Only accept messages from the same frame
  if (event.source !== window) return;

  // Check if the message is for toggling verbose mode
  if (event.data.type && event.data.type === 'FEEDBACK_LOOP_SET_VERBOSE') {
    if (event.data.value) {
      window.FeedbackLoop.enableVerbose();
    } else {
      window.FeedbackLoop.disableVerbose();
    }
  }
});

// Notify that the API is ready
window.dispatchEvent(new CustomEvent('feedbackloop-ready'));
window.FeedbackLoop.log('FeedbackLoop API is ready in page context'); 