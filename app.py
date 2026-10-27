import base64
import json
import urllib.request
import streamlit as st

st.set_page_config(
    page_title="Eco-Vision Recycler", page_icon="📸", layout="centered"
)

st.title("📸 Snap & Recycle")
st.write(
    "Take a picture or upload an image of your item to get instant AI disposal"
    " advice!"
)

# Sidebar for API Key
st.sidebar.header("⚙️ API Configuration")
api_token = st.sidebar.text_input(
    "Hugging Face API Token", type="password", value="HFAK0yKnr2GWvKImFMcFYn8rSePisNb"
)

# Image capture options
camera_image = st.camera_input("Take a photo of the item")
uploaded_image = st.file_uploader(
    "Or upload an image file", type=["jpg", "jpeg", "png"]
)

# Pick whichever input the user provided
active_image = camera_image if camera_image is not None else uploaded_image


def analyze_image_with_vision_ai(image_file, token):
  if not token:
    return (
        "**Error:** Please enter your Hugging Face API Token in the sidebar"
        " first!"
    )

  # Model endpoint for a vision-language model
  model_id = "meta-llama/Llama-3.2-11B-Vision-Instruct"
  url = f"https://api-inference.huggingface.co/models/{model_id}"

  # Read image bytes and convert to base64
  bytes_data = image_file.getvalue()
  base64_image = base64.b64encode(bytes_data).decode("utf-8")

  headers = {
      "Authorization": f"Bearer {token}",
      "Content-Type": "application/json",
  }

  # Prompt payload for vision analysis
  payload = {
      "inputs": {
          "image": f"data:image/jpeg;base64,{base64_image}",
          "prompt": (
              "Analyze this item. Identify what material it is made of"
              " (e.g. plastic film, cardboard, glass, rigid plastic). Then"
              " give clear disposal guidance: is it Recyclable, Compostable,"
              " or Landfill?"
          ),
      }
  }

  req = urllib.request.Request(
      url, data=json.dumps(payload).encode("utf-8"), headers=headers, method="POST"
  )

  try:
    with urllib.request.urlopen(req, timeout=15) as response:
      result = json.loads(response.read().decode("utf-8"))
      if isinstance(result, list) and len(result) > 0:
        return result[0].get(
            "generated_text", "Could not parse AI response text."
        )
      elif isinstance(result, dict) and "generated_text" in result:
        return result["generated_text"]
      return str(result)
  except Exception as e:
    return (
        f"**API Connection Error:** {e}\n\n*Note: Make sure your token is valid"
        " and has permissions for inference.*"
    )


if active_image is not None:
  st.success("Image received successfully!")
  st.image(active_image, caption="Your Item", use_container_width=True)

  if st.button("Analyze Photo for Recycling"):
    with st.spinner("Analyzing photo with Vision AI..."):
      advice = analyze_image_with_vision_ai(active_image, api_token)

      st.markdown("### 📋 AI Visual Analysis & Disposal Guidance")
      st.write(advice)
else:
  st.info(
      "Please take a photo using your camera or upload an image file above to"
      " get started."
  )