# Assets

This folder is reserved for optional static assets used by the Coddy Buddy
registration app, such as a logo or banner image.

No assets are required for the application to run — the current UI is built
entirely with Streamlit components and custom CSS (see `app.py`).

If you'd like to add a logo:

1. Place an image file here, e.g. `assets/logo.png`.
2. In `app.py`, load it with:

   ```python
   st.image("assets/logo.png", width=160)
   ```