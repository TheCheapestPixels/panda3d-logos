#version 110

uniform mat4 p3d_ModelViewProjectionMatrix;
attribute vec4 vertex;
attribute vec2 p3d_MultiTexCoord0;

varying vec2 v_clipTexCoord;


void main()  {
  gl_Position = p3d_ModelViewProjectionMatrix * vertex;
  v_clipTexCoord = 0.5 * gl_Position.xy + vec2(0.5 * gl_Position.w);
}
