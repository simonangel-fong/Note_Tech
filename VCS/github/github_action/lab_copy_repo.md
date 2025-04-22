# GitHub Action - Copy A Directory to A Remote Repository

[Back](../index.md)

- [GitHub Action - Copy A Directory to A Remote Repository](#github-action---copy-a-directory-to-a-remote-repository)

---

```yaml
# The name of the workflow. It will appear in the "Actions" tab
name: Copy directory to target repo
# The name for workflow runs generated from the workflow.
run-name: ${{ github.actor }} copy dir to target repo

# the trigger for this workflow
on:
  push:
    paths:
      # Triggered only by a custom directory
      - "DjangoBlog/**"

# variables that are available to the steps of all jobs in the workflow.
# define values here
env:
  REMOTE_URL: https://github.com/simonangel-fong/Target.git # custom remote url
  REMOTE_REPO: Target
  SOURCE_REPO: ${{ github.event.repository.name }}
  COMMIT_MESSAGE: ${{ github.event.head_commit.message }}
  TEMP_DIR: temp_dir
  TARGET_DIR: DjangoBlog # custom the target dir

# Groups together all the jobs that run in this workflow.
jobs:
  # Defines a job name.
  Copy-directory-to-target:
    # set a name for the job
    name: Copy directory to a target repository
    # define the type of machine to run the job on.
    runs-on: ubuntu-latest
    # a sequence of tasks in a job
    steps:
      # Task: Collect event information.
      - name: Collect event information.
        run: |
          echo "================================================="
          echo "🚀 Triggered event:     ${{ github.event_name }}" 
          echo "💻 Server OS:           ${{ runner.os }}"
          echo "📂 GitHub repository:   ${{ github.repository }}"
          echo "🔍 Repository name:     ${{ github.event.repository.name }}"
          echo "🌱 Branch:              ${{ github.ref }}"
          echo "📦 Workspace:           ${{ github.workspace }}"
          echo "✅ Job status:          ${{ job.status }}"
          echo "================================================="

      # Task: checks out a copy of repository.
      - name: Check out repository
        uses: actions/checkout@v4

      # Task: Clone the target repo
      - name: Clone the target repo
        run: |
          mkdir $TEMP_DIR
          git clone $REMOTE_URL $TEMP_DIR
        working-directory: /home/runner/work/${{env.SOURCE_REPO}}/

      # Task: Copy the directory to the target repository
      - name: Copy the directory to the target repository
        run: |
          cp -r ./$SOURCE_REPO/$TARGET_DIR ./$TEMP_DIR/$TARGET_DIR
        working-directory: /home/runner/work/${{env.SOURCE_REPO}}/

      # Task: Configure Git user for committing changes
      - name: Configure Git user
        run: |
          git config --global user.email "${{secrets.GIT_USER_EMAIL}}"
          git config --global user.name "${{secrets.GIT_USER_NAME}}"
        working-directory: /home/runner/work/${{env.SOURCE_REPO}}/${{env.TEMP_DIR}}/

      # Task: Commit the changes
      - name: Commit changes
        run: |
          git add -A
          git commit -m "$COMMIT_MESSAGE"
          git log --oneline -4
        working-directory: /home/runner/work/${{env.SOURCE_REPO}}/${{env.TEMP_DIR}}/

      # Task: Push the changes
      - name: Push changes
        run: |
          git remote set-url origin $REMOTE_URL
          git push https://${{env.REPO_TOKEN}}@github.com/${{secrets.GIT_USER_NAME}}/${{env.REMOTE_REPO}}.git
        working-directory: /home/runner/work/${{env.SOURCE_REPO}}/${{env.TEMP_DIR}}/
        env:
          REPO_TOKEN: ${{ secrets.REPO_TOKEN }}

      # Task: Remove temp dir
      - name: Remove temp dir
        run: |
          rm -rf ${{env.TEMP_DIR}}/
          pwd
          ls
        working-directory: /home/runner/work/${{env.SOURCE_REPO}}/
```

---

[TOP](#github-action---copy-a-directory-to-a-remote-repository)
