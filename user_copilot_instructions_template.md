# FeedbackFlow Integration Instructions

## Overview

This project uses FeedbackFlow, a Chrome extension that allows collecting user feedback from websites and sending it to AI assistants. The feedback is stored in a local log file that can be easily accessed in Cursor or VS Code.

## How to Use FeedbackFlow in JavaScript

### Basic Usage

To send feedback from your website to an AI assistant:

```javascript
// Check if FeedbackFlow is available
if (window.FeedbackFlow) {
  // Send feedback
  window.FeedbackFlow.sendFeedback("Your feedback message here");
}
```

### Handling Responses

To listen for responses from the FeedbackFlow extension:

```javascript
window.addEventListener('message', function(event) {
  if (event.source !== window) return;
  
  if (event.data.type && event.data.type === 'FEEDBACK_FLOW_RESPONSE') {
    console.log('Feedback sent:', event.data.success);
    // Handle the response here
  }
});
```

### Integration Examples

#### Adding a Feedback Button

```javascript
function createFeedbackButton() {
  const button = document.createElement('button');
  button.textContent = 'Send Feedback';
  button.addEventListener('click', () => {
    const feedback = prompt('Please enter your feedback:');
    if (feedback && window.FeedbackFlow) {
      window.FeedbackFlow.sendFeedback(feedback);
    }
  });
  document.body.appendChild(button);
}

// Call this function when the page loads
window.addEventListener('load', createFeedbackButton);
```

#### Creating a Feedback Form

```html
<form id="feedbackForm">
  <textarea id="feedbackText" placeholder="Enter your feedback"></textarea>
  <button type="submit">Send Feedback</button>
</form>

<script>
document.getElementById('feedbackForm').addEventListener('submit', function(e) {
  e.preventDefault();
  const feedback = document.getElementById('feedbackText').value;
  
  if (feedback && window.FeedbackFlow) {
    window.FeedbackFlow.sendFeedback(feedback);
    document.getElementById('feedbackText').value = '';
  }
});
</script>
```

## Reading Feedback in Cursor/VS Code

The feedback is stored in `~/.feedbackflow/feedback.log` and can be accessed using:

1. VS Code/Cursor tasks (if configured)
2. The `read_feedback.py` script from the FeedbackFlow project
3. Directly opening the log file

## Best Practices

1. Always check if `window.FeedbackFlow` exists before using it
2. Provide clear instructions to users about what kind of feedback is helpful
3. Consider adding keyboard shortcuts for sending feedback (e.g., Ctrl+Enter)
4. Handle responses to provide confirmation to users 