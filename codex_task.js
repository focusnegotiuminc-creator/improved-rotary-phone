// codex_task.js - Task Runner for GitHub Remote Connector

const { exec } = require('child_process');

// Function to execute a command
function execute(command) {
    return new Promise((resolve, reject) => {
        exec(command, (error, stdout, stderr) => {
            if (error) {
                reject(`Error: ${stderr}`);
            }
            resolve(stdout);
        });
    });
}

// Function to run GitHub connector tasks
async function runTask(task) {
    try {
        const output = await execute(task);
        console.log(`Task Output: ${output}`);
    } catch (error) {
        console.error(error);
    }
}

// Example usage
const task = 'git status'; // Replace with your task command
runTask(task);