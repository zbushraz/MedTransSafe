# MedTransSafe v0.1 — research demonstration

English–Urdu medical instruction change screening prototype. **Not clinically validated. Never use for patient care.**

## Run locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

Without a key, a *limited rule-based baseline* runs. It does not assess overall correctness. For the two-stage AI option, set `OPENAI_API_KEY` in the environment or in Streamlit Community Cloud Secrets (`OPENAI_API_KEY = "..."`). You may also enter a key in the sidebar during a private session. **Never commit keys to GitHub.** The model defaults to `gpt-4.1-mini` and can be changed in the UI. Model and API charges may apply.

## Get an actual shareable URL

1. Create a GitHub repository and upload `app.py`, `checker.py`, `requirements.txt`, `.gitignore`, and `README.md`.
2. Visit https://share.streamlit.io/ and select **Create app**, your repository, main branch, `app.py`.
3. In advanced settings add `OPENAI_API_KEY = "your-key"` as a secret (optional). Deploy. Copy the URL shown after deployment. Do not claim the app is online until the page opens.
4. Prefer private/restricted access while evaluating; a public app with your stored API key could cause unwanted charges. Use quotas and monitoring.

## Scientific reporting

The application implements two successive calls to a model prompted differently; **both calls may share systematic errors**. A warning is not a verified clinical danger and a no-issue verdict is not proof of safety. No F1/accuracy or reliability gain can be claimed without a held-out, independently expert-annotated evaluation. For the paper, accurately state implementation status and deployment date, and do not imply dataset-level evaluation if it has not happened.

## Data handling

AI mode transmits submitted texts to the configured API provider. Avoid patient names, IDs, private records and identifiable health details; review provider privacy/retention terms. Do not upload the full clinical dataset publicly without appropriate rights and de-identification.
