import csv
from typing import List, Dict, Tuple
from dataclasses import dataclass


@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float


@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool


# ---------------------------------------------------------------------------
# Step 1: Load songs from CSV
# ---------------------------------------------------------------------------

def load_songs(csv_path: str) -> List[Dict]:
    """Read songs from a CSV file and return them as a list of dicts with numeric fields converted."""
    songs = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            songs.append({
                "id":           int(row["id"]),
                "title":        row["title"],
                "artist":       row["artist"],
                "genre":        row["genre"],
                "mood":         row["mood"],
                "energy":       float(row["energy"]),
                "tempo_bpm":    int(row["tempo_bpm"]),
                "valence":      float(row["valence"]),
                "danceability": float(row["danceability"]),
                "acousticness": float(row["acousticness"]),
            })
    print(f"Loaded songs: {len(songs)}")
    return songs


# ---------------------------------------------------------------------------
# Step 2: Score a single song against a user profile
# ---------------------------------------------------------------------------

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Score one song against a user profile and return (total_score, list_of_reasons)."""
    score = 0.0
    reasons = []

    # --- Genre match (+2.0) ---
    if song["genre"] == user_prefs.get("genre", ""):
        score += 2.0
        reasons.append(f"genre match (+2.0)")

    # --- Mood match (+1.0) ---
    if song["mood"] == user_prefs.get("mood", ""):
        score += 1.0
        reasons.append(f"mood match (+1.0)")

    # --- Energy proximity (0.0 – 2.0) ---
    # Rewards songs whose energy is *close* to the target, not just high/low.
    target_energy = user_prefs.get("energy", 0.5)
    energy_pts = (1.0 - abs(song["energy"] - target_energy)) * 2.0
    score += energy_pts
    reasons.append(f"energy proximity ({energy_pts:.2f})")

    # --- Acousticness fit (+0.5) ---
    likes_acoustic = user_prefs.get("likes_acoustic", False)
    if likes_acoustic and song["acousticness"] > 0.6:
        score += 0.5
        reasons.append("acousticness fit (+0.5)")
    elif not likes_acoustic and song["acousticness"] < 0.4:
        score += 0.5
        reasons.append("acousticness fit (+0.5)")

    return score, reasons


# ---------------------------------------------------------------------------
# Step 3: Recommend top-k songs
# ---------------------------------------------------------------------------

def recommend_songs(
    user_prefs: Dict,
    songs: List[Dict],
    k: int = 5,
) -> List[Tuple[Dict, float, str]]:
    """Score every song, sort by score descending, and return the top-k as (song, score, explanation) tuples."""
    scored = []
    for song in songs:
        song_score, reasons = score_song(user_prefs, song)
        explanation = " | ".join(reasons) if reasons else "no matching features"
        scored.append((song, song_score, explanation))

    # sorted() returns a brand-new list; key=lambda pulls out the score (index 1)
    ranked = sorted(scored, key=lambda item: item[1], reverse=True)
    return ranked[:k]


# ---------------------------------------------------------------------------
# OOP interface — required by tests/test_recommender.py
# ---------------------------------------------------------------------------

class Recommender:
    """
    Object-oriented wrapper around the same scoring logic.
    Required by tests/test_recommender.py
    """

    def __init__(self, songs: List[Song]):
        """Initialize the recommender with a catalog of Song objects."""
        self.songs = songs

    def _score(self, user: UserProfile, song: Song) -> float:
        """Scores a Song dataclass against a UserProfile dataclass."""
        score = 0.0

        if song.genre == user.favorite_genre:
            score += 2.0
        if song.mood == user.favorite_mood:
            score += 1.0

        energy_pts = (1.0 - abs(song.energy - user.target_energy)) * 2.0
        score += energy_pts

        if user.likes_acoustic and song.acousticness > 0.6:
            score += 0.5
        elif not user.likes_acoustic and song.acousticness < 0.4:
            score += 0.5

        return score

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Returns the top-k Song objects sorted by score, highest first."""
        return sorted(self.songs, key=lambda s: self._score(user, s), reverse=True)[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Returns a human-readable explanation for why a song was recommended."""
        parts = []

        if song.genre == user.favorite_genre:
            parts.append(f"genre match: {song.genre} (+2.0)")
        if song.mood == user.favorite_mood:
            parts.append(f"mood match: {song.mood} (+1.0)")

        energy_pts = (1.0 - abs(song.energy - user.target_energy)) * 2.0
        parts.append(f"energy proximity: {energy_pts:.2f}")

        if user.likes_acoustic and song.acousticness > 0.6:
            parts.append("acousticness fit (+0.5)")
        elif not user.likes_acoustic and song.acousticness < 0.4:
            parts.append("acousticness fit (+0.5)")

        return " | ".join(parts) if parts else "no strong feature match"
