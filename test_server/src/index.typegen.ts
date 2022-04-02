// This file was automatically generated. Edits will be overwritten

export interface Typegen0 {
  "@@xstate/typegen": true;
  eventsCausingActions: {};
  internalEvents: {
    "xstate.init": { type: "xstate.init" };
  };
  invokeSrcNameMap: {};
  missingImplementations: {
    actions: never;
    services: never;
    guards: never;
    delays: never;
  };
  eventsCausingServices: {};
  eventsCausingGuards: {
    InStateOverCanvas: "mousedown";
  };
  eventsCausingDelays: {};
  matchesStates:
    | "EditMode"
    | "EditMode.AddPoints"
    | "EditMode.MovePoints"
    | "LeftMouse"
    | "LeftMouse.Up"
    | "LeftMouse.Down"
    | "MousePosition"
    | "MousePosition.OutCanvas"
    | "MousePosition.OverCanvas"
    | {
        EditMode?: "AddPoints" | "MovePoints";
        LeftMouse?: "Up" | "Down";
        MousePosition?: "OutCanvas" | "OverCanvas";
      };
  tags: never;
}
