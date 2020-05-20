#version 100

precision mediump float;
uniform sampler2D p3d_Texture0;
varying vec2 v_texcoord;
uniform float fade;
uniform float time;

void main () {
  // concentric circles
  //   float v = pow(v_texcoord.x - 0.5, 2.0) + pow(v_texcoord.y - 0.5, 2.0);
  // flickering
  //   float v = mod(time * 20.0, 1.0);
  // squarestar
  float v = min(abs(v_texcoord.x - 0.5), abs(v_texcoord.y - 0.5));

  // Scaling and movement
  v = mod(v * 2.0 - time * 5.0, 1.0);

  float phase = mod(v * 6.0, 1.0);
  vec2 phases = vec2(
    phase, // rising
    1.0 - phase // falling
  );

  int section = int(floor(v * 6.0));
  vec4 rgb = vec4(0.0);
  if (section == 0) {rgb = vec4(1.0,      phases.x, 0.0,      0.0);}
  if (section == 1) {rgb = vec4(phases.y, 1.0,      0.0,      0.0);}
  if (section == 2) {rgb = vec4(0.0,      1.0,      phases.x, 0.0);}
  if (section == 3) {rgb = vec4(0.0,      phases.y, 1.0,      0.0);}
  if (section == 4) {rgb = vec4(phases.x, 0.0,      1.0,      0.0);}
  if (section == 5) {rgb = vec4(1.0,      0.0,      phases.y, 0.0);}

  gl_FragColor = rgb * (1.0 - fade);
}
