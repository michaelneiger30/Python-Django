// Assumes the following uniforms exist in the surrounding context:
// uniform vec2 frame_shape;
// uniform float focal_distance;
// uniform float is_fixed_in_frame;

const vec2 DEFAULT_FRAME_SHAPE = vec2(8 * 16 / 9, 8);

vec4 get_gl_Position(vec3 point){
    vec4 result = vec4(point, 1);
    if(!bool(is_fixed_in_frame)){
        result.x *= 2 / frame_shape.x;
        result.y *= 2 / frame_shape.y;
        result.z /= focal_distance;
        result.xy /= max(1 - point.z, 0);
        // Todo, does this discontinuity add weirdness?  Theoretically, by this point,
        // the z-coordiante of gl_Position only matter for z-indexing.  The reason
        // for thie line is to avoid agressive clipping of distant points.
        if(result.z < 0) result.z *= 0.1;
    } else{
        result.x *= 2 / DEFAULT_FRAME_SHAPE.x;
        result.y *= 2 / DEFAULT_FRAME_SHAPE.y;
    }
    return result;
}