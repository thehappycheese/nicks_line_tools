import { assign, createMachine, spawn, send, sendParent, ContextFrom, EventFrom } from 'xstate';
import { createModel } from 'xstate/lib/model';
import { hit_test_edge, hit_test_point, Vector } from './geom';

// export type MouseState = {
//     position: Vector,
//     left_button_down: boolean,
//     index_point: number,
//     index_edge: number
// }

export type ModelContextType = {
    points: Vector[],
    active_item?: {
        type: "point" | "edge", index: number
    }
    drag_origin: {
        origin: Vector,
        unmodified_points: Vector[],
    }
}

let initial_context: ModelContextType = {
    points: [new Vector(100, 100), new Vector(200, 100), new Vector(200, 200), new Vector(100, 200)],
    drag_origin: {
        origin: new Vector(0, 0),
        unmodified_points: []
    }
}

export let model = createModel(
    initial_context,
    {
        events: {
            mousedown: (position: Vector) => ({ position }),
            mouseup: (position: Vector) => ({ position }),
            mousemove: (position: Vector) => ({ position }),
            mouseleave: (position: Vector) => ({ position }),
            mouseenter: (position: Vector) => ({ position }),

            mode_add: () => ({}),
            mode_move: () => ({}),
            mode_remove: () => ({}),

            endmode: () => ({}),
        }
    }
);



export type ModelEventType = EventFrom<typeof model>;


export let machine =
    /** @xstate-layout N4IgpgJg5mDOIC5QFsD2A3MB9ADqglgHYAusAdGpmRAE4CGUAxGgK6xiViKh6z7H5UhbiAAeiAKwSADGQDsARjkSALAukAOAJwBmaVoBMAGhABPRAFoV0ufIMKNGlQeVa5ANhUqAvt5OdcAhJyTmp6JlZ2ABswOkwRXn5BYSQxRA13MncnfR0NOR0VGV0TcwQLCR0JMgMvItU9Ax13LV9-DGw8IlIKDrCGZlQ2MBYcBNQ+ASERcQQXHTJrFSqtdwUJN2kq0ss8jRrmgwNpAw1pIt0JNpAAruDeqgALDppB4YhUAHcUngmk6dSsw0CjI0hsJxU+R0Wk0O3KBjcZD0Cj2CgUkJ0hXc11uQR6oWemFekQ4HXGk2SM0sR3kChaeU0mkMTjhVhsdgUMM8rjW2L8Nw6gW65DoEAgZEJYGJQ3YH2+5P+PzSCDRchUZEcci0Ug0Ok5RRUrJkmW1OgMEnsOi1LgUOMFdx6ovFkulw04CqmSqBdKyyg0tTVfpU7iNBkyy20FvRDmOtv5uOFZCd-QiMtJ8VSiU9VJV2VkLiOWjUMPReVZezIlWs6KKTnsUjtmCF92TtAGJNGHspgMQ6PNi307myBTN0OMZksEmBle0dLkcjOurkjc6eJFYpTb2isQzvwpANAs3RurIWgyWpOWhRR0NE-KqlkziUwNjVp88fta7INHTYAlLy3X8uwPZULhqCRsj2LZtA8OF1H2NENBkTljkKCEV2bHofwJACSTlJUs27Q90jDUFznUI5wXcKc4PZfQn0g5o9SHDCHVgQYIGwd1Mz+bMezmf0Z2UdxajDc5zVZORjlPETgQ8CChzjdomzYjjsCdYCvV7AtKxUbUVCk6jIIkVlsi0DUJE5aC1U0ETWLXNSsGwskeP3LSEGyfYpOcLwzy1TwFFM7QLKsvIbIyAxfH5QhUE4+BUgTe5QjbKBNJzaFqkcaQUTpTxrAkORyyLeRqwcJxPEjezExwok0v4lFZE8WoRPODZ3E0DQivVGzEPKyEiyuD8VK-bi90VHMrEyRR6UXJlTiKUzNBqdZgXatUiiUKqWw3F06uIlVssa5QNhsYsXyNFFFgKpQ6TpQozS2x0NxSvblXWPJFl0NVdBsJQdHLZRKwtWpdCcFFlmXIbV0TDTXPG-jrV9KcAwMqdg1M1RK3ayEMS8ArIqhzDyGcp4Xle2YmrIdEz3sfJqP9QK7wUewqbBPVlGkY15w0R7iaAuG+P25ZqnNSCsryNwQzvQoqaORw3GOTxCkh5ToeCcnLDkWRptBxltFOEy7wsM5ql0NRlYol8ou8IA */
    model.createMachine({
  context: model.initialContext,
  on: {
    mode_move: {
      target: ".move",
    },
    mode_add: {
      target: ".add",
    },
    mode_remove: {
      target: ".remove",
    },
  },
  initial: "move",
  states: {
    move: {
      initial: "hover",
      states: {
        drag: {
          on: {
            mousemove: {
              actions: "move_active_item",
            },
            mouseleave: {
              actions: "restore_unmodified_points",
              target: "hover",
            },
            mouseup: {
              target: "hover",
            },
          },
        },
        hover: {
          on: {
            mousedown: {
              actions: "set_drag_origin",
              cond: "have_active_item",
              target: "drag",
            },
            mousemove: {
              actions: "set_active_item",
            },
          },
        },
      },
    },
    add: {
      initial: "hover",
      states: {
        hover: {
          on: {
            mousedown: [
              {
                actions: "set_drag_origin",
                cond: "have_active_point",
                target: "drag",
              },
              {
                actions: [
                  "create_point_on_edge",
                  "set_active_item",
                  "set_drag_origin",
                ],
                cond: "have_active_edge",
                target: "drag",
              },
              {
                actions: [
                  "create_isolated_point",
                  "set_active_item",
                  "set_drag_origin",
                ],
                target: "drag",
              },
            ],
            mousemove: {
              actions: "set_active_item",
            },
          },
        },
        drag: {
          on: {
            mousemove: {
              actions: "move_active_item",
            },
            mouseup: {
              target: "hover",
            },
            mouseleave: {
              actions: "restore_unmodified_points",
              target: "hover",
            },
          },
        },
      },
    },
    remove: {
      initial: "hover",
      states: {
        hover: {
          on: {
            mousemove: {
              actions: "set_active_item",
            },
            mousedown: {
              actions: "remove_active_point",
              cond: "have_active_point",
            },
          },
        },
      },
    },
  },
  id: "move_points",
}, {
        actions: {
            set_active_item: model.assign({
                active_item: (context, event, s) => {
                    if ("position" in event) {
                        let point_index = hit_test_point(context.points, event.position, 5);
                        if (point_index > -1) {
                            return { type: "point", index: point_index };
                        }
                        let edge_index = hit_test_edge(context.points, event.position, 5);
                        if (edge_index > -1) {
                            return { type: "edge", index: edge_index };
                        }
                    } else {
                        throw new Error("set_active_item: no position in event");
                    }
                    return undefined
                }
            }),
            set_drag_origin: model.assign({
                drag_origin: (context, event) => {
                    if ("position" in event) {
                        return {
                            origin: event.position,
                            unmodified_points: [...context.points],
                        };
                    } else {
                        throw new Error("set_drag_origin: no position in event");
                    }
                }
            }),
            move_active_item: model.assign({
                points: (context, event) => {
                    if ("position" in event) {
                        let new_points = [...context.drag_origin.unmodified_points];
                        let drag_offset = event.position.sub(context.drag_origin.origin);
                        if (context.active_item.type == "point") {
                            new_points[context.active_item.index] = new_points[context.active_item.index].add(drag_offset);
                        } else if (context.active_item.type == "edge") {
                            new_points[context.active_item.index] = new_points[context.active_item.index].add(drag_offset);
                            new_points[context.active_item.index + 1] = new_points[context.active_item.index + 1].add(drag_offset);
                        }
                        return new_points;
                    } else {
                        throw new Error("move_active_item: no position in event");
                    }
                }
            }),
            restore_unmodified_points: model.assign({
                points: (context, event) => {
                    return context.drag_origin.unmodified_points;
                }
            }),
            clear_unmodified_points: model.assign({
                drag_origin: undefined
            }),
            remove_active_point: model.assign({
                points: (context, event) => {
                    let new_points = [...context.points];
                    new_points.splice(context.active_item.index, 1);
                    return new_points;
                }
            }),
            create_isolated_point: model.assign({
                points: (context, event) => {
                    let new_points = [...context.points];
                    if("position" in event)
                        new_points.push(event.position);
                    return new_points;
                }
            }),
            create_point_on_edge: model.assign({
                points: (context, event) => {
                    let new_points = [...context.points];
                    if("position" in event)
                        new_points.splice(context.active_item.index + 1, 0, event.position);
                    return new_points;
                }
            }),

        },
        guards: {
            have_active_item: (context: ModelContextType, event: any) => context.active_item !== undefined,
            have_active_point: (context: ModelContextType, event: any) => context?.active_item?.type === "point",
            have_active_edge: (context: ModelContextType, event: any) => context?.active_item?.type === "edge",

        },

    });

