// Define the path for the log file
// We'll use a hidden folder in the user's home directory
const LOG_FILE_PATH = '.feedbackloop/feedback.log';

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
        console.log('Feedback saved to local storage');
        
        // Also try to send to a native host if available
        try {
          chrome.runtime.sendNativeMessage(
            'com.feedbackloop.host',
            {
              action: 'writeFeedback',
              path: LOG_FILE_PATH,
              content: feedbackEntry
            },
            function(response) {
              if (response && response.success) {
                console.log('Feedback saved to log file');
                sendResponse({ success: true });
              } else {
                console.warn('Failed to save to log file, but saved to local storage');
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
      console.log('Feedback cleared from local storage');
      
      // Also try to send to a native host if available
      try {
        chrome.runtime.sendNativeMessage(
          'com.feedbackloop.host',
          {
            action: 'clearFeedback',
            path: LOG_FILE_PATH
          },
          function(response) {
            if (response && response.success) {
              console.log('Feedback log file cleared');
              sendResponse({ success: true });
            } else {
              console.warn('Failed to clear log file, but cleared local storage');
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
}); 