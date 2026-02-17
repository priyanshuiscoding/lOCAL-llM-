# Local LLM (Streamlit)

## Run locally

```bash
streamlit run app.py
```

## Deploy on Streamlit Community Cloud

1. Push this project to a GitHub repository.
2. In Streamlit Community Cloud, create a new app from that repo.
3. Set `app.py` as the main file path.
4. Add secrets (if needed) in app settings (for database credentials).

## Important hosting note

This project currently uses `Ollama(model="mistral")` in `utils.py`.
Streamlit Community Cloud does not run a local Ollama server, so querying will fail unless you:
- host Ollama separately and call it over network, or
- switch to a cloud LLM provider (OpenAI/Groq/etc).
