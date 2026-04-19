# DevOps - CI/CD

[Back](../index.md)

- [DevOps - CI/CD](#devops---cicd)
  - [CI/CD](#cicd)

---

## CI/CD

- `Continuous integration (CI) and continuous delivery (CD)`
  - a DevOps methodology **automating** the **building**, **testing**, and **deployment** of software to speed up development cycles and increase reliability.

---

- `Continuous integration (CI)`
  - a **software development practice** where developers **frequently—often** multiple times a **day—merge code** changes into **a central, shared repository**.

- Key features:
  - **Frequent Merging**:
    - Developers commit code to the main branch often;preventing "integration hell" where massive conflicts occur at the end of a project.
  - **Automated Testing & Builds**:
    - Upon **every commit**, automated systems automatically **build the application** and **run unit/integration tests** to ensure the new code doesn't break existing **functionality**.
  - **shifts testing left**:
    - bugs are caught during development

- Actions:
  - build/package application
  - unit/functional test

---

- `Continuous Delivery (CD)`
  - a software engineering practice where **code changes** are **automatically built, tested**, and **prepared for release** to a production environment.

- key features:
  - **Deployment-Ready State**:
    - The core principle is that the application is always ready to be deployed to production at any time with a "click of a button".
  - **Pipeline Stages**
    - automated **deployment to staging**, followed by **UI testing**, **load testing**, or `user acceptance testing (UAT)`.

- vs ci
  - CI focuses on testing **code changes**
  - CD packaging and deployment to testing and staging

- Actions:
  - deployment to testing/staging
  - UI testing
  - load testing
  - UAT

---

- `Continuous deployment (CD)`
  - the final stage of a CI/CD pipeline where code changes, after passing automated tests, are **automatically released** into the **production environment** without human intervention

- vs Delivery:
  - `continuous delivery` requires **human approval** to push to production
  - `continuous deployment`: fully automatic.
