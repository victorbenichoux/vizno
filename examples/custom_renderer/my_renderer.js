function MyCustomComponent({ parameter }) {
  console.log("I am rendering my custom component", parameter);
  return html`<p>This is my super custom component, the parameter is: ${parameter}</p>`;
}
