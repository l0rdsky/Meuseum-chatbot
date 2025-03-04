# How to Run MuseBot

Follow these steps to run the MuseBot application:

## Prerequisites

- Ensure you have Python and Node.js installed on your machine.
- Clone the repository or switch to the `su-complete` branch and pull the latest changes.

## Backend Setup

1. **Navigate to the backend directory**:
    ```sh
    cd backend
    ```

2. **Install the required Python packages**:
    ```sh
    pip install -r requirements.txt
    ```

3. **Add the [.env](http://_vscodecontentref_/0) file**:
    - Paste the [.env](http://_vscodecontentref_/1) file in the `/backend` directory.

4. **Start the backend server**:
    ```sh
    uvicorn main:app --reload --port 5000
    ```
    - Ensure  areyou in the `/backend` directory when running this command.

## Frontend Setup

1. **Open a new terminal**.

2. **Navigate to the frontend directory**:
    ```sh
    cd frontend
    ```

3. **Start the frontend server**:
    ```sh
    npm run dev
    ```

4. **Access the application**:
    - Press `Ctrl + Click` on the link provided in the terminal or navigate to [http://localhost:5173/](http://localhost:5173/) in your browser.

## Summary

1. Clone the repository or switch to the `su-complete` branch and pull the latest changes.
2. Set up and start the backend server.
3. Set up and start the frontend server.
4. Access the application in your browser.

Enjoy using MuseBot!