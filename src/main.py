"""
Command line runner for the Music Recommender Simulation.
Run with:  python -m src.main
"""

from src.recommender import load_songs, recommend_songs


# ---------------------------------------------------------------------------
# User profiles to test
# ---------------------------------------------------------------------------

PROFILES = [
    # --- Normal profiles ---
    {
        "label":        "High-Energy Pop",
        "genre":        "pop",
        "mood":         "happy",
        "energy":       0.9,
        "likes_acoustic": False,
    },
    {
        "label":        "Chill Lofi",
        "genre":        "lofi",
        "mood":         "chill",
        "energy":       0.35,
        "likes_acoustic": True,
    },
    {
        "label":        "Deep Intense Rock",
        "genre":        "rock",
        "mood":         "intense",
        "energy":       0.95,
        "likes_acoustic": False,
    },

    # --- Adversarial / edge-case profiles ---
    {
        "label":        "EDGE: Conflicting Energy + Mood (aggressive metal fan who wants chill)",
        "genre":        "metal",
        "mood":         "chill",      # only 1 metal song exists, and it is "aggressive" not "chill"
        "energy":       0.95,
        "likes_acoustic": False,
    },
    {
        "label":        "EDGE: Rare Genre (reggae) — only 1 catalog match",
        "genre":        "reggae",
        "mood":         "dreamy",
        "energy":       0.5,
        "likes_acoustic": True,
    },
    {
        "label":        "EDGE: Extreme Low Energy (0.0) — tests energy formula floor",
        "genre":        "ambient",
        "mood":         "chill",
        "energy":       0.0,
        "likes_acoustic": True,
    },
    {
        "label":        "EDGE: Genre not in catalog — score driven purely by energy + acousticness",
        "genre":        "k-pop",
        "mood":         "happy",
        "energy":       0.75,
        "likes_acoustic": False,
    },
]


def print_results(label: str, user_prefs: dict, recommendations: list) -> None:
    print()
    print("=" * 60)
    print(f"  {label}")
    print(f"  Genre: {user_prefs['genre']}  |  Mood: {user_prefs['mood']}  |  Energy: {user_prefs['energy']}")
    print("=" * 60)
    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        print(f"\n  #{rank}  {song['title']}  —  {song['artist']}")
        print(f"       Score : {score:.2f} / 5.50")
        print(f"       Why   : {explanation}")
    print()


def main() -> None:
    songs = load_songs("data/songs.csv")

    for profile in PROFILES:
        user_prefs = {k: v for k, v in profile.items() if k != "label"}
        recommendations = recommend_songs(user_prefs, songs, k=5)
        print_results(profile["label"], user_prefs, recommendations)


if __name__ == "__main__":
    main()
