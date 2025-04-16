document.getElementById("explain").addEventListener("click", async () => {
    const responseEl = document.getElementById("response");
    responseEl.textContent = "Kouri is thinking...";
  
    chrome.storage.local.get(["selectedText"], async (result) => {
      const selectedText = result.selectedText?.trim();
  
      if (!selectedText) {
        responseEl.textContent = "No text selected.";
        return;
      }
  
      try {
        const res = await fetch("https://openrouter.ai/api/v1/chat/completions", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "Authorization": "Bearer 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"
          },
          body: JSON.stringify({
            model: "shisa-ai/shisa-v2-llama3.3-70b:free",
            messages: [
              {
                role: "user",
                content: `Summarize this to 100 words at max. Keep the important details: "${selectedText}"`
              }
            ]
          })
        });
  
        const data = await res.json();
        console.log("🔍 OpenRouter response:", data);
  
        const output = data?.choices?.[0]?.message?.content;
  
        if (output) {
          responseEl.textContent = output;
        } else if (data?.error) {
          responseEl.textContent = `API Error: ${data.error.message || JSON.stringify(data.error)}`;
        } else {
          responseEl.textContent = "Unknown response format.";
        }
  
      } catch (err) {
        console.error("🚨 Fetch error:", err);
        responseEl.textContent = "Fetch Error: " + err.message;
      }
    });
  });
  