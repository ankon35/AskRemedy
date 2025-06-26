async function askQuestion() {
  const question = document.getElementById("question").value.trim();
  const answerEl = document.getElementById("answer");
  const sourceEl = document.getElementById("source");
  const headingEl = document.getElementById("answerHeading");
  const loaderEl = document.getElementById("loader");

  if (!question) {
    alert("Please enter a question!");
    return;
  }

  // Hide answer, heading and show loader
  answerEl.style.display = "none";
  headingEl.style.display = "none";
  sourceEl.innerText = "";
  loaderEl.style.display = "block"; // Show loading spinner

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
      const sentences = fullText.split(/(?<=\.)\s+/).filter(Boolean);

      let formattedHTML = "";

      if (sentences.length > 0) {
        formattedHTML += `<p>${sentences[0]}</p>`;

        if (sentences.length > 1) {
          formattedHTML += "<ol style='padding-left: 20px; line-height: 1.6;'>";
          for (let i = 1; i < sentences.length; i++) {
            formattedHTML += `<li>${sentences[i]}</li>`;
          }
          formattedHTML += "</ol>";
        }
      }

      answerEl.innerHTML = formattedHTML;

      // Scroll answer to top so text starts from the start
      answerEl.scrollTop = 0;

      sourceEl.innerText = "Source: " + (data.sources?.join(", ") || "N/A");
    }

    // Show heading and answer, hide loader
    headingEl.style.display = "block";
    answerEl.style.display = "block";
    loaderEl.style.display = "none";

  } catch (error) {
    answerEl.innerText = "Something went wrong. Check your server.";
    headingEl.style.display = "block";
    answerEl.style.display = "block";
    loaderEl.style.display = "none";
    console.error(error);
  }
}
