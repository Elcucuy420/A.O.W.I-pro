# Admin Quickstart

Welcome to your AI Receptionist! Follow these steps to get up and running quickly:

1. **Choose a preset:** Pick an industry preset from `templates/industry-presets/` (e.g., `frisor_salong.json`, `klinikk_fysio.json`, `bilverksted.json`, `restaurant.json`) and copy it to `config/business.json`.
2. **Configure business hours:** Edit `config/hours.json` to reflect your opening hours and time zone.
3. **Enable integrations:** Update `config/integrations.json` to enable or disable Google Calendar, Gmail, Tripletex invoicing, and Vipps payments. Provide the necessary API tokens via environment variables.
4. **Customize flows:** The default conversation flows live in `flows/flows.nb.yaml`. Adjust the triggers, prompts, and actions to match your business process. No coding required!
5. **Install dependencies:** Run the installation script to set up a Python virtual environment and install requirements:
   ```bash
   bash scripts/install.sh
   ```
6. **Start the server:** Launch the FastAPI application with Uvicorn:
   ```bash
   uvicorn server.fastapi_app:app --reload
   ```
7. **Add the widget to your site:** Open `EMBED_SNIPPET.html` and copy its contents into the `<body>` of your website. Replace `YOUR_SERVER_DOMAIN` with your server's domain.

That's it! Your AI receptionist will now answer customer questions, handle bookings and inquiries, and forward leads to your email or calendar.
