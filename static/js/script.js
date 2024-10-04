// Get the chat output container
const chatOutputContainer = document.querySelector('.chat-output-container');

// Add an event listener to the form submission
document.getElementById('myForm').addEventListener('submit', async (e) => {
  e.preventDefault();

  // Get the form data
  const formData = new FormData(e.target);

  // Get the question text from the input field
  const questionInput = document.querySelector('input[name="question"]');
  const questionText = questionInput.value;

  // Send the request to the /ask route
  const response = await fetch('/ask', {
    method: 'POST',
    body: formData,
  });

  // Get the response text
  const responseText = await response.text();

  // Update the chat output container with the question and response
  const chatOutput = document.querySelector('.chat-output');
  const questionHtml = `<div class="question"><h3>${questionText}</h3></div>`;
  const responseHtml = `<div class="answer"><h3>${responseText}</h3></div>`;
  chatOutput.innerHTML += questionHtml + responseHtml;
});