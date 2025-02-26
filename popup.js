document.addEventListener('DOMContentLoaded', function() {
  const feedbackText = document.getElementById('feedback-text');
  const sendButton = document.getElementById('send-feedback');
  const clearButton = document.getElementById('clear-feedback');
  const statusDiv = document.getElementById('status');
  const verboseToggle = document.getElementById('verbose-mode');

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

  // Initialize verbose mode toggle from storage
  chrome.storage.local.get(['verboseMode'], function(result) {
    verboseToggle.checked = result.verboseMode || false;
  });

  // Handle verbose mode toggle
  verboseToggle.addEventListener('change', function() {
    const isVerbose = verboseToggle.checked;
    
    // Send message to background script to toggle verbose mode
    chrome.runtime.sendMessage({ 
      action: 'toggleVerbose', 
      value: isVerbose 
    }, function(response) {
      if (response && response.success) {
        statusDiv.textContent = isVerbose ? 'Verbose mode enabled' : 'Verbose mode disabled';
        statusDiv.className = 'status success';
        
        // Clear status after 2 seconds
        setTimeout(function() {
          statusDiv.textContent = '';
          statusDiv.className = 'status';
        }, 2000);
      }
    });
  });

  // Get the current tab information
  async function getCurrentTab() {
    const queryOptions = { active: true, currentWindow: true };
    const [tab] = await chrome.tabs.query(queryOptions);
    return tab;
  }

  // Function to send feedback
  async function sendFeedback() {
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