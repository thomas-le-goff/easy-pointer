import { useEffect, useCallback, useState } from "react";

import { toaster } from "../utils/toaster";
import { Navigate, Outlet, useNavigate } from "react-router";
import { useAuth } from "../hooks/useAuth";
import {
  Navbar,
  Link,
  Icon,
  Image,
  Section,
  Container,
  Button,
} from "react-bulma-components";

export const AuthenticatedLayout = () => {
  const auth = useAuth();
  const [isDisconnecting, setIsDisconnecting] = useState(false);
  const [menuActive, setMenuActive] = useState(false);
  const navigate = useNavigate();

  const handleLogoutClick = useCallback(() => {
    setIsDisconnecting(true);
    auth.invalidateUser().then(() => {});
  }, [auth, navigate]);

  useEffect(() => {
    if (!auth.user) {
      isDisconnecting ? toaster.successDisconnected() : toaster.warnAuth();
      navigate("/auth");
    }
  }, [auth, isDisconnecting, navigate]);

  return (
    <>
      {!auth.user ? (
        <Section>
          {" "}
          <Outlet />{" "}
        </Section>
      ) : (
        <>
          <Navbar active={menuActive} fixed="top">
            <Navbar.Brand>
              <Navbar.Item renderAs={Link} to="/">
                EasyPointer - Editor
              </Navbar.Item>

              <Navbar.Burger
                aria-label="menu"
                aria-expanded={menuActive ? "true" : "false"}
                onClick={() => setMenuActive((v) => !v)}
              />
            </Navbar.Brand>

            <Navbar.Menu>
              <Navbar.Container align="right">
                <Navbar.Item>
                  <span className="mr-2">Bienvenue {auth.user.login}</span>
                  <Image
                    src={auth.user.avatar_url}
                    alt="Avatar utilisateur"
                    rounded
                  />
                </Navbar.Item>
                <Navbar.Item>
                  <Button onClick={handleLogoutClick}>Déconnexion</Button>
                </Navbar.Item>
              </Navbar.Container>
            </Navbar.Menu>
          </Navbar>

          <Section
            className="has-background"
            style={{ height: "calc(100vh - var(--bulma-navbar-height))" }}
          >
            <Outlet />
          </Section>
        </>
      )}
    </>
  );
};
