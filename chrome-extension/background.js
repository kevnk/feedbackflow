// Define the path for the log file
// We'll use a hidden folder in the user's home directory
const LOG_FILE_PATH = '.feedbackflow/feedback.log';

// Store the verbose mode state
let verboseMode = false;

// Listen for messages from popup or content scripts
chrome.runtime.onMessage.addListener(function(message, sender, sendResponse) {
  if (message.action === 'saveFeedback') {
    // Format the feedback entry
    const feedbackEntry = `
-------------------------------
Timestamp: ${message.timestamp}
URL: ${message.url}
Title: ${message.title}
Feedback: ${message.feedback}
-------------------------------
`;

    // Use Native Messaging to communicate with a native host application
    // that will write to the log file
    // Note: This requires setting up a native messaging host
    // For now, we'll store in local storage as a fallback
    chrome.storage.local.get(['feedbackLog'], function(result) {
      let feedbackLog = result.feedbackLog || '';
      feedbackLog += feedbackEntry;
      
      chrome.storage.local.set({ feedbackLog: feedbackLog }, function() {
        if (verboseMode) console.log('Feedback saved to local storage');
        
        // Also try to send to a native host if available
        try {
          chrome.runtime.sendNativeMessage(
            'com.feedbackflow.host',
            {
              action: 'writeFeedback',
              path: LOG_FILE_PATH,
              content: feedbackEntry
            },
            function(response) {
              if (response && response.success) {
                if (verboseMode) console.log('Feedback saved to log file');
                sendResponse({ success: true });
              } else {
                if (verboseMode) console.warn('Failed to save to log file, but saved to local storage');
                sendResponse({ 
                  success: true, 
                  warning: 'Saved to extension storage only. Native messaging not available.'
                });
              }
            }
          );
        } catch (error) {
          console.error('Native messaging error:', error);
          sendResponse({ 
            success: true, 
            warning: 'Saved to extension storage only. Native messaging error: ' + error.message
          });
        }
      });
    });
    
    // Return true to indicate we will send a response asynchronously
    return true;
  }
  else if (message.action === 'clearFeedback') {
    // Clear the feedback in local storage
    chrome.storage.local.set({ feedbackLog: '' }, function() {
      if (verboseMode) console.log('Feedback cleared from local storage');
      
      // Also try to send to a native host if available
      try {
        chrome.runtime.sendNativeMessage(
          'com.feedbackflow.host',
          {
            action: 'clearFeedback',
            path: LOG_FILE_PATH
          },
          function(response) {
            if (response && response.success) {
              if (verboseMode) console.log('Feedback log file cleared');
              sendResponse({ success: true });
            } else {
              if (verboseMode) console.warn('Failed to clear log file, but cleared local storage');
              sendResponse({ 
                success: true, 
                warning: 'Cleared extension storage only. Native messaging not available.'
              });
            }
          }
        );
      } catch (error) {
        console.error('Native messaging error:', error);
        sendResponse({ 
          success: true, 
          warning: 'Cleared extension storage only. Native messaging error: ' + error.message
        });
      }
    });
    
    // Return true to indicate we will send a response asynchronously
    return true;
  }
  else if (message.action === 'toggleVerbose') {
    // Toggle verbose mode
    verboseMode = message.value !== undefined ? message.value : !verboseMode;
    
    // Store the setting
    chrome.storage.local.set({ verboseMode: verboseMode }, function() {
      if (verboseMode) {
        console.log('Verbose mode enabled');
      } else {
        console.log('Verbose mode disabled');
      }
    });
    
    // Broadcast to all tabs
    chrome.tabs.query({}, function(tabs) {
      for (let tab of tabs) {
        try {
          chrome.tabs.sendMessage(tab.id, {
            action: 'setVerbose',
            value: verboseMode
          });
        } catch (error) {
          // Ignore errors for tabs that don't have our content script
        }
      }
    });
    
    sendResponse({ success: true, verbose: verboseMode });
    return true;
  }
});

// Initialize verbose mode from storage
chrome.storage.local.get(['verboseMode'], function(result) {
  verboseMode = result.verboseMode || false;
  if (verboseMode) {
    console.log('Verbose mode initialized to: ' + verboseMode);
  }
}); 