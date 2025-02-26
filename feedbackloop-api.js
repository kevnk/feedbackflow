// Define the FeedbackLoop API in the global scope
window.FeedbackLoop = {
  sendFeedback: function(feedback) {
    // Use a custom event to communicate with the content script
    const customEvent = new CustomEvent('feedbackloop-send', { 
      detail: { feedback: feedback } 
    });
    window.dispatchEvent(customEvent);
    return true;
  }
};

// Notify that the API is ready
window.dispatchEvent(new CustomEvent('feedbackloop-ready'));
console.log('FeedbackLoop API is ready in page context'); 