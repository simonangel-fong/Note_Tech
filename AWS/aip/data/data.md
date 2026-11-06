# AIP: Data Fundamental

[Back](../index.md)

- [AIP: Data Fundamental](#aip-data-fundamental)
  - [Data Formating](#data-formating)
    - [Structured Data](#structured-data)
    - [Unstructured Text](#unstructured-text)
    - [Divider Strings - Chunking](#divider-strings---chunking)
    - [Formatting Data for Conversations](#formatting-data-for-conversations)

---

## Data Formating

### Structured Data

- `Bedrock API` Requests
  - generally expects request payloads **in JSON format**

- `SageMaker AI` Endpoints
  - **Models deployed via SageMaker** expects a certain input and output format
    - Typically this is **JSON** for LLMs
    - for classical ML, it might be **csv** or ssomething else
  - SageMaker will **not format** your input for you
    - Your app and endpoint is **responsible** for this

---

### Unstructured Text

- Raw text can lose its structure.
- techniques:
  - convert your unstructured **text to HTML** (or something) that can preserve that structure
    - Useful for OCR or PDF text, for example
  - `pandoc`
    - transform files format
  - `Amazon Textract`(image to text) and `Amazon Comprehend`(text to structure)
    - can help **extract structure** from raw text or images.
  - `AWS Glue`: data ingestion pipeline
  - `Bedrock Data Automation (BDA)`: Multimodal Processing

---

### Divider Strings - Chunking

- When chunking data into a `vector store`, divider strings can be used for better chunking.
  - e.g.,
    - A `Lambda` Preprocessor in your `Knowledge Base` can convert HTML tags to **divider strings on the fly**
    - `AWS Glue ETL` could do it as part of a pipeline too

---

### Formatting Data for Conversations

- Bedrock’s `Converse API` requires JSON output that includes:
  - Role
    - The “role” is who is “talking.”
  - Content

```json
{
  "messages": [
    {
      "role": "user",
      "content": [{ "text": "You're a chicken expert. Ready?" }]
    },
    {
      "role": "assistant",
      "content": [{ "text": "Absolutely—let’s talk chickens!" }]
    },
    {
      "role": "user",
      "content": [{ "text": "How fast can a chicken run?" }]
    }
  ]
}
```
