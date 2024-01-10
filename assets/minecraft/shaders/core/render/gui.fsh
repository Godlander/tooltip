#version 330

#define hex(i) vec4((i&0xFF000000u)>>24,(i&0xFF0000u)>>16,(i&0xFF00u)>>8,(i&0xFFu))/255.

uniform float GameTime;

in vec4 vertexColor;
flat in int tooltip;
in vec3 Pos;
in vec3 Pos1;
in vec3 Pos2;
in vec3 Pos3;

out vec4 fragColor;

#moj_import <tooltip.glsl>

void main() {
    vec4 color = vertexColor;
    float time = GameTime * 1200;

    vec2 p1 = Pos1.xy / Pos1.z;
    vec2 p2 = Pos2.xy / Pos2.z;
    vec2 p3 = Pos3.xy / Pos3.z;
    vec2 pmax = max(max(p1,p2),p3);
    vec2 pmin = min(min(p1,p2),p3);
    vec2 size = vec2(pmax - pmin);

    if (tooltip == 1) {
        if (all(greaterThan(size, vec2(1e3)))) {discard; return;}
        int i = 0;
        ivec4 corner = ivec4(abs(vec4(pmin, pmax) - Pos.xyxy));
        ivec2 side = ivec2(clamp(abs(pmin - Pos.xy) - (size/2.) + (sizes.xy/2), ivec2(0), sizes.xy-1));
        ivec4 edge = ivec4(lessThan(corner, sizes.zzzz));
        switch ((edge.x<<0)+(edge.y<<1)+(edge.z<<2)+(edge.w<<3)) {
            case 1: //left, 0001
                i = (corner.x)           + (side.y)             * sizes.z; color = hex(l[i]); break;
            case 2: //top, 0010
                i = (side.x)             + (corner.y)           * sizes.x; color = hex(t[i]); break;
            case 4: //right, 0100
                i = (sizes.z-corner.z-1) + (side.y)             * sizes.z; color = hex(r[i]); break;
            case 8: //bottom, 1000
                i = (side.x)             + (sizes.z-corner.w-1) * sizes.x; color = hex(b[i]); break;
            case 3: //topleft, 0011
                i = (corner.x)           + (corner.y)           * sizes.z; color = hex(tl[i]); break;
            case 6: //topright, 0110
                i = (sizes.z-corner.z-1) + (corner.y)           * sizes.z; color = hex(tr[i]); break;
            case 9: //botleft, 1001
                i = (corner.x)           + (sizes.z-corner.w-1) * sizes.z; color = hex(bl[i]); break;
            case 12: //botright, 1100
                i = (sizes.z-corner.z-1) + (sizes.z-corner.w-1) * sizes.z; color = hex(br[i]); break;
            default:
                color = hex(base);
        }
    }
    if (color.a == 0) discard;
    fragColor = color;
}
