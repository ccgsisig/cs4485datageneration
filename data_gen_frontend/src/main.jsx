import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import { Auth0Provider } from "@auth0/auth0-react";
import App from "./App.jsx";
import "./index.css";

const domain = "dev-auif6sy5ey755omo.us.auth0.com"; // Your Auth0 domain
const clientId = "vQNIL6CxQEBEEQ4tikjQXCamjNZ9H9gw"; // Your Auth0 client ID

createRoot(document.getElementById("root")).render(
  <StrictMode>
    <Auth0Provider
      domain={domain}
      clientId={clientId}
      authorizationParams={{
        redirect_uri: "http://localhost:5173/callback", // Update to use the callback route
      }}
      cacheLocation="localstorage"
    >
      <App />
    </Auth0Provider>
  </StrictMode>
);
