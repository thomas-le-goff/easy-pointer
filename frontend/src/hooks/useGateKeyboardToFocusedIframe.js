import { useEffect } from "react";

export const useGateKeyboardToFocusedIframe = (iframeRef) => {
  useEffect(() => {
    const gate = (e) => {
      const iframe = iframeRef.current;
      if (!iframe) return;

      const iframeHasFocus = document.activeElement === iframe;
      if (!iframeHasFocus) {
        e.stopPropagation();
        e.stopImmediatePropagation?.();
      }
    };

    window.addEventListener("keydown", gate, { capture: false });
    window.addEventListener("keyup", gate, { capture: false });

    return () => {
      window.removeEventListener("keydown", gate, { capture: false });
      window.removeEventListener("keyup", gate, { capture: false });
    };
  }, [iframeRef]);
};
