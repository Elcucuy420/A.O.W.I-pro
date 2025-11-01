(function() {
  // Create the container for the chat widget
  const widget = document.createElement('div');
  widget.id = 'ai-resepsjonist-widget';
  widget.style.position = 'fixed';
  widget.style.bottom = '20px';
  widget.style.right = '20px';
  widget.style.width = '320px';
  widget.style.height = '420px';
  widget.style.boxShadow = '0 2px 8px rgba(0,0,0,0.15)';
  widget.style.background = '#fff';
  widget.style.borderRadius = '8px';
  widget.style.overflow = 'hidden';
  widget.style.zIndex = '9999';

  // Build the inner HTML structure
  widget.innerHTML = `
    <div style="background:#007acc;color:white;padding:10px;font-weight:bold;">AI Resepsjonist</div>
    <div id="chat-messages" style="padding:10px;height:300px;overflow-y:auto;font-family: sans-serif;font-size:14px;"></div>
    <form id="chat-form" style="display:flex;border-top:1px solid #eee;">
      <input id="chat-input" type="text" placeholder="Skriv en melding..." style="flex:1;padding:8px;border:none;outline:none;">
      <button type="submit" style="background:#007acc;color:white;border:none;padding:8px 12px;cursor:pointer;">Send</button>
    </form>
  `;

  document.body.appendChild(widget);

  const messagesEl = widget.querySelector('#chat-messages');
  const formEl = widget.querySelector('#chat-form');
  const inputEl = widget.querySelector('#chat-input');

  formEl.addEventListener('submit', async (event) => {
    event.preventDefault();
    const text = inputEl.value.trim();
    if (!text) return;
    // Append user message
    messagesEl.innerHTML += `<div style="margin-bottom:8px;"><strong>Du:</strong> ${text}</div>`;
    inputEl.value = '';
    messagesEl.scrollTop = messagesEl.scrollHeight;

    try {
      const response = await fetch('/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ message: text, session_id: 'anonymous' })
      });
      const data = await response.json();
      messagesEl.innerHTML += `<div style="margin-bottom:8px;"><strong>AI:</strong> ${data.reply || data.message || ''}</div>`;
      messagesEl.scrollTop = messagesEl.scrollHeight;
    } catch (err) {
      messagesEl.innerHTML += `<div style="margin-bottom:8px;color:red;">Feil ved henting av svar.</div>`;
    }
  });
})();
