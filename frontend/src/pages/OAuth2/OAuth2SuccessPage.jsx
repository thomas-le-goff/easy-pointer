import "react";
import { Heading, Icon, Container, Image } from "react-bulma-components";

import { Link } from "react-router";
import { Braces } from "lucide-react";
import { useAuth } from "../../hooks/useAuth";

export const OAuth2SuccessPage = () => {
  const auth = useAuth();

  return (
    <>
      <Heading size={3} className="has-text-centered mt-3">
        {!auth?.user ? (
          <span />
        ) : (
          <Container>
            <span>Bienvenue {auth.user.login} !</span>
            <figure class="image is-128x128 mt-4" style={{ margin: "0 auto" }}>
              <Image rounded src={auth.user.avatar_url} />
            </figure>
          </Container>
        )}
      </Heading>
      <Link
        to={"/editor"}
        fullwidth
        className={
          "button container is-link is-medium mt-4 " +
          (auth.user ? "" : "is-loading")
        }
      >
        <Icon className="mr-2">
          <Braces />
        </Icon>
        <span>Accéder à l'éditeur</span>
      </Link>
    </>
  );
};
