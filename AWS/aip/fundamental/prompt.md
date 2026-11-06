# LLM Fundamental: Prompt Engineering

[Back](../index.md)

- [LLM Fundamental: Prompt Engineering](#llm-fundamental-prompt-engineering)
  - [Prompt engineering](#prompt-engineering)
  - [Retrieval-Augmented Generation (RAG)](#retrieval-augmented-generation-rag)
    - [Embeddings](#embeddings)
    - [Retrieval](#retrieval)
    - [Chunking Techniques](#chunking-techniques)
    - [RAG flow](#rag-flow)

---

## Prompt engineering

- `Prompt engineering`
  - the practice of designing, structuring, and refining **natural language inputs **(`prompts`) to guide large language models (LLMs) and generative AI systems toward accurate, relevant, and useful outputs.

- **Core Techniques**
  - `Zero-Shot Prompting`:
    - Asking the model to perform a task without giving any prior examples or demonstrations.
  - `Few-Shot Prompting`:
    - Providing a small number of input-output examples in the prompt to show the model the desired pattern or format.
  - `Chain-of-Thought (CoT) Prompting`:
    - Encouraging the model to break down a complex problem into step-by-step reasoning before giving a final answer.
  - `Role Assignment`:
    - Giving the AI a specific persona or expert identity (e.g., "You are an experienced Python developer") to shape its tone and depth.

---

## Retrieval-Augmented Generation (RAG)

- `Retrieval-Augmented Generation (RAG)`
  - an AI technique that connects a Large Language Model (LLM) to an external `knowledge base` so it can pull accurate, real-time, or domain-specific **facts** before generating an answer.

- `Retrieval`: find useful information
- `Augment`: add it to the AI's knowledge
- `generate`: create a better response

- **How RAG Works**
  - 1. **Indexing**: External documents (like PDFs, company files, or web pages) are **split into smaller pieces** called `chunks`.
  - 2. **Embedding**: These text chunks are converted into **numerical vectors** using an `embedding model` and saved in a `vector database`.
  - 3. **Retrieval**: When you ask a question, the system turns your question into a `vector` and **searches** the `vector database` for the most relevant matching text.
  - 4. **Augmentation**: The system **combines** your original question with the retrieved text snippets **into a new prompt**.
  - 5. **Generation**: The LLM reads the combined prompt and writes an answer grounded in that external information.

- Benefits
  - Reduces Hallucinations
  - No Retraining Needed
  - Access to Private Data
  - Cost-Effective

---

- Common Database
  - `Graph database` (i.e., Neo4j) for retrieving product recommendations or **relationships between items**
  - `Opensearch` or something for **traditional text search** (TF/IDF)
  - But almost every example you find of RAG uses a `Vector database`
    - Note `Elasticsearch` / `Opensearch` can function as a `vector DB`

---

- `OpenSearch`
  - a free, open-source search and analytics suite built on `Apache Lucene`.
  - Use Cases
    - Log Analytics & Observability
    - Full-Text & Enterprise Search
    - AI & Vector Search
    - Security Analytics

---

### Embeddings

- `vector`
  - an **ordered list of numbers** that **represents real-world data** (such as words, images, or user preferences) so that computers can process and analyze it.

- `embedding`
  - the process in machine learning that **turns complex data**, such as words, sentences, images, or audio, **into vector**.
  - also represent a **high-dimensional vector or list of numbers** or **multi-dimensional space**
    - items with **similar meanings or traits sit close together**
    - **unrelated** items sit **far apart**.

- `vector database`
  - a specialized database designed to store, manage, and query **high-dimensional** `vector embeddings`.
  - common:
    - Opensearch / Elasticsearch, SQL, Neptune, Redis, MongoDB, Cassandra

- `Embedding model`
  - Converts text into embeddings.
    - e.g., `Amazon Titan Text Embeddings`.

- `Semantic search`
  - Finds information by meaning, even when wording differs.

---

### Retrieval

- the proces of finding and preparing useful evidence before the LLM generates an answer.

- **Pre-Retrieval**
  - **Indexing**:
    - Makes content searchable—for example, embedding chunks and storing vectors, text references, and metadata in a search index.
    - Data granularity matters: `Chunking` techniques
    - **Data extraction**: Converts source content into usable text or structured data
    - **Granularity / chunking**: Decides the size of each searchable unit: a paragraph, section, or whole document.
  - **Query Rewriting**: Reformulates the user’s question to improve retrieval
- **Retrieval**: Finds candidate chunks using vector search, keyword search, or hybrid search
- **Post-Retrieval**: Reranks candidates, removes duplicates or irrelevant passages, and **selects context** for the LLM.

![rag_retrieval](./img/rag_retrieval.png)

---

### Chunking Techniques

- `chunk`
  - a **small, discrete segment** of a **larger piece of data**, such as a section of a document, a paragraph, or a few sentences, that has been **split off** to be converted into **a numerical vector and stored**.

- `Chunking`
  - the process of **breaking** large documents (like PDFs, manuals, or web pages) **into smaller, manageable segments or pieces** ("chunks") **before converting** them into numerical vectors and storing them in a vector database.

- **Common Chunking Strategies**
  - **Fixed-Size Chunking**:
    - Splits text into **rigid, uniform blocks** based on character or token counts (e.g., every 256 or 512 tokens).
  - **Content-Aware / Structure-Based Chunking**:
    - Respects **natural boundaries** like paragraphs, sentences, headings, or code blocks (using tools like NLTK or spaCy).
  - **Hierarchical Chunking**:
    - Creates nested "child" and "parent" chunks; the system retrieves a small, precise child chunk for matching, then **passes the broader parent chunk** to the LLM for full context.
  - **Chunk Overlap**:
    - Copies a small percentage (typically 10%–20%) of the **end of one chunk** to the **beginning of the next** so that ideas straddling a break are not lost.
  - **Semantic Chunking**:
    - Groups sentences or paragraphs together based on **topic shifts** and **semantic similarity** rather than arbitrary lengths.
    - each chunk contains **semantically independent information**
    - common tooling:
      - Embedding-based (LlamaIndex / Langchain)
      - Model-based (BERT)
      - LLM-based (Basically tell it to do semantic chunking); This is costly

---

### RAG flow

- **Prepare the knowledge**:
  - Documents → chunks → embedding model → vector database

- Inference with LLM:
  - Question → embedding model → **search** for similar vectors → **retrieve** matching TEXT → question + retrieved text → LLM → answer

---

