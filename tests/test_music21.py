"""Test cases for music21 I/O."""
import muspy
from muspy.music import Music
from muspy.classes import Track, Note

from .utils import (
    TEST_JSON_PATH,
    check_key_signatures,
    check_tempos,
    check_time_signatures,
    check_tracks,
)


def test_music21():
    music = muspy.load(TEST_JSON_PATH)

    score = muspy.to_object(music, "music21")
    loaded = muspy.from_object(score)

    assert loaded.metadata.title == "Für Elise"
    assert loaded.resolution == 24

    check_tempos(loaded.tempos)
    check_key_signatures(loaded.key_signatures)
    check_time_signatures(loaded.time_signatures)
    check_tracks(loaded.tracks, loaded.resolution)
    # TODO: Check lyrics and annotations


def test_music21_with_rests():
    notes = [
        Note(time=0, pitch=60, duration=1),
        Note(time=2, pitch=60, duration=1),
        Note(time=4, pitch=60, duration=1),
    ]
    track = Track(notes=notes)
    music = Music(tracks=[track])
    
    score = muspy.to_object(music, "music21")
    loaded = muspy.from_object(score)
    assert len(loaded.tracks) == 1
    loaded_notes = loaded.tracks[0].notes
    assert len(notes) == len(loaded_notes)
    for note, loaded_note in zip(notes, loaded_notes):
        assert note.time == loaded_note.time
        assert note.pitch == loaded_note.pitch
        assert note.duration == loaded_note.duration