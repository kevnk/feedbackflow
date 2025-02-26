#!/usr/bin/env node

const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');
const os = require('os');

// Get the directory where this script is located
const scriptDir = path.dirname(fs.realpathSync(__filename));

console.log('Installing FeedbackFlow globally...');

try {
  // Check if npm is available
  execSync('npm --version', { stdio: 'ignore' });
  
  // Try to install globally with npm
  console.log('Installing with npm...');
  execSync('npm install -g .', { 
    cwd: scriptDir,
    stdio: 'inherit'
  });
  
  console.log('\nFeedbackFlow installed successfully!');
  console.log('\nYou can now use FeedbackFlow from anywhere with:');
  console.log('  feedbackflow <command>');
  
  // Add instructions for Cursor MCP integration
  console.log('\nTo add FeedbackFlow to Cursor\'s MCP settings, add this to your Cursor settings:');
  console.log(`
"mcp.commands": {
  "feedbackflow": {
    "name": "FeedbackFlow",
    "command": "feedbackflow",
    "args": ["mcp", "start", "--cursor"]
  }
}
`);
  
} catch (error) {
  console.error('Error installing FeedbackFlow globally:');
  console.error(error.message);
  
  // Suggest alternative installation methods
  console.log('\nAlternatively, you can use FeedbackFlow with npx without installing:');
  console.log('  npx feedbackflow <command>');
  
  process.exit(1);
} 