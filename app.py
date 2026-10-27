import base64
import json
import urllib.request
import streamlit as st

st.set_page_config(
    page_title="Eco-Vision Hybrid Recycler", page_icon="♻️", layout="centered"
)

st.title("♻️ Eco-Vision Hybrid Recycler")
st.write(
    "Take a picture or upload an image. The app will try AI analysis, with an"
    " instant local fallback if offline!"
)

# Sidebar for optional API configuration
st.sidebar.header("⚙️ AI Configuration")
api_token = st.sidebar.text_input(
    "Hugging Face API Token (Optional)", type="password", value="HFAKQWGcnxgUYmyOWgLgg9Huro4B0dl"
)

# Image capture options
camera_image = st.camera_input("Take a photo of the item")
uploaded_image = st.file_uploader(
    "Or upload an image file", type=["jpg", "jpeg", "png"]
)

active_image = camera_image if camera_image is not None else uploaded_image


def get_local_fallback_advice():
  return """
    **[Local Rules Engine Fallback]**
    Based on standard household material guidelines:
    * **Rigid Plastics / Bottles:** Rinse clean and place in curbside recycling.
    * **Flexible Plastics / Wrappers:** Cannot go in curbside bins. Check local grocery store drop-off bins or place in landfill.
    * **Cardboard / Paper:** Flatten completely and place in paper recycling.
    * **Glass Jars:** Rinse and place in glass recycling.
    * **Metal Cans:** Rinse lightly and place in metal recycling.
    """


def analyze_with_ai(image_file, token):
  model_id = "meta-llama/Llama-3.2-11B-Vision-Instruct"
  url = f"https://api-inference.huggingface.co/models/{model_id}"

  bytes_data = image_file.getvalue()
  base64_image = base64.b64encode(bytes_data).decode("utf-8")

  headers = {
      "Authorization": f"Bearer {token}",
      "Content-Type": "application/json",
  }

  payload = {
      "inputs": {
          "image": f"data:image/jpeg;base64,{base64_image}",
          "prompt": (
              "Analyze this item. Identify the material and provide clear"
              " disposal guidance (Recyclable, Compostable, or Landfill)."
          ),
      }
  }

  req = urllib.request.Request(
      url, data=json.dumps(payload).encode("utf-8"), headers=headers, method="POST"
  )

  with urllib.request.urlopen(req, timeout=10) as response:
    result = json.loads(response.read().decode("utf-8"))
    if isinstance(result, list) and len(result) > 0:
      return result[0].get("generated_text", "No response text found.")
    elif isinstance(result, dict) and "generated_text" in result:
      return result["generated_text"]
    return str(result)


if active_image is not None:
  st.success("Image received successfully!")
  st.image(active_image, caption="Your Uploaded Item", width="stretch")
  if st.button("Analyze Photo"):
    advice = ""

    # Hybrid Logic: Try AI if token exists, otherwise or on error, fallback to local rules
    if api_token:
      with st.spinner("Contacting Vision AI API..."):
        try:
          advice = analyze_with_ai(active_image, api_token)
          st.success("Successfully analyzed using AI API!")
        except Exception as e:
          st.info(
              f"API connection skipped/failed ({e}). Switching to local"
              " rules..."
          )
          advice = get_local_fallback_advice()
    else:
      with st.spinner("No API token detected. Applying local rules..."):
        advice = get_local_fallback_advice()

    st.markdown("### 📋 Disposal Guidance")
    st.write(advice)
else:
  st.info("Please take a photo or upload an image above to get started.")