import './style.css'
import htmx from 'htmx.org'
import alpine from 'alpinejs'
import { themeStore } from './stores/theme.ts'

declare global {
  interface Window {
    alpine: typeof alpine
    htmx: typeof htmx
  }
}

window.htmx = htmx
window.alpine = alpine

alpine.store('theme', themeStore)

alpine.start()
