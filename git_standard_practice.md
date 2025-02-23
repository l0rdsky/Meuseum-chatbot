# Git Standard Practice

### 1. Create Separate Branch for Each Feature
- Create a separate branch for each feature you're working on.
- Name the branch starting with the first letter of your first name and the first two letters of your last name, followed by the feature name.  
  - Example: If your name is Akash Pawar, the branch name would be:  
    ```
    apa-backendIntegration
    ```

### 2. Create New Branch from Main for Every Feature
- Always create a new branch for each feature, using the `main` branch as the base.  
- **Command to create and switch to a new branch:**  
    ```bash
    git checkout main           # Switch to main branch
    git pull origin main        # Pull the latest changes from main
    git checkout -b <branch_name>  # Create and switch to your new branch
    ```
    Example:  
    ```bash
    git checkout -b apa-newFeature
    ```

### 3. Do Not Make Changes Directly to Main
- Never make changes directly to the `main` branch.
- Always create a new branch and push your changes there.
- Once your feature is complete, **create a Pull Request** to merge your changes into the main branch.
- **Command to push changes to your branch:**  
    ```bash
    git add .                   # Stage your changes
    git commit -m "Your commit message"  # Commit your changes
    git push origin <your_branch_name>   # Push changes to your branch
    ```
    Example:  
    ```bash
    git push origin apa-newFeature
    ```

### 4. Push Only Relevant Files
- Ensure that only relevant files related to the feature are committed and pushed.
- Any unrelated files or changes will **not be merged**.

### 5. Keep Your Branch Updated with Latest Main
- Always pull the latest changes from the `main` branch and merge them into your current working branch whenever a new feature is merged into `main`.
- This prevents conflicts and keeps your branch up-to-date.
- **Command to pull latest main and merge into your current branch:**  
    ```bash
    git pull origin main    # Do this while on your current feature branch
    ```
    Example:  
    ```bash
    git pull origin main
    ```

### 6. Create Pull Requests for Merging
- After completing a feature, **create a Pull Request (PR)** to merge changes into `main`.
- Ensure the PR description is clear and provides sufficient context about the changes.
- Wait for at least one code review approval before merging.

### 7. Delete Merged Branches
- Once your PR is merged, **delete the feature branch** to keep the repository clean.
- **Command to delete a local branch:**  
    ```bash
    git branch -d <your_branch_name>
    ```
    Example:  
    ```bash
    git branch -d apa-newFeature
    ```
- **Command to delete a remote branch:**  
    ```bash
    git push origin --delete <your_branch_name>
    ```
    Example:  
    ```bash
    git push origin --delete apa-newFeature
    ```

### 8. Commit Messages
- Use clear and concise commit messages.
- Follow the format: `<type>: <description>`  
  - Example:  
    ```
    feat: add user authentication module
    fix: resolve navbar alignment issue
    refactor: optimize API call logic
    ```

### 9. Code Review and Approval
- Ensure your code is reviewed by at least one team member before merging.
- **Don't merge the PR by yourself let any two members to test the branch and    approve it**
- Address any feedback promptly.

---

Following this standard practice ensures consistency for better collaboration within the team. 

