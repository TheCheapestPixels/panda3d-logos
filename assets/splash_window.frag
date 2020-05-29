#version 110

uniform sampler2D background;
uniform float fade;
varying vec2 v_clipTexCoord;


void main () {
  vec4 pixel = texture2D(background, v_clipTexCoord * gl_FragCoord.w);
  gl_FragColor = pixel * (1.0 - fade);
}
