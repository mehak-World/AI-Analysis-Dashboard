import { Routes, Route } from "react-router-dom";
import { AuthProvider } from "./modules/auth/context/AuthContext";
import { ProtectedRoute, PublicOnlyRoute } from "./routes/ProtectedRoute";
import LoginPage from "./modules/auth/pages/LoginPage"
import DashboardPage from "./modules/dashboard/pages/DashboardPage";

const App = () => {
  return (
    <div>
      <AuthProvider>
        <Routes>
          <Route element={<ProtectedRoute />}>
            <Route path="/" element={<DashboardPage />} />
          </Route>
          <Route element={<PublicOnlyRoute />}>
            <Route path="/login" element={<LoginPage />} />
          </Route>
        </Routes>
      </AuthProvider>
    </div>
  );
};

export default App;
