import React, { useState } from "react";
import axios from "axios";
import Papa from "papaparse";

export default function FileUpload() {
  const [file, setFile] = useState(null);
  const [typedSchema, setTypedSchema] = useState(""); // For user-typed schema
  const [numRecords, setNumRecords] = useState(10); // Default value for number of records
  const [interval, setInterval] = useState(1); // Default value for interval (in minutes)
  const [message, setMessage] = useState("");
  const [filename, setFilename] = useState(""); // To store the output filename
  const [mode, setMode] = useState("batch"); //Default is batch, this is for updating which data generation mode we want
  const [csvContent, setCsvContent] = useState([]); //CSV data for display

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    setFile(selectedFile);

    const reader = new FileReader();
    reader.onload = (event) => {
      setTypedSchema(event.target.result); // Store the file content as string
    };
    reader.readAsText(selectedFile);
  };

  const handleFileUploadAndDownload = async () => {
    const formData = new FormData();

    if (typedSchema) {
      // Prioritize the typed schema if available
      const blob = new Blob([typedSchema], { type: "application/json" });
      formData.append("file", blob, "schema.json");
    } else if (file) {
      formData.append("file", file); // Use uploaded file if no typed schema
    } else {
      setMessage("Please upload or type a schema.");
      return;
    }

    formData.append("num_records", numRecords); // Send the number of records
    formData.append("interval", interval); // Send the interval (in minutes)
    formData.append("mode", mode); // Send the mode (batch or stream)

    try {
      const response = await axios.post(
        "http://localhost:8000/generate-csv",
        formData,
        {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        }
      );
      setMessage(response.data.message);
      setFilename(response.data.output_file); // Set the filename for downloading

      // Automatically download the generated CSV
      await handleDownloadCSV(response.data.output_file);
    } catch (error) {
      setMessage("Error uploading file");
      console.error(error);
    }
  };

  const handleDownloadCSV = async (filename) => {
    if (!filename) {
      setMessage("No file available for download.");
      return;
    }

    try {
      const response = await axios.get(
        `http://localhost:8000/download_csv/?filename=${filename}`,
        {
          responseType: "blob",
        }
      );
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement("a");
      link.href = url;
      link.setAttribute("download", filename); // Use the filename from the upload
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link); // Clean up after download

      //Display the CSV content
      const reader = new FileReader();
      reader.onload = function (e) {
        const text = e.target.result;
        Papa.parse(text, {
          header: true,
          complete: function (results) {
            setCsvContent(results.data); //set csv for display
          },
        });
      };
      reader.readAsText(new Blob([response.data]));
    } catch (error) {
      setMessage("Error downloading file");
      console.error(error);
    }
  };

  return (
    <div className="container mx-auto p-6">
      <h1 className="text-2xl font-bold mb-4">
        Upload JSON or Type Schema and Generate CSV
      </h1>

      <div className="mb-4">
        <input
          type="file"
          onChange={handleFileChange}
          className="border rounded-lg p-2"
        />
      </div>

      <div className="mb-4">
        <label className="block font-medium">Mode:</label>
        <select
          value={mode}
          onChange={(e) => setMode(e.target.value)}
          className="border rounded-lg p-2"
        >
          <option value="batch">Batch</option>
          <option value="stream">Stream</option>
        </select>
      </div>

      <div className="mb-4">
        <label className="block font-medium">
          Or Type Your JSON Schema (typed JSON will take priority):
        </label>
        <textarea
          value={typedSchema}
          onChange={(e) => setTypedSchema(e.target.value)}
          className="w-full h-40 border rounded-lg p-2"
          placeholder="Enter your JSON schema here"
        />
      </div>

      <div className="mb-4">
        <label className="block font-medium">Number of Records:</label>
        <input
          type="number"
          value={numRecords}
          onChange={(e) => setNumRecords(e.target.value)}
          className="border rounded-lg p-2"
        />
      </div>

      {mode == "stream" && (
        <div className="mb-4">
          <label className="block font-medium">Interval (minutes):</label>
          <input
            type="number"
            value={interval}
            onChange={(e) => setInterval(e.target.value)}
            className="border rounded-lg p-2"
          />
        </div>
      )}

      <button
        onClick={handleFileUploadAndDownload}
        className="bg-blue-500 text-white rounded-lg px-4 py-2 hover:bg-blue-600"
      >
        Generate and Download CSV
      </button>

      <p className="mt-4 text-red-500">{message}</p>
      {csvContent.length > 0 && (
        <div className="mt-6">
          <h2 className="text-xl font-bold mb-4">CSV Content:</h2>
          <table className="table-auto w-full">
            <thead>
              <tr>
                {Object.keys(csvContent[0]).map((header) => (
                  <th key={header} className="border px-4 py-2">
                    {header}
                  </th>
                ))}
              </tr>
            </thead>
            <tbody>
              {csvContent.map((row, rowIndex) => (
                <tr key={rowIndex}>
                  {Object.values(row).map((value, colIndex) => (
                    <td key={colIndex} className="border px-4 py-2">
                      {value}
                    </td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}
