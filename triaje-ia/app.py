"""Punto de entrada alternativo para plataformas que esperan `app.py` en la
raíz (Hugging Face Spaces con SDK Streamlit). El arranque normal sigue siendo
`python -m streamlit run app/main.py`.
"""

from app.main import main

main()
