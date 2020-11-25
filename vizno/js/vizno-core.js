"use strict";
const { html, render, useEffect, useRef, useState } = window.htmPreact;


const loadedComponents = {};
function loadDependencies({ componentName, jsDependencies, cssDependencies }) {
  const [readyJS, setReadyJS] = useState(
    loadedComponents[componentName] || false
  );
  const [readyCSS, setReadyCSS] = useState(
    loadedComponents[componentName] || false
  );
  useEffect(() => {
    jsDependencies.forEach((src, i) => {
      var script = document.createElement("script");
      script.src = src;
      script.type = "text/javascript";
      script.async = false;
      script.onload = () => {
        setReadyJS(i == jsDependencies.length - 1);
      };
      document.head.appendChild(script);
    });
    cssDependencies.forEach((src, i) => {
      var link = document.createElement("link");
      link.href = src;
      link.rel = "stylesheet";
      link.async = false;
      link.onload = () => {
        setReadyCSS(i == sources.length - 1);
      };
      document.head.appendChild(link);
    });
  });

  useEffect(()=> {
    if (readyJS && readyCSS) {
      loadedComponents[componentName] = true
    }
  }, [readyJS, readyCSS])

  return readyCSS && readyJS;
}

const dictComponent = {};
dictComponent.BokehContent = BokehContent;
function BokehContent({ spec, content_uuid }) {
  const divRef = useRef(null);

  useEffect(() => {
    if (divRef.current && content_uuid && window.Bokeh && window.Bokeh.embed) {
      window.Bokeh.embed.embed_item(spec, content_uuid);
    }
  }, [divRef, content_uuid, window.Bokeh]);

  return html`<div id="${content_uuid}" ref="${divRef}" />`;
}

dictComponent.VegaContent = VegaContent;
function VegaContent({ spec, content_uuid }) {
  const divRef = useRef(null);

  useEffect(() => {
    if (divRef.current && content_uuid && window.vegaEmbed) {
      spec.config.width = "container";
      spec.config.height = "container";
      window.vegaEmbed("#".concat(content_uuid), spec).catch(console.error);
    }
  }, [divRef, content_uuid, window.vegaEmbed]);

  return html`<div id="${content_uuid}" ref="${divRef}" />`;
}

dictComponent.MarkdownText = MarkdownText;
function MarkdownText({ text }) {
  const divRef = useRef(null);
  useEffect(() => {
    if (window.snarkdown && divRef.current) {
      divRef.current.innerHTML = window.snarkdown(text);
    }
  }, [window.snarkdown]);

  return html`<div ref="${divRef}" />`;
}

function SVGContainer({ data }) {
  const divRef = useRef(null);

  useEffect(() => {
    if (divRef.current) {
      divRef.current.innerHTML = data;
    }
  }, []);

  return html`<div ref="${divRef}" />`;
}

dictComponent.TableContent = TableContent;
function TableContent({ data, columns, content_uuid }) {
  const tableRef = useRef(null);
  useEffect(() => {
    if (tableRef.current && content_uuid && window.Tabulator) {
      var table = new window.Tabulator(`#${content_uuid}`, {
        data: data.map((d, i) => ({ id: i, ...d })),
        columns: columns.map((c) => ({ field: c, title: c })),
        layout: "fitColumns",
        height: "30vh",
      });
    }
  }, [tableRef, content_uuid]);

  return html`<div ref=${tableRef} id="${content_uuid}"></div>`;
}

dictComponent.SVGContent = SVGContent;
function SVGContent({ data }) {
  return html`<${SVGContainer} data="${data}" />`;
}

dictComponent.FallbackContent = FallbackContent;
function FallbackContent({ detected_type }) {
  return html`<p class="vz-text">Unknown content type "${detected_type}"</p>`;
}

function WidgetContent({ content }) {
  const { component, ...spec } = content;
  return html` <div class="vz-widget-content">
    ${dictComponent[component]
      ? html`<${dictComponent[component]} ...${spec} />`
      : html`<p class="vz-text">Component has no renderable content.</p>`}
  </div>`;
}

function Widget({ widgetSpec }) {
  const { name, description, content } = widgetSpec;
  return html` <div class="vz-widget">
    ${name ? html`<h3>${name}</h3>` : null}
    <${WidgetContent} content=${content} />
    ${description
      ? html`<div class="vz-description">
          <${MarkdownText} text=${description} />
        </div>`
      : null}
  </div>`;
}

function Header({ headerSpec }) {
  const { name, description } = headerSpec;
  return html` <div class="vz-header">
    ${name ? html`<h2>${name}</h2>` : null}
    <hr />
    ${description
      ? html`<div class="vz-text"><${MarkdownText} text=${description} /></div>`
      : null}
  </div>`;
}

function Text({ textSpec }) {
  const { text } = textSpec;
  return html` <div class="vz-text-element">
    <${MarkdownText} text=${text} />
  </div>`;
}

function Element({ element }) {
  const { element_type } = element;
  return html`<div class="vz-element">
    ${element_type === "widget"
      ? html` <${Widget} widgetSpec=${element} />`
      : element_type === "header"
      ? html`<${Header} headerSpec=${element} />`
      : element_type === "text"
      ? html`<${Text} textSpec=${element} />`
      : null}
  </div>`;
}

const widthToPureClass = [
  null,
  "1-12",
  "1-6",
  "1-4",
  "1-3",
  "5-12",
  "1-2",
  "7-12",
  "2-3",
  "3-4",
  "5-6",
  "11-12",
  "1-1",
];

function WidgetLayout({ elements }) {
  let currentLine = [];
  var currentLineWidth = 0;
  var elementLines = [];
  for (let element of elements) {
    if (
      element.element_type !== "header" &&
      currentLineWidth + element.layout.width <= 12 &&
      !element.layout.newline
    ) {
      currentLine = [...currentLine, element];
      currentLineWidth = currentLineWidth + element.layout.width;
    } else {
      elementLines = [...elementLines, currentLine];
      currentLineWidth = element.layout.width;
      currentLine = [element];
    }
  }
  if (currentLine.length) {
    elementLines = [...elementLines, currentLine];
  }
  return html`${elementLines.map(
    (line) =>
      html`<div class="pure-g">
        ${line.map(
          (e) => html` <div class="pure-u-${widthToPureClass[e.layout.width]}">
            <${Element} element=${e} />
          </div>`
        )}
      </div>`
  )}`;
}

function VizApp({ pageTitle, dateTime, description, elements }) {
  return html`
    <title>${pageTitle}</title>
    <div class="vz-body">
      <div class="vz-titlesection">
        <h1>${pageTitle}</h1>
        <div class="vz-datetime"><p>${dateTime}</p></div>
      </div>
      ${description
        ? html`<div class="vz-report-description vz-element">
            <${MarkdownText} text=${description} />
          </div>`
        : null}
      <div class="vz-widget-body">
        <${WidgetLayout} elements=${elements} />
      </div>
    </div>
  `;
}

function App() {
  const [configuration, setConfiguration] = useState(null);
  const [readyScript, setReadyScript] = useState(false);
  const [readyCSS, setReadyCSS] = useState(false);
  const [configurationRequest, setConfigurationRequest] = useState(null);

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
    if (window.configuration) {
      setConfiguration(window.configuration);
    } else {
      if (window.location.search) {
        let queryParams = new URLSearchParams(window.location.search);
        if (queryParams.has("configurationRequestURL")) {
          setConfigurationRequest(queryParams);
        }
      }
    }
  }, [window.configuration]);

  function loadScripts(sources) {
    sources.forEach((src, i) => {
      var script = document.createElement("script");
      script.src = src;
      script.type = "text/javascript";
      script.async = false;
      script.onload = () => {
        setReadyScript(i == sources.length - 1);
      };
      document.head.appendChild(script);
    });
  }

  function loadCSSScripts(sources) {
    sources.forEach((src, i) => {
      var link = document.createElement("link");
      link.href = src;
      link.rel = "stylesheet";
      link.async = false;
      link.onload = () => {
        setReadyCSS(i == sources.length - 1);
      };
      document.head.appendChild(link);
    });
  }

  useEffect(() => {
    if (configuration) {
      loadScripts(configuration.js_dependencies);
      loadCSSScripts(configuration.css_dependencies);
    }
  }, [configuration]);

  return configuration && readyScript && readyCSS
    ? html` <${VizApp}
        pageTitle="${configuration.title}"
        dateTime=${configuration.datetime}
        description=${configuration.description}
        elements=${configuration.elements}
      />`
    : html`No configuration`;
}

render(html` <${App} /> `, document.getElementById("root"));
