import os
import httpx
from typing import Optional
import structlog

logger = structlog.get_logger(__name__)

HAPI_BASE = os.getenv("HAPI_FHIR_BASE", "https://hapi.fhir.org/baseR4")
USE_MOCK = os.getenv("FHIR_USE_MOCK", "false").lower() == "true"


class HAPIFHIRClient:
    def __init__(self):
        self.base_url = HAPI_BASE
        self.client = httpx.AsyncClient(timeout=15.0)

    async def get_patient_bundle(self, patient_id: str) -> dict:
        url = f"{self.base_url}/Patient/{patient_id}/$everything"
        logger.info("fhir.fetch_start", patient_id=patient_id)
        resp = await self.client.get(url)
        resp.raise_for_status()
        bundle = resp.json()
        logger.info("fhir.fetch_ok", patient_id=patient_id, entries=len(bundle.get("entry", [])))
        return bundle

    async def search_patients(self, name: Optional[str] = None, count: int = 20) -> list[dict]:
        params: dict = {"_count": count, "_sort": "-_lastUpdated"}
        if name:
            params["name"] = name
        resp = await self.client.get(f"{self.base_url}/Patient", params=params)
        resp.raise_for_status()
        bundle = resp.json()
        return [self._simplify_patient(e["resource"]) for e in bundle.get("entry", []) if e.get("resource", {}).get("resourceType") == "Patient"]

    def parse_bundle(self, bundle: dict, patient_id: str) -> dict:
        conditions, medications, observations, vitals = [], [], [], []
        patient_name, age, gender = f"FHIR Patient {patient_id}", "Unknown", "Unknown"

        for entry in bundle.get("entry", []):
            r = entry.get("resource", {})
            rtype = r.get("resourceType", "")

            if rtype == "Patient":
                patient_name = self._extract_name(r)
                gender = r.get("gender", "Unknown").capitalize()
                age = self._calculate_age(r.get("birthDate", ""))
            elif rtype == "Condition":
                status = r.get("clinicalStatus", {}).get("coding", [{}])[0].get("code", "active")
                if status == "active":
                    conditions.append({"name": r.get("code", {}).get("text", "Unknown condition"), "status": status})
            elif rtype == "MedicationRequest":
                med_name = r.get("medicationCodeableConcept", {}).get("text") or r.get("medicationReference", {}).get("display", "Unknown medication")
                medications.append({"name": med_name, "status": r.get("status", "active")})
            elif rtype == "Observation":
                obs = self._parse_observation(r)
                if obs:
                    observations.append(obs)
                    categories = [c.get("coding", [{}])[0].get("code", "") for c in r.get("category", [])]
                    if "vital-signs" in categories:
                        vitals.append(obs)

        return {
            "patient_id": patient_id,
            "patient_name": patient_name,
            "age": age,
            "gender": gender,
            "conditions": conditions[:10],
            "medications": medications[:15],
            "observations": observations[:20],
            "vitals": vitals[:10],
            "fhir_source": "hapi_sandbox",
        }

    def _simplify_patient(self, r: dict) -> dict:
        return {"id": r.get("id", ""), "name": self._extract_name(r), "gender": r.get("gender", "Unknown"), "birthDate": r.get("birthDate", ""), "age": self._calculate_age(r.get("birthDate", ""))}

    def _extract_name(self, patient: dict) -> str:
        names = patient.get("name", [])
        if not names:
            return "Unknown Patient"
        n = names[0]
        return f"{' '.join(n.get('given', []))} {n.get('family', '')}".strip() or "Unknown Patient"

    def _calculate_age(self, birth_date: str) -> str:
        if not birth_date:
            return "Unknown"
        try:
            from datetime import date
            parts = birth_date.split("-")
            born = date(int(parts[0]), int(parts[1]), int(parts[2]))
            today = date.today()
            return str(today.year - born.year - ((today.month, today.day) < (born.month, born.day)))
        except Exception:
            return "Unknown"

    def _parse_observation(self, r: dict) -> dict | None:
        code = r.get("code", {}).get("text") or r.get("code", {}).get("coding", [{}])[0].get("display", "")
        if not code:
            return None
        value, unit = None, ""
        if "valueQuantity" in r:
            value = r["valueQuantity"].get("value")
            unit = r["valueQuantity"].get("unit", "")
        elif "valueString" in r:
            value = r["valueString"]
        return {"name": code, "value": value, "unit": unit, "date": r.get("effectiveDateTime", "")}

    async def close(self):
        await self.client.aclose()


async def get_patient_data(patient_id: str) -> dict:
    if USE_MOCK:
        return _get_mock_data(patient_id)
    client = HAPIFHIRClient()
    try:
        bundle = await client.get_patient_bundle(patient_id)
        return client.parse_bundle(bundle, patient_id)
    except Exception as exc:
        logger.warning("fhir.fallback_to_mock", patient_id=patient_id, error=str(exc))
        return _get_mock_data(patient_id)
    finally:
        await client.close()


def _get_mock_data(patient_id: str) -> dict:
    try:
        from fhir.mock_client import get_patient
        return get_patient(patient_id)
    except Exception:
        return {"patient_id": patient_id, "patient_name": f"Patient {patient_id}", "conditions": [], "medications": [], "observations": [], "vitals": [], "fhir_source": "stub"}