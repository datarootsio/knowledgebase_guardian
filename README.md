<div align="center">

<img src="https://github.com/datarootsio/knowledgebase_guardian/blob/main/images/kbg.png?raw=true">
</div>

<p align="center">
  <a href="https://dataroots.io"><img alt="Maintained by dataroots" src="https://dataroots.io/maintained-rnd.svg" /></a>
  <a href="https://img.shields.io"><img alt="Python versions" src="https://img.shields.io/badge/python-3.9-green" /> <img alt="Python versions" src="https://img.shields.io/badge/3.10-green"/> <img alt="Python versions" src="https://img.shields.io/badge/3.11-green"/>  </a>
  <a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg" /></a>
   <a href="http://mypy-lang.org/"><img alt="Mypy checked" src="https://img.shields.io/badge/mypy-checked-1f5082.svg" /></a>
  <img alt="Github License" src="https://img.shields.io/badge/License-MIT-green.svg" />
  <a href="https://pepy.tech/project/databooks"><img alt="Codecov" src="https://codecov.io/github/datarootsio/knowledgebase_guardian/main/graph/badge.svg" /></a>
  <a href="https://github.com/datarootsio/knowledgebase_guardian/actions"><img alt="test" src="https://github.com/datarootsio/knowledgebase_guardian/actions/workflows/tests.yaml/badge.svg" /></a>
</p>

Welcome to the KnowledgeBase Guardian, an LLM-powered solution to **keep your knowledge base consistent and free of contradictions**! How, you ask? Well, every time you want to add new information to your knowledge base, the Guardian will check that it does not conflict with information that is already contained in there. To grasp the general idea, feel free to have a look at this notebook: <a target="_blank" href="https://colab.research.google.com/drive/19iywHcBs12GwGBqhbKrgazWHx_q2YQW4#scrollTo=t6IqtnOgcM-n">
  <img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/>
</a>. <br>

Regardless of the purpose of your knowledge base, maintaining consistency is highly desirable. However, in a large and constantly evolving knowledge base, this can prove to be a challenging task. <br>

At Dataroots, we're developing an LLM-powered Q&A system, with our internal documents serving as the knowledge base. To us, maintaining consistency brings a range of benefits:
- **Enhanced user trust**: With conflicting information eliminated, users can rely on the knowledge base with confidence, leading to a positive user experience.
- **Improved answer quality**: By eliminating conflicting information, we can enhance the accuracy and reliability of the generated answers.
- **Simplified maintenance**: By automating conflict detection as much as possible, we reduce the manual effort required to maintain the knowledge base.

Off course, these benefits are not restricted to LLM-powered Q&A systems. If you're interested to keep your knowledge consistent as well, make sure to keep reading.

Keep in mind that this repo currently acts as a Proof of Concept and not as a full-fledged knowledge base management system.

# 💡 How it works

Our use case can be visualized as follows:

![workflow.png](images/workflow.png)

- We have an initial vector store, which contains embeddings of all documents in our knowledge base. To keep the example simple, we assume it is initially free of contradictions.
- We want to add new documents to this vector store, but are unsure if these documents are consistent with the information in the vector store.
- Before adding a document, we first retrieve the most semantically similar documents in the vector store. We then use an LLM to compare the documents and search for contradictions:
    * If no contradiction is detected, the document is added to the vector store.
    * If a contradiction is detected, the document is not added and we keep a log of the failed attempt.

# Prerequisites

- OS: Linux or MacOS
- Python: 3.9 or higher
- OpenAI account <br> OR <br> Azure OpenAI with deployed embedding and LLM

# ⚙️ Setup

1. Open a terminal and clone this repository by running
```bash
    git clone https://github.com/datarootsio/knowledgebase_guardian.git
```
2. Go to the cloned folder and create a virtual environment. Choose your favorite one or use venv:
```bash
  python -m venv contradiction_detection
  source contradiction_detection/bin/activate
```
3. Install the dependencies:
```bash
  python -m pip install -e .
```

# ⚡️ Quickstart

We provide a small demo example to get started right away. If you prefer to play around with your own data, you can jump ahead to the next section. <br>

In [data/vectorstore](/data/vectorstore) you'll find an index and vector store file called `belgium`. It was created from three articles about Belgian cities, which we scraped from Wikipedia and which you can find in [data/raw](/data/raw). In our example, we'll try to add three new documents to our vector store. You can find these in [data/extension](/data/extension). <br>

To follow along with the example, follow the setup section above and **execute the following steps**:


1. Make sure you have an OpenAI account. Look up your OpenAI API key and write it down in [.env](.env)
2. In your terminal, run
```bash
  python scripts/extend_vectorstore.py
```

This will result in the following three **outputs**:

1. A new index and vector store file called `belgium_extended`, located in the [data/vectorstore](/data/vectorstore/) folder.
2. A `contradictions.log` file, indicating for which new files a contradiction was detected. If all went well, you should see that the document `Leuven_contradictions` was not added to the vector store and the output should look more or less like this:
![Detected contradictions](images/contradictions.png)
3. A `execution.log` file providing information about the run. Here you'll also find logs for new documents that were added succesfully. Assuming all went well, you'll see that the documents `Leuven_aligned` and `Leuven_new` were succesfully added to the vector store. The first document contains only information that is already present in the vector store, while the second introduces new information that is not conflicting with any of the information contained in the vector store. The output should look similar to this:
![Aligned information](images/aligned.png)
and this:
![New information](images/new.png)

# ⚒️ Setting up KnowledgeBase Guardian with your own data

Make sure to first execute the steps of the setup section above.

## Choose OpenAI or Azure OpenAI

1. For AzureOpenAI, complete the [.env.cloud](.env.cloud) file. <br>
For OpenAI, complete the [.env](.env) file.
2. Set the `azure_openai` variable in [config.yml](/config.yml) to true if you use AzureOpenAI, else set it to false.

## Initializing your vector store

### A) You already have a FAISS vector store

Place the index file and the actual vector store file in the [data/vectorstore](/data/vectorstore/) folder. Make sure that:
- Both files have the same name
- The index file has extension `.index`
- The vector store file has extension `.pkl`

Now head over to [config.yml](/config.yml) and change the `vectorstore_name` parameter to the name of your vector store.

### B) You don't have a FAISS vector store

1. Place all your `.txt` data in the [data/raw](/data/raw/) folder.
2. Head over to [config.yml](/config.yml) and change the `vectorstore_name` parameter to the desired name for your vector store.
3. Optional: change the `chunk_size` and `chunk_overlap` parameters
4. Create a vector store and index file with the chosen name in the [data/vectorstore](/data/vectorstore/) folder by running
```bash
    python scripts/create_vectorstore.py
```

## Extending your vector store and detecting contradictions

Now we want to add new documents to the vector store, but only if they are not contradicting with the information that is already contained in the vector store.

1. Place the `.txt` files to be added in the [data/extension](/data/extension/) folder.
2. Optional: change the `chunk_size`, `chunk_overlap`, `nb_retrieval_docs`, `system_message` and `user_message` parameters in the [config.yml](/config.yml) file.
3. Start the contradiction detection and vector store extension with the following command. To bypass the contradiction detection mechanism, add `--disable-contradiction-detection`.
```bash
    python scripts/extend_vectorstore.py
```

The output is threefold:
1. A new index and vector store file in the [data/vectorstore](/data/vectorstore/) folder, recognizable by the presence of `_extended` in their name.
2. A `contradictions.log` file, indicating for which new files a contradiction was detected. For debugging purposes, it also displays the output of the LLM and the content of the most similar documents that were retrieved.
3. A `execution.log` file indicating information about the run. Here you'll also find logs for new documents that were added succesfully.

# 🧐 Limitations

1. The performance of this technique is highly dependent on the prompt. You will likely need to fine-tune the prompt (i.e., the `system_message` and `user_message` in [config.yml](/config.yml)) to your use-case

2. There is no consistent handling of all chunks in a document. This means that if your document is split into multiple chunks and some of them contain contradictions while others don't, some chunks will be added to the vector store and others will not. Depending on your use case, you might want to change this behaviour.

3. To keep the example as small as possible, we chose to support only

    - one vector store type (FAISS)
    - one file extension (`.txt`)

    Extending this code to other vector stores and file extensions is possible by leveraging Langchain or LlamaIndex.

# License

This project is licensed under the terms of the MIT license.
