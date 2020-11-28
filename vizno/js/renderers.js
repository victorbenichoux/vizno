const { html, useEffect, useRef } = window.htmPreact;
import { useDependencies } from "./hooks.js";
const dictComponent = {};

dictComponent.BokehContent = BokehContent;
/**
 * A Component that embeds Bokeh visuals
 * @param {Object} props
 * @param {Object} props.spec - An embeddable Bokeh item
 * @param {string} props.content_uuid - The id of the div to create and render to
 * @param {string[]} props.external_js_dependencies - The JS dependencies for BokehContent
 * @param {string[]} props.external_css_dependencies - The CSS dependencies for BokehContent
 */
function BokehContent({
  spec,
  content_uuid,
  external_js_dependencies,
  external_css_dependencies,
}) {
  const ready = useDependencies({
    componentName: "BokehContent",
    jsDependencies: external_js_dependencies,
    cssDependencies: external_css_dependencies,
  });

  const divRef = useRef(null);

  useEffect(() => {
    if (divRef.current && content_uuid && ready) {
      window.Bokeh.embed.embed_item(spec, content_uuid);
    }
  }, [divRef, content_uuid, ready, spec]);

  return html`<div id="${content_uuid}" ref="${divRef}" />`;
}

dictComponent.VegaContent = VegaContent;
/**
 * A Component that embeds Altair/Vega visuals
 * @param {Object} props
 * @param {Object} props.spec - An embeddable Vega item
 * @param {string} props.content_uuid - The id of the div to create and render to
 * @param {string[]} props.external_js_dependencies - The JS dependencies for VegaContent
 * @param {string[]} props.external_css_dependencies - The CSS dependencies for VegaContent
 */
function VegaContent({
  spec,
  content_uuid,
  external_js_dependencies,
  external_css_dependencies,
}) {
  const divRef = useRef(null);
  const ready = useDependencies({
    componentName: "VegaContent",
    jsDependencies: external_js_dependencies,
    cssDependencies: external_css_dependencies,
  });

  useEffect(() => {
    if (divRef.current && content_uuid && ready) {
      spec.config.width = "container";
      spec.config.height = "container";
      window.vegaEmbed("#".concat(content_uuid), spec).catch(console.error);
    }
  }, [divRef, content_uuid, ready, spec]);
  return html`<div id="${content_uuid}" ref="${divRef}" />`;
}

dictComponent.MarkdownText = MarkdownText;
/**
 * A Component that embeds Bokeh visuals
 * @param {Object} props
 * @param {string} props.text - Some markdown text
 */
export function MarkdownText({ text }) {
  const divRef = useRef(null);
  useEffect(() => {
    if (window.snarkdown && divRef.current) {
      divRef.current.innerHTML = window.snarkdown(text);
    }
  }, [text]);

  return html`<div ref="${divRef}" />`;
}

function SVGContainer({ data }) {
  const divRef = useRef(null);

  useEffect(() => {
    if (divRef.current) {
      divRef.current.innerHTML = data;
    }
  }, [data]);

  return html`<div ref="${divRef}" />`;
}

dictComponent.TableContent = TableContent;
/**
 * A Component that embeds tabular data with tabulator
 * @param {Object} props
 * @param {Object[]} props.columns - Columns of data
 * @param {string} props.content_uuid - The id of the div to create and render to
 * @param {string[]} props.external_js_dependencies - The JS dependencies for tabulator
 * @param {string[]} props.external_css_dependencies - The CSS dependencies for tabulator
 */
function TableContent({
  data,
  columns,
  content_uuid,
  external_js_dependencies,
  external_css_dependencies,
}) {
  const tableRef = useRef(null);
  const ready = useDependencies({
    componentName: "TableContent",
    jsDependencies: external_js_dependencies,
    cssDependencies: external_css_dependencies,
  });

  useEffect(() => {
    if (tableRef.current && content_uuid && ready) {
      new window.Tabulator(`#${content_uuid}`, {
        data: data.map((d, i) => ({ id: i, ...d })),
        columns: columns.map((c) => ({ field: c, title: c })),
        layout: "fitColumns",
        height: "30vh",
      });
    }
  }, [tableRef, content_uuid, ready, columns, data]);

  return html`<div ref=${tableRef} id="${content_uuid}"></div>`;
}

dictComponent.SVGContent = SVGContent;
function SVGContent({ data }) {
  return html`<${SVGContainer} data="${data}" />`;
}

dictComponent.CodeContent = CodeContent;
function CodeContent({
  external_js_dependencies,
  external_css_dependencies,
  code,
  language,
}) {
  console.log({
    external_js_dependencies,
    external_css_dependencies,
    code,
    language,
  });
  const ready = useDependencies({
    componentName: "CodeContent",
    jsDependencies: external_js_dependencies,
    cssDependencies: external_css_dependencies,
  });
  const codeRef = useRef(null);
  useEffect(() => {
    if (codeRef.current) {
      window.hljs.highlightBlock(codeRef.current);
    }
  });
  if (ready) {
    return html`<pre><code ref=${codeRef} class="language-${language}">${code}</code></pre>`;
  }
}

dictComponent.LatexContent = LatexContent;
function LatexContent({
  external_js_dependencies,
  external_css_dependencies,
  text,
}) {
  const ready = useDependencies({
    componentName: "LatexContent",
    jsDependencies: external_js_dependencies,
    cssDependencies: external_css_dependencies,
  });
  if (ready) {
    customElements.define("latex-js", window.latexjs.LaTeXJSComponent);
    return html`<latex-js baseURL="https://cdn.jsdelivr.net/npm/latex.js/dist/"
      >${text}</latex-js
    >`;
  }
}
dictComponent.MathJaxContent = MathJaxContent;
function MathJaxContent({
  external_js_dependencies,
  external_css_dependencies,
  text,
}) {
  const ready = useDependencies({
    componentName: "MathJaxContent",
    jsDependencies: external_js_dependencies,
    cssDependencies: external_css_dependencies,
  });
  const mathJaxRef = useRef(null);
  useEffect(() => {
    if (ready && window.MathJax) {
      window.MathJax.typeset(() => mathJaxRef.current);
    }
  });
  return html`<div ref=${mathJaxRef}>${text}</MathJax-js>`;
}

dictComponent.FallbackContent = FallbackContent;
function FallbackContent({ detected_type }) {
  return html`<p class="vz-text">Unknown content type "${detected_type}"</p>`;
}

function VZCustomComponent({ component, spec }) {
  console.log("Preparing to render custom component:", component);
  const {
    component_module,
    external_js_dependencies,
    external_css_dependencies,
    ...args
  } = spec;
  const ready = useDependencies({
    componentName: component,
    jsDependencies: [...external_js_dependencies, component_module],
    cssDependencies: external_css_dependencies,
  });
  return ready
    ? html`<${window[component]} ...${args} />`
    : html`<p class="vz-text">
        Could not resolve custom component ${component} from module
        ${component_module}
      </p>`;
}

export function WidgetContent({ content }) {
  const { component, ...spec } = content;
  return html` <div class="vz-widget-content">
    ${dictComponent[component]
      ? html`<${dictComponent[component]} ...${spec} />`
      : spec.component_module
      ? html`<${VZCustomComponent} component=${component} spec=${spec} />`
      : html`<p class="vz-text">Component has no renderable content.</p>`}
  </div>`;
}
