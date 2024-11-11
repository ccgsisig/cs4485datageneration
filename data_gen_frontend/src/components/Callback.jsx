import { useEffect } from "react";
import { useAuth0 } from "@auth0/auth0-react";
import { useNavigate } from "react-router-dom";

const Callback = () => {
  const { isLoading, error, isAuthenticated } = useAuth0();
  const navigate = useNavigate();

  useEffect(() => {
    // Only navigate if we're authenticated and not loading
    if (!isLoading && isAuthenticated) {
      navigate("/"); // or wherever you want to redirect after login
    }
  }, [isLoading, isAuthenticated, navigate]);

  if (error) {
    return <div>Authentication error: {error.message}</div>;
  }

  return (
    <div className="flex items-center justify-center min-h-screen bg-gray-100">
      <div className="text-center p-6 bg-white rounded shadow-md">
        <h1 className="text-2xl font-bold mb-4 text-black">Loading...</h1>
        <p className="text-lg text-gray-700">
          Please wait while we log you in.
        </p>
      </div>
    </div>
  );
};

export default Callback;
