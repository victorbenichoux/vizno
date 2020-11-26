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
      const ws = new WebSocket("ws://localhost:8000/ws");
      ws.onmessage = () => {
        setStatus({
          configuration: null,
          shouldUpdate: true,
        });
      };

      if (window.location.search) {
        let queryParams = new URLSearchParams(window.location.search);
        if (queryParams.has("configurationRequestURL")) {
          setConfigurationRequest(queryParams);
        }
      } else {
        const script = document.createElement("script");
        script.src = "vizno-config.js";
        script.type = "text/javascript";
        script.async = false;
        script.onload = () => {
          setStatus({
            shouldUpdate: false,
            configuration: window.configuration,
          });
        };
        document.head.appendChild(script);
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
