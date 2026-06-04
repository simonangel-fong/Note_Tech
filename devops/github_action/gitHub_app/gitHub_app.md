# GitHub App

[Back](../index.md)

- [GitHub App](#github-app)
  - [1. Create the App](#1-create-the-app)
  - [2. Generate credentials](#2-generate-credentials)
  - [3. Install the App on the config repo](#3-install-the-app-on-the-config-repo)
  - [4. Add secrets to the app repo](#4-add-secrets-to-the-app-repo)

---

## 1. Create the App

1. Go to github.com/settings/apps → New GitHub App (for a personal account; use the org settings page if the config repo is in an org).
2. Fill in:

- GitHub App name: gitops-config-bot (must be globally unique — add a suffix if taken)
- Homepage URL: anything, e.g. your app repo URL
- Webhook: uncheck Active (you don't need webhooks)
- Repository permissions — grant only:
  - Contents: Read and write (push the release branch)
  - Pull requests: Read and write (open the PR)
  - Metadata: Read-only (auto-enabled)
- Where can this GitHub App be installed? → Only on this account
- Click Create GitHub App.

---

## 2. Generate credentials

On the App's settings page:

- Note the App ID (top of page, numeric).
- Scroll to Private keys → Generate a private key → downloads a .pem file. Save it — you can't re-download it later.

---

## 3. Install the App on the config repo

On the App's page, left sidebar → Install App.
Pick your account → Only select repositories → choose Project_GitOps_Config_Repo → Install.

---

## 4. Add secrets to the app repo

In Project_GitOps_App_Repo → Settings → Secrets and variables → Actions → New repository secret:

CONFIG_BOT_APP_ID = the App ID from step 2
CONFIG_BOT_PRIVATE_KEY = full contents of the .pem file (including the -----BEGIN… / -----END… lines)
