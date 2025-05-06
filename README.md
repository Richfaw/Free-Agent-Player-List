# Free Player List Streamlit App

## Overview
Parses raw player data into a downloadable CSV via a Streamlit interface.
Includes columns:
- Player
- Position
- Nat.
- Nat. 2
- Age (numeric)
- Height
- Foot
- Last Club
- League
- Out of Contract Since
- Market Value

## Usage
1. Install dependencies:
   ```
   pip install streamlit pandas
   ```
2. Run the app:
   ```
   streamlit run streamlit_parser_app.py
   ```
3. Upload or paste your raw data.
4. Click **Parse & Download CSV** to retrieve `free_player_list.csv`.

## License
MIT
