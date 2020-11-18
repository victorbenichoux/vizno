"use strict";
const { html, render } = window.htmPreact;

function Widget({ widgetSpec }) {
  return html` <div class="vz-widget">
    <h2>${widgetSpec.name}</h2>
    <p>${widgetSpec.description}</p>
  </div>`;
}

function VizApp({ pageTitle, dateTime, description, widgets }) {
  return html`
    <title>${pageTitle}</title>
    <div class="vz-titlebar">
      <ul>
        <li><h1>${pageTitle}</h1></li>
        <li><p>${dateTime}</p></li>
      </ul>
    </div>
    <p>${description}</p>
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
