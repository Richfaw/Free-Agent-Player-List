import streamlit as st
import pandas as pd
import re

st.set_page_config(page_title="Free Player List", layout="wide")
st.title("📋 Free Player List")

st.markdown(
    "Upload a text file or paste raw player data, then click **Parse & Download CSV** to get a clean CSV file including Nat. and Nat. 2."
)

# --- Input Data ---
uploaded_file = st.file_uploader("Upload TXT file", type=["txt"])
raw_text = uploaded_file.read().decode("utf-8") if uploaded_file else st.text_area("Or paste data here:", height=200)

df = None

if st.button("Parse & Download CSV"):
    if not raw_text.strip():
        st.error("Please provide data to parse.")
    else:
        # Group lines into records
        lines = [l.strip() for l in raw_text.splitlines() if l.strip()]
        end_re = re.compile(r'^[A-Za-z]{3,9} \d{1,2}, \d{4}\s+€')
        records, current = [], []
        for line in lines:
            current.append(line)
            if end_re.match(line):
                records.append(current)
                current = []

        parsed = []
        for rec in records:
            player = rec[0].split('\t')[0]
            position = rec[1]
            # Locate the age/height line by 'm' in text
            idx = next(i for i, l in enumerate(rec) if re.search(r'\d+\.?\d*\s*m', l))
            age_line = rec[idx]
            # Split fields by tab or space
            fields = age_line.split('\t') if '\t' in age_line else age_line.split()
            # Extract nationalities: separate lines before idx
            nationals = rec[2:idx]
            # If nationality is included in age line, add it
            if fields and not fields[0].isdigit():
                nationals.append(fields[0])
            nat1 = nationals[0] if len(nationals) > 0 else ''
            nat2 = nationals[1] if len(nationals) > 1 else ''
            # Determine age position: first numeric field
            age_idx = next((i for i, v in enumerate(fields) if v.isdigit()), 1)
            age = fields[age_idx]
            height = fields[age_idx + 1]
            foot = fields[-1]
            # Last Club
            last_club = rec[idx + 1].split('\t')[0]
            # League: drop leading nationality if present
            league_line = rec[idx + 2]
            tokens = league_line.split()
            league = ' '.join(tokens[1:]) if tokens and tokens[0] in nationals else league_line
            # Out of contract and market value
            out_line = rec[idx + 3]
            out_fields = out_line.split('\t') if '\t' in out_line else out_line.split()
            out_date, market_val = out_fields[0], out_fields[1]

            parsed.append({
                'Player': player,
                'Position': position,
                'Nat.': nat1,
                'Nat. 2': nat2,
                'Age': int(age),
                'Height': height,
                'Foot': foot,
                'Last Club': last_club,
                'League': league,
                'Out of Contract Since': out_date,
                'Market Value': market_val
            })

        df = pd.DataFrame(parsed)
        st.success(f"Parsed {len(df)} records successfully!")
        # Center and auto-size
        styled = (
            df.style
              .set_properties(**{'text-align': 'center'})
              .set_table_styles([
                  {'selector': 'th', 'props': [('text-align', 'center')]},
                  {'selector': 'td', 'props': [('text-align', 'center')]}
              ])
        )
        st.dataframe(styled, use_container_width=True)
        # CSV download
        csv_bytes = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Download CSV",
            data=csv_bytes,
            file_name="free_player_list.csv",
            mime="text/csv"
        )
