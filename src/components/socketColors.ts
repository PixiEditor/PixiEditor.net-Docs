import { z } from "astro/zod";

export const SocketTypeSchema = z.enum([
  "Texture",
  "Filter",
  "Boolean",
  "Float",
  "Double",
  "Color",
  "Paintable",
  "Painter",
  "VecD",
  "Vec3D",
  "VecI",
  "Integer",
  "String",
  "Ellipse Data",
  "Points Data",
  "Text Data",
  "Vector Shape",
  "Matrix3x3",
  "Default",
] as const);

export type SocketType = z.infer<typeof SocketTypeSchema>;

export const socketColors: Record<SocketType, string> = {
  Texture: "#99c47a",
  Filter: "#cc5c5c",
  Boolean: "#68abdf",
  Float: "#ffc66d",
  Double: "#eea55c",
  Color: "#8cf2dd",
  Paintable: "#48b099",
  Painter: "#ff8c00",
  VecD: "#c984ca",
  Vec3D: "#597513",
  VecI: "#c9b4ca",
  Integer: "#4c64b1",
  String: "#C9E4C6",
  "Ellipse Data": "#a473a5",
  "Points Data": "#e1d0e1",
  "Text Data": "#f2f2f2",
  "Vector Shape": "conic-gradient(#a473a5 0% 33%, #f2f2f2 33% 66%, #e1d0e1 66% 100%)",
  Matrix3x3: "#ffea4f",
  Default: "#ff00ff"
};