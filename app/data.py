"""Static catalogue and Clear Key data for the legacy API."""

from typing import Any


def get_catalog(base_url: str) -> list[dict[str, Any]]:
    """Return the legacy video catalogue with URLs based on BASE_URL."""
    base_url = base_url.rstrip("/")

    return [
        {
            "id": "1",
            "title": "Introduction",
            "description": (
                "The Method's concept of integrated fitness allows you "
                "to learn and perform movements and exercises from four "
                "of the world's most proven physical conditioning "
                "philosophies: yoga, martial arts, classical dance, "
                "and the work of Joseph Pilates."
            ),
            "influencer": "Jennifer Kries",
            "thumbnail": (
                f"{base_url}/videos/jennifer-kries/the-method-pilates/"
                "target-specifics/00-introduction/images/00-intro.jpg"
            ),
            "source": (
                f"{base_url}/videos/jennifer-kries/the-method-pilates/"
                "target-specifics/00-introduction/stream.mpd"
            ),
            "contentType": "application/dash+xml",
            "aspectRatio": "4/3",
            "length": "1m",
            "category": "Pilates",
        },
        {
            "id": "2",
            "title": "Abs",
            "description": (
                "Combines a series of simple, yet challenging, exercises "
                "that target both the deep set muscles that support the "
                "lower spine and the larger abdominal muscle groups that "
                "give shape and firmness to your waistline."
            ),
            "influencer": "Jennifer Kries",
            "thumbnail": (
                f"{base_url}/videos/jennifer-kries/the-method-pilates/"
                "target-specifics/01-abs/images/01-abs.jpg"
            ),
            "source": (
                f"{base_url}/videos/jennifer-kries/the-method-pilates/"
                "target-specifics/01-abs/stream.mpd"
            ),
            "contentType": "application/dash+xml",
            "aspectRatio": "4/3",
            "length": "14m",
            "category": "Pilates",
        },
        {
            "id": "3",
            "title": "Arms",
            "description": (
                "Using only 1 to 3 lb. hand weights, this workout will "
                "firm up your arms (triceps, biceps, and shoulders) "
                "without fear of bulking up."
            ),
            "influencer": "Jennifer Kries",
            "thumbnail": (
                f"{base_url}/videos/jennifer-kries/the-method-pilates/"
                "target-specifics/02-arms/images/02-arms.jpg"
            ),
            "source": (
                f"{base_url}/videos/jennifer-kries/the-method-pilates/"
                "target-specifics/02-arms/stream.mpd"
            ),
            "contentType": "application/dash+xml",
            "aspectRatio": "4/3",
            "length": "14m",
            "category": "Pilates",
        },
        {
            "id": "4",
            "title": "Hips",
            "description": (
                "Features a combination of super toning exercises from "
                "yoga, dance strength training, and Pilates inspired "
                "moves that will trim and firm the width of your hips."
            ),
            "influencer": "Jennifer Kries",
            "thumbnail": (
                f"{base_url}/videos/jennifer-kries/the-method-pilates/"
                "target-specifics/03-hips/images/03-hips.jpg"
            ),
            "source": (
                f"{base_url}/videos/jennifer-kries/the-method-pilates/"
                "target-specifics/03-hips/stream.mpd"
            ),
            "contentType": "application/dash+xml",
            "aspectRatio": "4/3",
            "length": "14m",
            "category": "Pilates",
        },
        {
            "id": "5",
            "title": "Thighs",
            "description": (
                "Combines standing and floor exercises from yoga, "
                "dance, and the work of Joseph Pilates which have been "
                "favoured by dancers and models for many years."
            ),
            "influencer": "Jennifer Kries",
            "thumbnail": (
                f"{base_url}/videos/jennifer-kries/the-method-pilates/"
                "target-specifics/04-thighs/images/04-thighs.jpg"
            ),
            "source": (
                f"{base_url}/videos/jennifer-kries/the-method-pilates/"
                "target-specifics/04-thighs/stream.mpd"
            ),
            "contentType": "application/dash+xml",
            "aspectRatio": "4/3",
            "length": "14m",
            "category": "Pilates",
        },
        {
            "id": "6",
            "title": "Florida Man Wrestles Gator",
            "description": (
                "Witness a brave Florida Man catch and subdue a filthy swamp lizard."
            ),
            "influencer": "Florida Man",
            "thumbnail": (
                f"{base_url}/videos/florida-man/swamp-puppies/wrasslin/images/gator.jpg"
            ),
            "source": (
                f"{base_url}/videos/florida-man/swamp-puppies/wrasslin/stream.mpd"
            ),
            "contentType": "application/dash+xml",
            "aspectRatio": "9/16",
            "length": "25s",
            "category": "Florida",
        },
    ]


# Preserve the existing key IDs and values from the legacy implementation.
# Move these into an appropriate secret-management mechanism if they are
# production decryption keys; do not expose them in logs.
KEYS = {
    "1": {"k": "YGdr1s2ctWfP5DLg2e-5vA", "kid": "zs5NjiuGPqr_YumJFVe4rQ"},
    "2": {"k": "3DGjLFb6ekf6dKWODQWcnw", "kid": "trybSdqAABaygwfncAG-lw"},
    "3": {"k": "MCjCa7_0iuHdBVFV57f2-g", "kid": "xTjwb_yC6MKU-Rwb2aTOqQ"},
    "4": {"k": "ElKhgxu3mhJQN6jn7s6TtA", "kid": "rGVhfk9gCtlDX9_PU7gNfw"},
    "5": {"k": "xsBxLL6sjpP8HMTI9A57_A", "kid": "8Q2-ou_fRrQO83Vz4UclGw"},
    "6": {"k": "3LoR6oiYCsHQ3Vte2yaC7Q", "kid": "APs4ZOK3avnWw8mTpwUQbQ"},
}
