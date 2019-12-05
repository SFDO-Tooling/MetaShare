import json
from contextlib import ExitStack
from unittest.mock import MagicMock, patch

import pytest
from django.urls import reverse
from github3.exceptions import ResponseError

from ..models import SCRATCH_ORG_TYPES, TASK_STATUSES


@pytest.mark.django_db
def test_user_view(client):
    response = client.get(reverse("user"))

    assert response.status_code == 200
    assert response.json()["username"].endswith("@example.com")


@pytest.mark.django_db
def test_user_disconnect_view(client):
    response = client.post(reverse("user-disconnect-sf"))

    assert not client.user.socialaccount_set.filter(
        provider__startswith="salesforce-"
    ).exists()
    assert response.status_code == 200
    assert response.json()["username"].endswith("@example.com")


@pytest.mark.django_db
def test_user_refresh_view(client):
    with patch("metashare.api.gh.gh_given_user") as gh_given_user:
        repo = MagicMock()
        repo.url = "test"
        gh = MagicMock()
        gh.repositories.return_value = [repo]
        gh_given_user.return_value = gh

        response = client.post(reverse("user-refresh"))

    assert response.status_code == 202


@pytest.mark.django_db
class TestRepositoryView:
    def test_get_queryset(self, client, repository_factory, git_hub_repository_factory):
        git_hub_repository_factory(
            user=client.user, repo_id=123, repo_url="https://example.com/test-repo.git"
        )
        repo = repository_factory(repo_name="repo", repo_id=123)
        repository_factory(repo_name="repo2", repo_id=456)
        repository_factory(repo_name="repo3", repo_id=None)
        with patch("metashare.api.model_mixins.get_repo_info") as get_repo_info:
            get_repo_info.return_value = MagicMock(id=789)
            response = client.get(reverse("repository-list"))

        assert response.status_code == 200
        assert response.json() == {
            "count": 1,
            "previous": None,
            "next": None,
            "results": [
                {
                    "id": str(repo.id),
                    "name": str(repo.name),
                    "description": "",
                    "is_managed": False,
                    "slug": str(repo.slug),
                    "old_slugs": [],
                    "repo_url": (
                        f"https://github.com/{repo.repo_owner}/{repo.repo_name}"
                    ),
                }
            ],
        }

    def test_get_queryset__bad(
        self, client, repository_factory, git_hub_repository_factory
    ):
        git_hub_repository_factory(
            user=client.user, repo_id=123, repo_url="https://example.com/test-repo.git"
        )
        repo = repository_factory(repo_name="repo", repo_id=123)
        repository_factory(repo_name="repo2", repo_id=456)
        repository_factory(repo_name="repo3", repo_id=None)
        with patch("metashare.api.model_mixins.get_repo_info") as get_repo_info:
            get_repo_info.side_effect = ResponseError(MagicMock())
            response = client.get(reverse("repository-list"))

        assert response.status_code == 200
        assert response.json() == {
            "count": 1,
            "previous": None,
            "next": None,
            "results": [
                {
                    "id": str(repo.id),
                    "name": str(repo.name),
                    "description": "",
                    "is_managed": False,
                    "slug": str(repo.slug),
                    "old_slugs": [],
                    "repo_url": (
                        f"https://github.com/{repo.repo_owner}/{repo.repo_name}"
                    ),
                }
            ],
        }

    def test_hook__202__not_forced(
        self,
        client,
        repository_factory,
        git_hub_repository_factory,
        project_factory,
        task_factory,
    ):
        repo = repository_factory(repo_id=123, hook_secret="secret key")
        git_hub_repository_factory(repo_id=123)
        project = project_factory(repository=repo, branch_name="master")
        task = task_factory(project=project, branch_name="master")
        with patch("metashare.api.jobs.refresh_commits_job") as refresh_commits_job:
            response = client.post(
                reverse("repository-hook", kwargs={"pk": str(repo.id)}),
                json.dumps(
                    {
                        "payload": json.dumps(
                            {
                                "ref": "refs/heads/master",
                                "forced": False,
                                "commits": [
                                    {
                                        "id": "123",
                                        "author": {
                                            "name": "Test",
                                            "email": "test@example.com",
                                        },
                                        "committer": {
                                            "name": "Test",
                                            "email": "test@example.com",
                                        },
                                        "timestamp": "2019-11-20 21:32:53.668260+00:00",
                                        "message": "Message",
                                    }
                                ],
                            }
                        )
                    }
                ),
                content_type="application/json",
                # The sha1 hexdigest of the request body x the secret
                # key above:
                HTTP_X_HUB_SIGNATURE="sha1=b947c4672579f5d268837379038b020e08ed2f6f",
            )
            assert response.status_code == 202, response.content
            assert not refresh_commits_job.delay.called
            project.refresh_from_db()
            assert len(project.commits) == 1
            task.refresh_from_db()
            assert len(task.commits) == 1

    def test_hook__202__forced(
        self, client, repository_factory, git_hub_repository_factory
    ):
        repo = repository_factory(repo_id=123, hook_secret="secret key")
        git_hub_repository_factory(repo_id=123)
        with patch("metashare.api.jobs.refresh_commits_job") as refresh_commits_job:
            response = client.post(
                reverse("repository-hook", kwargs={"pk": str(repo.id)}),
                json.dumps(
                    {
                        "payload": json.dumps(
                            {"ref": "refs/heads/master", "forced": True, "commits": []}
                        )
                    }
                ),
                content_type="application/json",
                # The sha1 hexdigest of the request body x the secret
                # key above:
                HTTP_X_HUB_SIGNATURE="sha1=ecfb50b77a8ea763a45851ad79930443be9656ad",
            )
            assert response.status_code == 202, response.content
            assert refresh_commits_job.delay.called

    def test_hook__422(self, client, repository_factory, git_hub_repository_factory):
        repo = repository_factory(repo_id=123, hook_secret="secret key")
        git_hub_repository_factory(repo_id=123)
        response = client.post(
            reverse("repository-hook", kwargs={"pk": str(repo.id)}),
            json.dumps(
                {"payload": json.dumps({"ref": "refs/heads/master", "commits": []})}
            ),
            content_type="application/json",
            # This is NOT the sha1 hexdigest of the request body x the
            # secret key above:
            HTTP_X_HUB_SIGNATURE="sha1=924d6781b12339b700bc79e7c8c6fe6e051a08d1",
        )
        assert response.status_code == 422, response.json()

    def test_hook__403(self, client, repository_factory):
        repo = repository_factory(hook_secret="bleep bloop")
        response = client.post(
            reverse("repository-hook", kwargs={"pk": str(repo.id)}),
            json.dumps(
                {
                    "payload": json.dumps(
                        {"ref": "refs/heads/master", "forced": False, "commits": []}
                    )
                }
            ),
            content_type="application/json",
            # This is NOT the sha1 hexdigest of the request body x the
            # secret key above:
            HTTP_X_HUB_SIGNATURE="sha1=abe3868964305b53dc80bed60bdca7f8d2a70b97",
        )
        assert response.status_code == 403

    def test_hook__500(self, client, repository_factory):
        repo = repository_factory(hook_secret="secret key")
        response = client.post(
            reverse("repository-hook", kwargs={"pk": str(repo.id)}),
            json.dumps(
                {
                    "payload": json.dumps(
                        {"ref": "refs/heads/master", "forced": False, "commits": []}
                    )
                }
            ),
            content_type="application/json",
            # The sha1 hexdigest of the request body x the secret key
            # above:
            HTTP_X_HUB_SIGNATURE="sha1=52bf5b0b015bf7f5d1a55d025d1c5b5710d966a8",
        )
        assert response.status_code == 500

    def test_hook__202__pr__not_merged(
        self, client, repository_factory, git_hub_repository_factory
    ):
        repo = repository_factory(repo_id=123, hook_secret="secret key")
        git_hub_repository_factory(repo_id=123)
        response = client.post(
            reverse("repository-hook", kwargs={"pk": str(repo.id)}),
            json.dumps(
                {
                    "payload": json.dumps(
                        {
                            "number": 1,
                            "action": "closed",
                            "pull_request": {"merged": False},
                        },
                    )
                }
            ),
            content_type="application/json",
            # The sha1 hexdigest of the request body x the secret
            # key above:
            HTTP_X_HUB_SIGNATURE="sha1=3164a2651f615f4da07ff0bb9c3ec9a386a531a3",
        )
        assert response.status_code == 204, response.content

    def test_hook__202__pr__no_task(
        self, client, repository_factory, git_hub_repository_factory
    ):
        repo = repository_factory(repo_id=123, hook_secret="secret key")
        git_hub_repository_factory(repo_id=123)
        response = client.post(
            reverse("repository-hook", kwargs={"pk": str(repo.id)}),
            json.dumps(
                {
                    "payload": json.dumps(
                        {
                            "number": 1,
                            "action": "closed",
                            "pull_request": {"merged": True},
                        },
                    )
                }
            ),
            content_type="application/json",
            # The sha1 hexdigest of the request body x the secret
            # key above:
            HTTP_X_HUB_SIGNATURE="sha1=2d3c5c3ab0422ca76b5b9a9c6af0331accc1c910",
        )
        assert response.status_code == 204, response.content

    def test_hook__202__pr__update_task(
        self, client, repository_factory, git_hub_repository_factory, task_factory
    ):
        repo = repository_factory(repo_id=123, hook_secret="secret key")
        git_hub_repository_factory(repo_id=123)
        task = task_factory(project__repository=repo, pr_number=1)
        response = client.post(
            reverse("repository-hook", kwargs={"pk": str(repo.id)}),
            json.dumps(
                {
                    "payload": json.dumps(
                        {
                            "number": 1,
                            "action": "closed",
                            "pull_request": {"merged": True},
                        },
                    )
                }
            ),
            content_type="application/json",
            # The sha1 hexdigest of the request body x the secret
            # key above:
            HTTP_X_HUB_SIGNATURE="sha1=2d3c5c3ab0422ca76b5b9a9c6af0331accc1c910",
        )
        assert response.status_code == 200, response.content
        task.refresh_from_db()
        assert task.status == TASK_STATUSES.Completed


@pytest.mark.django_db
class TestScratchOrgView:
    def test_commit_happy_path(self, client, scratch_org_factory):
        scratch_org = scratch_org_factory(org_type="Dev", owner=client.user)
        with patch(
            "metashare.api.jobs.commit_changes_from_org_job"
        ) as commit_changes_from_org_job:
            response = client.post(
                reverse("scratch-org-commit", kwargs={"pk": str(scratch_org.id)}),
                {"commit_message": "Test message", "changes": {}},
                format="json",
            )
            assert response.status_code == 202
            assert commit_changes_from_org_job.delay.called

    def test_commit_sad_path__422(self, client, scratch_org_factory):
        scratch_org = scratch_org_factory(org_type="Dev")
        with patch(
            "metashare.api.jobs.commit_changes_from_org_job"
        ) as commit_changes_from_org_job:
            response = client.post(
                reverse("scratch-org-commit", kwargs={"pk": str(scratch_org.id)}),
                {"changes": {}},
                format="json",
            )
            assert response.status_code == 422
            assert not commit_changes_from_org_job.delay.called

    def test_commit_sad_path__403(self, client, scratch_org_factory):
        scratch_org = scratch_org_factory(org_type="Dev")
        with patch(
            "metashare.api.jobs.commit_changes_from_org_job"
        ) as commit_changes_from_org_job:
            response = client.post(
                reverse("scratch-org-commit", kwargs={"pk": str(scratch_org.id)}),
                {"commit_message": "Test message", "changes": {}},
                format="json",
            )
            assert response.status_code == 403
            assert not commit_changes_from_org_job.delay.called

    def test_list_fetch_changes(self, client, scratch_org_factory):
        scratch_org_factory(
            org_type=SCRATCH_ORG_TYPES.Dev,
            url="https://example.com",
            delete_queued_at=None,
            currently_capturing_changes=False,
            currently_refreshing_changes=False,
            owner=client.user,
        )
        with patch(
            "metashare.api.jobs.get_unsaved_changes_job"
        ) as get_unsaved_changes_job:
            url = reverse("scratch-org-list")
            response = client.get(url)

            assert response.status_code == 200
            assert get_unsaved_changes_job.delay.called

    def test_retrieve_fetch_changes(self, client, scratch_org_factory):
        scratch_org = scratch_org_factory(
            org_type=SCRATCH_ORG_TYPES.Dev,
            url="https://example.com",
            delete_queued_at=None,
            currently_capturing_changes=False,
            currently_refreshing_changes=False,
            owner=client.user,
        )
        with patch(
            "metashare.api.jobs.get_unsaved_changes_job"
        ) as get_unsaved_changes_job:
            url = reverse("scratch-org-detail", kwargs={"pk": str(scratch_org.id)})
            response = client.get(url)

            assert response.status_code == 200
            assert get_unsaved_changes_job.delay.called

    def test_create(self, client, task_factory, social_account_factory):
        task = task_factory()
        social_account_factory(
            user=client.user,
            provider="salesforce-production",
            extra_data={"preferred_username": "test-username"},
        )
        url = reverse("scratch-org-list")
        with ExitStack() as stack:
            stack.enter_context(
                patch("metashare.api.views.viewsets.ModelViewSet.perform_create")
            )
            get_devhub_api = stack.enter_context(
                patch("metashare.api.models.get_devhub_api")
            )
            resp = {"foo": "bar"}
            sf_client = MagicMock()
            sf_client.restful.return_value = resp
            get_devhub_api.return_value = sf_client

            response = client.post(url, {"task": str(task.id), "org_type": "Dev"})

        assert response.status_code == 201, response.content

    def test_create__bad(self, client, task_factory, social_account_factory):
        task = task_factory()
        social_account_factory(
            user=client.user,
            provider="salesforce-production",
            extra_data={"preferred_username": "test-username"},
        )
        url = reverse("scratch-org-list")
        with ExitStack() as stack:
            stack.enter_context(
                patch("metashare.api.views.viewsets.ModelViewSet.perform_create")
            )
            get_devhub_api = stack.enter_context(
                patch("metashare.api.models.get_devhub_api")
            )
            sf_client = MagicMock()
            sf_client.restful.return_value = None
            get_devhub_api.return_value = sf_client

            response = client.post(url, {"task": str(task.id), "org_type": "Dev"})

        assert response.status_code == 403, response.content

    def test_queue_delete(self, client, scratch_org_factory, social_account_factory):
        social_account_factory(
            user=client.user,
            provider="salesforce-production",
            extra_data={"preferred_username": "test-username"},
        )
        scratch_org = scratch_org_factory(owner_sf_id="test-username")
        with patch("metashare.api.models.ScratchOrg.queue_delete"):
            url = reverse("scratch-org-detail", kwargs={"pk": str(scratch_org.id)})
            response = client.delete(url)

            assert response.status_code == 204

    def test_queue_delete__bad(
        self, client, scratch_org_factory, social_account_factory
    ):
        social_account_factory(
            user=client.user,
            provider="salesforce-production",
            extra_data={"preferred_username": "test-username"},
        )
        scratch_org = scratch_org_factory(owner_sf_id="other-test-username")
        with patch("metashare.api.models.ScratchOrg.queue_delete"):
            url = reverse("scratch-org-detail", kwargs={"pk": str(scratch_org.id)})
            response = client.delete(url)

            assert response.status_code == 403

    def test_redirect__good(self, client, scratch_org_factory):
        scratch_org = scratch_org_factory(owner=client.user)
        with patch("metashare.api.models.ScratchOrg.get_login_url") as get_login_url:
            get_login_url.return_value = "https://example.com"
            url = reverse("scratch-org-redirect", kwargs={"pk": str(scratch_org.id)})
            response = client.get(url)

            assert response.status_code == 302

    def test_redirect__bad(self, client, scratch_org_factory):
        scratch_org = scratch_org_factory()
        with patch("metashare.api.models.ScratchOrg.get_login_url") as get_login_url:
            get_login_url.return_value = "https://example.com"
            url = reverse("scratch-org-redirect", kwargs={"pk": str(scratch_org.id)})
            response = client.get(url)

            assert response.status_code == 403


@pytest.mark.django_db
class TestTaskView:
    def test_create_pr(self, client, task_factory):
        task = task_factory()
        with patch("metashare.api.models.Task.queue_create_pr"):
            url = reverse("task-create-pr", kwargs={"pk": str(task.id)})
            response = client.post(
                url,
                {
                    "title": "My PR",
                    "critical_changes": "",
                    "additional_changes": "",
                    "issues": "",
                    "notes": "",
                },
                format="json",
            )

            assert response.status_code == 202, response.json()

    def test_create_pr__error(self, client, task_factory):
        task = task_factory()
        with patch("metashare.api.models.Task.queue_create_pr"):
            url = reverse("task-create-pr", kwargs={"pk": str(task.id)})
            response = client.post(url, {}, format="json")

            assert response.status_code == 422

    def test_create_pr__bad(self, client, task_factory):
        task = task_factory(pr_number=123)
        with patch("metashare.api.models.Task.queue_create_pr"):
            url = reverse("task-create-pr", kwargs={"pk": str(task.id)})
            response = client.post(
                url,
                {
                    "title": "My PR",
                    "critical_changes": "",
                    "additional_changes": "",
                    "issues": "",
                    "notes": "",
                },
                format="json",
            )

            assert response.status_code == 400
