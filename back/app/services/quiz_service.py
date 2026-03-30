from __future__ import annotations

import random

from app.db.mongo import get_db

PLACEHOLDER_CLASSES = [
    "High Prime",
    "Average Prime",
    "Low Prime",
    "High Choice",
    "Average Choice",
    "Low Choice",
    "High Select",
    "Low Select",
    "High Standard",
]

COLLECTION = "quiz_images"


class QuizService:
    @staticmethod
    async def get_quiz_question(target_class: str) -> dict:
        db = get_db()

        
        correct_docs = await db[COLLECTION].find(
            {"meat_quality_class": target_class}
        ).to_list(length=50)

        
        wrong_docs = await db[COLLECTION].find(
            {"meat_quality_class": {"$ne": target_class}}
        ).to_list(length=200)

        
        if not correct_docs or len(wrong_docs) < 2:
            return _build_placeholder_question(target_class)

        correct = random.choice(correct_docs)
        wrong_two = random.sample(wrong_docs, 2)

        images = [
            {
                "id": str(correct["_id"]),
                "image_url": correct["image_url"],
                "meat_quality_class": correct["meat_quality_class"],
                "is_correct": True,
            },
            {
                "id": str(wrong_two[0]["_id"]),
                "image_url": wrong_two[0]["image_url"],
                "meat_quality_class": wrong_two[0]["meat_quality_class"],
                "is_correct": False,
            },
            {
                "id": str(wrong_two[1]["_id"]),
                "image_url": wrong_two[1]["image_url"],
                "meat_quality_class": wrong_two[1]["meat_quality_class"],
                "is_correct": False,
            },
        ]
        random.shuffle(images)

        return {
            "target_class": target_class,
            "images": images,
        }


def _build_placeholder_question(target_class: str) -> dict:
    wrong_classes = [c for c in PLACEHOLDER_CLASSES if c != target_class]
    wrong_two = random.sample(wrong_classes, 2)

    images = [
        {
            "id": "placeholder-correct",
            "image_url": "",
            "meat_quality_class": target_class,
            "is_correct": True,
        },
        {
            "id": "placeholder-wrong-1",
            "image_url": "",
            "meat_quality_class": wrong_two[0],
            "is_correct": False,
        },
        {
            "id": "placeholder-wrong-2",
            "image_url": "",
            "meat_quality_class": wrong_two[1],
            "is_correct": False,
        },
    ]
    random.shuffle(images)

    return {
        "target_class": target_class,
        "images": images,
    }
