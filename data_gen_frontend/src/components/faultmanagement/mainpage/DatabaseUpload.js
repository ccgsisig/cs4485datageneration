import React, { useState } from "react";
import axios from "axios";

function DatabaseUpload() {
  const [tables, setTables] = useState([]);
  const [uploadError, setUploadError] = useState(null);

  const handleFileUpload = async (event) => {
    const file = event.target.files[0];
    const formData = new FormData();
    formData.append("database_file", file);

    try {
      const response = await axios.post("/upload_database", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      setTables(response.data.tables); // Adjust to match your backend response format
      setUploadError(null);
    } catch (error) {
      setUploadError("Error uploading database. Please try again.");
      console.error("Error uploading database:", error);
    }
  };

  return (
    <div className="bg-background h-full text-foreground container mx-auto p-6 overflow-y-auto">
      <h2 className="text-2xl font-bold mb-4">Upload Database or CSV</h2>

      {uploadError && (
        <div
          className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded-lg mb-4"
          role="alert"
        >
          <span>{uploadError}</span>
        </div>
      )}

      <form>
        <div className="mb-4">
          <label
            htmlFor="formFileUpload"
            className="block text-sm font-medium mb-2"
          >
            Select Database File (.db or .csv)
          </label>
          <input
            type="file"
            id="formFileUpload"
            onChange={handleFileUpload}
            accept=".db, .csv"
            className="block w-full text-sm file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0
              file:font-semibold file:bg-electricblue file:text-background
              hover:file:bg-blue-100"
          />
        </div>

        <div className="mb-4">
          <label
            htmlFor="formTableSelect"
            className="block text-sm font-medium mb-2"
          >
            Select Table
          </label>
          <select
            id="formTableSelect"
            className="block w-full border rounded-lg p-2 focus:outline-none focus:ring-electricblue"
          >
            {tables.map((table) => (
              <option key={table} value={table}>
                {table}
              </option>
            ))}
          </select>
        </div>

        <button
          type="submit"
          className={`relative flex h-9 w-full items-center justify-center px-4 before:absolute before:inset-0 before:rounded-full before:bg-electricblue before:transition before:duration-300 hover:before:scale-105 active:duration-75 active:before:scale-95 sm:w-max ${
            !tables.length && "opacity-50 cursor-not-allowed"
          }`}
          disabled={!tables.length}
        >
          <span className="relative text-sm font-semibold text-background">
            Submit
          </span>
        </button>
      </form>
    </div>
  );
}

export default DatabaseUpload;
