

import { createMachine } from 'xstate';


let machine =
    /** @xstate-layout N4IgpgJg5mDOIC5QGMCGA7Abq2A6AohAJYAuAsgPYRgDEl1AwgBYYwC0lmYAChUeiXhIQABwqxSRCukSgAHojYBGAOy4ALCvUA2AAwBOHbqWrdAZhUAaEAE9EAJm1LcAVnUAOe7rcr3L-Sr6AL5B1mhYOATE5FS09GDMrGBsAIIQELz8grKi4pLSOQoIbPbquhrqpV4uLipKZpXa1nYIjs5unmZm+iZK9i5mIWEY2HgAMmAAZjEArrBguACqIjQAthRzkBQA7jLCYhIkUnvyiGW4DdraLtr2gQNduk22ivUuuPruZu76T9r6Zhu2iGIHCo1wE2mlE2uAAIjt0GsNvMZiIcgd8icQEV7P0NN11C57L9zGZcepmq9AR8vj8-gCgSCwZFIbN5nCEUjNhsSOi8kcCsIipcNAF7H5dLp7GTni1lNTPt9flcGdd3EyRpFofNeIdjrgAPIzEgMTWwLnzfh8vWC07FfruXD2JS6Sp3YzaFRmWVU9ROgx3PxmPpezQaiJ4bU8fn6g1cABOpojFrAPOtmMKrzxZSUyqlRK8KisL2K9T9Xn0gYGIYaKhCoRA6FiQhQZqipHiuDSGT4AhbuRtWKKJUquFd6nqFfqru8lIQj1cPx+-iUHlqNXD4MIHdiuE40ay-YxAqHiG+Fx0Zl0gVK2gnNTnC5cS89HmlV6Um8i25i1HTJ8ze0rjHdQJzJAxpzKFw51UbRXBUbQvgdLxzAQr9ximNkFmWf9jkApQ3AudwTFQskXCUTwfXtPpcH+MliRdXFiPQiFMKjDldlw21sQcJQ4OJdxPH0Qx6mIjw530XAVGMaUXGvYiqk9FjWSjLjTwQPiLyuG47n0B4ryoko-Fou9akBK5ayuFio11TFDWNJNRjUwCSmJD4r2daSfi6YN3DnEoXQ+CjnyDPjpPUazkWjQdDQTRycGcoVFHfVxvWE-5b3k+x-KcJ0vk9cU6jJUCXEizZbIA-YY244dxXsJ0XTdaSwu9fzxTMXBBPS1c6tM9DErtNgDIa11cWaz1WpLIbn1owEem6RDbjDesgA */
    createMachine({
        tsTypes: {} as import("./index.typegen").Typegen0,
        type: "parallel",
        states: {
            EditMode: {
                initial: "AddPoints",
                states: {
                    AddPoints: {},
                    MovePoints: {},
                },
                on: {
                    "ModeChange-MovePoints": {
                        target: ".MovePoints",
                    },
                    "ModeChange-AddPoints": {
                        target: ".AddPoints",
                    },
                },
            },
            LeftMouse: {
                initial: "Up",
                states: {
                    Up: {
                        on: {
                            mousedown: {
                                cond: "InStateOverCanvas",
                                target: "Down",
                            },
                        },
                    },
                    Down: {
                        on: {
                            mouseup: {
                                target: "Up",
                            },
                            mouseout: {
                                target: "Up",
                            },
                        },
                    },
                },
            },
            MousePosition: {
                initial: "OutCanvas",
                states: {
                    OutCanvas: {
                        on: {
                            mousein: {
                                target: "OverCanvas",
                            },
                        },
                    },
                    OverCanvas: {
                        on: {
                            mouseout: {
                                target: "OutCanvas",
                            },
                        },
                    },
                },
            },
        },
        id: "canvas",
    },
    {
        guards:{
            InStateOverCanvas: (context, event) => {
                return false;
            }
        }
    }
);


type Point = [number, number];

let canvas: HTMLCanvasElement = document.getElementById("maincanvas") as HTMLCanvasElement;
let ctx = canvas.getContext("2d");
let points: Point[] = [];
let dragging: number | undefined = undefined;


function obtain_canvas_mouse_coordinates(event: MouseEvent): Point {
    let rect = canvas.getBoundingClientRect();
    return [event.clientX - rect.left, event.clientY - rect.top];
}


canvas.addEventListener("mousedown", function (e) {
    let mode = (document.querySelector('[name=mode]:checked') as HTMLInputElement).value;
    let coord = obtain_canvas_mouse_coordinates(e)
    let index = hit_test_point(coord);
    switch (mode) {
        case "draw":
            add_point(coord);
            draw();
            break
        case "move":
            if (index != -1) {
                dragging = index;
            }
        case "delete":
            if (index != -1) {
                points.splice(index, 1);
                draw();
            }
            break
    }
});

canvas.addEventListener("mousemove", function (e) {
    if (dragging) {
        let coord = obtain_canvas_mouse_coordinates(e);
        points[dragging] = coord;
        draw();
    }
});


function hit_test_point([cx, cy]: [number, number]) {
    for (let i = 0; i < points.length; i++) {
        let [px, py] = points[i];
        if (Math.abs(px - cx) + Math.abs(py - cy) < 5) {
            return i
        }
    }
    return -1;
}

function hit_test_edge([px, py]: Point) {
    for (let i = 0; i < points.length - 1; i++) {
        let [ax, ay] = points[i];
        let [bx, by] = points[i + 1];
        let [cx, cy] = project_point_onto_line([ax, ay], [bx, by], [px, py]);

    }
}
function project_point_onto_line([ax, ay]: Point, [bx, by]: Point, [px, py]: Point) {
    let [abx, aby] = [bx - ax, by - ay];
    let [apx, apy] = [px - ax, py - ay];

    let t = (abx * apx + aby * apy) / (abx * abx + aby * aby);
    return [ax + t * abx, ay + t * aby];
}

function distance_between_points([ax, ay]: Point, [bx, by]: Point): number {
    return Math.sqrt((ax - bx) * (ax - bx) + (ay - by) * (ay - by));
}

function add_point([x, y]: Point) {
    if (points.length > 0) {
        let [lastx, lasty] = points[points.length - 1];
        if (distance_between_points([lastx, lasty], [x, y]) < 5) {
            return;
        }
    }
    points.push([x, y]);
}

function draw() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    ctx.beginPath();
    for (let [x, y] of points) {
        ctx.lineTo(x, y);
    }
    ctx.stroke();

    for (let [x, y] of points) {
        ctx.beginPath();
        ctx.arc(x, y, 5, 0, 2 * Math.PI);
        ctx.fill();
    }
}