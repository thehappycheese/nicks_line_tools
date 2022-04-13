
import React, { useEffect } from "react";

import {Vector, project_point_onto_line, hit_test_point, hit_test_edge} from './geom'



import {ModelContextType, model, machine} from './state';
import {useMachine} from '@xstate/react'



function mouse_coordinates_from_event(event:React.MouseEvent<HTMLCanvasElement, MouseEvent>): Vector {
    let rect = (event.target as HTMLCanvasElement).getBoundingClientRect();
    return new Vector(
        event.clientX - rect.left,
        event.clientY - rect.top
    );
}

// function add_point(point: Vector, tolerance: number=5) {
//     if (points.length > 0) {
//         let last = points[points.length - 1];
//         if (last.sub(point).magsq() < tolerance**2) {
//             return;
//         }
//     }
//     points.push(point);
// }



function draw(ctx:CanvasRenderingContext2D, context:ModelContextType) {
    ctx.clearRect(0, 0, ctx.canvas.width, ctx.canvas.height);
    ctx.beginPath();
    for (let {x, y} of context.points) {
        ctx.lineTo(x, y);
    }
    ctx.stroke();

    for (let {x, y} of context.points) {
        ctx.beginPath();
        ctx.arc(x, y, 5, 0, 2 * Math.PI);
        ctx.fill();
    }
    switch(context?.active_item?.type){
        case 'point':
            let {x, y} = context.points[context.active_item.index];
            ctx.fillStyle = "red"
            ctx.beginPath();
            ctx.arc(x, y, 5, 0, 2 * Math.PI);
            ctx.fill();
            ctx.fillStyle = "black"
            break
        case 'edge':
            let {x:x1,y:y1} = context.points[context.active_item.index];
            let {x:x2,y:y2} = context.points[context.active_item.index+1];
            ctx.strokeStyle="red";
            ctx.beginPath();
            ctx.moveTo(x1,y1);
            ctx.lineTo(x2,y2);
            ctx.stroke();
            ctx.strokeStyle="black";
            break
    }

}


function send_mouse_event(
        send:  Function,
        event:any,
        e:React.MouseEvent<HTMLCanvasElement, MouseEvent>,
        ctx:CanvasRenderingContext2D
    ) {
    let position = mouse_coordinates_from_event(e);
    let state = send(event(position));
    draw(ctx, state.context);
}

export function App() {
    let ref_canvas = React.useRef<HTMLCanvasElement>(null);
    let ref_ctx = React.useRef<CanvasRenderingContext2D>(null);
    let [state, send] = useMachine(machine);
    useEffect(()=>{
        ref_ctx.current = ref_canvas.current.getContext("2d");
    }, [ref_canvas])

    useEffect(()=>{
        draw(ref_ctx.current, state.context);
    },[state.context]);


    return <>
        <div id="leftbar">
            <div id="react-root"></div>
            <h3>Mode</h3>
            {
            state.nextEvents.map(event=>{
                return <button onClick={()=>send({type:event as any})}>{event}</button>
            })
            }
            {/* <button 
                onClick={()=>{
                    send(model.events.mode_add())
                }}
                disabled={!state.can("mode_add")}
            >
                Add
            </button> */}
            <pre id="tempout">
                {JSON.stringify(state.context, null, 2)}
            </pre>
            <pre id="tempout">
                {JSON.stringify(state.nextEvents, null, 2)}
            </pre>
        </div>
        <div id="mainbar">
            <canvas 
                ref={ref_canvas}
                id="maincanvas"
                width="1600"
                height="900"
                onMouseDown ={ e=> send_mouse_event(send, model.events.mousedown,  e, ref_ctx.current)}
                onMouseUp   ={ e=> send_mouse_event(send, model.events.mouseup,    e, ref_ctx.current)}
                onMouseMove ={ e=> send_mouse_event(send, model.events.mousemove,  e, ref_ctx.current)}
                onMouseEnter={ e=> send_mouse_event(send, model.events.mouseenter, e, ref_ctx.current)}
                onMouseLeave={ e=> send_mouse_event(send, model.events.mouseleave, e, ref_ctx.current)}
            ></canvas>
        </div>
    </>
}