const vscode = require('vscode');
const { exec } = require('child_process');
const path = require('path');

/**
 * @param {vscode.ExtensionContext} context
 */
function activate(context) {
    console.log('Feedback Flow extension is now active');

    // Register the command to add feedback log to composer
    let disposable = vscode.commands.registerCommand('feedbackflow.addToComposer', function () {
        const workspaceFolders = vscode.workspace.workspaceFolders;
        if (!workspaceFolders) {
            vscode.window.showErrorMessage('No workspace folder is open');
            return;
        }

        const scriptPath = path.join(workspaceFolders[0].uri.fsPath, 'add_feedback_to_composer.py');
        
        // Run the Python script
        exec(`python "${scriptPath}"`, (error, stdout, stderr) => {
            if (error) {
                vscode.window.showErrorMessage(`Error running script: ${error.message}`);
                return;
            }
            if (stderr) {
                vscode.window.showErrorMessage(`Script error: ${stderr}`);
                return;
            }
            
            vscode.window.showInformationMessage('Feedback log has been prepared for the Composer. You can now drag and drop it into the Composer.');
        });
    });

    context.subscriptions.push(disposable);
}

function deactivate() {}

module.exports = {
    activate,
    deactivate
}; 