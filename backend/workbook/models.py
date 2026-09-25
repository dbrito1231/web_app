from django.db import models


class Attempt(models.Model):
    MODE_PRACTICE = "practice"
    MODE_EXAM = "exam"
    MODE_CHOICES = [
        (MODE_PRACTICE, "Practice"),
        (MODE_EXAM, "Exam"),
    ]

    question_id = models.CharField(max_length=128, db_index=True)
    mode = models.CharField(max_length=16, choices=MODE_CHOICES)
    presented_order = models.JSONField(default=list, blank=True)
    selected_ids = models.JSONField(default=list)
    correct = models.BooleanField()
    assisted = models.BooleanField(default=False)
    is_first_exam_attempt = models.BooleanField(default=False)
    submitted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-submitted_at"]
        indexes = [
            models.Index(fields=["question_id", "mode"]),
        ]


class LabCheckpoint(models.Model):
    STATUS_NOT_STARTED = "not-started"
    STATUS_SELF_REPORTED = "self-reported"
    STATUS_UNRESOLVED = "unresolved"
    STATUS_CHOICES = [
        (STATUS_NOT_STARTED, "Not started"),
        (STATUS_SELF_REPORTED, "Self-reported"),
        (STATUS_UNRESOLVED, "Unresolved"),
    ]

    lab_id = models.CharField(max_length=64, db_index=True)
    checkpoint_id = models.CharField(max_length=128)
    status = models.CharField(
        max_length=32, choices=STATUS_CHOICES, default=STATUS_NOT_STARTED
    )
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = [("lab_id", "checkpoint_id")]


class CostEntry(models.Model):
    description = models.CharField(max_length=512)
    amount_usd = models.DecimalField(max_digits=10, decimal_places=2)
    lab_id = models.CharField(max_length=64, blank=True, default="")
    recorded_at = models.DateTimeField(auto_now_add=True)


class SettingBlob(models.Model):
    key = models.CharField(max_length=128, unique=True)
    value = models.JSONField(default=dict)
    updated_at = models.DateTimeField(auto_now=True)
