import React, { useState } from "react";
import axios from "axios";

function AlertConfig() {
  const [alertTitle, setAlertTitle] = useState("");
  const [alertMessage, setAlertMessage] = useState("");
  const [fieldName, setFieldName] = useState("");
  const [lowerBound, setLowerBound] = useState("");
  const [higherBound, setHigherBound] = useState("");

  const handleAddAlert = async () => {
    try {
      await axios.post("/add_alert", {
        alert_title: alertTitle,
        alert_message: alertMessage,
        field_name: fieldName,
        lower_bound: lowerBound,
        higher_bound: higherBound,
      });
      alert("Alert added successfully");
      // Reset fields after successful submission
      setAlertTitle("");
      setAlertMessage("");
      setFieldName("");
      setLowerBound("");
      setHigherBound("");
    } catch (error) {
      console.error("Error adding alert:", error);
    }
  };

  return (
    <div className="bg-background h-full text-foreground container mx-auto p-6 overflow-y-auto">
      <div className="max-w-md mx-auto">
        <h2 className="text-2xl font-bold mb-6 text-center">Add an Alert</h2>
        <form>
          <div className="space-y-4">
            <input
              type="text"
              className="w-full rounded-lg border p-3 shadow-sm text-background focus:border-electricblue focus:ring-electricblue"
              placeholder="Alert Title"
              value={alertTitle}
              onChange={(e) => setAlertTitle(e.target.value)}
            />
            <input
              type="text"
              className="w-full rounded-lg border p-3 shadow-sm text-background focus:border-electricblue focus:ring-electricblue"
              placeholder="Alert Message"
              value={alertMessage}
              onChange={(e) => setAlertMessage(e.target.value)}
            />
            <input
              type="text"
              className="w-full rounded-lg border p-3 shadow-sm text-background focus:border-electricblue focus:ring-electricblue"
              placeholder="Field Name"
              value={fieldName}
              onChange={(e) => setFieldName(e.target.value)}
            />
            <input
              type="number"
              className="w-full rounded-lg border p-3 shadow-sm text-background focus:border-electricblue focus:ring-electricblue"
              placeholder="Lower Bound"
              value={lowerBound}
              onChange={(e) => setLowerBound(e.target.value)}
            />
            <input
              type="number"
              className="w-full rounded-lg border p-3 shadow-sm text-background focus:border-electricblue focus:ring-electricblue"
              placeholder="Higher Bound"
              value={higherBound}
              onChange={(e) => setHigherBound(e.target.value)}
            />
          </div>
          <button
            type="button"
            className="relative flex h-9 w-full items-center justify-center px-4 mt-6 before:absolute before:inset-0 before:rounded-full before:bg-electricblue before:transition before:duration-300 hover:before:scale-105 active:duration-75 active:before:scale-95 sm:w-max"
            onClick={handleAddAlert}
          >
            <span className="relative text-sm font-semibold text-background">
              Add Alert
            </span>
          </button>
        </form>
      </div>
    </div>
  );
}

export default AlertConfig;
