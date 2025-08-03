import React, { useState } from "react";
import axios from "axios";

const ResumeUploader = () => {
  const [file, setFile] = useState(null);
  const [selectedRole, setSelectedRole] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const roles = [
    "Data Analyst",
    "AI Engineer",
    "Full Stack Developer",
    "Software Engineer",
  ];

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    if (
      selectedFile &&
      ["application/pdf", "application/vnd.openxmlformats-officedocument.wordprocessingml.document"].includes(
        selectedFile.type
      )
    ) {
      setFile(selectedFile);
      setError("");
      setResult(null);
    } else {
      setError("Only PDF or DOCX files are allowed.");
    }
  };

  const handleUpload = async () => {
    if (!file || !selectedRole) {
      setError("Please select a role and upload a resume.");
      return;
    }

    const formData = new FormData();
    formData.append("resume", file);
    formData.append("desired_role", selectedRole);

    setLoading(true);
    try {
      const res = await axios.post("http://localhost:5000/parse_resume", formData);
      setResult(res.data);
      setError("");
    } catch (err) {
      setError("Failed to parse resume.");
    }
    setLoading(false);
  };

  return (
    <div className="min-h-screen bg-gray-100 py-10 px-4 font-sans">
      <div className="max-w-2xl mx-auto bg-white shadow-md p-8 rounded-lg">
        <h2 className="text-2xl font-bold text-center text-indigo-600 mb-6">Resume Match Analyzer</h2>

        <label className="block mb-2 text-sm font-medium text-gray-700">Select Desired Role:</label>
        <select
          className="w-full border rounded px-3 py-2 mb-4"
          value={selectedRole}
          onChange={(e) => setSelectedRole(e.target.value)}
        >
          <option value="">-- Select a Role --</option>
          {roles.map((role) => (
            <option key={role} value={role}>{role}</option>
          ))}
        </select>

        <input
          type="file"
          accept=".pdf,.docx"
          onChange={handleFileChange}
          className="mb-4"
        />

        <button
          onClick={handleUpload}
          className="w-full bg-indigo-600 hover:bg-indigo-700 text-white font-semibold py-2 px-4 rounded"
        >
          {loading ? "Analyzing..." : "Upload Resume"}
        </button>

        {error && <p className="text-red-600 mt-4">{error}</p>}

        {result && (
          <div className="mt-6 bg-gray-50 border rounded p-4">
            <h3 className="text-lg font-bold text-gray-800 mb-2">Match Result</h3>

            <p className="mb-2">
              <strong className="text-gray-700">Selected Role:</strong> {result.desired_role}
            </p>
            <p className="mb-2">
              <strong className="text-gray-700">Matched Keywords:</strong>{" "}
              {result.matched_keywords.length
                ? result.matched_keywords.join(", ")
                : "None"}
            </p>
            <p className="mb-2">
              <strong className="text-gray-700">Match Count:</strong> {result.match_count}
            </p>
            <p className="mt-4 font-semibold text-indigo-600">{result.recommendation}</p>
          </div>
        )}
      </div>
    </div>
  );
};

export default ResumeUploader;
