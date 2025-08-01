# RPA - Mod07

[Back](../rpa.md)

- [RPA - Mod07](#rpa---mod07)
  - [OCR](#ocr)
    - [Windows OCR Engine](#windows-ocr-engine)
    - [Tesseract OCR Engine](#tesseract-ocr-engine)
  - [How OCR Technology Works](#how-ocr-technology-works)
  - [Multi-Language OCR](#multi-language-ocr)
  - [OCR Challenges](#ocr-challenges)
    - [Overcoming the challenges](#overcoming-the-challenges)
  - [Exception Handling](#exception-handling)
    - [Error Types](#error-types)
  - [“On Block Error” action](#on-block-error-action)
    - [Throw Error or Continue Flow Run](#throw-error-or-continue-flow-run)
    - [Action Level Exception Handling](#action-level-exception-handling)
    - [Graceful Recovery](#graceful-recovery)

---

## OCR

- `OCR(or Optical Character Recognition)`

  - a technology that **transforms scanned images or printed text** into **editable and searchable data**.

  - allows computers to **interpret and extract text from images** or documents, making it easier for users to search for specific words or phrases within a document.

- OCR has many **uses**, including:
  - Digitizing **physical** documents
  - Automating **data entry processes**
  - Improving accessibility for visually **impaired individuals**

---

- `Power Automate` enables users to **read, extract, and manage** data within files through optical character recognition (`OCR`).
- The **default OCR engine** in Power Automate is the **Windows OCR engine**.
- Apart from the Windows OCR engine, Power Automate supports the **Tesseract engine (Open Source)**.

---

### Windows OCR Engine

- `Optical Character Recognition (OCR)`
  - part of the **Universal Windows Platform (UWP)**, which means that it can be used in all apps targeting Windows 10 and up.
- With OCR you can e**xtract text and text layout information from images**.
- It’s designed to handle various **types of images**, from scanned documents to photos.
- The Windows 10 update enabled OCR for four new languages, bringing the total number of **supported languages** to 25.

---

### Tesseract OCR Engine

- `Tesseract` was originally developed at Hewlett-Packard Laboratories Bristol UK and at Hewlett-Packard Co, Greeley Colorado USA between 1985 and 1994, with some more changes made in 1996 to port to Windows, and some C++izing in 1998.
- In 2005 Tesseract was open sourced by **HP**.
- From 2006 until November 2018, it was developed by **Google**.
- Tesseract can extract text in **five languages** without further configuration: English, German, Spanish, French, and Italian.

---

## How OCR Technology Works

- OCR technology works by **analyzing the patterns of pixels** in an image of a document and **recognizing them as characters**.
- It then **converts** the recognized characters into **editable text** that can be stored and manipulated digitally.
- OCR software relies on a **database of character patterns** to recognize the characters in the image accurately.
- Therefore, it is essential to use the **correct language settings** when using OCR software to ensure that the database used is appropriate for the document’s language.

---

## Multi-Language OCR

- `OCR` technology can be used to **extract data from documents** in **many languages**. Here are some **use cases** of using OCR technology for extracting data from documents in other languages
- OCR technology can be used to extract data from documents **written in different languages** across various industries.
- This technology can help to increase efficiency, accuracy, and productivity in data processing, management, and analysis.

---

- **Business Contracts**
  - OCR technology can be used to **extract data from business contracts written in languages** other than the user’s native **language**.
  - This can include information such as the names of the parties involved, the terms of the contract, and any specific clauses or conditions
- **Legal documents**

  - Lawyers and legal professionals can use OCR technology to **extract data from legal documents written** in different languages.
  - This can include contracts, court documents, and other **legal documents** that may be written in a language other than the user’s **native language**.

- **Financial documents**
  - OCR technology can be used to extract data from **financial documents** such as invoices, receipts, and bank statements written in different languages.
  - This can include information such as the amounts, dates, and transaction details.
- **Medical records**
  - Healthcare professionals can use OCR technology to extract data from **medical records** written in different languages.
  - This can include patient names, medical history, test results, and other relevant medical information.
- **Government documents**
  - OCR technology can be used to extract data from **government documents** such as passports, visas, and identity cards written in different languages.
  - This can include information such as personal details, expiration dates, and other relevant information.

---

## OCR Challenges

- The **accuracy** of OCR technology **depends on several factors** such as the **quality** of the input document, **font type**, and language **complexity**.
- One of the main reasons why OCR accuracy varies depending on the language is due to the **complexity of the scripts and character sets.**
- Generally, advanced OCR software has an accuracy rate of 99%, provided the input is a high-quality, **black-and-white image** with **large fonts**.
- The accuracy rate is often compromised when OCR deals with **handwritten content**, intricate layouts, or **skewed texts**.
- OCR software also generates incorrect readings from minuscule texts and **low-quality images**.

---

### Overcoming the challenges

- **Preprocessing**

  - Before running the document through OCR software, preprocess it **by applying filters** to **enhance the contrast and clarity** of the text.
  - This will improve the software’s **accuracy** in recognizing the characters.
  - While this provides improved accuracy, it is not efficient, and filters not backed by AI are limited.

- Some of the basic Preprocessing techniques are:
  - **Binarization**
    - Converting a coloured image into an image which consists of only **black and white pixels**
  - **Skew Correction**
    - While scanning a document, it might be **slightly skewed** (image **aligned at a certain angle** with horizontal). Detecting & correcting the skew is crucial.
  - **Noise Removal**
    - Smoothen the image by **removing small dots/patches** which have higher intensity than the rest of the image
  - **Thinning and Skeletonization (for handwritten text)**
    - Since different writers have a different styles of writing and hence different stroke width. We have to perform Thinning and Skeletonization to **make the strokes uniform**.
  - **Human Validation**
    - This method is the “old school” method.
    - Data is validated by having a human reviewer check it for accuracy.
    - This is particularly important when dealing with documents in languages that you are not familiar with.
    - The obvious drawback here is scalability and the time it takes.
  - **Hire Professional Translation and Localization Services**
    - If you need to process documents in **multiple languages regularly**, companies often resort to hiring professional translation and localization services to ensure that the OCR software can accurately recognize and extract data from the documents.
    - The drawbacks are scaling and efficiency.
  - **AI-Driven OCR**
    - OCR technology has made document processing and management much more efficient and accurate.
    - When dealing with documents in non-native languages, however, there can still be challenges in recognizing the characters, grammar, and cultural context of the language.
    - The question becomes, how can companies do multilingual transactions globally, when their ability to extract data is limited by their inability to understand documents in foreign languages?

---

## Exception Handling

- `Exceptional handling`
  - essential for **adapting to changes**, ensuring **data integrity**, and efficient automation.
  - The ability to **handle and recover from unexpected circumstances** is a critical factor in automating business processes.
  - The **risk of errors** is present in any automated task - this risk may come from multiple factors, such as changes in the applications used, changes in business processes, unavailability of hardware, software, files, and services.

---

- It is important to include error-handling in every Power Automate flow.
- W**hen a flow fails**, the owner should **be notified** that the flow failed. The message should say **why the flow failed** and **identify the flow** run.
- When a flow fails the Flow should take an **alternative action** which may include sending a **message**, writing to a **log**, **executing another** flow or sub-flow.

---

### Error Types

- **Design-time errors**

  - associated with the **configuration of the deployed actions**.
  - appear during **development** and prevent desktop flows from running.
  - For example, an empty mandatory field or an **undefined variable** can cause this type of error.

- **Run-time errors**, also known as `exceptions`,
  - **occur during execution** and make desktop **flows fail**.
  - For example, an **invalid file path** can cause this kind of error.
  - Use any of the available **error-handling options to prevent** your desktop flows from failing.

---

## “On Block Error” action

- Some scenarios may require you to **implement the same error-handling** functionality for several actions in your desktop flows.
- Instead of configuring each action separately, you can deploy the **On block error action** and **configure error-handling** for all the actions inside the block.
- This action works similar to a ‘Try-Catch’ block that we find in other programming paradigms.
- We can **add an exception handler** around a group of actions.
- Should any action fail within that group, our On block error exception handler will be invoked.

---

- Actions in between the **On block error** and **End actions** are affected by the **block’s exception handling rules**
- The order in which exception handling is applied is from the bottom up; this means that, in case an action fails, its individual exception handling rules will take effect immediately.
  - If that is not enough to resume the flow, any block-level exception handling will take effect.
- Therefore, **any action-level exception handling rules** run before the respective **block-level rules**.

---

- As part of our **“On block error”** action we can indicate what actions we would like to take when an error does occur.
- One option we can leverage is to call a `subflow`.
- We can design our subflow to be **reusable** so that any **On block error action** can use it.
  - Inside this `subflow`, we can include the ability to write to a **log file**, a database, API or other source.
- Consider a flow that interacts with a web portal.
  - If at any point during this task the portal or browser becomes unresponsive, the preferred action is to close the browser, launch it again, and restart the entire web portal interaction from the beginning.
  - However, a web portal interaction can span tens, or even hundreds of actions; so assigning the same exception handling rules to each action individually is impractical.
- The On block error action allows you to **apply one set of exception handling rules** to an **entire block of actions**:

---

### Throw Error or Continue Flow Run

- `“Throw Error”` will **terminate** in the event of an error. This is the **default behavior** even without using an Error Handler.
- `“Continue Flow Run”` allows us to **perform some action** when an error event occurs.

---

### Action Level Exception Handling

- The **Exception Handling** works the same as the “On Block Error” Action but **only applies to the Action** it has been configured for.
- By default, exception handling takes effect when any exception occurs while this action is running - however, you can configure it so that exception handling occurs **only on a specific type of exception**.
- Each action has specific exception types that it may produce

---

### Graceful Recovery

- Bot Developers should **plan for failure** and **build graceful recovery** into RPA bots.
- When a robot throws a business exception while processing a transaction in an application, for instance, it should be programmed to **clean up temporary files**, **undo partially completed records**, and **return to the starting point** so the robot can **begin the next transaction** from the correct screen.
- Or if a robot throws an application error while trying to navigate to a URL, it should **close** the web application, then **restart** it and navigate to the URL.

---

- A vital component to exception handling is **logging**.
- An `exception log` should contain **data relevant** to the transaction, including the **time** the error occurred, the **error message** string, and any unique **identifiers**.
- These logs can be used to **help debug** the automation and fine-tune business requirements. They also **help create** analytics that assesses the efficiency of automation.
- When an RPA bot is sufficiently programmed to handle exceptions, recover gracefully and log the related data; the business is well on the way to **maximizing a return on RPA investment.**
