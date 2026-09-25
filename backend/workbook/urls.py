from django.urls import path

from workbook import views

urlpatterns = [
    path("health", views.health, name="health"),
    path("content/summary", views.content_summary_view, name="content-summary"),
    path("content/catalog", views.question_catalog_view, name="question-catalog"),
    path("lessons/<str:lesson_id>", views.lesson_detail, name="lesson-detail"),
    path("questions/<str:question_id>", views.question_detail, name="question-detail"),
    path("attempts", views.create_attempt, name="create-attempt"),
    path("labs/<str:lab_id>", views.lab_detail, name="lab-detail"),
    path(
        "labs/<str:lab_id>/checkpoints",
        views.lab_checkpoint,
        name="lab-checkpoint",
    ),
    path("progress", views.progress_view, name="progress"),
    path("export", views.export_view, name="export"),
    path("import", views.import_view, name="import"),
    path("reset", views.reset_view, name="reset"),
    path("metrics/readiness", views.readiness_metrics, name="readiness-metrics"),
    path("coverage", views.coverage_registry, name="coverage"),
]
