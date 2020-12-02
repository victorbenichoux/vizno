const { html, render, useEffect, useRef, useState } = window.htmPreact;

import { DependencyLoader } from "./hooks.js";

import { VizApp } from "./elements.js";

function App() {
  const [configurationRequest, setConfigurationRequest] = useState(null);
  const isLoadingDependencies = useRef({});
  const [canRender, setCanRender] = useState({});
  const [status, setStatus] = useState({
    configuration: null,
    shouldUpdate: true,
  });
  const hasWebSocket = useRef(false);

  useEffect(() => {
    if (configurationRequest) {
      const configurationRequestURL = configurationRequest.get(
        "configurationRequestURL"
      );
      configurationRequest.delete("configurationRequestURL");
      fetch(`${configurationRequestURL}?${configurationRequest.toString()}`, {
        headers: { "content-type": "application/json" },
        method: "GET",
      })
        .then((resp) => resp.json())
        .then((configuration) =>
          setStatus({
            shouldUpdate: false,
            configuration,
          })
        );
    }
  }, [configurationRequest]);

  useEffect(() => {
    if (status.shouldUpdate) {
      if (!hasWebSocket.current) {
        try {
          const ws = new WebSocket("ws://localhost:8000/ws");
          ws.onmessage = () => {
            hasWebSocket.current = true;
            setStatus({
              configuration: null,
              shouldUpdate: true,
            });
          };
          ws.onerror = () => {
            console.log("No auto update available");
          };
        } catch (error) {
          console.log("No auto update available", error);
        }
      }

      if (window.location.search) {
        let queryParams = new URLSearchParams(window.location.search);
        if (queryParams.has("configurationRequestURL")) {
          setConfigurationRequest(queryParams);
        }
      } else {
        setStatus({
          shouldUpdate: false,
          configuration: window.configuration,
        });
      }
    }
  }, [status]);

  return status.configuration
    ? html` <${DependencyLoader.Provider} value=${{
        isLoadingDependencies,
        canRender,
        setCanRender,
      }}><${VizApp}
        pageTitle="${status.configuration.title}"
        dateTime=${status.configuration.datetime}
        description=${status.configuration.description}
        elements=${status.configuration.elements}
      /></${DependencyLoader}>`
    : html`Loading configuration...`;
}

render(html` <${App} /> `, document.getElementById("root"));
