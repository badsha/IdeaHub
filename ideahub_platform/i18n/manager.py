import i18n
import os
from typing import Optional, Dict, Any
from pathlib import Path

class I18nManager:
    """Internationalization manager for the application."""
    
    def __init__(self, locale_dir: str = "locales", default_locale: str = "en"):
        self.locale_dir = Path(locale_dir)
        self.default_locale = default_locale
        self._setup_i18n()
    
    def _setup_i18n(self):
        """Setup the i18n configuration."""
        # Ensure locale directory exists
        self.locale_dir.mkdir(exist_ok=True)
        
        # Configure i18n
        i18n.load_path.append(str(self.locale_dir))
        i18n.set('filename_format', '{locale}')
        i18n.set('skip_locale_root_data', True)
        i18n.set('enable_memoization', True)
    
    def get_text(self, key: str, locale: str = None, **kwargs) -> str:
        """Get translated text for a given key and locale."""
        locale = locale or self.default_locale
        try:
            return i18n.t(key, locale=locale, **kwargs)
        except Exception:
            # Fallback to default locale if translation not found
            if locale != self.default_locale:
                try:
                    return i18n.t(key, locale=self.default_locale, **kwargs)
                except Exception:
                    pass
            # Return key as fallback
            return key
    
    def get_locale_data(self, locale: str) -> Dict[str, Any]:
        """Get all translations for a specific locale."""
        try:
            return i18n.get_namespace(locale)
        except Exception:
            return {}
    
    def get_supported_locales(self) -> list:
        """Get list of supported locales."""
        locales = []
        if self.locale_dir.exists():
            for file in self.locale_dir.glob("*.json"):
                locale = file.stem
                if locale != "base":
                    locales.append(locale)
        return sorted(locales) if locales else [self.default_locale]
    
    def create_locale_file(self, locale: str, translations: Dict[str, Any]):
        """Create or update a locale file."""
        locale_file = self.locale_dir / f"{locale}.json"
        import json
        
        # Load existing translations if file exists
        existing = {}
        if locale_file.exists():
            try:
                with open(locale_file, 'r', encoding='utf-8') as f:
                    existing = json.load(f)
            except Exception:
                pass
        
        # Merge with new translations
        existing.update(translations)
        
        # Write back to file
        with open(locale_file, 'w', encoding='utf-8') as f:
            json.dump(existing, f, ensure_ascii=False, indent=2)
        
        # Reload i18n
        i18n.reload()

# Global i18n manager instance
i18n_manager = I18nManager()

def get_text(key: str, locale: str = None, **kwargs) -> str:
    """Global function to get translated text."""
    return i18n_manager.get_text(key, locale, **kwargs)

def t(key: str, locale: str = None, **kwargs) -> str:
    """Short alias for get_text."""
    return get_text(key, locale, **kwargs)
