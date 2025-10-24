import { useCallback, useEffect } from "react";
import { useAuth } from "../../hooks/useAuth";
import { useNavigate } from "react-router";

import { Heading, Icon, Button } from "react-bulma-components";

import { SiGithub } from "@icons-pack/react-simple-icons";

export const OAuth2ProviderPage = () => {
  const auth = useAuth();
  const navigate = useNavigate();

  useEffect(() => {
    if (auth.user) {
      navigate("/editor");
    }
  }, [auth, navigate]);

  const handleProviderOnClick = useCallback(() => {
    window.location.href = "/api/auth/github/authorize";
  }, []);

  return (
    <>
      <Heading size={3} className="has-text-centered mt-3">
        Valider mon identité
      </Heading>
      <Heading subtitle size={6} className="has-text-grey has-text-centered">
        avec
      </Heading>
      <Button
        onClick={handleProviderOnClick}
        className="button container is-link is-medium mt-4"
      >
        <Icon className="mr-2">
          <SiGithub />
        </Icon>
        <span>Continuer avec GitHub</span>
      </Button>
    </>
  );
};
