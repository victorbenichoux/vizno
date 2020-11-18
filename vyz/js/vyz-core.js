"use strict";
const { html, render, useEffect, useRef } = window.htmPreact;

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

function SVGContent({ data }) {
  return html`<${SVGContainer} data="${data}" />`;
}

function FallbackContent({ detected_type }) {
  return html`<p>Unknown content type "${detected_type}"</p>`;
}

function WidgetContent({ content }) {
  const { component, ...spec } = content;
  return html` <div class="vz-widget-content">
    ${component === "FallbackContent"
      ? html`<${FallbackContent} ...${spec} />`
      : component === "SVGContent"
      ? html`<${SVGContent} ...${spec} />`
      : component=== "TextContent"
      ? html`<${MarkdownText} ...${spec} />`
      : html`<p>Error</p>`}
  </div>`;
}

function Widget({ widgetSpec }) {
  const { name, description, content } = widgetSpec;
  return html` <div class="vz-widget">
    <h2>${name}</h2>
    <${MarkdownText} text=${description} />
    <${WidgetContent} content=${content} />
  </div>`;
}

function VizApp({ pageTitle, dateTime, description, widgets }) {
  return html`
    <title>${pageTitle}</title>
    <div class="vz-titlebar">
      <ul>
        <li><h1>${pageTitle}</h1></li>
        <li><p>text=${dateTime}</p></li>
      </ul>
    </div>
    <${MarkdownText} text=${description} />
    <div class="vz-widget-body">
      ${widgets.map((d) => html`<${Widget} widgetSpec=${d} />`)}
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
