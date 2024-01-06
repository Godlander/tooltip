#version 330

#define hex(i) vec4((i&0xFF000000u)>>24,(i&0xFF0000u)>>16,(i&0xFF00u)>>8,(i&0xFFu))/255.

in vec3 Position;
in vec4 Color;

uniform mat4 ModelViewMat;
uniform mat4 ProjMat;

out vec4 vertexColor;
flat out int tooltip;
out vec3 Pos;
out vec3 Pos1;
out vec3 Pos2;
out vec3 Pos3;

const vec2[] corners = vec2[](vec2(1, 1),vec2(1, -1),vec2(-1, -1),vec2(-1, 1));

#moj_import <tooltip.glsl>

void main() {
    Pos = Position;
    vertexColor = Color;
    int corner = gl_VertexID % 4;

    tooltip = 0;
    if (Position.z > 100) {
        tooltip = 1;
        Pos.xy += pad * corners[corner];
        if (gl_VertexID / 4 != 2) Pos = vec3(0);
    }

    Pos1 = Pos2 = Pos3 = vec3(0);
    switch (corner) {
        case 0: Pos1 = vec3(Pos.xy, 1); break;
        case 1: Pos2 = vec3(Pos.xy, 1); break;
        case 2: Pos3 = vec3(Pos.xy, 1); break;
    }

    gl_Position = ProjMat * ModelViewMat * vec4(Pos, 1.0);
}