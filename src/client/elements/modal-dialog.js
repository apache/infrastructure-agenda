import React, { forwardRef} from "react";

//
// Bootstrap modal dialogs are great, but they require a lot of boilerplate.
// This component provides the boiler plate so that other form components
// don't have to.  The elements provided by the calling component are
// distributed to header, body, and footer sections.
//
function ModalDialog(props, ref) {
  let header = [];
  let body = [];
  let footer = [];

  let children = React.Children.toArray(props.children);
  while (children.length === 1 && typeof children[0].type !== 'string') {
    children = React.Children.toArray(children[0].props.children);
  }

  for (let child of children) {
    if (child.type === "h4") {
      // place h4 elements into the header, adding a modal-title class
      child = addClass(child, "modal-title");
      header.push(child);
      ModalDialog.h4 = child
    } else if (child.type === "button") {
      // place button elements into the footer, adding a btn class
      child = addClass(child, "btn");
      footer.push(child)
    } else if (child.type === "input" || child.type === "textarea") {
      // wrap input and textarea elements in a form-control,
      // add label if present
      child = addClass(child, "form-control");
      let label = null;

      if (child.props.label && child.props.id) {
        let props = { htmlFor: child.props.id };

        if (child.props.type === "checkbox") {
          props = { ...child.props, ...props, className: 'checkbox' }
          child = React.createElement("label", props, child, child.props.label);
          label = null
        } else {
          label = React.createElement("label", props, child.props.label);
          child = React.cloneElement(child, { label: null })
        }
      };

      body.push(React.createElement(
        "div",
        { className: "form-group", key: child?.props?.id || child?.props?.name },
        label,
        child
      ))
    } else {
      // place all other elements into the body
      body.push(child)
    }
  };

  return <div ref={ref} className={"fade modal " + props.className} id={props.id}>
    <div className="modal-dialog">
      <div className="modal-content">
        <div className={"modal-header " + props.color}>
          <button className="close" type="button" data-dismiss="modal">×</button>
          {header}
        </div>

        <div className="modal-body">{body}</div>
        <div className={"modal-footer " + props.color}>{footer}</div>
      </div>
    </div>
  </div>
}

// helper method: add a class to an element, returning new element
function addClass(element, name) {
  if (!element.props.className) {
    element = React.cloneElement(element, { className: name })
  } else if (!element.props.className.split(" ").includes(name)) {
    element = React.cloneElement(
      element,
      { className: `${element.props.className} ${name}` }
    )
  };

  return element
}

export default forwardRef(ModalDialog);
