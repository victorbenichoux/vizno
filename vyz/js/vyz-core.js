"use strict";
const { html, render, useEffect, useRef } = window.htmPreact;

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
      window
        .vegaEmbed("#".concat(content_uuid), spec)
        .then(function (result) {})
        .catch(console.error);
    }
  }, [divRef, content_uuid, window.vegaEmbed]);

  return html`<div id="${content_uuid}" ref="${divRef}" />`;
}

dictComponent.MarkdownText = MarkdownText;
function MarkdownText({ text }) {
  const divRef = useRef(null);

  useEffect(() => {
    if (divRef.current) {
      divRef.current.innerHTML = marked(text);
    }
  }, []);

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
    ${name ? html`<h2>${name}</h2>` : null}
    ${description
      ? html`<div class="vz-text"><${MarkdownText} text=${description} /></div>`
      : null}
    <${WidgetContent} content=${content} />
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
  console.log(widgets);
  let currentLine = [];
  var currentLineWidth = 0;
  var widgetLines = [];
  for (let widget of widgets) {
    if (
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
            <${Widget} widgetSpec=${w} />
          </div>`
        )}
      </div>`
  )}`;
}

function VizApp({ pageTitle, dateTime, description, widgets }) {
  return html`
    <title>${pageTitle}</title>
    <div class="vz-titlebar">
      <div class="container">
        <div id="title">${pageTitle}</div>
        <div id="date-time">${dateTime}</div>
      </div>
    </div>
    <div class="vz-body">
      ${description
        ? html`<div class="vz-report-description">
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
  const configuration = window.configuration;
  return html`<${VizApp}
    pageTitle="${configuration.title}"
    dateTime=${configuration.datetime}
    description=${configuration.description}
    widgets=${configuration.widgets}
  />`;
}

render(html` <${App} /> `, document.getElementById("root"));
