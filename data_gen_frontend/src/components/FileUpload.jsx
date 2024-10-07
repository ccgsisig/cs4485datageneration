import React, { useState } from "react";
import axios from "axios";

export default function FileUpload() {
  const [file, setFile] = useState(null);
  const [numRecords, setNumRecords] = useState(10); // Default value for number of records
  const [interval, setInterval] = useState(1); // Default value for interval (in minutes)
  const [message, setMessage] = useState("");
  const [filename, setFilename] = useState(""); // To store the output filename

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleFileUpload = async () => {
    const formData = new FormData();
    formData.append("file", file);
    formData.append("num_records", numRecords); // Send the number of records
    formData.append("interval", interval); // Send the interval (in minutes)

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
    } catch (error) {
      setMessage("Error uploading file");
      console.error(error);
    }
  };

  const handleDownloadCSV = async () => {
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
    } catch (error) {
      setMessage("Error downloading file");
      console.error(error);
    }
  };

  return (
    <div className="container mx-auto p-6">
      <h1 className="text-2xl font-bold mb-4">Upload JSON and Generate CSV</h1>

      <div className="mb-4">
        <input
          type="file"
          onChange={handleFileChange}
          className="border rounded-lg p-2"
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

      <div className="mb-4">
        <label className="block font-medium">Interval (minutes):</label>
        <input
          type="number"
          value={interval}
          onChange={(e) => setInterval(e.target.value)}
          className="border rounded-lg p-2"
        />
      </div>

      <button
        onClick={handleFileUpload}
        className="bg-blue-500 text-white rounded-lg px-4 py-2 mr-2 hover:bg-blue-600"
      >
        Upload and Generate
      </button>

      <button
        onClick={handleDownloadCSV}
        className="bg-green-500 text-white rounded-lg px-4 py-2 hover:bg-green-600"
      >
        Download CSV
      </button>

      <p className="mt-4 text-red-500">{message}</p>
    </div>
  );
}
