# Amazon Bedrock: Data Automation

[Back](../index.md)

- [Amazon Bedrock: Data Automation](#amazon-bedrock-data-automation)
  - [Data Automation](#data-automation)
    - [Document Processing](#document-processing)
    - [Image Processing](#image-processing)
    - [Video Processing](#video-processing)
    - [Audio Processing](#audio-processing)
  - [Custom Output - Blueprints](#custom-output---blueprints)

---

## Data Automation

- `Amazon Bedrock Data Automation (BDA)`
  - a managed capability of Amazon Bedrock that uses generative AI to **transform unstructured multimodal data**, such as documents, images, video, and audio, **into structured, usable formats**.

- Common use cases:
  - **Preparing data** for vector stores / KBs
  - Intelligent Document Processing (IDP)
  - Analyzing **video**
    - Scene summaries
    - ID explicit content
    - Extract text in video
    - Find ads

- Outputs:
  - **Standard Output**
    - Automatically **extracts default insights** (like document summaries, audio transcriptions, and video scene breakdowns) **without extra configuration**.
      - For documents this is probably JSON.
      - For audio it’s a transcript. Etc.
  - **Custom Output**:
    - define a **custom schema**(`Blueprint`) using natural language to pull specific data points out of proprietary or specialized documents.
- Bedrock API:
  - `InvokeDataAutomationAsync`

---

### Document Processing

- Accepts `PDF`, `TIFF`, `JPEG`, `PNG`, `DOCX`
- Outputs `JSON` or `JSON+` files
  - Files might include `CSV` for tables, overall **text extraction**, **markdown**
  - `HTML` and `CSV` structured **output** is also possible
    - Remember this came up earlier in the context of structuring **unstructured data** for better **chunking**
- You can select the granularity of responses
  - **Page**-level, **element**-level (default), **word**-level
  - **Bounding boxes** and generative **summaries** can be enabled per level

---

### Image Processing

- Accepts `JPEG`, `PNG`
- Generates:
  - Image **summary / caption**
  - IAB **Taxonomy** (Interactive Advertising Bureau)
  - **Logos** found
  - **Text** in images
  - **Content** moderation
- …all in **JSON**

---

### Video Processing

- Accepts `MP4`, `MOV`, `AVI`, `MKV`, `WEBM`
- Extracts:
  - Full video **summary**
  - Chapter **summaries**
    - This implies it can break the video down too!
  - IAB **Taxonomy**
  - **Transcript**
  - **Text** in video
  - **Logos** found
  - **Content** Moderation
- …all in JSON

---

### Audio Processing

- Accepts `AMR`, `FLAC`, `M4A`, `MP3`, `Ogg`, `WAV`
  - …and a variety of languages
- Extracts:
  - **Summary** of the file
  - Full **transcript**
  - **Speaker and Channel labeling** in transcript
  - Breaking up into **Topics**
  - **Content** moderation
- …all in JSON

---

## Custom Output - Blueprints

- Basic **fields**
  - Explicit or implicit (transformed)
- **Table** fields
- **Groups** (for organizing fields)
- **Custom** types
  - Example: “address” consisting of city, street, zip, etc.
- You can create Blueprints just **from a prompt** as well!
- Again there are many **pre-existing blueprints** you can use for common document types.

---

- usages
  - **Classification**
  - The document class and description can be used to **automatically classify documents** that match this blueprint
  - **Extraction**
    - Allows you **extract** specific fields, even if it’s from tabular data
  - **Normalization**
    - **Key Normalization** can deal with different names for the same data
    - **Value Normalization** can ensure data is extracted in a **consistent format** and in consistent **data types**
  - **Transformation**
    - You can **split and restructure** data fields
  - **Validation**
    - Ensure the **accuracy** of data. Is it within specified **ranges**? Have the expected size? Etc.
