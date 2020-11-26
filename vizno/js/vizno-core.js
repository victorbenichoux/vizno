const { html, render, useEffect, useRef, useState } = window.htmPreact;

import { DependencyLoader } from "./hooks.js";

import { VizApp } from "./elements.js";

function App() {
  const [configuration, setConfiguration] = useState(null);
  const [configurationRequest, setConfigurationRequest] = useState(null);
  const isLoadingDependencies = useRef({});
  const [canRender, setCanRender] = useState({});

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
        .then((configuration) => setConfiguration(configuration));
    }
  }, [configurationRequest]);

  useEffect(() => {
    if (window.location.search) {
      let queryParams = new URLSearchParams(window.location.search);
      if (queryParams.has("configurationRequestURL")) {
        setConfigurationRequest(queryParams);
      }
    } else {
      const script = document.createElement("script");
      script.src = "./vizno-config.js";
      script.type = "text/javascript";
      script.async = false;
      script.onload = () => {
        setConfiguration(window.configuration);
      };
      document.head.appendChild(script);
    }
  }, []);

  return configuration
    ? html` <${DependencyLoader.Provider} value=${{
        isLoadingDependencies,
        canRender,
        setCanRender,
      }}><${VizApp}
        pageTitle="${configuration.title}"
        dateTime=${configuration.datetime}
        description=${configuration.description}
        elements=${configuration.elements}
      /></${DependencyLoader}>`
    : html`Loading configuration...`;
}

render(html` <${App} /> `, document.getElementById("root"));
