# save as app.py
import pandas as pd
import streamlit as st

# Load dataset
@st.cache_data
def load_data():
    df = pd.read_excel("Indian food database  (1).xlsx", sheet_name='Sheet1')
    df.columns = df.columns.str.strip()  # Remove spaces from column names
    return df

df = load_data()

# Debug: print columns so we know the exact names
# st.write(df.columns.tolist())  # Uncomment if you want to see them in the app

st.title("🥘 What Can I Cook? - Indian Recipe Finder")
st.write("Enter the ingredients you have, and I'll suggest recipes that use the most of them.")

# User input
user_input = st.text_input("Enter ingredients (comma-separated):")

if user_input:
    # Clean and split user input
    user_ingredients = [x.strip().lower() for x in user_input.split(",")]

    def match_score(row):
        recipe_ingredients = [x.strip().lower() for x in str(row['ingredients']).split(",")]
        return len(set(user_ingredients) & set(recipe_ingredients))

    # Calculate match score
    df['match_count'] = df.apply(match_score, axis=1)

    # Filter and sort recipes
    results = df[df['match_count'] > 0].sort_values(by='match_count', ascending=False)

    if not results.empty:
        st.subheader("Top Recipe Suggestions:")
        for idx, row in results.head(3).iterrows():
            st.markdown(f"### {row['name']}")
            st.write(f"*Matched Ingredients:* {row['match_count']}")
            st.write(f"*Ingredients:* {row['ingredients']}")
            st.write(f"*Recipe:* {row['Sweet Name Detailed Recipe']}")  # Updated column name
            st.markdown("---")
    else:
        st.warning("No matching recipes found.")