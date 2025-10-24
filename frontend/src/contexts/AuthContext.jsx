import { createContext } from "react";
import { useCallback, useMemo, useEffect } from "react";
import { useLocalStorage } from "../hooks/useLocalStorage";

export const AuthContext = createContext(undefined);

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useLocalStorage("user", undefined);

  const invalidateUser = useCallback(() => {
    return fetch("/api/auth/logout", {
      method: "POST",
      credentials: "include",
    }).then(() => {
      setUser(undefined);
    });
  }, [setUser]);

  const value = useMemo(
    () => ({
      user: user,
      setUser: setUser,
      invalidateUser: invalidateUser,
    }),
    [user, setUser, invalidateUser]
  );

  useEffect(() => {
    if (user != undefined) return;
    (async () => {
      const response = await fetch("/api/users/me", {
        credentials: "include",
      });
      if (!response.ok) {
        invalidateUser();
        return;
      }

      const user = await response.json();
      setUser(user);
    })();
  }, []);

  return <AuthContext value={value}>{children}</AuthContext>;
};
