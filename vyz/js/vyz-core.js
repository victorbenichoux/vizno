"use strict";
const { html, render, useEffect, useRef, useState } = window.htmPreact;

const dictComponent = {};

dictComponent.BokehContent = BokehContent;
function BokehContent({ spec, content_uuid }) {
  const divRef = useRef(null);

  useEffect(() => {
    if (divRef.current && content_uuid) {
      window.Bokeh.embed.embed_item(spec, content_uuid);
    }
  }, [divRef, content_uuid, window.Bokeh]);

  return html`<div id="${content_uuid}" ref="${divRef}" />`;
}

dictComponent.VegaContent = VegaContent;
function VegaContent({ spec, content_uuid }) {
  const divRef = useRef(null);

  useEffect(() => {
    if (divRef.current && content_uuid) {
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
    if (tableRef.current && content_uuid) {
      // console.log(columns.map((c) => ({ field: c, title: c })));
      // console.log(data.map((d, i) => ({ id: i, ...d }))[0]);
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

function Header({ widgetSpec }) {
  const { name, description } = widgetSpec;
  return html` <div class="vz-header">
    ${name ? html`<h2>${name}</h2>` : null}
    <hr />
    ${description
      ? html`<div class="vz-text"><${MarkdownText} text=${description} /></div>`
      : null}
  </div>`;
}

function Text({ widgetSpec }) {
  const { text } = widgetSpec;
  console.log(text);
  return html` <div class="vz-text-element">
    <${MarkdownText} text=${text} />
  </div>`;
}

function Element({ widgetSpec }) {
  const { element_type } = widgetSpec;
  return html`<div class="vz-element">
    ${element_type === "widget"
      ? html` <${Widget} widgetSpec=${widgetSpec} />`
      : element_type === "header"
      ? html`<${Header} widgetSpec=${widgetSpec} />`
      : element_type === "text"
      ? html`<${Text} widgetSpec=${widgetSpec} />`
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

function WidgetLayout({ widgets }) {
  let currentLine = [];
  var currentLineWidth = 0;
  var widgetLines = [];
  console.log(widgets);
  for (let widget of widgets) {
    if (
      widget.element_type !== "header" &&
      currentLineWidth + widget.layout.width <= 12 &&
      !widget.layout.newline
    ) {
      currentLine = [...currentLine, widget];
      currentLineWidth = currentLineWidth + widget.layout.width;
    } else {
      widgetLines = [...widgetLines, currentLine];
      currentLineWidth = widget.layout.width;
      currentLine = [widget];
    }
  }
  if (currentLine.length) {
    widgetLines = [...widgetLines, currentLine];
  }
  return html`${widgetLines.map(
    (line) =>
      html`<div class="pure-g">
        ${line.map(
          (w) => html` <div class="pure-u-${widthToPureClass[w.layout.width]}">
            <${Element} widgetSpec=${w} />
          </div>`
        )}
      </div>`
  )}`;
}

function VizApp({ pageTitle, dateTime, description, widgets }) {
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
        <${WidgetLayout} widgets=${widgets} />
      </div>
    </div>
  `;
}

function App() {
  const [configuration, setConfiguration] = useState(null);
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
  return configuration
    ? html`<${VizApp}
        pageTitle="${configuration.title}"
        dateTime=${configuration.datetime}
        description=${configuration.description}
        widgets=${configuration.widgets}
      />`
    : html`No configuration`;
}

render(html` <${App} /> `, document.getElementById("root"));
