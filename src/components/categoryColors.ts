import { z } from "astro/zod";

export const CategorySchema = z.enum([
  "Image",
  "Structure",
  "Filters",
  "Shape",
  "Numbers",
  "Color",
  "Animation",
  "Effects",
  "Matrix",
  "Workspace"
] as const);

export type Category = z.infer<typeof CategorySchema>;

export const categoryColors: Record<Category, string> = {
  Image: "#5B7348",
  Structure: "#735C39",
  Filters: "#733535",
  Shape: "#654266",
  Numbers: "#666666",
  Color: "#3B665D",
  Animation: "#4D4466",
  Effects: "#e36262",
  Matrix: "#9169ff",
  Workspace: "#303030"
};