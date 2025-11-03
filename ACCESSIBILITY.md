# Accessibility Guidelines

To make the AI Receptionist widget accessible to all users, including those using screen readers or keyboard navigation, follow these best practices:

- **Semantic HTML:** The embed widget (`embed.js`) uses `<button>`, `<label>`, and `<input>` elements appropriately so that assistive technologies can identify interactive components.
- **Focus management:** When the chat window opens, focus is moved to the input field. After sending a message, focus returns to the message input. Users can navigate between messages and controls using the keyboard.
- **High contrast:** Ensure the chat widget contrasts sufficiently with your website’s background. You can override colors in your site’s CSS to meet WCAG AA contrast ratios.
- **Keyboard navigation:** All interactive elements in the widget are reachable via `Tab` and actionable via `Enter` or `Space` keys.
- **Aria labels:** The widget includes `aria-label` attributes for buttons and input fields to provide descriptive labels for screen readers.
- **Responsive design:** The chat widget adapts to mobile and desktop viewports. Ensure there is enough space on your page to avoid overlapping important content.

By adhering to these guidelines, you ensure that users of all abilities can interact with your AI receptionist effectively.
