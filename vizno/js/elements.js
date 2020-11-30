const { html } = window.htmPreact;

import { MarkdownText, WidgetContent } from "./renderers.js";

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

function TextElement({ textSpec }) {
  const { text } = textSpec;
  return html` <div class="vz-text-element">
    <${MarkdownText} text=${text} />
  </div>`;
}

function ViznoElement({ element }) {
  const { element_type } = element;
  return element_type === "widget"
    ? html` <${Widget} widgetSpec=${element} />`
    : element_type === "header"
    ? html`<${Header} headerSpec=${element} />`
    : element_type === "text"
    ? html`<${TextElement} textSpec=${element} />`
    : null;
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
  let currentLineWidth = 0;
  let elementLines = [];
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
            <${ViznoElement} element=${e} />
          </div>`
        )}
      </div>`
  )}`;
}

export function VizApp({ pageTitle, dateTime, description, elements }) {
  return html`
    <title>${pageTitle}</title>
    <div class="vz-body">
      <div class="vz-titlesection">
        <h1>${pageTitle}</h1>
        <div class="vz-datetime"><p>${dateTime}</p></div>
      </div>
      ${description
        ? html`<div class="vz-report-description">
            <${MarkdownText} text=${description} />
          </div>`
        : null}
      <div class="vz-widget-body">
        <${WidgetLayout} elements=${elements} />
      </div>
    </div>
  `;
}
