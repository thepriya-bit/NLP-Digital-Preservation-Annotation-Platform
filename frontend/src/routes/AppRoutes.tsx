import { Routes, Route } from "react-router-dom";

import Home from "../pages/Home";
import Login from "../pages/Login";
import Dashboard from "../pages/Dashboard";
import ContributorDashboard from "../pages/ContributorDashboard";
import VerifyPage from "../pages/VerifyPage";
import AdminConsole from "../pages/AdminConsole";
import NotFound from "../pages/NotFound";
import ProtectedRoute from "../components/auth/ProtectedRoute";

const AppRoutes = () => {
  return (
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/login" element={<Login />} />
      <Route
        path="/dashboard"
        element={
          <ProtectedRoute>
            <Dashboard />
          </ProtectedRoute>
        }
      />
      <Route
        path="/contributor"
        element={
          <ProtectedRoute roles={["annotator", "verifier"]}>
            <ContributorDashboard />
          </ProtectedRoute>
        }
      />
      <Route
        path="/contributor-dashboard"
        element={
          <ProtectedRoute roles={["annotator", "verifier"]}>
            <ContributorDashboard />
          </ProtectedRoute>
        }
      />
      <Route
        path="/verify"
        element={
          <ProtectedRoute roles={["verifier", "admin"]}>
            <VerifyPage />
          </ProtectedRoute>
        }
      />
      <Route
        path="/admin"
        element={
          <ProtectedRoute roles={["admin"]}>
            <AdminConsole />
          </ProtectedRoute>
        }
      />
      <Route path="*" element={<NotFound />} />
    </Routes>
  );
};

export default AppRoutes;
