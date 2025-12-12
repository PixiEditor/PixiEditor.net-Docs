import { z } from "astro/zod";
import { SocketTypeSchema } from "./components/socketColors";
import { CategorySchema } from "./components/categoryColors";

const SocketBaseSchema = z.object({
  name: z.string(),
  type: SocketTypeSchema,
  displayType: z.string().optional(),
  typeLink: z.string().optional(),
  min: z.string().optional(),
  max: z.string().optional(),
  hideSocket: z.boolean().optional().default(false),
  isContextful: z.boolean().optional().default(false),
  description: z.string().optional(),
  default: z.unknown().optional(),
});

const InputSchema = SocketBaseSchema;
const OutputSchema = SocketBaseSchema;

const NodeSchema = z.object({
  name: z.string(),
  category: CategorySchema,
  description: z.string(),
  isPair: z.boolean().optional().default(false),
  pairNode: z.string().optional(),
  hasPreview: z.boolean().optional().default(false),
  icon: z.string().optional(),
  inputs: z.array(InputSchema).optional().nullable(),
  outputs: z.array(OutputSchema).optional().nullable(),
});

export const ExtendedSchema = z.object({
  node: NodeSchema.optional(),
});

// Types inferred from schemas
export type SocketBase = z.infer<typeof SocketBaseSchema>;
export type Input = z.infer<typeof InputSchema>;
export type Output = z.infer<typeof OutputSchema>;
export type Node = z.infer<typeof NodeSchema>;
export type Extended = z.infer<typeof ExtendedSchema>;
