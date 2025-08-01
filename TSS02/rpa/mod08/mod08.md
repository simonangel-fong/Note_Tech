# RPA - Mod08

[Back](../rpa.md)

- [RPA - Mod08](#rpa---mod08)
  - [Security and Governance](#security-and-governance)
    - [Security:](#security)
    - [Data privacy:](#data-privacy)
    - [Governance:](#governance)
    - [Compliance](#compliance)
    - [Auditing](#auditing)
  - [Access Control](#access-control)
  - [Data Privacy](#data-privacy-1)
    - [Apply data masking techniques](#apply-data-masking-techniques)
        - [Substitution](#substitution)
      - [Shuffling](#shuffling)
      - [Data Encryption](#data-encryption)
      - [Pseudonymization](#pseudonymization)
  - [Governance](#governance-1)
  - [Compliance](#compliance-1)
    - [Regulatory Compliance:](#regulatory-compliance)
    - [5 Ways RPA Enables Compliance](#5-ways-rpa-enables-compliance)
    - [Compilance Examples](#compilance-examples)
  - [Auditing](#auditing-1)

---

## Security and Governance

- By implementing effective RPA **security and governance measures**, organizations can **ensure** that their RPA systems are **secure, efficient, and compliant with relevant regulations**.
- Additionally, proper RPA security and governance can **help organizations to mitigate risks, improve performance, and maintain the trust of customers, employees, and stakeholders.**
- Security and Governance are critical aspects of implementing and managing RPA solutions within an organization.

---

### Security:

- RPA systems handle **sensitive data** and **interact with critical systems and applications**, so it is important to ensure the security of these systems.
- RPA security measures include **access control**, **encryption**, and **secure communication protocols**. Additionally, RPA systems should be **regularly monitored** and **audited to detect and prevent security breaches**.

---

### Data privacy:

- RPA systems may **handle personal data**, so it is important to ensure that this data is handled in accordance with relevant data protection laws and regulations.
- This may involve implementing **data privacy controls**, such as data **masking**, and performing **regular data privacy audits**.

---

### Governance:

- RPA governance is about **ensuring the proper management and control of RPA systems**.
- This includes **establishing clear policies and procedures** for RPA development, deployment, and management, as well as **establishing an RPA governance framework** that includes **roles and responsibilities**, decision-making processes, and performance metrics.

---

### Compliance

- RPA systems may be subject to various **regulatory requirements**, such as data protection laws and financial industry regulations.
- It is important to ensure that RPA **systems are designed and operated in compliance with these requirements**.

---

### Auditing

- **Regular auditing** is an important part of RPA governance.
- This may include **regular security and privacy audits**, as well as **audits of the RPA system** itself to ensure that it is operating as expected.

---

## Access Control

- **Users** managing bots, bots acting as users
- Though RPA replaces humans with bots, people still need to work with bots to schedule, run, view and edit their processes.
- To successfully and securely do this, **security admins** must to be able to **specify who does what** -- `access control` for humans and bots alike is critical.
- Be concerned about **who can do what** -- or in the case of RPA, **what can do what** -- and also consider more **granular concerns**, such as **what time** of day or days of the week an individual or bot has access.

---

- To applications, a bot is just **another user that needs to authenticate** -- i.e., log in -- to use most systems.
- Be sure to understand **where those credentials are stored** when not in use by the bot and how they are protected.
- Is the credential vault **encrypted**? **Who holds** the key?
- When the bot is running, know **where the credentials are stored**.
  - If, for example, credentials are being stored in the bot computer's memory in clear text, they could be compromised by a third party.

---

- The bot, which effectively is an application program itself, is part of a business process and, thus an **intellectual property asset** of the enterprise using it.
- It is important that the bot code be **protected from unauthorized copying**.
- Because bots mimic users, they interact with apps using keyboard and mouse peripheral inputs.
- An unauthorized person having **physical access** to the computer running a bot might be able to change data or otherwise change the bot processing by intervening through the peripherals.

---

## Data Privacy

- **Encrypt sensitive data**

  - One of the most basic and essential ways to secure data in the RPA development phase is to encrypt sensitive data.

- `Encryption` is the **process of transforming data into an unreadable format** that can **only be decoded with a key or a password**.
  - can **prevent hackers, malicious insiders**, or **accidental users** from **accessing or tampering** with **confidential** information, such as personal data, financial records, or trade secrets.
- You can encrypt data **at rest**, which means storing it in an encrypted format on a disk or a cloud service, or data **in transit**, which means transferring it in an encrypted format over a network or a communication channel.

---

- You can use various **encryption methods and tools**, such as **symmetric** or **asymmetric encryption**, hashing, digital signatures, or certificates, depending on your data type and security requirements.
- Power Automate provides the ability to **encrypt and decrypt files** using `AES encryption`.
- All customer data stored in Power Platform is **encrypted at rest** using Microsoft-managed keys or Customer provided keys.

---

### Apply data masking techniques

- `Data masking`
  - the process of **hiding or replacing sensitive data** with fictitious or **anonymized data**, while **preserving the original format** and functionality.
- Data masking can **help you protect the privacy and confidentiality of data**, especially when you need to share it with **external parties**, such as vendors, consultants, or auditors, or when you need to use it for **testing**, **debugging**, or **training** purposes.
- You can use various **data masking techniques** and tools, such as **substitution**, **shuffling**, **encryption**, or **pseudonymization**, depending on your data type and security objectives.

---

##### Substitution

- `Substitutes` **original values** in a data set with **randomized data** using various data shuffling and manipulation techniques.
- The obfuscated data **maintains the unique characteristics** of the original data so that it yields the same results as the original data set.

---

#### Shuffling

- A technique similar to substitution.
- It is also used to **substitute original data with other data that looks authentic**.
  - The difference is that the **entities** in the same column are **randomly shuffled**.
- For instance, organizations can use this technique to shuffle employee name columns of multiple employee records randomly. This technique can be **prone to reverse engineering** if anyone gets their hands on the shuffling algorithm.

---

#### Data Encryption

- A technique that **allows access to data only with the decryption key**.
- It is the most **complex data masking algorithm** and the most secure one. In addition to the complexity, it requires proper **encryption key management** to ensure security.

---

#### Pseudonymization

- The processing of **personal data** in such a way that the data can no longer be attributed to a specific data subject without the use of additional information.”
- To pseudonymise a data set, the “additional information” must be “kept separately and subject to technical and organisational measures to ensure non-attribution to an identified or identifiable person.”
- `Pseudonymization` **translates a sensitive data field into a pseudorandom string** (hence the name). The resulting string is always the **same** for the same input, so that **analytical correlations** are still possible. This process is alternatively called **“data tokenization**.”

---

## Governance

- As organizations adopt RPA at a rapid pace, there is a growing need for `governance` to **ensure the security, reliability, and overall effectiveness** of these automations.
- RPA governance can help organizations **establish a framework for managing the development, deployment, and ongoing maintenance** of RPA solutions.
- Def - `Governance` is the **process of making and enforcing decisions** within an organization or society. It encompasses **decision-making, rule-setting, and enforcement mechanisms** to guide the functioning of an organization or society.

---

- The first step in implementing RPA governance is to **establish a clear strategy** and **set of objectives**.
- This should include a **clear understanding of what RPA** is, what it **can** and **can**'t do, and what the organization hopes to **achieve** through its use.
- This can help to ensure that the **right resources are allocated**, that the **right processes** are in place, and that the right people are involved in the implementation of RPA.

---

- The next step is to **develop a set of policies and procedures** for RPA development, deployment, and maintenance.
- This should include **guidelines for creating, testing, and deploying** RPA solutions, as well as **policies for monitoring and managing them** once they are in place.
- This will help to **ensure** that the automations are **reliable and secure**, and that the organization is able to quickly identify and resolve any issues that arise.

---

- It is important to **engage key stakeholders**, including business and IT leaders, in the development and implementation of these policies and procedures.
- Finally, it is important to **continuously monitor and evaluate the performance** of RPA solutions, and to make changes as needed to ensure their ongoing effectiveness.
- This may involve **adjusting policies and procedures**, making changes to the automations themselves, or even retiring automations that are no longer providing the desired benefits.

---

## Compliance

- `RPA compliance` refers to **ensuring** that Robotic Process Automation (RPA) **implementations adhere to relevant regulations**, industry **standards**, and organizational **policies**.
- Compliance considerations are crucial for organizations leveraging RPA technologies, particularly when dealing with **sensitive data**, regulated industries, and complex business processes.

---

### Regulatory Compliance:

- Organizations must ensure that RPA implementations **comply with relevant laws and regulations** governing data privacy, security, and other areas.
  - Through RPA compliance organizations can **mitigate regulatory risks** and **build trust** in their RPA initiatives.
- Effective compliance management helps organizations **leverage the benefits** of RPA while **maintaining regulatory compliance** and safeguarding sensitive data and business processes.
- For example, regulations such as:
  - `General Data Protection Regulation (GDPR)`, `Health Insurance Portability and Accountability Act (HIPAA)`, `Sarbanes-Oxley Act (SOX)`, `Payment Card Industry Data Security Standard (PCI DSS)`, and others may apply depending on the nature of the data and processes involved.

---

### 5 Ways RPA Enables Compliance

- Eliminate **unauthorized access to privileged data**
  - RPA bots can replicate data manipulation processes such as entry, transfer, and storage, without human intervention.
- **Verify process logs** against regulations and policies
  - Bots can **verify process logs against regulation and policy documents** to detect missing steps and non-compliant processes
- **Automate low value regulatory reporting tasks**
  - RPA bots can extract data from business datasets, verify **that the data matches original sources,** generate compliance reports and send them for verification
- **Keep up to date with regulatory requirements**
  - Rely on RPA bots to **scrape policy makers’ websites**, extract news about regulations, laws, or rules, and update regulation data in the organization’s internal regulation databases
- **Minimize errors in onboarding and due diligence**
  - Leverage bots to complete due diligence processes to **reduce human errors**, increase speed of **onboarding completion**, and generate a comprehensive audit trail for later compliance analysis.

---

### Compilance Examples

- Retail banking, RPA can be used to **automate compliance-related tasks** such as Know Your Customer (KYC) checks, **Anti-Money Laundering (AML) checks**, and **regulatory reporting**.

---

## Auditing

- One of the main pain points in auditing is **data collection**. This can be **time-consuming** and **error-prone**, mainly if data is **spread across multiple systems**.
- If your information is wrong, your whole audit could be thrown off.
- RPA can **automate data collection** from various sources and consolidate it into a single system for further analysis.
- This not only saves time but also reduces the chances of errors.

---

- RPA in audit can **automate repetitive and manual tasks** in the audit process, freeing up time for auditors to focus on higher-value activities.
- For example, RPA can **generate standard reports**, upda**te record**s, prepare documents, send emails, and more.
- This not only makes auditors' jobs easier but also **reduces the risk of human error.**

---

- RPA in audits can help **improve the quality of audits** by **providing a consistent and repeatable process**. By automating critical tasks, auditors can be sure that steps are not missed, and that data is collected accurately.
- RPA in audits can provide **real-time feedback** on the progress of an audit, which can help identify potential problems early on.
- Auditors often need to collect information from clients in order to complete an audit. RPA in audit can automate this process by sending emails, setting up meetings, and sending reminders. This can help to improve client service and make the audit process smoother for all involved.
- RPA can also help **improve client service** by providing faster turnaround times on reports and other deliverables.

---

- RPA can **help detect fraud by identifying patterns in data** that may indicate fraudulent activity.
- For example, robotic process automation in audit and compliance can **compare data across multiple systems** to look for **discrepancies**. This can help to flag the instances of fraud so that they can be investigated further.
