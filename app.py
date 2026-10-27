import streamlit as st

st.set_page_config(
    page_title="Eco-Sort Recycler", page_icon="♻️", layout="centered"
)

st.title("♻️ Eco-Sort & Recycle")
st.write(
    "Type an item name (e.g., plastic pouch, cardboard box, glass bottle) to get"
    " instant disposal advice!"
)

# Input field for the item name or barcode
query_input = st.text_input("Enter Item Name (e.g., plastic pouch, box):")

st.write("Or take a photo of the item:")
camera_image = st.camera_input("Take a picture")

if camera_image is not None:
  st.success("Photo captured!")


def get_recycling_advice(item):
  item_lower = item.lower()

  # Built-in smart recycling rules for common household materials
  if "plastic" in item_lower or "pouch" in item_lower or "wrapper" in item_lower:
    return (
        "**Recyclable (Soft Plastic / Store Drop-Off)**: Most flexible plastic"
        " pouches and wrappers cannot go in standard curbside bins. Check if"
        " your local grocery store has a soft plastic recycling drop-off bin,"
        " otherwise place in Landfill."
    )
  elif "cardboard" in item_lower or "box" in item_lower:
    return (
        "**Recyclable (Paper/Cardboard)**: Flatten the box completely. Ensure it"
        " is clean and dry (free of food residue or grease) before putting it"
        " in your recycling bin."
    )
  elif "glass" in item_lower or "bottle" in item_lower:
    return (
        "**Recyclable (Glass)**: Rinse out any remaining liquid. Remove caps or"
        " lids if they are made of a different material. Place in glass"
        " recycling."
    )
  elif "can" in item_lower or "tin" in item_lower or "aluminum" in item_lower:
    return (
        "**Recyclable (Metal)**: Rinse lightly and place in your curbside"
        " recycling bin. Metals can be recycled indefinitely!"
    )
  else:
    return (
        f"**General Guidance for '{item}'**: Check local municipal"
        " guidelines. If the item is clean and made of rigid plastic, paper, or"
        " metal, it is usually recyclable. When in doubt, place in Landfill to"
        " avoid contaminating other recyclables."
    )


if st.button("Get Recycling Advice"):
  if query_input:
    clean_query = query_input.strip()
    with st.spinner("Analyzing item..."):
      advice = get_recycling_advice(clean_query)

      st.markdown("### 📋 Disposal Guidance")
      st.write(advice)
  else:
    st.warning("Please enter an item name first.")