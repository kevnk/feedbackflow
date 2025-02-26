- [x] Is there a way to add the feedback.log to the context of composer easily in cursor/vscode?
- [x] Is there a way to clear the feedback.log? 
- [x] For sending feedback (in the popup and sample website), send feedback with command/crtl + enter; add the shortcut indication on the button 
- [x] if I run watch log in cursor, every time it updates, can we run "Add Feedback to Composer"? is those possible?
- [x] Error when trying to send feedback from console.
	```
	FeedbackFlow.sendFeedback("ok what's up")
	content.js:38 Uncaught Error: Extension context invalidated.
			at content.js:38:20
	(anonymous) @ content.js:38Understand this errorAI
	true
	```
- [ ] instead of creating a copy of the feedback.log, can we just open the ~/.feedbackflow/feedback.log file in the editor?
- [ ] is native-host/com.feedbackflow.host.json created when the extension is installed, if so, it probably should be in the repo. If not, we shouldn't use my username in the path.