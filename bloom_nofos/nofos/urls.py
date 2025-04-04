from django.urls import path

from . import views

app_name = "nofos"
urlpatterns = [
    path("", views.NofosListView.as_view(), name="nofo_index"),
    path("import", views.NofosImportNewView.as_view(), name="nofo_import"),
    path("<int:pk>/delete", views.NofosArchiveView.as_view(), name="nofo_archive"),
    path(
        "<int:pk>/history",
        views.NofoHistoryView.as_view(),
        name="nofo_history",
    ),
    path(
        "<int:pk>/import",
        views.NofosImportOverwriteView.as_view(),
        name="nofo_import_overwrite",
    ),
    path(
        "<int:pk>/compare",
        views.NofosImportCompareView.as_view(),
        name="nofo_import_compare",
    ),
    path(
        "<int:pk>/confirm-import/",
        views.NofosConfirmReimportView.as_view(),
        name="nofo_import_confirm_overwrite",
    ),
    path(
        "<int:pk>/import/title",
        views.NofoImportTitleView.as_view(),
        name="nofo_import_title",
    ),
    path(
        "<int:pk>/import/number",
        views.NofoImportNumberView.as_view(),
        name="nofo_import_number",
    ),
    path("<int:pk>", views.NofosDetailView.as_view(), name="nofo_view"),
    path("<int:pk>/edit", views.NofosEditView.as_view(), name="nofo_edit"),
    path(
        "<int:pk>/edit/coach-designer",
        views.NofoEditCoachDesignerView.as_view(),
        name="nofo_edit_coach_designer",
    ),
    path(
        "<int:pk>/edit/title", views.NofoEditTitleView.as_view(), name="nofo_edit_title"
    ),
    path(
        "<int:pk>/edit/number",
        views.NofoEditNumberView.as_view(),
        name="nofo_edit_number",
    ),
    path(
        "<int:pk>/edit/group",
        views.NofoEditGroupView.as_view(),
        name="nofo_edit_group",
    ),
    path(
        "<int:pk>/edit/application-deadline",
        views.NofoEditApplicationDeadlineView.as_view(),
        name="nofo_edit_application_deadline",
    ),
    path(
        "<int:pk>/edit/tagline",
        views.NofoEditTaglineView.as_view(),
        name="nofo_edit_tagline",
    ),
    path(
        "<int:pk>/edit/metadata",
        views.NofoEditMetadataView.as_view(),
        name="nofo_edit_metadata",
    ),
    path(
        "<int:pk>/edit/opdiv",
        views.NofoEditOpDivView.as_view(),
        name="nofo_edit_opdiv",
    ),
    path(
        "<int:pk>/edit/agency",
        views.NofoEditAgencyView.as_view(),
        name="nofo_edit_agency",
    ),
    path(
        "<int:pk>/edit/subagency",
        views.NofoEditSubagencyView.as_view(),
        name="nofo_edit_subagency",
    ),
    path(
        "<int:pk>/edit/subagency2",
        views.NofoEditSubagency2View.as_view(),
        name="nofo_edit_subagency2",
    ),
    path(
        "<int:pk>/edit/theme",
        views.NofoEditThemeView.as_view(),
        name="nofo_edit_theme",
    ),
    path(
        "<int:pk>/edit/cover",
        views.NofoEditCoverView.as_view(),
        name="nofo_edit_cover",
    ),
    path(
        "<int:pk>/edit/cover-image",
        views.NofoEditCoverImageView.as_view(),
        name="nofo_edit_cover_image",
    ),
    path(
        "<int:pk>/edit/icon-style",
        views.NofoEditIconStyleView.as_view(),
        name="nofo_edit_icon_style",
    ),
    path(
        "<int:pk>/edit/status",
        views.NofoEditStatusView.as_view(),
        name="nofo_edit_status",
    ),
    path(
        "<int:pk>/edit/modifications",
        views.NofoEditModificationView.as_view(),
        name="nofo_modifications",
    ),
    path("<int:pk>/print/", views.PrintNofoAsPDFView.as_view(), name="print_pdf"),
    path(
        "<int:pk>/section/<int:section_pk>/subsection/create",
        views.NofoSubsectionCreateView.as_view(),
        name="subsection_create",
    ),
    path(
        "<int:pk>/section/<int:section_pk>",
        views.NofoSectionDetailView.as_view(),
        name="section_detail",
    ),
    path(
        "<int:pk>/section/<int:section_pk>/subsection/<int:subsection_pk>/edit",
        views.NofoSubsectionEditView.as_view(),
        name="subsection_edit",
    ),
    path(
        "<int:pk>/section/<int:section_pk>/subsection/<int:subsection_pk>/delete",
        views.NofoSubsectionDeleteView.as_view(),
        name="subsection_delete",
    ),
    path(
        "<int:pk>/check-links",
        views.CheckNOFOLinksDetailView.as_view(),
        name="nofo_check_links",
    ),
    path(
        "check-link",
        views.CheckNOFOLinkSingleView.as_view(),
        name="nofo_check_link_single",
    ),
]
