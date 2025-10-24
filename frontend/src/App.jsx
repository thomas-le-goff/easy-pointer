import { ToastContainer } from "react-toastify";
import { BrowserRouter, Navigate, Route, Routes } from "react-router";
import { EditorPage } from "./pages/EditorPage";
import { OAuth2ProviderPage } from "./pages/OAuth2/OAuth2ProviderPage";
import { OAuth2Layout } from "./pages/OAuth2/OAuth2Layout";
import { OAuth2SuccessPage } from "./pages/OAuth2/OAuth2SuccessPage";
import { AuthenticatedLayout } from "./pages/AuthenticatedLayout";
import "bulma/css/bulma.min.css";
import { AuthProvider } from "./contexts/AuthContext";

export const App = () => {
  return (
    <AuthProvider>
      <ToastContainer />
      <BrowserRouter>
        <Routes>
          <Route index element={<Navigate to="editor" replace />} />
          <Route path="auth">
            <Route element={<OAuth2Layout />}>
              <Route index element={<OAuth2ProviderPage />} />
              <Route path="success" element={<OAuth2SuccessPage />} />
            </Route>
          </Route>
          <Route element={<AuthenticatedLayout />}>
            <Route path="editor" element={<EditorPage />} />
          </Route>
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  );
};