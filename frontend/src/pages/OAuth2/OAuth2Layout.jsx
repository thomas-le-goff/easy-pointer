import { ShieldUser } from "lucide-react";
import "react";

import {
  Box,
  Columns,
  Container,
  Heading,
  Hero,
  Icon,
} from "react-bulma-components";
import { Outlet } from "react-router";

export const OAuth2Layout = () => {
  return (
    <Hero size="fullheight" className="has-background">
      <Hero.Body>
        <Container breakpoint="desktop">
          <Columns centered>
            <Columns.Column size={5}>
              <Box className="p-5" style={{ borderRadius: 16 }}>
                <div className="has-text-centered">
                  <span className="icon is-large">
                    <ShieldUser size={48} />
                  </span>
                </div>

                <Outlet />
              </Box>
            </Columns.Column>
          </Columns>
        </Container>
      </Hero.Body>
    </Hero>
  );
};
