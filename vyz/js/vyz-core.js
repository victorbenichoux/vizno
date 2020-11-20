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
  }, [divRef, content_uuid,  window.vegaEmbed]);

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
  return html`<p>Unknown content type "${detected_type}"</p>`;
}

function WidgetContent({ content }) {
  const { component, ...spec } = content;
  return html` <div class="vz-widget-content">
    ${dictComponent[component]
      ? html`<${dictComponent[component]} ...${spec} />`
      : html`<p>Error</p>`}
  </div>`;
}

function Widget({ widgetSpec }) {
  const { name, description, content } = widgetSpec;
  return html` <div class="vz-widget pure-u-1-3">
    <h2>${name}</h2>
    <${MarkdownText} text=${description} />
    <${WidgetContent} content=${content} />
  </div>`;
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
      <div class="vz-report-description">
        <${MarkdownText} text=${description} />
      </div>
      <div class="vz-widget-body pure-g">
        ${widgets.map((d) => html`<${Widget} widgetSpec=${d} />`)}
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
