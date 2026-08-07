// routes/ProtectedRoute.tsx
import { Navigate, Outlet, useLocation } from "react-router-dom";
import { useAuth } from "../modules/auth/context/AuthContext";
import { FullScreenSpinner } from "../shared/ui/FullScreenSpinner";

export function ProtectedRoute() {
  const { isAuthenticated, isLoading } = useAuth();
  const location = useLocation();

  if (isLoading) return <FullScreenSpinner />;
  if (!isAuthenticated) return <Navigate to="/login" state={{ from: location }} replace />;
  return <Outlet />;
}

export function PublicOnlyRoute() {
  const { isAuthenticated, isLoading } = useAuth();
  if (isLoading) return <FullScreenSpinner />;
  if (isAuthenticated) return <Navigate to="/" replace />;
  return <Outlet />;
}