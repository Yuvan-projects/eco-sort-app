import json
import urllib.request
import streamlit as st

st.set_page_config(
    page_title="Universal Barcode Lookup", page_icon="📦", layout="centered"
)

st.title("📦 Universal Barcode Lookup & Recycler")
st.write(
    "Type any product barcode number. If it's not in the database, our smart"
    " fallback will guide you!"
)

# Sidebar for API Key Configuration
st.sidebar.header("⚙️ API Configuration")
api_key = st.sidebar.text_input(
    "Product API Key (Optional)", type="password", value="HFAK0yKnr2GWvKImFMcFYn8rSePisNb"
)

# Main Barcode Typing Input
barcode_input = st.text_input(
    "Enter Barcode Number:", placeholder="e.g. 8904132956728"
)


def lookup_universal_barcode(code, key):
  if not key:
    return None, None
  url = f"https://go-upc.com/api/v1/code/{code}"
  headers = {"Authorization": f"Bearer {key}"}
  req = urllib.request.Request(url, headers=headers)
  try:
    with urllib.request.urlopen(req) as response:
      data = json.loads(response.read().decode("utf-8"))
      product = data.get("product", {})
      return product.get("name"), product.get("description")
  except Exception:
    return None, None


if st.button("Lookup & Get Advice"):
  if barcode_input:
    clean_code = barcode_input.strip()

    if not clean_code.isdigit():
      st.error("Please enter numbers only for the barcode.")
    else:
      product_name = None
      description = None

      with st.spinner("Searching databases..."):
        if api_key:
          product_name, description = lookup_universal_barcode(
              clean_code, api_key
          )

        if product_name:
          st.success(f"**Product Found:** {product_name}")
          if description:
            st.write(f"**Description:** {description}")
        else:
          st.info(
              "Barcode not found in the external database. Using material"
              " category fallback..."
          )

        # Universal Recycling Guidance (Always triggers so you get an answer)
        st.markdown("### 📋 Disposal Guidance")

        # Quick check based on barcode country code (e.g., 890 = India)
        if clean_code.startswith("890"):
          st.write(
              "* **Origin Note:** This item was manufactured or registered in"
              " India (Barcode prefix 890)."
          )

        st.write(
            "• **Rigid Plastic / Bottles / Jars:** Rinse clean and place in"
            " curbside recycling.\n"
            "• **Flexible Pouches / Soft Plastic Wrappers:** Typically cannot"
            " go in curbside bins. Check local store drop-off programs or place"
            " in landfill.\n"
            "• **Cardboard Boxes / Paper Packaging:** Flatten completely and"
            " place in paper recycling."
        )
  else:
    st.warning("Please type a barcode number first.")