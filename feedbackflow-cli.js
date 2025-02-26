#!/usr/bin/env node

const { spawn, execSync } = require('child_process');
const path = require('path');
const fs = require('fs');

// Get the directory where this script is located
const scriptDir = path.dirname(fs.realpathSync(__filename));

// Main function to handle CLI commands
function main() {
  const args = process.argv.slice(2);
  
  if (args.length === 0 || args[0] === '--help' || args[0] === '-h') {
    showHelp();
    return;
  }

  const command = args[0];
  const commandArgs = args.slice(1);

  switch (command) {
    case 'add-to-composer':
      runPythonScript('add_feedback_to_composer.py', commandArgs);
      break;
    case 'start-mcp':
      runPythonScript('mcp_server.py', commandArgs);
      break;
    case 'setup-cursor-mcp':
      runPythonScript('ff-mcp', ['cursor', ...commandArgs]);
      break;
    case 'install-mcp':
      runPythonScript('install_mcp.py', commandArgs);
      break;
    case 'read':
      runPythonScript('read_feedback.py', commandArgs);
      break;
    case 'clear':
      runPythonScript('clear_feedback.py', commandArgs);
      break;
    case 'check-extension':
      runPythonScript('check_extension.py', commandArgs);
      break;
    case 'mcp':
      // Handle MCP subcommands
      if (commandArgs.length === 0) {
        console.error('Error: Missing MCP subcommand');
        showMcpHelp();
        return;
      }
      
      const mcpCommand = commandArgs[0];
      const mcpArgs = commandArgs.slice(1);
      
      switch (mcpCommand) {
        case 'start':
          runPythonScript('ff-mcp', ['start', ...mcpArgs]);
          break;
        case 'stop':
          runPythonScript('ff-mcp', ['stop', ...mcpArgs]);
          break;
        case 'install':
          runPythonScript('ff-mcp', ['install', ...mcpArgs]);
          break;
        case 'cursor':
          runPythonScript('ff-mcp', ['cursor', ...mcpArgs]);
          break;
        default:
          console.error(`Error: Unknown MCP subcommand: ${mcpCommand}`);
          showMcpHelp();
      }
      break;
    default:
      // Pass all arguments to ff.py for any other commands
      runPythonScript('ff.py', args);
  }
}

// Function to run a Python script
function runPythonScript(scriptName, args = []) {
  const scriptPath = path.join(scriptDir, scriptName);
  
  // Determine Python executable (python3 or python)
  let pythonCmd = 'python3';
  try {
    execSync('python3 --version', { stdio: 'ignore' });
  } catch (e) {
    pythonCmd = 'python';
  }

  // Spawn the process
  const pythonProcess = spawn(pythonCmd, [scriptPath, ...args], {
    stdio: 'inherit',
    shell: process.platform === 'win32' // Use shell on Windows
  });

  pythonProcess.on('error', (err) => {
    console.error(`Error executing ${scriptName}: ${err.message}`);
    process.exit(1);
  });

  pythonProcess.on('close', (code) => {
    if (code !== 0) {
      console.error(`${scriptName} exited with code ${code}`);
      process.exit(code);
    }
  });
}

// Show help information
function showHelp() {
  console.log(`
FeedbackFlow CLI - Collect and manage feedback for AI-driven development

Usage:
  npx feedbackflow <command> [options]

Commands:
  add-to-composer       Add feedback log to Cursor composer
  start-mcp             Start the MCP server
  setup-cursor-mcp      Setup Cursor MCP integration
  install-mcp           Install MCP components
  read                  Read feedback log
  clear                 Clear feedback log
  check-extension       Check if the Chrome extension is installed
  mcp <subcommand>      MCP-related commands (start, stop, install, cursor)

Options:
  --help, -h            Show this help message

For more information, visit: https://github.com/yourusername/feedbackflow
`);
}

// Show MCP-specific help
function showMcpHelp() {
  console.log(`
FeedbackFlow MCP Commands:

Usage:
  npx feedbackflow mcp <subcommand> [options]

Subcommands:
  start                 Start the MCP server
  stop                  Stop the MCP server
  install               Install MCP as a service
  cursor                Setup Cursor MCP integration

Options:
  --transport <type>    Transport type (default: sse)
  --port <number>       Port number (default: 8080)
  --cursor              Run in Cursor mode
`);
}

// Run the main function
main(); 