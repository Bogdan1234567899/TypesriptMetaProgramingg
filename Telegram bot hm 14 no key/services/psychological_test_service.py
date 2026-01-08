import json
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple

_DEFAULT_SCALES = {
    "uk": [
        ("Здоров'я", "Оціни своє здоров'я та енергію від 1 до 10:"),
        ("Кар'єра/Навчання", "Оціни задоволення від кар'єри або навчання від 1 до 10:"),
        ("Фінанси", "Оціни свій фінансовий стан від 1 до 10:"),
        ("Стосунки", "Оціни стосунки з близькими від 1 до 10:"),
        ("Особистий розвиток", "Оціни особистий розвиток від 1 до 10:"),
        ("Відпочинок", "Оціни відпочинок та хобі від 1 до 10:"),
        ("Оточення", "Оціни комфорт дому/оточення від 1 до 10:"),
        ("Духовність", "Оціни внутрішню гармонію від 1 до 10:"),
    ],
    "ru": [
        ("Здоровье", "Оцени своё здоровье и энергию от 1 до 10:"),
        ("Карьера/Учёба", "Оцени удовлетворённость карьерой или учёбой от 1 до 10:"),
        ("Финансы", "Оцени своё финансовое состояние от 1 до 10:"),
        ("Отношения", "Оцени отношения с близкими от 1 до 10:"),
        ("Личное развитие", "Оцени личное развитие от 1 до 10:"),
        ("Отдых", "Оцени отдых и хобби от 1 до 10:"),
        ("Окружение", "Оцени комфорт дома/окружения от 1 до 10:"),
        ("Духовность", "Оцени внутреннюю гармонию от 1 до 10:"),
    ],
    "en": [
        ("Health", "Rate your health and energy from 1 to 10:"),
        ("Career/Study", "Rate your satisfaction with career or study from 1 to 10:"),
        ("Finance", "Rate your financial situation from 1 to 10:"),
        ("Relationships", "Rate your relationships from 1 to 10:"),
        ("Personal growth", "Rate your personal growth from 1 to 10:"),
        ("Rest", "Rate your rest and hobbies from 1 to 10:"),
        ("Environment", "Rate your home/environment comfort from 1 to 10:"),
        ("Spirituality", "Rate your inner harmony from 1 to 10:"),
    ],
}

def default_scales(lang: str) -> List[Tuple[str, str]]:
    l = (lang or "uk").lower()
    if l.startswith("ru"):
        return list(_DEFAULT_SCALES["ru"])
    if l.startswith("en"):
        return list(_DEFAULT_SCALES["en"])
    return list(_DEFAULT_SCALES["uk"])

def build_scales(lang: str, extra: List[Tuple[str, str]]) -> List[Tuple[str, str]]:
    base = default_scales(lang)
    seen = {s.strip().lower() for s, _ in base}
    result = list(base)
    for sphere, prompt in extra:
        key = sphere.strip().lower()
        if not key or key in seen:
            continue
        result.append((sphere.strip(), prompt.strip()))
        seen.add(key)
    return result

def parse_score(text: str) -> Optional[int]:
    if text is None:
        return None
    t = str(text).strip().replace(",", ".")
    try:
        v = int(float(t))
    except ValueError:
        return None
    if 1 <= v <= 10:
        return v
    return None

def _sphere_key(s: str) -> str:
    return "".join(ch for ch in s.lower() if ch.isalnum())

def _tip_for(sphere: str, score: int, lang: str) -> str:
    k = _sphere_key(sphere)
    l = (lang or "uk").lower()
    ru = l.startswith("ru")
    en = l.startswith("en")

    def msg(uk: str, r: str, e: str) -> str:
        if en:
            return e
        if ru:
            return r
        return uk

    if any(x in k for x in ["фінанс", "финанс", "finance"]):
        return msg("перевір витрати за категоріями та постав бюджет", "проверь расходы по категориям и поставь бюджет", "review category spending and set a budget")
    if any(x in k for x in ["здоров", "health"]):
        return msg("додай сон/воду/прогулянку на 20 хв", "добавь сон/воду/прогулку на 20 минут", "add sleep/water/20-min walk")
    if any(x in k for x in ["карєра", "карьера", "career", "study", "учеб", "навчан"]):
        return msg("визнач 1 маленький крок у навчанні/кар'єрі на тиждень", "определи 1 маленький шаг в учёбе/карьере на неделю", "pick 1 small weekly step for study/career")
    if any(x in k for x in ["стосунк", "отношен", "relationship"]):
        return msg("заплануй 1 розмову/зустріч з близькими цього тижня", "запланируй 1 разговор/встречу с близкими на этой неделе", "plan one quality conversation/meetup this week")
    if any(x in k for x in ["розвит", "growth", "development", "развит"]):
        return msg("виділи 15 хв щодня на навичку або читання", "выдели 15 минут в день на навык или чтение", "spend 15 min daily on a skill or reading")
    if any(x in k for x in ["відпоч", "rest", "отдых", "hobby", "хоб"]):
        return msg("додай 1 вечір без роботи та екранів", "добавь 1 вечер без работы и экранов", "add one evening without work/screens")
    if any(x in k for x in ["оточ", "environment", "окруж"]):
        return msg("зроби маленьке прибирання/організацію простору", "сделай маленькую уборку/организацию пространства", "do a small cleanup/space organization")
    if any(x in k for x in ["духов", "spirit"]):
        return msg("спробуй 5 хв тиші/медитації або щоденник", "попробуй 5 минут тишины/медитации или дневник", "try 5 min silence/meditation or journaling")
    if score <= 3:
        return msg("почни з простого кроку та повторюй щодня", "начни с простого шага и повторяй ежедневно", "start with one simple step and repeat daily")
    return msg("зроби 1-2 невеликі зміни найближчим часом", "сделай 1-2 небольших изменения в ближайшее время", "make 1–2 small changes soon")

@dataclass
class PsychologicalTestSession:
    user_id: int
    lang: str
    scales: List[Tuple[str, str]]
    index: int = 0
    scores: Dict[str, int] = field(default_factory=dict)

    def current_prompt(self) -> str:
        sphere, prompt = self.scales[self.index]
        return f"{sphere}\n{prompt}"

    def record_score(self, value: int) -> None:
        sphere, _ = self.scales[self.index]
        self.scores[sphere] = int(value)
        self.index += 1

    def is_active(self) -> bool:
        return self.index < len(self.scales)

    def recommendations(self) -> List[str]:
        if not self.scores:
            return []
        items = sorted(self.scores.items(), key=lambda x: x[1])
        low = [x for x in items if x[1] <= 6]
        target = low[:3] if low else items[:2]
        return [f"{s}: {_tip_for(s, v, self.lang)}" for s, v in target]

    def to_json(self) -> str:
        payload = {
            "user_id": self.user_id,
            "lang": self.lang,
            "scales": self.scales,
            "index": self.index,
            "scores": self.scores,
        }
        return json.dumps(payload, ensure_ascii=False)

    @staticmethod
    def from_json(data: str) -> "PsychologicalTestSession":
        obj = json.loads(data)
        return PsychologicalTestSession(
            user_id=int(obj["user_id"]),
            lang=str(obj.get("lang") or "uk"),
            scales=[(str(a), str(b)) for a, b in obj["scales"]],
            index=int(obj.get("index", 0)),
            scores={str(k): int(v) for k, v in (obj.get("scores") or {}).items()},
        )

def make_recommendations(scores: Dict[str, int], lang: str) -> List[str]:
    if not scores:
        return []
    items = sorted(scores.items(), key=lambda x: x[1])
    low = [x for x in items if x[1] <= 6]
    target = low[:3] if low else items[:2]
    return [f"{s}: {_tip_for(s, v, lang)}" for s, v in target]
