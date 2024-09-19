// Get the chat output container
const chatOutputContainer = document.querySelector('.chat-output-container');

// Add an event listener to the form submission
document.getElementById('myForm').addEventListener('submit', async (e) => {
  e.preventDefault();

  // Get the form data
  const formData = new FormData(e.target);

  // Send the request to the /ask route
  const response = await fetch('/ask', {
    method: 'POST',
    body: formData,
  });

  // Get the response text
  const responseText = await response.text();

  // Update the chat output container with the response
  const chatOutput = document.querySelector('.chat-output');
  chatOutput.innerHTML += `<p>${responseText}</p>`;
});