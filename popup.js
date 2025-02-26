document.addEventListener('DOMContentLoaded', function() {
  const feedbackText = document.getElementById('feedback-text');
  const sendButton = document.getElementById('send-feedback');
  const clearButton = document.getElementById('clear-feedback');
  const statusDiv = document.getElementById('status');

  // Get the current tab information
  async function getCurrentTab() {
    const queryOptions = { active: true, currentWindow: true };
    const [tab] = await chrome.tabs.query(queryOptions);
    return tab;
  }

  // Send feedback when button is clicked
  sendButton.addEventListener('click', async function() {
    const feedback = feedbackText.value.trim();
    
    if (!feedback) {
      statusDiv.textContent = 'Please enter some feedback.';
      statusDiv.className = 'status error';
      return;
    }

    try {
      const tab = await getCurrentTab();
      const message = {
        action: 'saveFeedback',
        feedback: feedback,
        url: tab.url,
        title: tab.title,
        timestamp: new Date().toISOString()
      };

      // Send message to background script
      chrome.runtime.sendMessage(message, function(response) {
        if (response && response.success) {
          statusDiv.textContent = 'Feedback sent successfully!';
          statusDiv.className = 'status success';
          feedbackText.value = '';
        } else {
          statusDiv.textContent = 'Error: ' + (response ? response.error : 'Unknown error');
          statusDiv.className = 'status error';
        }
      });
    } catch (error) {
      statusDiv.textContent = 'Error: ' + error.message;
      statusDiv.className = 'status error';
    }
  });

  // Clear feedback log when clear button is clicked
  clearButton.addEventListener('click', function() {
    // Show confirmation dialog
    if (confirm('Are you sure you want to clear the feedback log? This cannot be undone.')) {
      // Send message to background script
      chrome.runtime.sendMessage({ action: 'clearFeedback' }, function(response) {
        if (response && response.success) {
          statusDiv.textContent = 'Feedback log cleared successfully!';
          statusDiv.className = 'status success';
        } else {
          statusDiv.textContent = 'Error: ' + (response ? response.error : 'Unknown error');
          statusDiv.className = 'status error';
        }
      });
    }
  });
}); 