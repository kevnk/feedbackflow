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

    // Register command to start MCP server
    let startMcpServer = vscode.commands.registerCommand('feedbackflow.startMcpServer', function () {
        const workspaceFolders = vscode.workspace.workspaceFolders;
        if (!workspaceFolders) {
            vscode.window.showErrorMessage('No workspace folder is open');
            return;
        }

        const ffMcpPath = path.join(workspaceFolders[0].uri.fsPath, 'ff-mcp');
        
        // Ask user for transport type
        vscode.window.showQuickPick(['SSE (default)', 'stdio'], {
            placeHolder: 'Select transport protocol'
        }).then(transport => {
            if (!transport) return; // User cancelled
            
            const transportArg = transport.startsWith('stdio') ? '--transport stdio' : '';
            
            // Run the MCP server
            const terminal = vscode.window.createTerminal('FeedbackFlow MCP');
            terminal.show();
            terminal.sendText(`python "${ffMcpPath}" start ${transportArg}`);
            
            vscode.window.showInformationMessage('FeedbackFlow MCP server started. Check the terminal for details.');
        });
    });

    context.subscriptions.push(startMcpServer);

    // Register command to stop MCP server
    let stopMcpServer = vscode.commands.registerCommand('feedbackflow.stopMcpServer', function () {
        const workspaceFolders = vscode.workspace.workspaceFolders;
        if (!workspaceFolders) {
            vscode.window.showErrorMessage('No workspace folder is open');
            return;
        }

        const ffMcpPath = path.join(workspaceFolders[0].uri.fsPath, 'ff-mcp');
        
        // Run the stop command
        const terminal = vscode.window.createTerminal('FeedbackFlow MCP');
        terminal.show();
        terminal.sendText(`python "${ffMcpPath}" stop`);
        
        vscode.window.showInformationMessage('FeedbackFlow MCP server stop command sent. Check the terminal for details.');
    });

    context.subscriptions.push(stopMcpServer);

    // Register command to setup Cursor MCP integration
    let setupCursorMcp = vscode.commands.registerCommand('feedbackflow.setupCursorMcp', function () {
        const workspaceFolders = vscode.workspace.workspaceFolders;
        if (!workspaceFolders) {
            vscode.window.showErrorMessage('No workspace folder is open');
            return;
        }

        const ffMcpPath = path.join(workspaceFolders[0].uri.fsPath, 'ff-mcp');
        
        // Run the cursor setup command
        const terminal = vscode.window.createTerminal('FeedbackFlow MCP');
        terminal.show();
        terminal.sendText(`python "${ffMcpPath}" cursor`);
        
        vscode.window.showInformationMessage('FeedbackFlow Cursor MCP setup started. Follow the instructions in the terminal.');
    });

    context.subscriptions.push(setupCursorMcp);
}

function deactivate() {}

module.exports = {
    activate,
    deactivate
}; 