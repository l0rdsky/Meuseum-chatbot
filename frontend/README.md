# Museum Chatbot Frontend

This is the frontend for the Museum Chatbot Ticketing System built using React and Vite. It provides an interactive user interface for visitors to:
- Check ticket availability
- Get information about exhibitions and events
- Purchase tickets securely through integrated payment gateways

---

## Tech Stack
- React (with Vite for fast build and development)
- React Router for navigation
- Axios for API calls
- TailwindCSS for styling

---

## Prerequisites
- Node.js (v16 or later) and npm installed

---

## Installation and Setup
1. Clone the repository:
    ```bash
    git clone https://github.com/l0rdsky/Meuseum-chatbot.git
    cd frontend
    ```

2. Install dependencies:
    ```bash
    npm install
    ```

3. Start the development server:
    ```bash
    npm run dev
    ```
    The application will be accessible at `http://localhost:5173`

---

## Project Structure

```frontend/
├── public/
├── src/
│   ├── api/               # For Axios API calls
│   ├── components/        # Reusable components like Chatbot, Navbar, Footer
│   ├── pages/             # Pages like Home, Exhibitions, Ticketing
│   ├── App.jsx
│   └── main.jsx
├── index.html
└── package.json```


---

## Available Scripts
- `npm run dev`: Start the development server
- `npm run build`: Build the project for production
- `npm run preview`: Preview the production build

---

## Environment Variables
Create a `.env` file in the root directory with the following:
VITE_API_BASE_URL=http://localhost:8000 # FastAPI backend URL


---

## Features
- Real-time ticket availability
- Detailed information about exhibitions and events
- Secure payment processing

---

## Contributing
Contributions are welcome! Please submit a pull request or open an issue for suggestions.

---

## License
This project is licensed under the MIT License.
