# Terraform - Fundamental: Project Structure

[Back](../index.md)

- [Terraform - Fundamental: Project Structure](#terraform---fundamental-project-structure)
  - [Prject Structure](#prject-structure)

---

## Prject Structure

- Separate **development** and **production** environments
  - development env: to test terraform changes, preventing production impact
- Create **multiple AWS accounts**
  - dev account: for development
  - prod account: for production
  - billing account: for billing
- Spliting out terraform in **multiple projects**, reducing the maintenance overhead