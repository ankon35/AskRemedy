async function askQuestion() {
  const question = document.getElementById("question").value.trim();
  const answerEl = document.getElementById("answer");
  const sourceEl = document.getElementById("source");

  if (!question) {
    alert("Please enter a question!");
    return;
  }

  answerEl.innerText = "Loading...";
  sourceEl.innerText = "";

  try {
    const res = await fetch("http://127.0.0.1:5000/ask", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ question }),
    });

    const data = await res.json();

    if (data.error) {
      answerEl.innerText = data.error;
    } else {
      const fullText = data.answer.trim();

      // Split the text into sentences (naive split on '. ')
      const sentences = fullText.split(/(?<=\.)\s+/).filter(Boolean);

      let formattedHTML = "";

      if (sentences.length > 0) {
        // First sentence as intro
        formattedHTML += `<p>${sentences[0]}</p>`;

        if (sentences.length > 1) {
          // Numbered list starts from second sentence
          formattedHTML += "<ol style='padding-left: 20px; line-height: 1.6;'>";
          for (let i = 1; i < sentences.length; i++) {
            formattedHTML += `<li>${sentences[i]}</li>`;
          }
          formattedHTML += "</ol>";
        }
      }

      answerEl.innerHTML = formattedHTML;
      sourceEl.innerText = "Source: " + (data.sources?.join(", ") || "N/A");
    }
  } catch (error) {
    answerEl.innerText = "Something went wrong. Check your server.";
    console.error(error);
  }
}
