import React, { useState } from "react";
import axios from "axios";

function SchemaUpload() {
  const [schema, setSchema] = useState("");
  const [successMessage, setSuccessMessage] = useState("");
  const [errorMessage, setErrorMessage] = useState("");

  const handleSchemaUpload = async () => {
    try {
      await axios.post("/upload_schema", { schema_data: schema });
      setSuccessMessage("Schema data uploaded successfully");
      setErrorMessage("");
      setSchema(""); // Clear the schema field after successful upload
    } catch (error) {
      console.error("Error uploading schema:", error);
      setErrorMessage("Error uploading schema");
      setSuccessMessage("");
    }
  };

  return (
    <div className="bg-background h-full text-foreground container mx-auto p-6 overflow-y-auto">
      <h2 className="text-center text-2xl font-bold mb-4">
        Upload Schema Data
      </h2>
      <div className="flex justify-center">
        <div className="w-full md:w-2/3">
          {successMessage && (
            <div
              className="bg-green-100 border border-green-400 text-green-700 px-4 py-3 rounded-lg mb-4"
              role="alert"
            >
              <span>{successMessage}</span>
            </div>
          )}
          {errorMessage && (
            <div
              className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded-lg mb-4"
              role="alert"
            >
              <span>{errorMessage}</span>
            </div>
          )}
          <form>
            <div className="mb-4">
              <label
                htmlFor="schemaTextarea"
                className="block text-sm font-medium mb-2"
              >
                Schema JSON
              </label>
              <textarea
                id="schemaTextarea"
                rows={10}
                value={schema}
                onChange={(e) => setSchema(e.target.value)}
                placeholder="Enter schema data as JSON..."
                className="w-full rounded-lg border text-background p-2 shadow-sm focus:border-electricblue focus:ring-electricblue"
              />
            </div>
            <button
              type="button"
              className="relative flex h-9 w-full items-center justify-center px-4 before:absolute before:inset-0 before:rounded-full before:bg-electricblue before:transition before:duration-300 hover:before:scale-105 active:duration-75 active:before:scale-95 sm:w-max"
              onClick={handleSchemaUpload}
            >
              <span className="relative text-sm font-semibold text-background">
                Upload Schema
              </span>
            </button>
          </form>
        </div>
      </div>
    </div>
  );
}

export default SchemaUpload;
