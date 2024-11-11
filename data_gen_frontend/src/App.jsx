import { useAuth0 } from "@auth0/auth0-react";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import FileUpload from "./components/FileUpload";
import Callback from "./components/Callback";

function App() {
  const { isAuthenticated, loginWithRedirect, logout, user, isLoading } =
    useAuth0();

  if (isLoading) {
    return <div>Loading...</div>; // Display a loading message while checking authentication
  }

  return (
    <Router>
      <Routes>
        <Route
          path="/"
          element={
            !isAuthenticated ? (
              <button onClick={loginWithRedirect}>Log In</button>
            ) : (
              <div>
                <h2>Welcome, {user.name}!</h2>
                <button
                  onClick={() =>
                    logout({ returnTo: `${window.location.origin}/` })
                  }
                >
                  Log Out
                </button>
                <FileUpload />
              </div>
            )
          }
        />
        <Route path="/fileupload" element={<FileUpload />} />
        <Route path="/callback" element={<Callback />} />{" "}
        {/* Add Callback route */}
      </Routes>
    </Router>
  );
}

export default App;
