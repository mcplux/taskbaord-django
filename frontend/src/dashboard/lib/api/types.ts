import type { components } from './schema'

type Schemas = components['schemas']

export type User = Schemas['UserOut']

export type Task = Schemas['TaskOut']
export type TaskPriority = Schemas['TaskPriority']
export type TaskStatus = Schemas['TaskStatus']
export type TaskIn = Schemas['TaskIn']
export type TaskPatch = Schemas['TaskPatch']
