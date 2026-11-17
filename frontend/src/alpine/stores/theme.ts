export type ThemeMode = 'light' | 'dark' | 'system'
const STORAGE_KEY = 'theme'
const MODES: ThemeMode[] = ['light', 'dark', 'system']
const media = window.matchMedia('(prefers-color-scheme: dark)')

const readLocalStorage = (): ThemeMode => {
  try {
    const v = localStorage.getItem(STORAGE_KEY)
    if (v === 'light' || v === 'dark' || v === 'system') return v
  } catch {}
  return 'system'
}

export interface ThemeStore {
  mode: ThemeMode
  systemDark: boolean
  readonly isDark: boolean
  init(): void
  set(mode: ThemeMode): void
  cycle(): void
  apply(): void
}

export const themeStore: ThemeStore = {
  mode: readLocalStorage(),
  systemDark: media.matches,
  get isDark() {
    return this.mode === 'dark' || (this.mode === 'system' && this.systemDark)
  },
  init() {
    this.apply()

    media.addEventListener('change', (e) => {
      this.systemDark = e.matches
      this.apply()
    })

    window.addEventListener('storage', (e) => {
      if (e.key === STORAGE_KEY || e.key === null) {
        this.mode = readLocalStorage()
        this.apply()
      }
    })
  },

  set(mode) {
    this.mode = mode
    try {
      localStorage.setItem(STORAGE_KEY, mode)
    } catch {}
    this.apply()
  },

  cycle() {
    this.set(MODES[(MODES.indexOf(this.mode) + 1) % MODES.length])
  },

  apply() {
    const root = document.documentElement
    root.classList.toggle('dark', this.isDark)
  },
}
