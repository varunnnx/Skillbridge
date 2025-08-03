import React from "react";

const RoleSelector = ({ selectedRole, setSelectedRole }) => (
  <div>
    <label htmlFor="role-select"><strong>Choose your desired role:</strong> </label>
    <select
      id="role-select"
      value={selectedRole}
      onChange={(e) => setSelectedRole(e.target.value)}
    >
      <option value="">--Select--</option>
      <option value="Data Analyst">Data Analyst</option>
      <option value="AI Engineer">AI Engineer</option>
      <option value="Full Stack Developer">Full Stack Developer</option>
      <option value="Software Engineer">Software Engineer</option>
    </select>
  </div>
);

export default RoleSelector;
