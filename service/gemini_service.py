"""
Gemini AI Service
Handles all Gemini API interactions with retry logic and fallback
"""

import os
import time
from typing import Optional, Any

try:
    from google import genai  # type: ignore
except Exception:
    genai = None  # type: ignore


class GeminiService:
    """Service for interacting with Google Gemini API."""
    
    def __init__(self):
        self.api_key = os.environ.get("GEMINI_API_KEY")
        self.model = os.environ.get("GEMINI_MODEL", "gemini-2.5-flash")
        self.max_retries = int(os.environ.get("GEMINI_MAX_RETRIES", "2"))
        self.retry_delay_ms = int(os.environ.get("GEMINI_RETRY_DELAY_MS", "400"))
        # Preinscription URL (Université de Douala)
        # Avoid session-specific query params like jsessionid
        self.preinscription_url = os.environ.get(
            "PREINSCRIPTION_URL",
            "http://www.systhag-online.cm:8080/SYSTHAG-ONLINE/faces/etudiants/preInscription.xhtml",
        )
        self.client: Optional[Any] = None
        
        if self.api_key and genai:
            try:
                self.client = genai.Client(api_key=self.api_key)
            except Exception as e:
                print(f"[WARN] Failed to initialize Gemini client: {e}")
                self.client = None
    
    def is_available(self) -> bool:
        """Check if Gemini service is configured and available."""
        return self.client is not None

    def health_check(self) -> dict:
        """Return health information for the Gemini service."""
        if not self.client:
            return {"available": False, "model": self.model, "error": "Client not initialized"}
        # Perform a very lightweight no-op style check
        try:
            # Some Gemini APIs may not have a pure ping; attempt a minimal generation with a short prompt
            response = self.client.models.generate_content(
                model=self.model,
                contents="ping"
            )
            ok = bool(getattr(response, "text", "")) or True
            return {"available": ok, "model": self.model}
        except Exception as e:
            return {"available": False, "model": self.model, "error": str(e)}
    
    def generate_reply(self, message: str, context: list) -> str:
        """
        Generate AI reply with context awareness.
        
        Args:
            message: User message
            context: List of recent messages [{'role': 'user/assistant', 'content': '...'}]
        
        Returns:
            Generated reply text
        
        Raises:
            Exception: If generation fails after retries
        """
        if not self.is_available():
            raise Exception("Gemini not configured or unavailable")
        
        # Format conversation context
        formatted_context = []
        for m in context:
            formatted_context.append(f"{m['role']}: {m['content']}")
        
        system_instruction = (
            "Vous êtes Bot4Univ, un assistant universitaire dédié aux préinscriptions à l'Université de Douala. "
            "Votre objectif principal est d'aider les étudiants à comprendre et à réussir leur préinscription. "
            "Soyez clair, concis et pratique. Lorsque pertinent, orientez vers le portail officiel de préinscription: "
            f"{self.preinscription_url}. "
            "Ne demandez jamais d'informations sensibles (mots de passe, numéros de carte). "
            "Rappelez que le paiement et la validation se font uniquement via les canaux officiels. "
            "Si la question dépasse la préinscription, répondez brièvement dans un cadre académique général."
        )

        guidance = (
            "Quand on vous demande 'comment faire', proposez des étapes génériques (ex: créer/accéder au compte, "
            "remplir le formulaire, téléverser les pièces requises, vérifier et valider), et ajoutez le lien. "
            "Si l'utilisateur demande un lien direct, fournissez: " + self.preinscription_url + "."
        )

        prompt = (
            system_instruction + "\n\n" + guidance + "\n\n" +
            "Contexte de conversation:\n" + "\n".join(formatted_context[-10:]) +
            f"\n\nUtilisateur: {message}\nBot4Univ:"
        )
        
        last_error: Optional[Exception] = None
        
        for attempt in range(1, self.max_retries + 2):
            try:
                response = self.client.models.generate_content(
                    model=self.model,
                    contents=prompt,
                )
                text = getattr(response, "text", None)
                if not text:
                    return "Désolé, je n'ai pas de réponse pour le moment."
                return text.strip()
                
            except Exception as e:
                last_error = e
                msg = str(e)
                
                # Check if transient error (overload, unavailable)
                transient = (
                    "UNAVAILABLE" in msg or 
                    "503" in msg or 
                    "overloaded" in msg.lower() or
                    "quota" in msg.lower()
                )
                
                if transient and attempt <= self.max_retries:
                    print(f"[GeminiService] Transient error attempt {attempt}/{self.max_retries}: {msg}")
                    time.sleep(self.retry_delay_ms / 1000.0)
                    continue
                
                if transient:
                    # After retries exhausted, surface error to caller
                    raise Exception(f"Transient Gemini error after retries: {msg}")
                
                # Non-transient error
                raise Exception(f"Gemini API error: {e}")
        
        # Fallback if loop exits unexpectedly
        if last_error:
            raise Exception(f"Gemini API unexpected failure: {last_error}")
        
        raise Exception("Gemini generation failed for unknown reasons")


# Singleton instance
_gemini_service: Optional[GeminiService] = None


def get_gemini_service() -> GeminiService:
    """Get or create singleton Gemini service instance."""
    global _gemini_service
    if _gemini_service is None:
        _gemini_service = GeminiService()
    return _gemini_service
