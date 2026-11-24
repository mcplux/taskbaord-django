import createClient, { type Middleware } from 'openapi-fetch'
import type { paths } from './schema'

const SAFE_METHODS = new Set(['GET', 'HEAD', 'OPTIONS', 'TRACE'])

const readCsrf = (): string => {
  const el = document.querySelector<HTMLMetaElement>('meta[name=csrf-token]')
  const content = el?.content
  if (!content) {
    throw new Error('Missing <meta name="csrf-token"> in the dashboard template')
  }
  return content
}

const csrfMiddleware: Middleware = {
  onRequest({ request }) {
    if (!SAFE_METHODS.has(request.method)) {
      request.headers.set('X-CSRFToken', readCsrf())
    }
    return request
  },
}

export const api = createClient<paths>({
  baseUrl: window.location.origin,
  credentials: 'same-origin',
})

api.use(csrfMiddleware)
