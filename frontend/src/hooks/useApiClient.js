import { useNavigate } from "react-router";
import { useAuth } from "./useAuth";

const defaultInit = {
  credentials: "include", // TODO: replace by samesite
};

export const useApiClient = () => {
  const auth = useAuth();
  const navigate = useNavigate();

  const _fetch = (input, init) => {
    const url = input;
    return fetch(url, { ...defaultInit, ...init }).then((response) => {
      if (response.status == 401) {
        auth.invalidateUser();
        navigate("/auth");
      }

      return response;
    });
  };

  return {
    fetch: _fetch,
  };
};
