"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from src.recommender import load_songs, recommend_songs


def main() -> None:
    songs = load_songs("data/songs.csv") 

    # User taste profile — edit these values to test different listener types
    # favorite_genre: the genre the user most wants to hear
    # favorite_mood:  the emotional vibe they are looking for
    # target_energy:  0.0 (very calm) to 1.0 (very intense)
    # likes_acoustic: True = prefers acoustic sounds, False = prefers electronic
    user_prefs = {
        "genre": "pop",
        "mood": "happy",
        "energy": 0.8,
        "likes_acoustic": False,
    }

    recommendations = recommend_songs(user_prefs, songs, k=5)

    print()
    print("=" * 52)
    print("  TOP RECOMMENDATIONS")
    print(f"  Genre: {user_prefs['genre']}  |  Mood: {user_prefs['mood']}  |  Energy: {user_prefs['energy']}")
    print("=" * 52)

    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        print(f"\n  #{rank}  {song['title']}  —  {song['artist']}")
        print(f"       Score : {score:.2f} / 5.50")
        print(f"       Why   : {explanation}")

    print()
    print("=" * 52)


if __name__ == "__main__":
    main()
