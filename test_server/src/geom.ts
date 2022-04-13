

export class Vector {
    x:number;
    y:number;
    constructor(x:number, y:number) {
        this.x = x;
        this.y = y;
    }
    add(v:Vector) {
        return new Vector(this.x + v.x, this.y + v.y);
    }  
    sub(v:Vector) {
        return new Vector(this.x - v.x, this.y - v.y);
    }
    mul(s:number) {
        return new Vector(this.x * s, this.y * s);
    }
    div(s:number) {
        return new Vector(this.x / s, this.y / s);
    }
    dot(v:Vector) {
        return this.x * v.x + this.y * v.y;
    }
    /**
     * Magnitude
     * @returns {number}
     */
    mag() {
        return Math.sqrt(this.x * this.x + this.y * this.y);
    }

    /**
     * Magnitude Squared
     * @returns {number}
     */
    magsq() {
        return this.x * this.x + this.y * this.y;
    }

    unit() {
        let mag = Math.sqrt(this.x * this.x + this.y * this.y);
        return new Vector(this.x/mag, this.y/mag);
    }
}


export function project_point_onto_line(a: Vector, b:Vector, p:Vector) {
    let ab = b.sub(a);
    let ap = p.sub(a);
    let t = ab.dot(ap) / ab.magsq();
    return a.add(ab.mul(t));
}

export function project_point_onto_segment(a: Vector, b:Vector, p:Vector) {
    let ab = b.sub(a);
    let ap = p.sub(a);
    let t = ab.dot(ap) / ab.magsq();
    if (t < 0) {
        return a;
    }
    if (t > 1) {
        return b;
    }
    return a.add(ab.mul(t));
}


export function hit_test_point(points:Vector[], point:Vector, tolerance:number=5) {
    let tolerance_sq = tolerance * tolerance;
    return points.findIndex(p=>p.sub(point).magsq()<tolerance_sq);
}

export function hit_test_edge(points:Vector[], point:Vector, tolerance:number=3) {
    let tolerance_sq = tolerance * tolerance;
    for (let i = 0; i < points.length - 1; i++) {
         let a = points[i];
         let b = points[i + 1];
         let c = project_point_onto_segment(a,b,point);

         if(c.sub(point).magsq() < tolerance_sq) {
             return i;
         }
    }
    return -1;
}


