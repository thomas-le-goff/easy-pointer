import "react";
import { useCallback, useEffect, useRef, useState } from "react";
import { useGateKeyboardToFocusedIframe } from "../hooks/useGateKeyboardToFocusedIframe";
import "./EditorPage.css";

import "../userWorker";

import MonacoEditor from "react-monaco-editor";
import Markdown from "react-markdown";

import {
  Columns,
  Navbar,
  Panel,
  Button,
  Heading,
  Box,
  Block,
} from "react-bulma-components";
import { useApiClient } from "../hooks/useApiClient";

const codeChangeTimeout = 1000;

export const EditorPage = () => {
  const client = useApiClient();
  const [code, setCode] = useState();
  const [markdown, setMarkdown] = useState("");
  const [errors, setErrors] = useState([]);
  const gameIframeRef = useRef();
  const debounceTimerRef = useRef();

  useGateKeyboardToFocusedIframe(gameIframeRef);

  const onCodeChange = useCallback((value) => {
    if (value !== code) {
      setCode(code);
      clearTimeout(debounceTimerRef.current);
      debounceTimerRef.current = setTimeout(async () => {
        const response = await client.fetch(`/api/editor/code`, {
          method: "PUT",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            code: value,
          }),
        });

        if (response.ok) {
          // Refresh game renderer
          gameIframeRef.current.src += "";
        }
      }, codeChangeTimeout);
    }
  });

  const onMonacoMount = useCallback((editor) => {
    editor.onDidBlurEditorText(() => {});
    editor.onDidFocusEditorText(() => {});
  }, []);

  useEffect(() => {
    async function fetchCode() {
      const response = await client.fetch(`/api/editor/code`);

      if (response.ok) {
        const body = await response.json();
        setCode(body.code);
      }
    }

    fetchCode();
  }, []);

  return (
    <Columns className="editor-app" style={{ height: "100%" }}>
      <Columns.Column className="is-two-forth">
        <Box shadowless style={{ height: "100%" }}>
          <MonacoEditor
            value={code}
            onChange={onCodeChange}
            onMonacoMount={onMonacoMount}
            theme="vs-dark"
            language="c"
            options={{
              fontSize: 18,
              fontFamily: "PixelCode",
              selectOnLineNumbers: true,
              minimap: { enabled: false },
            }}
          />
        </Box>
      </Columns.Column>

      <Columns.Column>
        <Box
          shadowless
          className="has-background-primary p-0"
          style={{ height: "100%" }}
        >
          <Box
            shadowless
            className="m-0"
            style={{
              height: "50%",
              borderRadius: "0.5rem 0.5rem 0 0",
            }}
          >
            <iframe
              style={{
                width: "100%",
                height: "100%",
                display: "block",
                border: 0,
              }}
              allow="fullscreen; gamepad; autoplay"
              ref={gameIframeRef}
              id="game"
              src={`/api/editor/game`}
            />
          </Box>
          <Box
            shadowless
            className="m-0"
            style={{
              height: "50%",
              borderRadius: "0 0 0.5rem 0.5rem",
            }}
          >
            <Markdown>{markdown}</Markdown>
          </Box>
        </Box>
      </Columns.Column>
    </Columns>
  );
};
