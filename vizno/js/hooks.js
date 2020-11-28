const { useEffect, useRef, useContext, createContext } = window.htmPreact;

export const DependencyLoader = createContext({});

/**
 * @param {Object} props
 * @param {string} props.componentName
 * @param {string[]} props.jsDependencies
 * @param {string[]} props.cssDependencies
 */
export function useDependencies({
  componentName,
  jsDependencies,
  cssDependencies,
}) {
  const dependencyContext = useContext(DependencyLoader);
  const readyJSRef = useRef(jsDependencies.length == 0);
  const readyCSSRef = useRef(cssDependencies.length == 0);

  useEffect(() => {
    if (
      dependencyContext.canRender[componentName] !== true &&
      dependencyContext.isLoadingDependencies.current[componentName] !== true
    ) {
      dependencyContext.isLoadingDependencies.current = {
        ...dependencyContext.isLoadingDependencies.current,
        [componentName]: true,
      };
      jsDependencies.forEach((src, i) => {
        const script = document.createElement("script");
        script.src = src;
        script.type = "text/javascript";
        script.async = false;
        script.onload = () => {
          if (i == jsDependencies.length - 1) {
            if (readyCSSRef.current) {
              dependencyContext.setCanRender((prevState) => ({
                ...prevState,
                [componentName]: true,
              }));
            }
            readyJSRef.current = true;
          }
        };
        document.head.appendChild(script);
      });
      cssDependencies.forEach((src, i) => {
        const link = document.createElement("link");
        link.href = src;
        link.rel = "stylesheet";
        link.async = false;
        link.onload = () => {
          if (i == cssDependencies.length - 1) {
            if (readyJSRef.current) {
              dependencyContext.setCanRender((prevState) => ({
                ...prevState,
                [componentName]: true,
              }));
            }
            readyCSSRef.current = true;
          }
        };
        document.head.appendChild(link);
      });
    }
  }, [componentName, cssDependencies, dependencyContext, jsDependencies]);
  return dependencyContext.canRender[componentName];
}
