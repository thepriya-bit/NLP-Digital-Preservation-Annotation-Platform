import { Routes, Route } from "react-router-dom";

import Home from "../pages/Home";
import Login from "../pages/Login";
import Dashboard from "../pages/Dashboard";
import Contributor from "../pages/Contributor";
import ContributorDashboard from "../pages/ContributorDashboard";
import NotFound from "../pages/NotFound";

const AppRoutes = () => {
  return (
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/login" element={<Login />} />
      <Route path="/dashboard" element={<Dashboard />} />
      <Route path="/contributor" element={<ContributorDashboard />} />
      <Route path="/contributor-dashboard" element={<ContributorDashboard />} />
      <Route path="/verify" element={<Contributor />} />
      <Route path="*" element={<NotFound />} />
    </Routes>
  );
};

export default AppRoutes;